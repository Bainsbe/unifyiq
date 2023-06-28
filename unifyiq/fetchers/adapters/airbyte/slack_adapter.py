from datetime import datetime

from fetchers.adapters.airbyte.airbyte_adapter import AirbyteAdapter, get_airbyte_data
from fetchers.database.fetchers_slack_db import insert_channel_membership, \
    get_current_channel_membership, delete_channel_membership, get_current_channel_info, update_channel_info, \
    insert_channel_info

CHANNEL_MESSAGES = 1
THREADS = 2
CHANNELS = 3
CHANNEL_MEMBERS = 4
USERS = 5
UNKNOWN = -1


def get_date_from_ts(ts):
    return datetime.fromtimestamp(int(float(ts))).strftime("%Y%m%d")


class SlackAdapter(AirbyteAdapter):
    def __init__(self, config, version):
        super().__init__(config, version)

    @staticmethod
    def parse_channel_info(data, curr_info, new_info):
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
        if channel_id not in curr_info:
            new_info.append(info)
        elif curr_info[channel_id] != info:
            # Channel info has changed
            curr_info[channel_id] = info
        else:
            # Channel info has not changed
            curr_info.pop(channel_id, None)

    @staticmethod
    def parse_channel_members(data, curr_mappings, new_mappings):
        mid = data.get('member_id')
        channel_id = data.get('channel_id')
        if (channel_id, mid) not in curr_mappings:
            # New member in channel. Should be inserted to DB
            new_mappings.append({'channel_id': channel_id, 'member_id': mid})
        # Mark the member as active
        curr_mappings[(channel_id, mid)] = True

    @staticmethod
    def parse_user_info(data, curr_mappings, new_mappings):
        # TODO Add user metadata for org user matching
        pass

    def parse_messages(self, data):
        # ignore messages with subtypes like channel join etc.
        if 'subtype' not in data:
            id_str = data.get('channel_id') + "." + data.get('ts')
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
                                                 group=data['channel_id'], created_at=ts_int, last_updated_at=ts_int)
                return data
            else:
                return None
        else:
            return None

    def parse_threads(self, data):
        if 'thread_ts' in data and data['thread_ts'] != data['ts']:
            # process only threads and ignore regular messages
            # there seems to be a bug in airbyte slack connecter where it is sending regular messages as threads
            return self.parse_messages(data)

    def pass_through(self, *args):
        pass

    @staticmethod
    def get_data_type(file_name):
        if 'channel_messages' in file_name:
            return CHANNEL_MESSAGES
        elif 'threads' in file_name:
            return THREADS
        elif 'channels' in file_name:
            return CHANNELS
        elif 'channel_members' in file_name:
            return CHANNEL_MEMBERS
        elif 'users' in file_name:
            return USERS
        else:
            return UNKNOWN

    def parse_jsonl(self, jsonl_file):
        data_type = self.get_data_type(jsonl_file.name)
        meta_data_parser = self.pass_through
        message_parser = self.pass_through
        update_metadata = self.pass_through
        curr_metadata = {}
        new_metadata = []
        file_name = "unknown"

        if data_type == CHANNELS:
            curr_metadata = get_current_channel_info()
            meta_data_parser = self.parse_channel_info
            update_metadata = self.update_channel_info
        elif data_type == CHANNEL_MEMBERS:
            curr_metadata = get_current_channel_membership()
            meta_data_parser = self.parse_channel_members
            update_metadata = self.update_channel_membership
        elif data_type == USERS:
            meta_data_parser = self.parse_user_info
        elif data_type == CHANNEL_MESSAGES:
            file_name = "messages"
            message_parser = self.parse_messages
        elif data_type == THREADS:
            file_name = "threads"
            message_parser = self.parse_threads

        with open(jsonl_file, 'r') as file:
            for line in file:
                src_data = get_airbyte_data(line)
                meta_data_parser(src_data, curr_metadata, new_metadata)
                json_output = message_parser(src_data)
                if json_output:
                    self.validate_and_write_json(json_output, file_name)
            update_metadata(curr_metadata, new_metadata)

    @staticmethod
    def update_channel_membership(curr_metadata, new_metadata):
        if len(curr_metadata) > 0:
            insert_channel_membership(new_metadata)
        deleted_membership = []
        for (key, value) in curr_metadata.items():
            if value is False:
                # Mark the member as inactive
                deleted_membership.append({'channel_id': key[0], 'member_id': key[1]})
        if len(deleted_membership) > 0:
            delete_channel_membership(deleted_membership)

    @staticmethod
    def update_channel_info(curr_metadata, new_metadata):
        if len(curr_metadata) > 0:
            update_channel_info(curr_metadata)
        if len(new_metadata) > 0:
            insert_channel_info(new_metadata)

    def get_slack_url(self, id_str):
        parts = id_str.split(".")
        return self.config.url_prefix + "/archives/" + parts[0] + "/p" + parts[1] + parts[2]
