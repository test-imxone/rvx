import json
import os
import re

import requests
from loguru import logger

import utils.utils as ut
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs


def get_env(url):
    # Get env file contents
    try:
        response = requests.get(url)
        content = response.text
        if response.status_code != 200:
            logger.error(f"Failed to fetch the .env file. Status code: {response.status_code}", flush=True)
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
            url = ut.manage_dls(value, repository, branch)
            dls.add(url)
    if default_patch_dl not in dls:
        dls.add(ut.manage_dls(default_patch_dl))
    return list(dls)


@logger.catch
def get_patch_data(dl_list):
    json_data = []
    for url in dl_list:
        api_url, org = ut.github_api_url(url, repository, branch)
        raw_url, org_name, tag = get_assets(api_url, org)
        json_data.append(
            {
                "org_name": org_name,
                "tag_name": tag,
                "raw_url": raw_url,
                "patches_json_dl": url,
            },
        )
    return json_data


@logger.catch
def manage_tasks(action):
    if action == "write_json":
        logger.info(f"Updating the '{output_file.split('/')[-1]}' file.", flush=True)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parse_env.patches_data, f, indent=4)


@logger.catch
def get_assets(url, org):
    patches_json_url = url
    org_name = org
    tag_name = None

    if url.startswith("https://api.github.com"):
        response = requests.get(url)
        data = response.json()
        assets = (obj["browser_download_url"] for obj in data["assets"])
        pattern = re.compile(r"json$")
        patches_json_url = next(item for item in assets if pattern.search(item))
        org_name = patches_json_url.split("/")[3]
        tag_name = data["tag_name"]

    return patches_json_url, org_name, tag_name


# Parse json_data from env_content
@logger.catch
def parse_env():
    env_content = get_env(env_url)

    env_dict = {}
    lines = env_content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.isspace():
            continue
        if "#" in line:
            line = line.split("#")[0].strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        env_dict[key] = value

    dl_data = get_patches_dls(env_dict)
    patches_data = get_patch_data(dl_data)
    patches_data.sort(key=lambda x: (x["org_name"] != "ReVanced", x["org_name"] != "inotia00", x["org_name"].lower()))
    parse_env.patches_data = patches_data
    logger.debug(f"\nCurrently using Custom Patch Resources: \n\n{json.dumps(patches_data, indent=4)}\n")
    return patches_data


gh = GitHubRepo()
repository = gh.get_repo()
branch = gh.get_backup_branch()  # Branch to get the env
urls = GitHubURLs(repository, branch)

env_url = urls.get_env()
default_patch_dl = urls.get_patches_dl()
output_file = "auto/json/patch-sources.json"

if __name__ == "__main__":
    patches_data = parse_env()
