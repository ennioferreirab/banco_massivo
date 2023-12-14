from data_extractor_commit import DataExtractorCommit
import pandas as pd
from data_extractor_fork import DataExtractorFork
from data_extractor_issue import DataExtractorIssue
from data_extractor_pull import DataExtractorPull
import requests

def get_contributors(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    response = requests.get(url)
    return response.json()

commit = DataExtractorCommit('data')
items = []

for file in commit.l_files:
    file_items = commit.get_item(file)
    items.extend(file_items)


df = pd.DataFrame.from_records([item.model_dump() for item in items])



fork = DataExtractorFork('data')
fork_items = []

for file in fork.l_files:
    file_items = fork.get_item(file)
    fork_items.extend(file_items)


example_fork = fork_items[0]


example_fork

#%%


issue = DataExtractorIssue('data')
issue_items = []

for file in issue.l_files:
    file_items = issue.get_item(file)
    issue_items.extend(file_items)

issue_items
# %%


pull = DataExtractorPull('data')
pull_items = []

for file in pull.l_files:
    file_items = pull.get_item(file)
    pull_items.extend(file_items)




get_contributors('pandas-dev', 'pandas')
# %%

from datetime import datetime
import pytz


def convert_star_date(str):
    core_date_str = " ".join(str.split()[:5])
    parsed_date = datetime.strptime(core_date_str, '%a %b %d %Y %H:%M:%S')
    return parsed_date

stars = pd.read_csv('data/star_history.csv', header=None, names=['owner_repo', 'date','stars'], parse_dates=True)
stars['date'] = stars['date'].apply(convert_star_date)





# %%
