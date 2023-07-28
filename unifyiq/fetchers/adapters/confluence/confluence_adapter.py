import datetime

import requests
from langchain.document_loaders import ConfluenceLoader

from fetchers.adapters.base_adapter import BaseAdapter
from fetchers.database.fetchers_confluence_db import get_current_page_info, insert_page_info_to_db, \
    update_page_info_to_db, get_page_id
from utils.constants import CONFLUENCE
from utils.database import unifyiq_config_db
from utils.database.unifyiq_config_db import get_confluence_email_address, get_confluence_api_key
from utils.log_util import get_logger


class ConfluenceAdapter(BaseAdapter):

    def __init__(self, source_config, version):
        super().__init__(source_config, version, get_logger(__name__))
        self.username = get_confluence_email_address(source_config.config_json)
        self.api_key = get_confluence_api_key(source_config.config_json)
        self.curr_page_info = {}
        self.new_page_info = []
        self.url = f"{source_config.url_prefix}/wiki/rest/api"

    def load_metadata_from_db(self):
        # load author, title, modified date, space, page id from DB and store to a dict
        self.curr_page_info = get_current_page_info()

    def save_metadata_to_db(self):
        if self.new_page_info:
            insert_page_info_to_db(self.new_page_info)
        if self.curr_page_info:
            update_page_info_to_db(self.curr_page_info.values())

    def get_all_spaces(self):
        url = f"{self.url}/space"
        params = {
            "limit": 100,  # Adjust the limit based on your needs
            "start": 0
        }

        all_spaces = []

        while True:
            response = requests.get(url, auth=(self.username, self.api_key), params=params)

            if response.status_code == 200:
                data = response.json()
                spaces = data.get('results', [])
                all_spaces.extend(spaces)

                if data['size'] < params['limit']:
                    break
                else:
                    params['start'] += params['limit']
            else:
                print(f"Failed to retrieve spaces. Status code: {response.status_code}")
                break

        return all_spaces

    def get_modified_pages(self):
        all_pages = {}
        spaces = self.get_all_spaces()
        for space in spaces:
            all_pages[space['key']] = []
            # Explore only public spaces
            if space['type'] != 'global':
                continue
            url = f"{self.url}/content"
            start_time = datetime.datetime.fromtimestamp(self.start_ts).strftime('%Y-%m-%dT%H:%M:%S.%f')
            end_time = datetime.datetime.fromtimestamp(self.end_ts).strftime('%Y-%m-%dT%H:%M:%S.%f')
            params = {
                "spaceKey": space['key'],
                "expand": "version",
                "status": "current",
                "modified": f">{start_time} and <{end_time}",
                "limit": 100  # Adjust the limit based on your needs
            }

            response = requests.get(url, auth=(self.username, self.api_key), params=params)

            if response.status_code == 200:
                data = response.json()
                pages = data.get('results', [])
                all_pages[space['key']].extend(pages)
            else:
                self.logger.error(f"Failed to retrieve pages. Status code: {response.status_code}")
        return all_pages

    def fetch_and_save_raw_data(self):
        pages = self.get_modified_pages()
        loader = ConfluenceLoader(url=self.url, username=self.username, api_key=self.api_key)
        for space in pages:
            for page in pages[space]:
                ts = int(datetime.datetime.strptime(page['version']['when'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
                meta_data = {'page_id': page['id'], 'space_key': space, 'topic': page['title'],
                             'author_email': page['version']['by']['email'],
                             'last_modified_time': ts, 'status': page['status']}
                self.update_meta_data(meta_data)
                if page['status'] == 'trashed':
                    continue
                if page['type'] != 'page' and page['type'] != 'blogpost' and page['status'] != 'current':
                    continue
                doc = {'title': page['title'], 'space_key': space}
                documents = loader.load(include_attachments=False, limit=50, page_ids=[meta_data['page_id']])
                for document in documents:
                    self.set_required_values_in_json(doc, id_str=get_page_id(space, meta_data['page_id']),
                                                     parent_id=space,
                                                     text=document.page_content,
                                                     url=document.metadata['source'],
                                                     user=meta_data['author_email'], group=meta_data['page_id'],
                                                     created_at=ts, last_updated_at=ts)
                    self.validate_and_write_json(doc, "confluence-pages")

    def update_meta_data(self, meta_data):
        comp_page_id = get_page_id(meta_data['space_key'], meta_data['page_id'])
        if comp_page_id in self.curr_page_info:
            curr_meta_data = self.curr_page_info[comp_page_id]
            if curr_meta_data != meta_data:
                self.curr_page_info[comp_page_id] = meta_data
            else:
                self.curr_page_info.pop(comp_page_id)
        else:
            self.new_page_info.append(meta_data)


if __name__ == "__main__":
    source_configs = unifyiq_config_db.get_fetcher_configs()
    current_date_hod = datetime.datetime.now().strftime("%Y-%m-%dT00-00-00")
    for config in source_configs:
        if config.connector_type == CONFLUENCE:
            c = ConfluenceAdapter(config, current_date_hod)
            c.fetcher()
