import requests


def get_from_bin(url):

    # Step 1: Identify source
    source = None
    if "pastebin.com/" in url: source = "pastebin"
    if "hastebin.com/" in url: source = "hastebin"
    if "github" in url: source = "github"
    if source is None:
        return "error", "error"

    # Step 2: Correct URL
    if source == "pastebin":
        if "raw" in url:
            unique_reference = url.split("pastebin.com/raw/", 1)[1]
        else:
            unique_reference = url.split("pastebin.com/", 1)[1]
        url = "https://pastebin.com/raw/" + unique_reference

    if source == "hastebin":
        if "raw" in url:
            unique_reference = url.split("hastebin.com/raw/", 1)[1]
        else:
            unique_reference = url.split("hastebin.com/", 1)[1]
        url = "https://hastebin.com/raw/" + unique_reference

    if source == "github":
        unique_reference = url.rsplit("/", 1)[1]

        if "raw" not in url:
            gist_path = url.split("github.com/", 1)[1]
            url = "https://raw.githubusercontent.com/" + gist_path
            url = url.replace("/blob", "")

    # Step 3: Download content
    r = requests.get(url)
    if r.status_code != 200:
        return "error", "error"

    # Deliver content
    content = r.text

    return content, unique_reference


#content, unique_reference = get_from_bin("hastebin.com/raw/aqiqaladen")
#print (content)