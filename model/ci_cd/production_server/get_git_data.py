import pandas as pd
import requests
import time
import re
from collections import Counter
import datetime
from numpy import loadtxt

def get_github_repo(page=1):

    # GitHub auth token to get access
    auth = 'auth'

    search_params = {
        'q': 'stars:>=50',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 1000,
        'page': page
    }

    # Set the request headers with the auth token and media type
    headers = {
        'Authorization': f'Token {auth}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # the GET request for the GitHub API
    response = requests.get(f'https://api.github.com/search/repositories', params=search_params, headers=headers)

    # Take care of the github rate limit
    remaining_requests = int(response.headers.get('X-RateLimit-Remaining'))
    reset_time = int(response.headers.get('X-RateLimit-Reset'))

    if remaining_requests == 0:
        sleep_duration = reset_time - time.time() + 10
        time.sleep(sleep_duration)
        return get_github_repo(page=page)

    # Process response to get repo features. This is now a list of repos that have different features
    repositories = response.json().get('items', [])

    repo_features = []

    for repository in repositories:

        repo_features.append({
            'language': repository['language'],
            'stars': repository['stargazers_count'],
            'forks': repository['forks_count'],
            'watchers': repository['watchers_count'],
            'open_issues': repository['open_issues_count'],
            'size': repository['size'],
            'created_at': repository['created_at'],
            'updated_at': repository['updated_at'],
            'name': repository['name'],
            'full_name': repository['full_name'],
            'commits': repository['commits_url'],
            'forks_url': repository['forks_url'],
            'watchers_url': repository['subscribers_url'],

        })


    if 'next' in response.links:
        repo_features.extend(get_github_repo(page=page+1))

    return repo_features


repo_features = get_github_repo()

repo_data = pd.DataFrame(repo_features)

#Save to a CSV file
repo_data.to_csv('repo_features.csv', index=False)
