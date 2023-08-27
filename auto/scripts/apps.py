import re
import requests
from loguru import logger

import patch_sources as srcs
import utils.writer as wr
import utils.utils as ut
from utils.scraper import scraper
from utils.repo import GitHubRepo
from utils.urls import GitHubURLs

gh = GitHubRepo()
repo = gh.get_repo()
branch = gh.get_branch()
branch = "customs"
backup_branch = gh.get_backup_branch()
urls = GitHubURLs(repo, branch)
patches_py_url = urls.get_patches_py()

rvxm_json_file = "auto/apps/patch_apps/apps-merged.json"
md_file = "auto/docs/README.md"

@logger.catch
def get_available_patch_apps(url):
    response = requests.get(url)
    python_code = response.text
    # Extract package_name and app_code from the Python code
    pattern = r'"([^"]+)":\s*"([^"]+)",'
    matches = re.findall(pattern, python_code)
    package_name = []
    app_code = []
    for package, code in matches:
        package_name.append(package.strip())
        app_code.append(code.strip())
    return package_name, app_code

@logger.catch
def get_app_code(package):
    if isinstance(package, list):
        code = []
        for pkg in package:
            i = available_packages.index(pkg)
            code.append(app_code[i])
    elif isinstance(package, str):
        i = available_packages.index(package)
        code = app_code[i]
    return code

@logger.catch
def get_patches_json(url):
    r = requests.get(url)
    patches = r.json()
    return patches

@logger.catch
def get_packages_from_patches(patches):
    packages = set()
    for item in patches:
        for package in item["compatiblePackages"]:
            packages.add(package["name"])
    return packages

scraped_app_data = []
@logger.catch
def scrape_package(package_name):
    serial = len(scraped_app_data) + 1
    logger.debug("{}. {}", serial, package_name)
    app_codename = get_app_code(package_name)
    if not app_codename: app_codename = None
    app_name, app_icon, app_url = scraper(package_name, app_codename)
    app_obj = {
        "app_package": package_name,
        "app_code": app_codename,
        "app_name": app_name,
        "app_url": app_url,
        "app_icon": app_icon,
    }
    scraped_app_data.append(app_obj)
    ut.sort_packages(scraped_app_data)
    return app_obj

@logger.catch
def get_package_scrape(packages):
    app_data = []
    for package in packages:
        pkg_obj = next(filter(lambda item: item["app_package"] == package, scraped_app_data), None)
        if pkg_obj:
            app_data.append(pkg_obj)
        else:
            scrape_obj = scrape_package(package)
            app_data.append(scrape_obj)
        logger.debug(package)
    return app_data

@logger.catch
def merge_jsons(json_lists):
    merged_dict = {}
    for json_list in json_lists:
        for obj in json_list:
            app_package = obj['app_package']
            if app_package not in merged_dict:
                merged_dict[app_package] = obj
    merged_list = list(merged_dict.values())
    ut.sort_packages(merged_list)
    wr.write_json(rvxm_json_file, merged_list)
    return merged_list

@logger.catch
def unsupport_scrape():

    for package_name in unadded_packages:
        logger.info("Scraping for unadded package - {}", package_name)
        app_name, app_icon, app_url = scraper(package_name, None)
        if app_name == "Unavailable":
            logger.error("Unadded package: {}", package_name)
        unadded_scrape.append({
                "app_package": package_name,
                "app_name": app_name,
                "app_url": app_url,
                "app_icon": app_icon,
            })
        
    for package_name in removed_packages:
        logger.info("Scraping for removed package - {}", package_name)
        app_name, app_icon, app_url = scraper(package_name, None)
        if app_name == "Unavailable":
            logger.error("Removed package: {}", package_name)
        removed_scrape.append({
                "app_package": package_name,
                "app_name": app_name,
                "app_url": app_url,
                "app_icon": app_icon,
            })
        
    logger.info("\nUnadded Scrape: {}", unadded_scrape)
    logger.info("\nRemoved Scrape: {}", removed_scrape)

@logger.catch
def array_lengths(arrays):
    lengths = []
    for array in arrays:
        lengths.append(len(array))
    return lengths

# Get custom patch sources from .env file
patches_data = srcs.parse_env()
patches_data = sorted(patches_data, key=ut.custom_sort_key)

# Get available packages from the config files.
available_packages, app_code = get_available_patch_apps(patches_py_url)
if not available_packages and not app_code:
    logger.warning("Fallback to {} branch", backup_branch)
    backup_urls = GitHubURLs(repo, backup_branch)
    patches_py_url = backup_urls.get_patches_py()
    available_packages, app_code = get_available_patch_apps(patches_py_url)


# Scrape app data based on the custom patches.json
universal_packages = set()
scrape_apps_data = []
for item in patches_data:
    patch_dl = item["patches_json_dl"]
    org_name = item["org_name"]
    raw_url = item["raw_url"]

    patches = get_patches_json(raw_url)
    all_packages = get_packages_from_patches(patches)
    packages = list(set(all_packages) & set(available_packages))
    codes = get_app_code(packages)

    app_data = get_package_scrape(packages)
    scrape_apps_data.append(app_data)
    universal_packages.update(all_packages)
    logger.info(
        (
            f"\n\nAvailable packages to be patched from '{org_name}':\n"
            f"\nPatch DL: {patch_dl}\n"
            f"\nRaw url: {raw_url}\n"
            f"\nPackage Names: {packages}\n"
            f"\nApp Codes: {codes}\n\n"
        )
    )

# Generate unavailable packages.
unadded_packages = list(universal_packages - set(available_packages))
removed_packages = list(set(available_packages) - universal_packages)
removed_apps_data = get_package_scrape(removed_packages)

unadded_scrape = []
removed_scrape = []
# Generate unavailable app data.
unsupport_scrape()

# Generate no. of apps and their respective app data
supported_data = scrape_apps_data
supported_apps = array_lengths(supported_data)
unsupported_data = [unadded_scrape, removed_scrape]
unsupported_apps = array_lengths(unsupported_data)

# Generate the supported & unsupported apps data as markdown doc
supported_data = wr.filter_empty_data(supported_data)
unsupported_data = wr.filter_empty_data(unsupported_data)
content = wr.write_supported(supported_apps, patches_data, supported_data)
content += wr.write_unsupported(unsupported_apps, unsupported_data)
header = wr.heading_and_toc(content)
content = (header + content).strip() + "\n"
# Write the md content
wr.write_md(md_file, content)

# Add the removed apps data to the available apps data
scrape_apps_data.append(removed_apps_data)
# Merge all app data
merge_jsons(scrape_apps_data)