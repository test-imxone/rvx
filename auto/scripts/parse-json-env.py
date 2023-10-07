import json
import re

import requests
from loguru import logger

import utils.writer as wr
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs


@logger.catch
def parse_env_json_to_env(json_data, output_file, key_order, key_order_placeholder):
    # Load the JSON data
    data = json.loads(json_data)

    global_old_key = data["env"][0].get("global_old_key", "")
    global_keystore = data["env"][0].get("global_keystore_file_name", "")
    global_archs = ",".join(data["env"][0].get("global_archs_to_build", []))
    global_space_format = data["env"][0].get("global_space_format_patch", "")
    global_cli_dl = data["env"][0].get("global_cli_dl", "")
    global_patches_dl = data["env"][0].get("global_patches_dl", "")
    global_patches_json_dl = data["env"][0].get("global_patches_json_dl", "")
    global_integrations_dl = data["env"][0].get("global_integrations_dl", "")

    # Extract the required values from the JSON
    env_dict = {}
    env_dict["GLOBAL_REALNAME"] = "Global"
    env_dict["DRY_RUN"] = data["env"][0].get("dry_run", "")
    env_dict["GLOBAL_OLD_KEY"] = global_old_key
    env_dict["GLOBAL_KEYSTORE_FILE_NAME"] = global_keystore
    env_dict["GLOBAL_ARCHS_TO_BUILD"] = global_archs
    env_dict["GLOBAL_SPACE_FORMATTED_PATCHES"] = global_space_format
    env_dict["GLOBAL_CLI_DL"] = global_cli_dl
    env_dict["GLOBAL_PATCHES_DL"] = global_patches_dl
    env_dict["GLOBAL_PATCHES_JSON_DL"] = global_patches_json_dl
    env_dict["GLOBAL_INTEGRATIONS_DL"] = global_integrations_dl

    extra_files = [f'{item["url"]}@{item["name"]}' for item in data["env"][0].get("extra_files", [])]
    env_dict["EXTRA_FILES"] = ",".join(extra_files)
    existing_downloaded_apks = [apk["app_name"] for apk in data["env"][0].get("existing_downloaded_apks", [])]
    env_dict["EXISTING_DOWNLOADED_APKS"] = ",".join(existing_downloaded_apks)

    patch_apps = []
    for app_data in data["env"][0].get("patch_apps", []):
        app_package = app_data["app_package"]
        app_info = next(filter(lambda item: item["app_package"] == app_package, apps_info), None)

        app_name = next(iter(app_data[app_package][0].values()))
        real_app_name = app_info["app_name"] if app_info else None
        if not real_app_name:
            real_app_name = re.sub(r"[-_]", " ", app_name).capitalize()

        # Extract the required values
        app_version = app_data[app_package][0].get("version", "")
        app_old_key = app_data[app_package][0].get("old_key", "")
        app_keystore = app_data[app_package][0].get("keystore", "")
        app_archs = ",".join(app_data[app_package][0].get("archs", []))
        app_dl = app_data[app_package][0].get("apk_dl", "")
        app_dl_source = app_data[app_package][0].get("apk_dl_source", "")
        cli_dl = app_data[app_package][0].get("cli_dl", "")
        patches_dl = app_data[app_package][0].get("patches_dl", "")
        patches_json_dl = app_data[app_package][0].get("patches_json_dl", "")
        integrations_dl = app_data[app_package][0].get("integrations_dl", "")
        space_format = app_data[app_package][0].get("space_format_patch", "")
        include_patch = ",".join(app_data[app_package][0].get("include_patch_app", []))
        exclude_patch = ",".join(app_data[app_package][0].get("exclude_patch_app", []))

        # Add the keys and values to the environment dictionary
        env_dict[f"{app_name.upper()}_REALNAME"] = real_app_name
        if app_dl or app_dl_source:
            env_dict[f"{app_name.upper()}_PACKAGE_NAME"] = app_package
        env_dict[f"{app_name.upper()}_VERSION"] = app_version
        env_dict[f"{app_name.upper()}_OLD_KEY"] = app_old_key
        env_dict[f"{app_name.upper()}_KEYSTORE_FILE_NAME"] = app_keystore
        env_dict[f"{app_name.upper()}_ARCHS_TO_BUILD"] = app_archs

        if app_dl:
            env_dict[f"{app_name.upper()}_DL"] = app_dl
        elif app_dl_source:
            env_dict[f"{app_name.upper()}_DL_SOURCE"] = app_dl_source

        env_dict[f"{app_name.upper()}_CLI_DL"] = cli_dl
        env_dict[f"{app_name.upper()}_PATCHES_DL"] = patches_dl
        env_dict[f"{app_name.upper()}_PATCHES_JSON_DL"] = patches_json_dl
        env_dict[f"{app_name.upper()}_INTEGRATIONS_DL"] = integrations_dl
        env_dict[f"{app_name.upper()}_SPACE_FORMATTED_PATCHES"] = space_format
        env_dict[f"{app_name.upper()}_INCLUDE_PATCH"] = include_patch
        env_dict[f"{app_name.upper()}_EXCLUDE_PATCH"] = exclude_patch

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

        if (
            value
            and key.startswith("GLOBAL_")
            and (
                (key.endswith("_OLD_KEY") and value == "True")
                or (key.endswith("_KEYSTORE_FILE_NAME") and value == default_keystore)
                or (key.endswith("_ARCHS_TO_BUILD") and set(value.split(",")) == set(default_archs.split(",")))
                or (key.endswith("_SPACE_FORMATTED_PATCHES") and value == "True")
                or (
                    key.endswith("_DL")
                    and value.lower()
                    in {default_cli_dl, default_patches_dl, default_patches_json_dl, default_integrations_dl}
                )
            )
        ):
            env_content += f"# {key}={value}\n"

        elif (
            value
            and not key.startswith("GLOBAL_")
            and (
                (key.endswith("_VERSION") and value == "latest_supported")
                or (key.endswith("_OLD_KEY") and value == global_old_key)
                or (key.endswith("_KEYSTORE_FILE_NAME") and value == global_keystore)
                or (key.endswith("_ARCHS_TO_BUILD") and set(value.split(",")) == set(global_archs.split(",")))
                or (key.endswith("_SPACE_FORMATTED_PATCHES") and value == global_space_format)
                or (
                    key.endswith("_DL")
                    and value.lower()
                    in {global_cli_dl, global_patches_dl, global_patches_json_dl, global_integrations_dl}
                )
            )
        ):
            env_content += f"# {key}={value}\n"

        elif value:
            env_content += f"{key}={value}\n"

        elif key.endswith(("_PACKAGE_NAME", "_DL", "_DL_SOURCE")):
            continue

        else:
            env_content += f"# {key}={value}\n"

    env_content = env_content.lstrip()
    wr.check_path(output_file)
    # Write the env_content to a file
    with open(output_file, "w") as file:
        file.write(env_content)
    logger.debug(env_content)


if __name__ == "__main__":
    gh = GitHubRepo()
    repo = gh.get_repo()
    branch = gh.get_branch()
    backup_branch = gh.get_backup_branch()
    urls = GitHubURLs(repo, branch)
    json_file = urls.get_env_json()
    json_data = requests.get(json_file).text
    apps_json = urls.get_apps_json()
    apps_info = requests.get(apps_json).json()
    if json_data == "404: Not Found":
        logger.warning(f"Fallback to {backup_branch} branch")
        backup_urls = GitHubURLs(repo, backup_branch)
        json_file = backup_urls.get_env_json()
        json_data = requests.get(json_file).text
    urls = GitHubURLs(repo, branch)
    json_file = urls.get_env_json()
    json_data = requests.get(json_file).text
    output_file = "auto/.env"

    default_keystore = "revanced.keystore"
    default_archs = "arm64-v8a,armeabi-v7a,x86_64,x86"
    default_cli_dl = urls.get_cli_dl()
    default_patches_dl = urls.get_patches_dl()
    default_patches_json_dl = urls.get_patches_json_dl()
    default_integrations_dl = urls.get_integrations_dl()

    # Define the desired sorting key order
    key_order = [
        "GLOBAL_REALNAME",
        "DRY_RUN",
        "GLOBAL_OLD_KEY",
        "GLOBAL_KEYSTORE_FILE_NAME",
        "GLOBAL_ARCHS_TO_BUILD",
        "GLOBAL_SPACE_FORMATTED_PATCHES",
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
        "APP_NAME_PACKAGE_NAME",
        "APP_NAME_DL",
        "APP_NAME_DL_SOURCE",
        "APP_NAME_VERSION",
        "APP_NAME_OLD_KEY",
        "APP_NAME_KEYSTORE_FILE_NAME",
        "APP_NAME_ARCHS_TO_BUILD",
        "APP_NAME_CLI_DL",
        "APP_NAME_PATCHES_DL",
        "APP_NAME_PATCHES_JSON_DL",
        "APP_NAME_INTEGRATIONS_DL",
        "APP_NAME_SPACE_FORMATTED_PATCHES",
        "APP_NAME_INCLUDE_PATCH",
        "APP_NAME_EXCLUDE_PATCH",
    ]

    parse_env_json_to_env(json_data, output_file, key_order, key_order_placeholder)
