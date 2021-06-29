import requests
import base64


def get_file_list(user, repo_name, tree):

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


def get_gist(url):
    r = requests.get(url)
    print (r.status_code)

    gist = base64.b64decode(r.json()['content'])
    return gist


repo = get_file_list("hankhank10", "crew-resource-management", "main")
print(get_gist(repo[2]['url']))