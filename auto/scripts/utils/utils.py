import os
import re
from loguru import logger

from utils.repo import GitHubRepo
from utils.urls import GitHubURLs

# Constants for GitHub URLs
gh = GitHubRepo()
repo = gh.get_repo()
branch = gh.get_branch()
branch = "customs"
urls = GitHubURLs(repo, branch)
sources_py_url = urls.get_sources_py()
extras_json_url = urls.get_extras_json()

@logger.catch
def generate_path(base, obj, branch=branch):
    file = f'{obj["org_name"].lower()}'
    pattern = r'[^a-zA-Z0-9_-]'
    file = f"{re.sub(pattern, '_', file)}-options.json"
    path = os.path.join(base, file)
    branch_prefix = f"../../tree/{branch}"
    generate_path.branch = os.path.join(branch_prefix, path).replace("\\", "/")
    return path

@logger.catch
def manage_dls(url, repo=repo, branch=branch):
    new_url = url

    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        arrL = len(url_arr)
        prefix = "https://github.com"
        owner = url_arr[3].lower()
        repo = url_arr[4].lower()
        suffix = f"{owner}/{repo}"

        if arrL > 5:
            suffix = suffix + "/" + "/".join(url_arr[5:])
        if arrL == 5:
            suffix = suffix + "/releases/latest"
        if arrL == 6:
            suffix = suffix + "/latest"

        new_url = f"{prefix}/{suffix}"

    elif url.startswith("local://"):
        url_arr = url.split("/")
        file = url_arr[-1]
        new_url = f"https://raw.githubusercontent.com/{repo}/{branch}/apks/{file}"

    return new_url

@logger.catch
def github_api_url(url, repo=repo, branch=branch):
    api_url = url
    org_name = "Link Resources"

    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        prefix = 'https://api.github.com/repos'
        suffix = "/".join(url_arr[3:])
        if "/tag/" in url:
            suffix = suffix.replace("/tag/", "/tags/")
        elif url.endswith("releases"):
            suffix = suffix + "/latest"
        elif not url.endswith("latest"):
            suffix = suffix + "/releases/latest"
        api_url = f"{prefix}/{suffix}"
        org_name = "GitHub Resources"

    elif url.startswith("local://") or url.startswith(f"https://raw.githubusercontent.com/{repo}/{branch}"):
        url_arr = url.split("/")
        file = url_arr[-1]
        api_url = f"https://raw.githubusercontent.com/{repo}/{branch}/apks/{file}"
        org_name = "Local Resources"

    # print(api_url, flush=True)
    return api_url, org_name

@logger.catch
def github_user(url):
    user = "the Custom Link"
    repo = "the resource"

    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        user = url_arr[3]
        repo = url_arr[4]

    elif url.startswith("local://") or url.startswith(f"https://raw.githubusercontent.com/{repo}/"):
        url_arr = url.split("/")
        user = "the Current Repository"
        repo = f"`{url_arr[-1]}`"

    return [user, repo]

@logger.catch
def extract_values(objects_array, key):
    values = []
    for obj in objects_array:
        if key in obj:
            values.append(obj[key])
    return values

@logger.catch
def sort_packages(json_data):
    json_data.sort(key=lambda x: (x["app_name"] != "YouTube", x["app_name"] != "YouTube Music", x["app_name"].lower()))
    return json_data

@logger.catch
def custom_sort_key(item):
    org_name = item["org_name"]
    if org_name == "ReVanced":
        return (0, org_name)
    elif org_name == "inotia00":
        return (1, org_name)
    elif org_name.startswith("Local Resources"):
        return (3, org_name)
    elif org_name.startswith("Link Resources"):
        return (4, org_name)
    else:
        return (2, org_name)

@logger.catch
def numbered_duplicate_orgs(json_data):
    org_name_counts = {}
    fixed_data = []
    for item in json_data:
        org_name = item.get("org_name")
        if org_name is not None:
            count = org_name_counts.get(org_name, 0)
            org_name_counts[org_name] = count + 1
            if count > 0:
                item["org_name"] = f"{org_name}: v{count + 1}"
        fixed_data.append(item)
    return fixed_data

@logger.catch
def find_object(obj, data):
    org = obj['org_name']
    tag = obj['tag_name']
    raw = obj['raw_url']
    dl = obj['patches_json_dl']

    condition = (
        lambda x: 
            x['org_name'].startswith(org) and
            x['tag_name'] == tag and
            x['raw_url'] == raw and 
            x['patches_json_dl'] == dl
    )
    filtered = filter(condition, data)
    result = next(filtered, None)
    return result