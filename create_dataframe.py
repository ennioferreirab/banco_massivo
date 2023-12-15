from data_extractor_commit import DataExtractorCommit
import pandas as pd
from data_extractor_fork import DataExtractorFork
from data_extractor_issue import DataExtractorIssue
from data_extractor_pull import DataExtractorPull
import requests



commit = DataExtractorCommit('data')
items = []

for file in commit.l_files:
    file_items = commit.get_item(file)
    items.extend(file_items)


df_commits = pd.DataFrame.from_records([item.model_dump() for item in items])



fork = DataExtractorFork('data')
fork_items = []

for file in fork.l_files:
    file_items = fork.get_item(file)
    fork_items.extend(file_items)


df_forks = pd.DataFrame.from_records([item.model_dump() for item in fork_items])


issue = DataExtractorIssue('data')
issue_items = []

for file in issue.l_files:
    file_items = issue.get_item(file)
    issue_items.extend(file_items)

df_issues = pd.DataFrame.from_records([item.model_dump() for item in issue_items])

pull = DataExtractorPull('data')
pull_items = []

for file in pull.l_files:
    file_items = pull.get_item(file)
    pull_items.extend(file_items)

df_pulls = pd.DataFrame.from_records([item.model_dump() for item in pull_items])
