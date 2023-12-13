from tenacity import retry, stop_after_attempt, wait_fixed
import httpx
import json
import os
import asyncio

toke = ""
PER_PAGE = 100
url_base = "https://api.github.com/repos"
headers = {"Authorization": f"token {token}"}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def make_request(url, params):
    async with httpx.AsyncClient(headers=headers) as client:
        return await client.get(url, params=params)

async def get_data(url, category, repo_name, start_page=1, stop_page=2):
    page = start_page
    while page <= stop_page:
        print(f'Processing {category}, Page: {page}')
        response = await make_request(url, params={"page": page, "per_page": PER_PAGE})

        if response.status_code == 200:
            data = response.json()
            save_to_json(data, f"data/{category}/{repo_name}_{category}_{page}.json")
            save_last_page_info(repo_name, category, page)
            yield data
            if not data:
                break
        else:
            print(f"Erro ao acessar a API do GitHub: {response.status_code}")
            break
        page += 1

def save_last_page_info(repo_name, category, last_page):
    with open(f"data/last_page_info/{repo_name}_{category}_last_page.json", 'w') as file:
        json.dump({"last_page": last_page}, file, indent=4)



def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)



def read_last_page_info(repo_name, category):
    filename = f"data/last_page_info/{repo_name}_{category}_last_page.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get("last_page", 0)
    return 0

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



async def main():
    for repo in repos:
        owner, repo_name = repo.split("/")
        print(f"Processando {repo}")

        # last_page_forks = read_last_page_info(repo_name, "forks")
        # async for _ in get_data(f"{url_base}/{owner}/{repo_name}/forks", "forks", repo_name, last_page_forks + 1, 999):
        #     pass

        # last_page_issues = read_last_page_info(repo_name, "issues")
        # async for _ in get_data(f"{url_base}/{owner}/{repo_name}/issues", "issues", repo_name, last_page_issues + 1, 999):
        #     pass

        # last_page_commits = read_last_page_info(repo_name, "commits")
        # async for _ in get_data(f"{url_base}/{owner}/{repo_name}/commits", "commits", repo_name, last_page_commits + 1, 999):
        #     pass

        last_page_pulls = read_last_page_info(repo_name, "pulls")
        async for _ in get_data(f"{url_base}/{owner}/{repo_name}/pulls", "pulls", repo_name, last_page_pulls + 1, 999):
            pass

asyncio.run(main())


