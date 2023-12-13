import pandas as pd
from urllib.parse import urlparse
import glob
import json
from pydantic import BaseModel

# Pydantic model for each fork
class ForkModel(BaseModel):
    url: str
    owner: str
    repo: str
    created_at: str
    updated_at: str
    languages_url: str
    stargazers_url: str
    stargazers_count: int
    watchers_count: int
    language: str | None
    has_issues: bool
    forks_count: int
    open_issues_count: int
    contributors_url: str

class DataExtractorFork:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.type_folder = 'forks'
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
            items.append(ForkModel(
                url=url, 
                owner=owner, 
                repo=repo, 
                created_at=data_element['created_at'],
                updated_at=data_element['updated_at'],
                languages_url=data_element.get('languages_url', ''),
                stargazers_url=data_element.get('stargazers_url', ''),
                stargazers_count=data_element.get('stargazers_count', 0),
                watchers_count=data_element.get('watchers_count', 0),
                language=data_element.get('language'),
                has_issues=data_element.get('has_issues', False),
                forks_count=data_element.get('forks_count', 0),
                open_issues_count=data_element.get('open_issues_count', 0),
                contributors_url=data_element.get('contributors_url', '')
            ))
        return items