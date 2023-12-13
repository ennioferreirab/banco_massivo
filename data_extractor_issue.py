import pandas as pd
from urllib.parse import urlparse
import glob
import json
from pydantic import BaseModel
from typing import Optional, List, Dict

# Pydantic model for each issue

class IssueModel(BaseModel):
    owner: str
    repo: str
    html_url: str
    title: str
    created_at: str
    updated_at: str
    closed_at: str | None
    merged_at: str | None
    pull_request_url: str
    author_association: str
    labels: List[Dict]
    state: str
    assignee: Optional[Dict]
    milestone: Optional[Dict]
    body: str | None
    user_login: str
    user_type: str
    reactions_positive: int
    reactions_negative: int
    reactions_laugh: int
    reactions_hooray: int
    reactions_confused: int
    reactions_heart: int
    reactions_rocket: int
    reactions_eyes: int

class DataExtractorIssue:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.type_folder = 'issues'
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
            pull_request_url = data_element.get('pull_request', {}).get('url', '')
            pull_request_merged_at = data_element.get('pull_request', {}).get('merged_at', '')
            items.append(IssueModel(
                owner=owner,
                repo=repo,
                html_url=url, 
                title=data_element['title'], 
                created_at=data_element['created_at'],
                updated_at=data_element['updated_at'],
                closed_at=data_element.get('closed_at', ''),
                merged_at=pull_request_merged_at,
                pull_request_url=pull_request_url,
                author_association=data_element['author_association'],
                labels=data_element['labels'],
                state=data_element['state'],
                assignee=data_element.get('assignee', {}),
                milestone=data_element.get('milestone', {}),
                body=data_element['body'],
                user_login=data_element['user']['login'],
                user_type=data_element['user']['type'],
                reactions_positive=data_element['reactions']['+1'],
                reactions_negative=data_element['reactions']['-1'],
                reactions_laugh=data_element['reactions']['laugh'],
                reactions_hooray=data_element['reactions']['hooray'],
                reactions_confused=data_element['reactions']['confused'],
                reactions_heart=data_element['reactions']['heart'],
                reactions_rocket=data_element['reactions']['rocket'],
                reactions_eyes=data_element['reactions']['eyes']
                )
            )
        return items
