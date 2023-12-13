import pandas as pd
from urllib.parse import urlparse
import glob
import json
from pydantic import BaseModel
from typing import Optional, List, Dict


class PullModel(BaseModel):
    owner: str
    repo: str
    html_url: str
    state: str
    title: str
    user_type: str
    user_login: str
    body: str | None
    created_at: str
    updated_at: str | None
    closed_at: str | None
    merged_at: str | None
    assignee: dict | None
    labels: list
    milestone: dict | None

class DataExtractorPull:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.type_folder = 'pulls'
        self.l_files = glob.glob(self.folder + '/' + self.type_folder + '/*.json')

    def load_data(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
        return data
    
    def get_owner_and_repo(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        return path_parts[1], path_parts[2]
    
    def get_url(self, data_element):
        return data_element['html_url']
    
    def get_item(self, file):
        data = self.load_data(file)
        items = []
        for data_element in data:
            url = self.get_url(data_element)
            owner, repo = self.get_owner_and_repo(url)
            items.append(PullModel(
                owner=owner, 
                repo=repo, 
                html_url=url, 
                state=data_element['state'],
                title=data_element['title'],
                user_type=data_element['user']['type'],
                user_login=data_element['user']['login'],
                body=data_element['body'],
                created_at=data_element['created_at'],
                updated_at=data_element.get('updated_at', None),
                closed_at=data_element.get('closed_at', None),
                merged_at=data_element.get('merged_at', None),
                assignee=data_element.get('assignee', None),
                labels=data_element.get('labels', []),
                milestone=data_element.get('milestone', None)
            ))
        return items