import requests
import datetime
TOP = 20


def fetch_trending_repositories(top_size):
    week_ago_date = str(datetime.date.today() - \
                        datetime.timedelta(days=7))
    request_to_github = requests.get\
    ('https://api.github.com/search/repositories?q=created:>{}'.\
     format(week_ago_date))
    response_list = request_to_github.json()['items'][:top_size]
    return response_list


def fetch_list_open_issues(repo_owner, repo_name):
    request_to_github = requests.get('https://api.github.com/repos/{}/{}/issues'\
                                     .format(repo_owner, repo_name))
    response_list = request_to_github.json()
    return list(filter(lambda response: response['state'] == \
                                        'open', response_list))


def print_open_issues_of_repo(repo_owner, repo_name, stars_count, list_of_issues):
    print('{name}\'s repository {repo} has {stars_count}\
 stars and {issues_count} open issues.'.format(name=repo_owner,\
    repo=repo_name,stars_count=stars_count,issues_count=len(list_of_issues)))
    print('Links to issues:')
    for issue in list_of_issues:
        print(issue['url'])
    print('')


if __name__ == '__main__':
    top_reps = fetch_trending_repositories(TOP)
    for repo in top_reps:
        repo_owner = repo['owner']['login']
        repo_name = repo['name']
        stars_count = repo['stargazers_count']
        list_of_open_issues = fetch_list_open_issues(repo_owner, repo_name)
        if len(list_of_open_issues) > 0:
            print_open_issues_of_repo(repo_owner, repo_name, stars_count, list_of_open_issues)
