from create_dataframe import df_commits, df_pulls, df_forks, df_issues
import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from datetime import datetime
import pytz

repos = [
    "langchain-ai/langchain",
    "PaddlePaddle/PaddleNLP",
    "nebuly-ai/nebuly",
    "microsoft/torchscale",
    "postgresml/postgresml",
    "run-llama/llama_index",
    "argilla-io/argilla",
    "bigscience-workshop/petals",
    "neuml/txtai",
    "intel/intel-extension-for-transformers",
    "uptrain-ai/uptrain",
    "skypilot-org/skypilot",
    "lancedb/lance",
    "swirlai/swirl-search",
    "BlinkDL/RWKV-LM",
    ]

def convert_star_date(str):
    core_date_str = " ".join(str.split()[:5])
    parsed_date = datetime.strptime(core_date_str, '%a %b %d %Y %H:%M:%S')
    return parsed_date

def get_contributors(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    response = requests.get(url)
    return response.json()


class RepositoryAnalyticsElapsed:
    def __init__(self, df_commits, df_pulls, df_issues, df_forks, df_stars):
        self.df_commits = df_commits
        self.df_pulls = df_pulls
        self.df_issues = df_issues
        self.df_forks = df_forks
        self.df_stars = df_stars


    def prepare_dataframe(self, df, metric):
        df_prepared = df.copy()
        df_prepared['created_at'] = pd.to_datetime(df_prepared['created_at'])
        df_prepared.sort_values(by=['repo', 'created_at'], inplace=True)
        df_prepared['time_since_first'] = df_prepared.groupby('repo')['created_at'].transform(lambda x: (x - x.min()).dt.days)
        return df_prepared

    def create_count_metric_elapsed(self, df, metric):
        df_prepared = self.prepare_dataframe(df, metric)
        count_metric = df_prepared.groupby(['time_since_first', 'repo'])[metric].count().unstack().fillna(0).cumsum()
        return count_metric

    def create_latency_metric_elapsed(self, df, metric):
        df_prepared = self.prepare_dataframe(df, metric)
        df_prepared['closed_at'] = pd.to_datetime(df_prepared['closed_at'])
        df_prepared['latency'] = (df_prepared['closed_at'] - df_prepared['created_at']).dt.days
        latency_metric = df_prepared.groupby(['time_since_first', 'repo'])['latency'].mean().unstack().fillna(0)
        return latency_metric

    def plot_metric_elapsed(self, metric, owner_repos, title):
        sns.set_theme(style="whitegrid")

        repos = [repo.split('/')[1] for repo in owner_repos]
        metric_filtered = metric[repos]
        metric_melted = metric_filtered.reset_index().melt(id_vars=['time_since_first'], var_name='Repositório', value_name='Count')

        sns.lineplot(data=metric_melted, x='time_since_first', y='Count', hue='Repositório')

        plt.title(title)
        plt.xlabel('Dias desde o início')
        plt.ylabel('Contagem Acumulada')
        plt.show()

    def plot_commits(self, repo):
        count_commits = self.create_count_metric_elapsed(self.df_commits, 'url')
        self.plot_metric_elapsed(count_commits, repo, 'Número acumulado de commits')

    def plot_pull_requests(self, repo):
        count_pulls = self.create_count_metric_elapsed(self.df_pulls, 'repo')
        self.plot_metric_elapsed(count_pulls, repo, 'Número acumulado de pull requests')

    def plot_issues(self, repo):
        count_issues = self.create_count_metric_elapsed(self.df_issues, 'repo')
        self.plot_metric_elapsed(count_issues, repo, 'Número acumulado de issues')

    def plot_forks(self, repo):
        count_forks = self.create_count_metric_elapsed(self.df_forks, 'repo')
        self.plot_metric_elapsed(count_forks, repo, 'Número acumulado de forks')

    def plot_latency_pulls(self, repo):
        latency_pulls = self.create_latency_metric_elapsed(self.df_pulls, 'repo')
        self.plot_metric_elapsed(latency_pulls, repo, 'Latência média de pull requests')

    def plot_latency_issues(self, repo):
        latency_issues = self.create_latency_metric_elapsed(self.df_issues, 'repo')
        self.plot_metric_elapsed(latency_issues, repo, 'Latência média de issues')
    
    def plot_stars_over_time_elapsed(self, repos):
        all_stars_data = pd.DataFrame()

        for repo in repos:
            repo_stars = self.df_stars.query(f'owner_repo == "{repo}"')
            if not repo_stars.empty:
                repo_stars = repo_stars.copy()
                repo_stars['time_since_first'] = (repo_stars['date'] - repo_stars['date'].min()).dt.days
                repo_stars['repo'] = repo
                all_stars_data = pd.concat([all_stars_data, repo_stars])


        sns.lineplot(data=all_stars_data, x='time_since_first', y='stars', hue='owner_repo')
        plt.title('Estrelas acumuladas ao longo do tempo')
        plt.xlabel('Dias desde o início')
        plt.ylabel('Estrelas acumuladas')
        plt.xticks(rotation=45)
        plt.legend(title='Repositório')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(15, 8))


    



class RepositoryAnalytics:
    def __init__(self, df_commits, df_pulls, df_issues, df_forks, df_stars):
        self.df_commits = df_commits
        self.df_pulls = df_pulls
        self.df_issues = df_issues
        self.df_forks = df_forks
        self.df_stars = df_stars
        
        
    def create_count_metric(self, df, metric):
        df_metric = df.copy()
        df_metric['created_at'] = pd.to_datetime(df_metric['created_at'])
        df_metric.set_index('created_at', inplace=True)
        count_metric = df_metric.groupby([pd.Grouper(freq='M'), 'repo'])[metric].count().unstack()
        return count_metric

    def create_latency_metric(self, df, metric):
        df_latency = df.copy()
        df_latency['created_at'] = pd.to_datetime(df_latency['created_at'])
        df_latency['closed_at'] = pd.to_datetime(df_latency['closed_at'])
        df_latency['latency'] = (df_latency['closed_at'] - df_latency['created_at']).dt.days
        df_latency.set_index('created_at', inplace=True)
        latency_metric = df_latency.groupby([pd.Grouper(freq='M'), 'repo'])['latency'].mean().unstack()
        return latency_metric

    def plot_metric(self, metric, owner_repos, title):
        sns.set_theme(style="whitegrid")
        repos = [repo.split('/')[1] for repo in owner_repos]
        metric_filtered = metric[repos]
        metric_melted = metric_filtered.reset_index().melt(id_vars=[metric.index.name], var_name='Repositório', value_name='Count')
        sns.lineplot(data=metric_melted, x=metric.index.name, y='Count', hue='Repositório')
        plt.xlabel('Month/Year')
        plt.title(title)
        plt.legend(title='Repositório')
        plt.xticks(rotation=45)
        plt.show()

    def plot_commits(self, repo):
        count_commits = self.create_count_metric(self.df_commits, 'url')
        self.plot_metric(count_commits, repo, 'Número de commits por mês')

    def plot_pull_requests(self, repo):
        count_pulls = self.create_count_metric(self.df_pulls, 'repo')
        self.plot_metric(count_pulls, repo, 'Número de pull requests por mês')

    def plot_issues(self, repo):
        count_issues = self.create_count_metric(self.df_issues, 'repo')
        self.plot_metric(count_issues, repo, 'Número de issues por mês')

    def plot_forks(self, repo):
        count_forks = self.create_count_metric(self.df_forks, 'repo')
        self.plot_metric(count_forks, repo, 'Número de forks por mês')

    def plot_latency_pulls(self, repo):
        latency_pulls = self.create_latency_metric(self.df_pulls, 'repo')
        self.plot_metric(latency_pulls, repo, 'Latência de pull requests por mês')

    def plot_latency_issues(self, repo):
        latency_issues = self.create_latency_metric(self.df_issues, 'repo')
        self.plot_metric(latency_issues, repo, 'Latência de issues por mês')
    
    def plot_stars_over_time(self, repos):
        stars_df = self.df_stars.copy()
        stars_df['date'] = pd.to_datetime(stars_df['date'])

        filtered_stars_df = stars_df[stars_df['owner_repo'].isin(repos)]

        sns.set_theme(style="whitegrid")

        sns.lineplot(data=filtered_stars_df, x='date', y='stars', hue='owner_repo')

        plt.xlabel('Data')
        plt.ylabel('Estrelas Acumuladas')
        plt.title('Evolução das Estrelas ao Longo do Tempo')
        plt.legend(title='Repositório')
        plt.xticks(rotation=45)
        plt.show()



df_stars = pd.read_csv('data/star_history.csv', header=None, names=['owner_repo', 'date','stars'])
df_stars['date'] = df_stars['date'].apply(convert_star_date)
contributors = get_contributors('langchain-ai', 'langchain')


from datetime import datetime
from pytz import utc


end_date = datetime.strptime("2023-06-30", '%Y-%m-%d').replace(tzinfo=utc)

analytics_elapsed = RepositoryAnalyticsElapsed(df_commits, df_pulls, df_issues, df_forks, df_stars)
analytics = RepositoryAnalytics(df_commits, df_pulls, df_issues, df_forks,df_stars)

analytics.plot_commits(['langchain-ai/langchain', 'PaddlePaddle/PaddleNLP'])
analytics.plot_pull_requests(['langchain-ai/langchain', 'PaddlePaddle/PaddleNLP'])

analytics_elapsed.plot_commits(['bigscience-workshop/petals', 'neuml/txtai'])
analytics_elapsed.plot_latency_pulls(['bigscience-workshop/petals', 'neuml/txtai'])


analytics.plot_stars_over_time(['langchain-ai/langchain', 'PaddlePaddle/PaddleNLP'])


analytics_elapsed.plot_stars_over_time_elapsed(['langchain-ai/langchain', 'PaddlePaddle/PaddleNLP'])
