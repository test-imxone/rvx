import json
import requests
from loguru import logger

import utils.writer as wr
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs

@logger.catch
def parse_env_json_to_env(json_data, output_file, key_order, key_order_placeholder):
    # Load the JSON data
    data = json.loads(json_data)

    # Extract the required values from the JSON
    env_dict = {}
    env_dict["DRY_RUN"] = data["env"][0].get("dry_run", "")
    env_dict["GLOBAL_KEYSTORE_FILE_NAME"] = data["env"][0].get("keystore_file_name", "")
    env_dict["GLOBAL_ARCHS_TO_BUILD"] = ",".join(data["env"][0].get("archs_to_build", []))
    env_dict["BUILD_EXTENDED"] = data["env"][0].get("build_extended", "False")
    env_dict["GLOBAL_CLI_DL"] = data["env"][0].get("global_cli_dl", "")
    env_dict["GLOBAL_PATCHES_DL"] = data["env"][0].get("global_patches_dl", "")
    env_dict["GLOBAL_PATCHES_JSON_DL"] = data["env"][0].get("global_patches_json_dl", "")
    env_dict["GLOBAL_INTEGRATIONS_DL"] = data["env"][0].get("global_integrations_dl", "")

    extra_files = [f'{item["url"]}@{item["name"]}' for item in data["env"][0].get("extra_files", [])]
    env_dict["EXTRA_FILES"] = ",".join(extra_files)
    existing_downloaded_apks = [apk["app_name"] for apk in data["env"][0].get("existing_downloaded_apks", [])]
    env_dict["EXISTING_DOWNLOADED_APKS"] = ",".join(existing_downloaded_apks)

    patch_apps = []
    for app_data in data["env"][0].get("patch_apps", []):
        app_package = app_data["app_package"]
        app_package_to_name = {app["app_package"]: app["app_name"] for app in apps_info}
        real_app_name = app_package_to_name.get(app_package)
        ## Add a fallback for app_code if app_name is unavailable
        app_name = list(app_data[app_package][0].values())[0]
        
        # Extract the required values
        app_version = app_data[app_package][0].get("version", "")
        app_keystore = app_data[app_package][0].get("keystore", "")
        app_archs = ",".join(app_data[app_package][0].get("archs", []))
        cli_dl = app_data[app_package][0].get("cli_dl", "")
        patches_dl = app_data[app_package][0].get("patches_dl", "")
        patches_json_dl = app_data[app_package][0].get("patches_json_dl", "")
        integrations_dl = app_data[app_package][0].get("integrations_dl", "")
        include_patch = ",".join(app_data[app_package][0].get("include_patch_app", []))
        exclude_patch = ",".join(app_data[app_package][0].get("exclude_patch_app", []))
        alternative_patches = ",".join(app_data[app_package][0].get("alternative_app_patches", []))

        # Add the keys and values to the environment dictionary
        env_dict[f"{app_name.upper()}_REALNAME"] = real_app_name
        env_dict[f"{app_name.upper()}_VERSION"] = app_version
        env_dict[f"INCLUDE_PATCH_{app_name.upper()}"] = include_patch
        env_dict[f"EXCLUDE_PATCH_{app_name.upper()}"] = exclude_patch
        env_dict[f"ALTERNATIVE_{app_name.upper()}_PATCHES"] = alternative_patches

        # Replace the placeholder APP_NAME with the actual app names in the key_order
        for key in key_order_placeholder:
            key = key.replace("APP_NAME", app_name.upper())
            key_order.append(key)

        # Add the app_name to the patch_apps list
        patch_apps.append(app_name)
    env_dict["PATCH_APPS"] = ",".join(patch_apps)

    # Write the env_content
    env_content = ""
    for key in key_order:
        value = env_dict.get(key)
        if key.endswith("_REALNAME"):
            env_content += f"\n\n### {value}:\n"
            continue
        if key.endswith("_VERSION") and value == "latest_supported":
            env_content += f"# {key}={value}\n"
        elif value:
            env_content += f"{key}={value}\n"

    wr.check_path(output_file)
    # Write the env_content to a file
    with open(output_file, "w") as file:
        file.write(env_content)
    logger.debug(env_content)

# Get the JSON data
# json_file = open('apps/env.json', 'r')
# json_data = json_file.read()
# json_file.close()


if __name__ == "__main__":
    gh = GitHubRepo()
    repo = gh.get_repo()
    branch = gh.get_branch()
    backup_branch = gh.get_backup_branch()
    urls = GitHubURLs(repo, "changelogs")
    json_file = urls.get_env_json()
    json_data = requests.get(json_file).text
    apps_json = urls.get_apps_json()
    apps_info = requests.get(apps_json).json()
    if json_data == "404: Not Found":
        logger.warning("Fallback to {} branch", backup_branch)
        backup_urls = GitHubURLs(repo, backup_branch)
        json_file = backup_urls.get_env_json()
        json_data = requests.get(json_file).text
    output_file = "apps/.env"

    # Define the desired sorting key order
    key_order = [
        "DRY_RUN",
        "GLOBAL_KEYSTORE_FILE_NAME",
        "GLOBAL_ARCHS_TO_BUILD",
        "GLOBAL_CLI_DL",
        "GLOBAL_PATCHES_DL",
        "GLOBAL_PATCHES_JSON_DL",
        "GLOBAL_INTEGRATIONS_DL",
        "PATCH_APPS",
        "EXTRA_FILES",
        "EXISTING_DOWNLOADED_APKS",
    ]
    key_order_placeholder = [
        "APP_NAME_REALNAME",
        "APP_NAME_VERSION",
        "APP_NAME_KEYSTORE_FILE_NAME",
        "APP_NAME_ARCHS_TO_BUILD",
        "APP_NAME_CLI_DL",
        "APP_NAME_PATCHES_DL",
        "APP_NAME_PATCHES_JSON_DL",
        "APP_NAME_INTEGRATIONS_DL",        
        "INCLUDE_PATCH_APP_NAME",
        "EXCLUDE_PATCH_APP_NAME",
        "ALTERNATIVE_APP_NAME_PATCHES",
    ]

    parse_env_json_to_env(json_data, output_file, key_order, key_order_placeholder)