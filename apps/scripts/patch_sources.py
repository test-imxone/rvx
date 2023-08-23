import os
import re
import json
import requests
from loguru import logger

import utils.writer as wr
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs

def get_env(url, branch):
    # Get env file contents
    try:
        response = requests.get(url)
        content = response.text
        if response.status_code != 200:
            logger.debug(f"Failed to fetch the .env file. Status code: {response.status_code}", flush=True)
            print("Assuming the .env file doesn't exist, using an empty one...", flush=True)
            content = "# Empty .env file"
    except:
        print("The .env file doesn't exist. Using an empty one...", flush=True)
        content = "# Empty .env file"
    finally:
        return content

@logger.catch
def get_patches_dls(dict):
    dls = set()
    for key, value in dict.items():
        if key.endswith("_JSON_DL"):
            url = manage_dls(value)
            dls.add(url)
    if not dls:
        dls.add(manage_dls(default_patch_dl))
    dl_list = list(dls)
    return dl_list

@logger.catch
def get_patch_data(dl_list):
    json_data = []
    for url in dl_list:
        api_url, org = github_api_url(url)
        raw_url, org_name, tag = get_assets(api_url, org)
        json_data.append({
            "org_name": org_name,
            "tag_name": tag,
            "raw_url": raw_url,
            "patches_json_dl": url,
        })
    return json_data

@logger.catch
def manage_tasks(action):

    if action == "write_json":
        logger.info(f"Updating the '{output_file.split('/')[-1]}' file.", flush=True)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parse_env.patches_data, f, indent=4)

@logger.catch
def manage_dls(url):
    new_url = url

    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        prefix = "https://github.com"
        suffix = "/".join(url_arr[3:4]).lower() + "/" + "/".join(url_arr[4:])
        if not url.endswith("latest"):
            suffix = suffix + "/releases/latest"
        new_url = f"{prefix}/{suffix}"

    return new_url

@logger.catch
def github_api_url(url):
    api_url = url
    org_name = "Link Resources"

    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        prefix = 'https://api.github.com/repos'
        suffix = "/".join(url_arr[3:])
        if "/tag/" in url:
            suffix = suffix.replace("/tag/", "/tags/")
        elif not url.endswith("latest"):
            suffix = suffix + "/releases/latest"
        api_url = f"{prefix}/{suffix}"
        org_name = "GitHub Resources"

    elif url.startswith("local://"):
        url_arr = url.split("/")
        file = url_arr[-1]
        api_url = f"https://raw.githubusercontent.com/{repository}/{branch}/apks/{file}"
        org_name = "Local Resources"

    # print(api_url, flush=True)
    return api_url, org_name

@logger.catch
def get_assets(url, org):
    patches_json_url = url
    org_name = org
    tag_name = None

    if url.startswith("https://api.github.com"):
        response = requests.get(url)
        data = response.json()
        assets = map(lambda obj: obj['browser_download_url'], data['assets'])
        pattern = re.compile(r'json$')
        patches_json_url = next(item for item in assets if pattern.search(item))
        org_name = patches_json_url.split("/")[3]
        tag_name = data['tag_name']

    return patches_json_url, org_name, tag_name

# Parse json_data from env_content
@logger.catch
def parse_env():
    env_content = get_env(env_url, branch)

    env_dict = {}
    lines = env_content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.isspace():
            continue
        if '#' in line:
            line = line.split('#')[0].strip()
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        env_dict[key] = value

    dl_data = get_patches_dls(env_dict)
    patches_data = get_patch_data(dl_data)
    patches_data.sort(key=lambda x: (x["org_name"] != "ReVanced", x["org_name"] != "inotia00", x["org_name"].lower()))
    parse_env.patches_data = patches_data
    logger.debug((
        f"\nCurrently using Custom Patch Resources: \n"
        f"\n{json.dumps(patches_data, indent=4)}\n"
        ))
    # manage_tasks("write_json")
    return patches_data


gh = GitHubRepo()
repository = gh.get_repo()
branch = gh.get_branch() # Branch to get the env
urls = GitHubURLs(repository, "customs")

env_url = urls.get_env()
default_patch_dl = urls.get_patches_dl()
output_file = "apps/json/patch-sources.json"

if __name__ == "__main__":
    patches_data = parse_env()

# patches_data = json.loads('''[
# {
#     "org_name": "ReVanced",
#     "tag_name": "v2.187.0",
#     "raw_url": "https://github.com/ReVanced/revanced-patches/releases/download/v2.187.0/patches.json",
#     "patches_json_dl": "https://github.com/revanced/revanced-patches/releases/latest"
# },
# {
#     "org_name": "inotia00",
#     "tag_name": "v2.187.1",
#     "raw_url": "https://github.com/inotia00/revanced-patches/releases/download/v2.187.1/patches.json",
#     "patches_json_dl": "https://github.com/inotia00/revanced-patches/releases/latest"
# },
# {
#     "org_name": "Link Resources",
#     "tag_name": null,
#     "raw_url": "https://raw.githubusercontent.com/revanced/revanced-patches/main/patches.json",
#     "patches_json_dl": "https://raw.githubusercontent.com/revanced/revanced-patches/main/patches.json"
# },
# {
#     "org_name": "Local Resources",
#     "tag_name": null,
#     "raw_url": "https://raw.githubusercontent.com/IMXEren/rvx-builds/changelogs/apks/options.json",
#     "patches_json_dl": "local://options.json"
# },
# {
#     "org_name": "YT-Advanced",
#     "tag_name": "v2.188.1",
#     "raw_url": "https://github.com/YT-Advanced/ReX-patches/releases/download/v2.188.1/patches.json",
#     "patches_json_dl": "https://github.com/yt-advanced/ReX-patches/releases/latest"
# }
# ]''')