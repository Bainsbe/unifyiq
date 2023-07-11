import time
from datetime import datetime

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from fetchers.adapters.base_adapter import BaseAdapter
from fetchers.database.fetchers_slack_db import insert_channel_membership, \
    get_current_channel_membership, delete_channel_membership, get_current_channel_info, update_channel_info, \
    insert_channel_info
from utils import constants
from utils.configs import get_slack_bot_token
from utils.constants import MAX_ATTEMPTS_FOR_SLACK_API_CALL
from utils.database import unifyiq_config_db
from utils.log_util import get_logger

CHANNEL_MESSAGES = 1
THREADS = 2
CHANNELS = 3
CHANNEL_MEMBERS = 4
USERS = 5
UNKNOWN = -1


def get_date_from_ts(ts):
    return datetime.fromtimestamp(int(float(ts))).strftime("%Y%m%d")


def get_slack_ts(ts):
    return "{:.6f}".format(ts)


class SlackAdapter(BaseAdapter):

    def __init__(self, config, version):
        super().__init__(config, version, get_logger(__name__))
        self.client = WebClient(token=get_slack_bot_token())
        self.attempts = {}
        self.slack_start_ts = get_slack_ts(self.start_ts)
        self.slack_end_ts = get_slack_ts(self.end_ts)
        self.curr_channel_info = {}
        self.curr_channel_membership = {}
        self.new_channel_info = []
        self.new_channel_membership = []

    def load_metadata(self):
        self.curr_channel_info = get_current_channel_info()
        self.curr_channel_membership = get_current_channel_membership()

    def save_metadata(self):
        self.update_channel_info()
        self.update_channel_membership()

    def fetch_and_save_raw_data(self):
        self.fetch_conversations()
        # self.fetch_threads("channel_id")
        pass

    def fetch_conversations(self):
        # TODO: Ignore messages from bots
        self.attempts['fetch_conversations'] = self.attempts.get('fetch_conversations', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_list(cursor=cursor, exclude_archived=True)
                channels = result["channels"]
                for channel in channels:
                    self.parse_channel_info(channel)
                    # Extract messages from public channels
                    if channel['is_channel'] and not channel['is_private']:
                        self.fetch_conversation_messages(channel['id'])
                        self.fetch_members(channel['id'])
                if not result['response_metadata']['next_cursor']:
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.fetch_conversations)

    def fetch_conversation_messages(self, conversation_id):
        self.attempts['fetch_conversation_messages'] = self.attempts.get('fetch_conversation_messages', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_history(cursor=cursor, channel=conversation_id,
                                                           oldest=self.slack_start_ts,
                                                           latest=self.slack_end_ts)
                conversation_history = result["messages"]
                for conversation in conversation_history:
                    message = self.parse_messages(conversation_id, conversation)
                    if message:
                        self.validate_and_write_json(message, "conversations")
                if not result['response_metadata'] or not result['response_metadata']['next_cursor']:
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.fetch_conversation_messages, conversation_id)

    def retry_slack_api(self, exception, function, *args, **kwargs):
        if exception.response["error"] == "ratelimited":
            retry_after = exception.response.headers["Retry-After"]
            self.logger.error("Rate limited. Retrying in {} seconds".format(retry_after))
            time.sleep(int(retry_after))
            if self.attempts['fetch_conversations'] < MAX_ATTEMPTS_FOR_SLACK_API_CALL:
                function(args, kwargs)
            else:
                self.logger.error("Max attempts reached for slack api call")
        else:
            self.logger.error("Error fetching conversations: {}".format(exception))

    def parse_channel_info(self, data):
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

    def parse_channel_members(self, data):
        mid = data.get('member_id')
        channel_id = data.get('channel_id')
        if (channel_id, mid) not in self.curr_channel_membership:
            # New member in channel. Should be inserted to DB
            self.new_channel_membership.append({'channel_id': channel_id, 'member_id': mid})
        # Mark the member as active
        self.curr_channel_membership[(channel_id, mid)] = True

    @staticmethod
    def parse_user_info(data, curr_mappings, new_mappings):
        # TODO Add user metadata for org user matching
        pass

    def parse_messages(self, conversation_id, data):
        # ignore messages with subtypes like channel join etc.
        if 'subtype' not in data:
            id_str = conversation_id + "." + data.get('ts')
            ts_int = int(float(data.get('ts')))
            if 'thread_ts' in data:
                parent_id = data['thread_ts']
            else:
                # This is a regular message and won't have a parent
                parent_id = data['ts']
            text = ""
            # Get only plain text, ignore other types like links, mentions etc.
            if 'blocks' in data and 'elements' in data.get('blocks')[0] and 'elements' in \
                    data.get('blocks')[0].get('elements')[0]:
                for e in data.get('blocks')[0].get('elements')[0].get('elements'):
                    if 'text' in e and e.get('type', 'unknown') == 'text':
                        text += e.get('text')
            if text:
                self.set_required_values_in_json(json_data=data, id_str=id_str, parent_id=parent_id, text=text,
                                                 url=self.get_slack_url(id_str), user=data['user'],
                                                 group=conversation_id, created_at=ts_int, last_updated_at=ts_int)
                return data
            else:
                return None
        else:
            return None

    def parse_threads(self, data):
        if 'thread_ts' in data and data['thread_ts'] != data['ts']:
            # process only threads and ignore regular messages
            return self.parse_messages(data)

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
            update_channel_info(self.curr_channel_info)
        if len(self.new_channel_info) > 0:
            insert_channel_info(self.new_channel_info)

    def get_slack_url(self, id_str):
        parts = id_str.split(".")
        return self.config.url_prefix + "/archives/" + parts[0] + "/p" + parts[1] + parts[2]

    def fetch_members(self, channel_id):
        """
        Fetches the members of a channel using slack client
        """
        self.attempts['fetch_members'] = self.attempts.get('fetch_members', 0) + 1
        try:
            cursor = None
            while True:
                result = self.client.conversations_members(cursor=cursor, channel=channel_id)
                members = result["members"]
                for member in members:
                    self.curr_channel_membership[(channel_id, member)] = True
                if not result['response_metadata']['next_cursor']:
                    break
                cursor = result['response_metadata']['next_cursor']
        except SlackApiError as e:
            # handle slack rate limit
            self.retry_slack_api(e, self.fetch_conversations)

    def fetch_threads(self, channel_id):
        pass


if __name__ == '__main__':
    configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")
    for config in configs:
        if config.connector_platform == constants.CUSTOM and config.connector_type == constants.SLACK:
            slack = SlackAdapter(config, current_date_hod)
            slack.fetcher()
