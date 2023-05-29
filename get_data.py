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

    data["created_at"] = pd.to_datetime(data["created_at"])
    data["age"] = current_year - data["created_at"].dt.year

    if "language" in data.columns:
        encoded = pd.get_dummies(data["language"], prefix="language")
        data = pd.concat([data, encoded], axis=1)
        data = data.drop(columns=["language"])
    return data


token_ranges = [
    ('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', '20000..400000'),
    ('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', '10000..20000'),
    ('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', '5000..10000'),
    ('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', '3000..5000'),
    ('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', '1000..3000')
]

for token, stars_range in token_ranges:
    repo_features = get_github_repo(token, page=1, per_page=1000, stars_range=stars_range)

    

    df = pd.DataFrame(repo_features)
    repo_data = preprocess_data(df)

    filename = f'repo_features_{stars_range}.csv'
    repo_data.to_csv(filename, index=False)

