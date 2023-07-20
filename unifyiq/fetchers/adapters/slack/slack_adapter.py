import time
from datetime import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from fetchers.adapters.base_adapter import BaseAdapter
from fetchers.database.fetchers_slack_db import insert_channel_membership, \
    get_current_channel_membership, delete_channel_membership, get_current_channel_info, insert_channel_info_to_db, \
    update_channel_info_to_db
from utils import constants
from utils.configs import get_slack_bot_token
from utils.constants import MAX_ATTEMPTS_FOR_SLACK_API_CALL
from utils.database import unifyiq_config_db
from utils.file_utils import skip_index_file_name
from utils.log_util import get_logger
from utils.time_utils import get_slack_ts

THREE_DAYS = 3 * 24 * 60 * 60


class SlackAdapter(BaseAdapter):

    def __init__(self, source_config, version):
        super().__init__(source_config, version, get_logger(__name__))
        self.client = WebClient(token=get_slack_bot_token())
        self.bot_user_id = self.client.auth_test()['user_id']
        self.attempts = {}
        self.curr_channel_info = {}
        self.curr_channel_membership = {}
        self.new_channel_info = []
        self.new_channel_membership = []

    def load_metadata_from_db(self):
        self.curr_channel_info = get_current_channel_info()
        self.curr_channel_membership = get_current_channel_membership()

    def save_metadata_to_db(self):
        self.update_channel_info()
        self.update_channel_membership()

    def fetch_and_save_raw_data(self):
        self.fetch_channels(get_slack_ts(self.start_ts), get_slack_ts(self.end_ts),
                            get_slack_ts(self.start_ts - THREE_DAYS))

    def fetch_channels(self, slack_start_ts, slack_end_ts, thread_lookback_ts):
        # TODO: Set start_ts / end_ts at channel level to handle failures
        self.attempts['fetch_channels'] = self.attempts.get('fetch_channels', 0) + 1
        try:
            cursor = None
            while True:
                # TODO: Remove public channel filter once we have a way to handle private channels
                result = self.client.conversations_list(cursor=cursor, exclude_archived=True, types="public_channel")
                channels = result["channels"]
                for channel in channels:
                    self.update_channel_info_metadata(channel)
                    unifyiq_bot_in_channel = self.fetch_channel_members(channel['id'])
                    if not unifyiq_bot_in_channel:
                        # Add unifyiq bot to the public channel
                        self.client.conversations_join(channel=channel['id'])
                    self.fetch_channel_messages(channel['id'], slack_start_ts, slack_end_ts, thread_lookback_ts)
                if not result['response_metadata'] or not result['response_metadata']['next_cursor']:
                    self.attempts['fetch_channels'] = 0
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.attempts['fetch_channels'], self.fetch_channels, slack_start_ts, slack_end_ts,
                                 thread_lookback_ts)

    def fetch_channel_messages(self, channel_id, slack_start_ts, slack_end_ts, thread_lookback_ts):
        self.attempts['fetch_channel_messages'] = self.attempts.get('fetch_channel_messages', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_history(cursor=cursor, channel=channel_id,
                                                           oldest=thread_lookback_ts,
                                                           latest=slack_end_ts)
                messages = result["messages"]
                for message in messages:
                    file_name = "channels"
                    # Store bot messages separately
                    if self.is_bot_message(message):
                        file_name = skip_index_file_name(file_name)
                    # Process thread replies for all messages including lookback messages
                    if message.get('thread_ts') and message.get('latest_reply') and message.get(
                            'latest_reply') > slack_start_ts:
                        self.fetch_threads(channel_id, message['thread_ts'], slack_start_ts, slack_end_ts)
                    # Process new messages only
                    if message.get('ts') and slack_start_ts < message['ts'] < slack_end_ts:
                        message = self.parse_message_response(channel_id, message)
                        if message:
                            self.validate_and_write_json(message, file_name)
                if not result['response_metadata'] or not result['response_metadata']['next_cursor']:
                    self.attempts['fetch_channel_messages'] = 0
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.attempts['fetch_channel_messages'], self.fetch_channel_messages, channel_id,
                                 slack_start_ts, slack_end_ts, thread_lookback_ts)

    def is_bot_message(self, message):
        return message.get('bot_id') or message.get('subtype') == 'bot_message' or message.get(
            'user') == self.bot_user_id or self.bot_user_id in message.get('text')

    def fetch_channel_members(self, channel_id):
        """
        Fetches the members of a channel using slack client
        """
        unifyiq_bot_in_channel = False
        self.attempts['fetch_members'] = self.attempts.get('fetch_members', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_members(cursor=cursor, channel=channel_id)
                unifyiq_bot_in_channel |= self.update_membership_metadata(channel_id, result["members"])
                if not result['response_metadata'] or not result['response_metadata']['next_cursor']:
                    self.attempts['fetch_members'] = 0
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.attempts['fetch_members'], self.fetch_channel_members, channel_id)
        return unifyiq_bot_in_channel

    def fetch_threads(self, channel_id, ts, slack_start_ts, slack_end_ts):
        """
        Fetches the threads of a channel using slack client
        """
        self.attempts['fetch_threads'] = self.attempts.get('fetch_threads', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_replies(cursor=cursor, channel=channel_id, ts=ts,
                                                           oldest=slack_start_ts, latest=slack_end_ts)
                messages = result["messages"]
                for message in messages:
                    file_name = "threads"
                    # Store bot messages separately
                    if self.is_bot_message(message):
                        file_name = skip_index_file_name(file_name)
                    message = self.parse_thread_response(channel_id, message)
                    if message:
                        self.validate_and_write_json(message, file_name)
                if not result['response_metadata'] or not result['response_metadata']['next_cursor']:
                    self.attempts['fetch_threads'] = 0
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.attempts['fetch_threads'], self.fetch_threads, channel_id, ts, slack_start_ts,
                                 slack_end_ts)

    def update_channel_info_metadata(self, data):
        channel_id = data.get('id')
        info = {"channel_id": channel_id,
                "name": data.get('name'),
                "topic": data.get('topic').get('value'),
                "purpose": data.get('purpose').get('value'),
                "is_archived": data.get('is_archived'),
                "is_private": data.get('is_private'),
                "is_channel": data.get('is_channel'),
                "is_group": data.get('is_group'),
                "is_im": data.get('is_im'),
                "is_mpim": data.get('is_mpim')}
        if channel_id not in self.curr_channel_info:
            self.new_channel_info.append(info)
        elif self.curr_channel_info[channel_id] != info:
            # Channel info has changed
            self.curr_channel_info[channel_id] = info
        else:
            # Channel info has not changed
            self.curr_channel_info.pop(channel_id, None)

    def update_membership_metadata(self, channel_id, members):
        unifyiq_bot_in_channel = False
        for mid in members:
            if mid == self.bot_user_id:
                unifyiq_bot_in_channel = True
            if (channel_id, mid) not in self.curr_channel_membership:
                # New member in channel. Should be inserted to DB
                self.new_channel_membership.append({'channel_id': channel_id, 'member_id': mid})
            # Mark the member as active
            self.curr_channel_membership[(channel_id, mid)] = True
        return unifyiq_bot_in_channel

    def parse_message_response(self, channel_id, data):
        # ignore messages with subtypes like channel join etc.
        if 'subtype' not in data:
            id_str = channel_id + "." + data.get('ts')
            ts_int = int(float(data.get('ts')))
            if 'thread_ts' in data:
                parent_id = data['thread_ts']
            else:
                # This is a regular message and won't have a parent
                parent_id = data['ts']
            data['raw_text'] = data['text']
            text = ""
            # Get only plain text and links, ignore other types mentions etc.
            for b in data.get('blocks', []):
                for e in b.get('elements', []):
                    for ee in e.get('elements', []):
                        element_type = ee.get('type', 'unknown')
                        if 'text' in ee and element_type == 'text':
                            text += ee.get('text')
                        elif 'url' in ee and element_type == 'link':
                            text += ee.get('url')
            if text:
                self.set_required_values_in_json(json_data=data, id_str=id_str, parent_id=parent_id, text=text,
                                                 url=self.get_slack_url(id_str), user=data['user'],
                                                 group=channel_id, created_at=ts_int, last_updated_at=ts_int)
                return data
            else:
                return None
        else:
            return None

    def parse_thread_response(self, channel_id, data):
        if 'thread_ts' in data and data['thread_ts'] != data['ts']:
            # process only threads and ignore regular messages
            return self.parse_message_response(channel_id, data)

    def update_channel_membership(self):
        if len(self.curr_channel_membership) > 0:
            insert_channel_membership(self.new_channel_membership)
        deleted_membership = []
        for (key, value) in self.curr_channel_membership.items():
            if value is False:
                # Mark the member as inactive
                deleted_membership.append({'channel_id': key[0], 'member_id': key[1]})
        if len(deleted_membership) > 0:
            delete_channel_membership(deleted_membership)

    def update_channel_info(self):
        if len(self.curr_channel_info) > 0:
            update_channel_info_to_db(self.curr_channel_info)
        if len(self.new_channel_info) > 0:
            insert_channel_info_to_db(self.new_channel_info)

    def get_slack_url(self, id_str):
        parts = id_str.split(".")
        return self.source_config.url_prefix + "/archives/" + parts[0] + "/p" + parts[1] + parts[2]

    def retry_slack_api(self, exception, attempt_count, function, *args):
        if exception.response["error"] == "ratelimited":
            retry_after = exception.response.headers["Retry-After"]
            self.logger.error("Rate limited. Retrying in {} seconds".format(retry_after))
            if attempt_count < MAX_ATTEMPTS_FOR_SLACK_API_CALL:
                time.sleep(int(retry_after))
                function(args)
            else:
                self.logger.error("Max attempts reached for slack api call")
        else:
            self.logger.error("Error fetching slack api: {}".format(exception))


if __name__ == '__main__':
    source_configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")
    for source_config in source_configs:
        if source_config.connector_type == constants.SLACK:
            slack = SlackAdapter(source_config, current_date_hod)
            slack.fetcher()
