import requests
import base64


def get_gist_list_from_repo(url):

    # Get default tree
    r = requests.get(url)
    trees_url = (r.json()['trees_url'])
    default_branch = (r.json()['default_branch'])

    # Build tree url
    trees_url = trees_url.replace('{/sha}', "/" + default_branch + "?recursive=1")

    r = requests.get(trees_url)

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


#repo = get_gist_list_from_repo("hankhank10", "crew-resource-management", "main")

#gist = get_gist(repo[3]['url'])
