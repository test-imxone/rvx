import re
import json
import requests
from loguru import logger

import utils.writer as wr
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs

@logger.catch
def deduplicate(list):
    seen = {}
    new_list = [seen.setdefault(x, x) for x in list if x not in seen]
    return new_list

# Get info from .env and supported packages & its codes
@logger.catch
def get_pkg():
    # Get env file contents
    response = requests.get(env_file_url)
    env_content = response.text
    
    # Get App Packages and Codes
    response = requests.get(py_file_url)
    python_code = response.text
    pattern = r'"([^"]+)":\s*"([^"]+)",'
    matches = re.findall(pattern, python_code)
    get_pkg.packages = []
    get_pkg.codes = []
    for package_name, code in matches:
        get_pkg.packages.append(package_name.strip())
        get_pkg.codes.append(code.strip())
    get_pkg.packages = deduplicate(get_pkg.packages)
    get_pkg.codes = deduplicate(get_pkg.codes)
    return env_content

# Parse json_data from env_content
@logger.catch
def parse_json_data(env_content):
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

    # Generate the JSON structure
    extra_files_list = env_dict.get("EXTRA_FILES", "").split(",")
    existing_downloaded_apks_list = env_dict.get("EXISTING_DOWNLOADED_APKS", "").split(",")
    patch_apps_list = env_dict.get("PATCH_APPS", "").split(",")
    default_keystore = "revanced.keystore"
    default_archs = "arm64-v8a,armeabi-v7a,x86_64,x86"
    default_cli_dl = urls.get_cli_dl()
    default_patches_dl = urls.get_patches_dl()
    default_patches_json_dl = urls.get_patches_json_dl()
    default_integrations_dl = urls.get_integrations_dl()


    json_data = {
        "env": [
            {
                "dry_run": env_dict.get("DRY_RUN", "False"),
                "global_keystore_file_name": env_dict.get("GLOBAL_KEYSTORE_FILE_NAME", default_keystore),
                "global_archs_to_build": env_dict.get("GLOBAL_ARCHS_TO_BUILD", default_archs).split(","),
                "global_cli_dl": env_dict.get("GLOBAL_CLI_DL", default_cli_dl),
                "global_patches_dl": env_dict.get("GLOBAL_PATCHES_DL", default_patches_dl),
                "global_patches_json_dl": env_dict.get("GLOBAL_PATCHES_JSON_DL", default_patches_json_dl),
                "global_integrations_dl": env_dict.get("GLOBAL_INTEGRATIONS_DL", default_integrations_dl),
                "extra_files": [{"url": url_name.split("@")[0], "name": url_name.split("@")[1]} for url_name in extra_files_list if "@" in url_name],
                "existing_downloaded_apks": [{"app_name": code, "app_package": package} for package, code in zip(get_pkg.packages, get_pkg.codes) if code in existing_downloaded_apks_list],
                "patch_apps": []
            }
        ]
    }

    for package, code in zip(get_pkg.packages, get_pkg.codes):
        if code in patch_apps_list:
            app_data = {
                "app_package": package,
                package: [
                    {
                        "app_name": code,
                        "version": env_dict.get(f"{code.upper()}_VERSION", "latest_supported"),
                        "keystore": env_dict.get(f"{code.upper()}_KEYSTORE_FILE_NAME", default_keystore),
                        "archs": env_dict.get(f"{code.upper()}_ARCHS_TO_BUILD", default_archs).split(","),
                        "cli_dl": env_dict.get(f"{code.upper()}_CLI_DL", default_cli_dl),
                        "patches_dl": env_dict.get(f"{code.upper()}_PATCHES_DL", default_patches_dl),
                        "patches_json_dl": env_dict.get(f"{code.upper()}_PATCHES_JSON_DL", default_patches_json_dl),
                        "integrations_dl": env_dict.get(f"{code.upper()}_INTEGRATIONS_DL", default_integrations_dl),
                        "include_patch_app": env_dict.get(f"{code.upper()}_INCLUDE_PATCH", "").split(","),
                        "exclude_patch_app": env_dict.get(f"{code.upper()}_EXCLUDE_PATCH", "").split(","),
                    }
                ]
            }
            # Removed but kept for reference
            # if code in ['youtube', 'youtube_music']:
            #     alternative_app_patches = env_dict.get(f"ALTERNATIVE_{code.upper()}_PATCHES", "").split(",")
            #     if alternative_app_patches:
            #         app_data[package][0]["alternative_app_patches"] = alternative_app_patches
            
            json_data["env"][0]["patch_apps"].append(app_data)
    return json_data

# Replace empty lists with []
@logger.catch
def replace_empty_lists(data):
    if isinstance(data, dict):
        return {k: replace_empty_lists(v) if v != [""] else [] for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_empty_lists(v) if v != [""] else [] for v in data]
    else:
        return data

if __name__ == "__main__":
    gh = GitHubRepo()
    repo = gh.get_repo()
    branch = gh.get_branch()
    backup_branch = gh.get_backup_branch()
    urls = GitHubURLs(repo, "customs")
    py_file_url = urls.get_patches_py()
    env_file_url = urls.get_env()
    env_content = get_pkg()
    if env_content == "404: Not Found":
        logger.warning("Fallback to {} branch", backup_branch)
        backup_urls = GitHubURLs(repo, backup_branch)
        py_file_url = backup_urls.get_patches_py()
        env_file_url = backup_urls.get_env()
        env_content = get_pkg()
    json_data = parse_json_data(env_content)
    json_data = replace_empty_lists(json_data)
    json_string = json.dumps(json_data, indent=4)
    output_file = "apps/json/env.json"
    wr.write_json(output_file, json_data)
    logger.debug(json_string)