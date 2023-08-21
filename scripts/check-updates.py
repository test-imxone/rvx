import os
import sys
import json
import requests

def get_env(branch):
    # Get env file contents
    url = f"https://raw.githubusercontent.com/{repository}/{branch}/.env"
    try:
        response = requests.get(url)
        content = response.text
        if response.status_code != 200:
            print(f"Failed to fetch the .env file. Status code: {response.status_code}", flush=True)
            print("Assuming the .env file doesn't exist, using an empty one...", flush=True)
            content = "# Empty .env file"
    except:
        print("The .env file doesn't exist. Using an empty one...", flush=True)
        content = "# Empty .env file"
    finally:
        return content

def get_monitored_patches(branch, file):
    # Get monitored-patches.json file contents
    url = f"https://raw.githubusercontent.com/{repository}/{branch}/{file}"
    try:
        response = requests.get(url)
        data = response.json()
    except:
        print("The monitored-patches.json file doesn't exist. It'd be created in the following run.", flush=True)
        data = []
    finally:
        return data
        
def get_patches_dls(dict):
    dls = set()
    for key, value in dict.items():
        if key.endswith("_JSON_DL"):
            value = manage_dls(value)
            dls.add(value)
    dls = set(filter(lambda value: value is not None, dls))
    if not dls:
        dls.add(manage_dls(default_patch_dl))
    dl_list = list(dls)
    return dl_list

def get_patch_data(dl_list):
    api_dls = []
    tags = []
    json_data = []
    for url in dl_list:
        api_url = github_api_url(url)
        api_dls.append(api_url)
        response = requests.get(api_url)
        release_json = response.json()
        tag = release_json["tag_name"]
        tags.append(tag)
        json_data.append({
            "patches_json_dl": url,
            "tag_name": tag
        })
    print("Different Patch DLs: ", "\n".join(dl_list), flush=True)
    json_str = json.dumps(json_data, indent=4)
    print("Latest JSON of Patch DLs:", json_str, flush=True)
    get_patch_data.json = json_data
    return json_data

def compare_tags(old_json, new_json):
    data1 = old_json
    data2 = new_json

    for entry2 in data2:
        patch_dl = entry2["patches_json_dl"]
        tag = entry2["tag_name"]
        if entry2 in data1:
            # The iterated object is already present
            continue
        else:
            # The iterated object isn't present
            # Checking if the patch Dl is present
            # patch_dl = "hello1"
            patch_obj = next((item for item in data1 if item['patches_json_dl'] == patch_dl), None)

            # Patch DL was already present
            # Trying to match tag
            if patch_obj:
                old_tag = patch_obj["tag_name"]
                if old_tag != tag:
                    print(f"Update found!!\nThe following Patch Dl was updated with tag '{tag}': \n{patch_dl}\n", flush=True)
                    return "build"

            # Patch Dl wasn't present and therefore would only update the 'monitored.json' & no build
            else:
                print(f"Oh, a Patch DL was modified!! \n{patch_dl}\n", flush=True)
                print("I expect that the user would have already run the build manually.", flush=True)
                print("Thus, the building would be done in the upcoming runs of the script.", flush=True)
                return "write_json"
    
    print("The patches are already up-to-date!!", flush=True)
    return "write_json"

def trigger_workflow(access_token, repository, branch, workflow_name):
    url = f"https://api.github.com/repos/{repository}/actions/workflows/{workflow_name}/dispatches"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "ref": branch  # The branch to trigger the workflow on
        # You can add any inputs required by your workflow here
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 204:
            print("Workflow triggered successfully!", flush=True)
        else:
            print(f"Failed to trigger workflow. Status code: {response.status_code}", flush=True)
    except Exception as e:
        print("Error:", e, flush=True)

def manage_tasks(action):
    if action == "write_json":
        print("Updating the 'monitored-patches.json' file.", flush=True)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(get_patch_data.json, f, indent=4)

    elif action == "build":
        print("Running the workflow: Build & Release", flush=True)
        # trigger_workflow(access_token, repository, branch, workflow_name)
        
def manage_dls(url):
    new_url = None
    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        prefix = "https://github.com"
        suffix = "/".join(url_arr[3:4]).lower() + "/" + "/".join(url_arr[4:])
        if not url.endswith("latest"):
            suffix = suffix + "/releases/latest"
        new_url = f"{prefix}/{suffix}"
    return new_url

def github_api_url(url):
    api_url = None
    if url.startswith("https://github.com"):
        url_arr = url.split("/")
        prefix = 'https://api.github.com/repos'
        suffix = "/".join(url_arr[3:])
        if "/tag/" in url:
            suffix = suffix.replace("/tag/", "/tags/")
        elif not url.endswith("latest"):
            suffix = suffix + "/releases/latest"
        api_url = f"{prefix}/{suffix}"
    # print(api_url, flush=True)
    return api_url

# Parse json_data from env_content
def parse_env():
    env_content = get_env(branch)
    old_patches_data = get_monitored_patches(monitored_branch, output_file)

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

    dl_list = get_patches_dls(env_dict)
    latest_patches_data = get_patch_data(dl_list)
    action = compare_tags(old_patches_data, latest_patches_data)
    manage_tasks(action)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python <script.py> <USER/REPO>", flush=True)
    else:
        repository = sys.argv[1]
        access_token = os.environ.get('GH_TOKEN')
        workflow_name = "build-apk.yml"

        branch = "customs" # Branch to get the env
        monitored_branch = "check-updates" # Branch to get the monitored-patches.json
        output_file = "scripts/monitored-patches.json"

        default_patch_dl = "https://github.com/revanced/revanced-patches"
        # old_patches_data = json.loads('''[
        # {
        #     "patches_json_dl":"https://github.com/inotia00/revanced-patches/releases/latest",
        #     "tag_name":"v2.187.1"
        # },
        # {
        #     "patches_json_dl":"https://github.com/revanced/revanced-patches/releases/latest",
        #     "tag_name":"v2.187.01"
        # },
        #     {
        #         "patches_json_dl": "hello",
        #         "tag_name": "bye"                         
        #     }
        # ]''')
        parse_env()