import pandas as pd
import requests
import time
import datetime

TOKENS = [
    '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',
    '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',
    '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',
    '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',
    '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'
]

def get_github_repo(token, page=1, per_page=1000, stars_range=''):
    auth = token

    search_params = {
        'q': f'stars:{stars_range}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': per_page,
        'page': page
    }

    headers = {
        'Authorization': f'Token {auth}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(f'https://api.github.com/search/repositories', params=search_params, headers=headers)

    remaining_requests = int(response.headers.get('X-RateLimit-Remaining'))
    reset_time = int(response.headers.get('X-RateLimit-Reset'))
    if remaining_requests == 0:
        sleep_duration = reset_time - time.time() + 10
        time.sleep(sleep_duration)
        return get_github_repo(token, page=page, per_page=per_page, stars_range=stars_range)

    repositories = response.json().get('items', [])

    repo_features = []

    for repository in repositories:
        created_at = datetime.datetime.strptime(repository['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        repo_features.append({
            'name': repository['name'],
            'full_name': repository['full_name'],
            'stars': repository['stargazers_count'],
            'forks': repository['forks_count'],
            'watchers': repository['watchers_count'],
            'commits': repository['commits_url'],
            'forks_url': repository['forks_url'],
            'watchers_url': repository['subscribers_url'],
            'created_at': repository['created_at'],
            'open_issues': repository['open_issues'],
            'size': repository['size'],
            'language': repository['language']
        })

    if 'next' in response.links:
        repo_features.extend(get_github_repo(token, page=page+1, per_page=per_page, stars_range=stars_range))

    return repo_features


def preprocess_data(data):
    current_year = datetime.datetime.now().year

    if "created_at" in data.columns:
        data["created_at"] = pd.to_datetime(data["created_at"])
        data["age"] = current_year - data["created_at"].dt.year

    if "language" in data.columns:
        encoded = pd.get_dummies(data["language"], prefix="language")
        data = pd.concat([data, encoded], axis=1)
        data = data.drop(columns=["language"])
    return data

token_ranges = [
    ('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', '500..1000'),
    ('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', '6000..7000'),
    ('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', '5000..6000'),
    ('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', '3000..4000'),
    ('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', '1000..2000')
]

for token, stars_range in token_ranges:
    repo_features = get_github_repo(token, page=1, per_page=1000, stars_range=stars_range)

    

    df = pd.DataFrame(repo_features)
    repo_data = preprocess_data(df)

    filename = f'repo_features_{stars_range}.csv'
    repo_data.to_csv(filename, index=False)

