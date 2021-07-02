import requests
import base64


def get_gist_list_from_repo(user, repo_name, tree):
    api_url = "https://api.github.com/repos/" + user + "/" + repo_name +"/git/trees/" + tree + "?recursive=1"
    r = requests.get(api_url)

    output = []
    for item in r.json()['tree']:
        if item['type'] == "blob":
            output.append({
                'path': item['path'],
                'type': item['type'],
                'url': item['url']
            })

    return output


def get_gist(url, list_format = True):
    r = requests.get(url)

    gist = base64.b64decode(r.json()['content'])
    gist = str(gist,'utf-8')

    if list_format:
        gist = gist.splitlines()

    return gist


repo = get_gist_list_from_repo("hankhank10", "crew-resource-management", "main")

gist = get_gist(repo[3]['url'])
