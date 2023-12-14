import pandas as pd
from urllib.parse import urlparse
import glob
import json
from pydantic import BaseModel


class Item(BaseModel):
    created_at : str
    url: str
    owner: str
    repo: str
    author: str
    data_element: dict

class DataExtractorCommit:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.type_folder = 'commits'
        self.l_files = glob.glob(self.folder + '/' + self.type_folder + '/*.json')

    def load_data(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
        return data

    def get_owner_and_repo(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        return path_parts[1], path_parts[2]

    def get_created_at(self, data_element):
        return data_element['commit']['author']['date']

    def get_url(self, data_element):
        return data_element['html_url']

    def get_author(self, data_element):
        return data_element['commit']['author']['name']

    def get_item(self, file):
        data = self.load_data(file)
        items = []
        for data_element in data:
            date = self.get_created_at(data_element)
            url = self.get_url(data_element)
            owner, repo = self.get_owner_and_repo(url)
            author = self.get_author(data_element)
            items.append(Item(created_at=date, url=url, owner=owner, repo=repo, author=author, data_element=data_element))
        return items