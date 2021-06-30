import requests


def download_content(url):

    # Step 1: Correct URL
    if "pastebin.com/" not in url: return "error"
    if "raw" in url:
        unique_reference = url.split("pastebin.com/raw/", 1)[1]
        url = "https://pastebin.com/raw/" + unique_reference
    else:
        unique_reference = url.split("pastebin.com/", 1)[1]
        url = "https://pastebin.com/raw/" + unique_reference

    # Step 2: Download content
    r = requests.get(url)
    if r.status_code != 200: return "error"

    # Step 3: Split into lines
    content = r.text.splitlines()

    return content
