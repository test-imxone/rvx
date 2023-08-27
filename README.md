<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/IMXEren/rvx-builds/main/auto/profile/logo_big_dark-bg.svg">
  <img alt="rvx-builds_logo" src="https://raw.githubusercontent.com/IMXEren/rvx-builds/main/auto/profile/logo_big_light-bg.svg">
</picture>

# Table of Contents

- [**Overview**](#overview)
- [**Requirements**](#requirements)
- [**Usage**](#usage)
- [**Updates & Changelogs**](#updates--changelogs)
- [**Credits**](#credits)
- [**Support**](#support)

<<<<<<< HEAD
## Overview
=======
 <a id="only-builder-support"></a>This is just a builder for revanced and not a revanced support. Please be
 understanding and refrain from asking about revanced features/bugs. Discuss those on proper relevant forums.
>>>>>>> pr/9

**Are you tired of patching ReVanced apps on your mobile devices? Which version to patch and which apk to provide for patching? Is the waiting period long enough and still the patch doesn't work as it should? Device compatibility issues? Auto-updates?...** All that can be done with the help of this [github repository](https://github.com/IMXEren/rvx-builds) (for patching & building) and this [**RVX-Builds**](https://taskernet.com/shares/?user=AS35m8k0QSchKA1x02SixFIhiL41a828J1qapOYfcEuyL2zSn%2FfJTN5WVSi01o18x6EAFb4%3D&id=Project%3ARVX-Builds) project in Tasker (for interactive selection & automation).

***Note: Neither the mentioned github repository nor the Tasker project are in anyway officially related to ReVanced Team. All this work falls under 3rd party so please don't ask for support from ReVanced Team regarding it.***

## Requirements

- [GitHub Account](https://github.com/join) (Free)
- Tasker ([Trial](https://tasker.joaoapps.com/download.html) -> [Paid](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm))
- Join ([Trial -> Paid](https://play.google.com/store/apps/details?id=com.joaomgcd.join); Optional)

<<<<<<< HEAD
## Usage
=======
- 🚀 **GitHub** (**_`Recommended`_**)
>>>>>>> pr/9

### Pre-Forked

I think that there might be possibility that some people would've already forked the parent repository of @nikhilbadyal or it's child repository (for example, of @Spacellary). So, here are [listed files](/apps/docs/pre-forked.md) (may or may not replace originals) which you can copy to repository clone folder and push those changes. It'll make your repository eligible to be used in **Automation** and somewhat similar to mine. Proceed with patch methods.

**Note: The automation integration won't work if [*Custom Patch Resources*](https://github.com/nikhilbadyal/docker-py-revanced/pull/239) PR is merged to any of the repositories due to major changes. Your only choice is to use this repository while I update.**

### Methods

There are actually two ways to patch apps - **Manual** & **Automated**. The Manual way simply requires the GitHub Repository only and you've to do all the work yourself like customizing the patches, downloading & installing. The Automated way requires the GitHub Repository as well as the RVX-Builds project in Tasker. In the automated way, you can easily customize and configure many more properties using Tasker.

If you're doing it for the first time, I'd suggest you to go with Manual method to make yourself comfortable with the different patching terms in the repository and configure some necessary setups before automating.

### 1. Manual

Here's the manual way to patch apps.

<<<<<<< HEAD
1. Create a [GitHub account](https://github.com/join) if you haven't.
2. Fork this [repository](https://github.com/IMXEren/rvx-builds) under anyname.
3. Read this [page](/apps/docs/customize-patches.md) onwards. This is to customize the patching. After reading, you might have prepared an `.env` file.
4. Congrats, you're ready to patch these apps.
5. Go to `Actions` tab. Select `Build & Release`. Click on `Run Workflow` button.
6. Wait for sometime while it patches and build all those apps mentioned in the `.env` file.
7. Once complete and successful, you'll get your patched apks in the `Releases` section.
8. Download & install those apks. Now, you've installed the patched apps!!
9. Here are some [extra things](/apps/docs/extras.md) to configure.

### 2. Automated
=======
- 🐳 **_Docker Compose_**<br>

    1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
    2. Clone the repo
       ```bash
       git clone https://github.com/nikhilbadyal/docker-py-revanced
       ```
    3. cd to the cloned repo
       ```bash
       cd docker-py-revanced
       ```
    4. Update `.env` file if you want some customization(See notes)
    5. Run script with
       ```shell
       docker-compose up --build
       ```
>>>>>>> pr/9

It'll be better for yourself if you have some [basic knowledge about Tasker](https://www.youtube.com/watch?v=EVNUGUv-lIY) like knowing about tasks, profiles, events, states, projects.

<<<<<<< HEAD
1. Go to this [page](https://github.com/settings/tokens) and `Generate new token > Classic`. Enter `RVX-Builds` in Note, set any expiration period and select these scopes (sufficient) - `repo, workflow, write:packages`. Click `Generate Token`. Note the token - `ghp_*`
2. Import [**RVX-Builds**](https://taskernet.com/shares/?user=AS35m8k0QSchKA1x02SixFIhiL41a828J1qapOYfcEuyL2zSn%2FfJTN5WVSi01o18x6EAFb4%3D&id=Project%3ARVX-Builds) project on Tasker and setup the GitHub credentials. It'll popup itself for you to setup or you can run `RVX-Builds - Setup` Task in `Tasks` Tab inside `RVX-Builds` Project. Projects are listed horizontally on bottom bar.
3. Once completed, you're ready to customize patches. Run `RVX-Builds - Manager` to do so. It'll consist of menu items -
    - Apps: To modify app related properties. (**Must configure**)
    - Downloads: To modify download & installation of app properties. (**Must configure**)
    - Merge: To merge your customization (locally on Tasker) with the `.env` file in your GitHub Repo. Only shown if you've made customization changes in *Apps* or opened it (i.e. always open Apps even when don't change).
    - Releases: To build your patched apps and release them. Set the above options accordingly and make a stable release.
4. If you have access to Join paid version, enable `RVX-Builds - New Release [Join]` Profile in `Profiles` Tab. Also enable `RVX-Builds - Check For Updates` if you want it to handle cancelled or errored out downloads due to any reason. Also, you need to add **JOIN API** [secrets](/apps/docs/extras.md#github-secrets). Here's [how to](/apps/docs/extras.md#join-api) do it.
5. If you don't have access to Join paid version, enable `RVX-Builds - Check For Updates` Profile in `Profiles` Tab. Disable `RVX-Builds - New Release [Join]` in this case.
6. After the successful release, the workflow would make an API call to Join (`RVX-Builds - New Release [Join]`) which would ultimately initialize an event and the downloader & installer task would run and work based upon your configuration of `Downloads` menu option in `RVX-Builds - Manager` task. Another workaround is that this profile `RVX-Builds - Check For Updates` would periodically (15 min; you can change) perform checks. It can also handle cancelled or errored out downloads.
7. Finally, after all the downloading or installation, there'll be a notification to let you know that it was successful. Note that, it requires ADB Wifi access to Tasker to let it install apps in the background.
8. Patched apps have been installed and apks are at `/storage/emulated/0/Tasker/rvx-builds/downloads/REPO_RELEASE_TAG_NAME/*.apk`. Note that you shouldn't delete any of those apks otherwise you'd face infinite-looping of downloads because of `6th - RVX-Builds - Check For Updates`. You may disable actions from `A17-28` in the linked task as a solution to it.
=======
    1. Install Docker or [Docker Desktop](https://www.docker.com/products/docker-desktop/).
       ```bash
       curl -fsSL https://get.docker.com -o get-docker.sh
       sh get-docker.sh
       ```
    2. Run script with
       ```shell
       docker run -v "$(pwd)"/apks:/app/apks/  nikhilbadyal/docker-py-revanced
       ```
       You can pass the below environment variables (See notes) with the `-e` flag or use the `--env-file`
       [flag](https://docs.docker.com/engine/reference/commandline/run/#options).
>>>>>>> pr/9

### Patching

<<<<<<< HEAD
The patching is done using the CLI for both revanced & revanced-extended resources. The `/apks` folder is used as the base folder in which you can source your `options.json` or whatever files you need. Here's the list of [patch apps](../../tree/changelogs/apps/docs/README.md) and *incompletely* generated [`options.json`](../../tree/changelogs/apps/apps/options) which you can look into.
=======
    1. Install Java >= 17
    2. Install Python >= 3.11
    3. Create virtual environment
       ```
       python3 -m venv venv
       ```
    4. Activate virtual environment
       ```
       source venv/bin/activate
       ```
    5. Install Dependencies with
       ```
       pip install -r requirements.txt
       ```
    6. Run the script with
       ```
       python main.py
       ```
>>>>>>> pr/9

**Note: A possible error while installing the released patched apks can be due to signature mismatch of the apk and it's installed app. In this case, either provide the same the keystore file to sign apks in `/apks` folder in GitHub repository and add `GLOBAL_KEYSTORE_FILE_NAME=*.keystore` in `.env` file OR simply delete (make backup if possible; one-time process) those already installed non-patched (same package) or patched apps.**

## Updates & Changelogs

<<<<<<< HEAD
The `RVX-Builds - Project Updates` profile will let you know of any updates I push so, make sure it's enabled.
=======
| **Env Name**                                             |                  **Description**                  | **Default**                                                                                              |
|:---------------------------------------------------------|:-------------------------------------------------:|:---------------------------------------------------------------------------------------------------------|
| [PATCH_APPS](#patch-apps)                                |                Apps to patch/build                | youtube                                                                                                  |
| [EXISTING_DOWNLOADED_APKS ](#existing-downloaded-apks)   |           Already downloaded clean apks           | []                                                                                                       |
| [PERSONAL_ACCESS_TOKEN](#personal-access-token)          |              Github Token to be used              | None                                                                                                     |
| DRY_RUN                                                  |                   Do a dry run                    | False                                                                                                    |
| [GLOBAL_CLI_DL*](#global-resources)                      |     DL for CLI to be used for patching apps.      | [Revanced CLI](https://github.com/revanced/revanced-cli)                                                 |
| [GLOBAL_PATCHES_DL*](#global-resources)                  |   DL for Patches to be used for patching apps.    | [Revanced Patches](https://github.com/revanced/revanced-patches)                                         |
| [GLOBAL_PATCHES_JSON_DL*](#global-resources)             | DL for Patches Json to be used for patching apps. | [Revanced Patches](https://github.com/revanced/revanced-patches)                                         |
| [GLOBAL_INTEGRATIONS_DL*](#global-resources)             | DL for Integrations to be used for patching apps. | [Revanced Integrations](https://github.com/revanced/revanced-integrations)                               |
| [GLOBAL_KEYSTORE_FILE_NAME*](#global-keystore-file-name) |       Key file to be used for signing apps        | [Builder's own key](https://github.com/nikhilbadyal/docker-py-revanced/blob/main/apks/revanced.keystore) |
| [GLOBAL_ARCHS_TO_BUILD*](#global-archs-to-build)         |         Arch to keep in the patched apk.          | All                                                                                                      |
| REDDIT_CLIENT_ID                                         |       Reddit Client ID to patch reddit apps       | None                                                                                                     |
| VT_API_KEY                                               |           Virus Total Key to scan APKs            | None                                                                                                     |
| [TELEGRAM_CHAT_ID](#telegram-support)                    |            Receiver in Telegram upload            | None                                                                                                     |
| [TELEGRAM_BOT_TOKEN](#telegram-support)                  |          APKs Sender for Telegram upload          | None                                                                                                     |
| [TELEGRAM_API_ID](#telegram-support)                     |         Used for telegram Authentication          | None                                                                                                     |
| [TELEGRAM_API_HASH](#telegram-support)                   |         Used for telegram Authentication          | None                                                                                                     |
| [EXTRA_FILES](#extra-files)                              |    Extra files apk to upload in GitHub upload.    | None                                                                                                     |
>>>>>>> pr/9

>> Taskernet - [**RVX-Builds**](https://taskernet.com/shares/?user=AS35m8k0QSchKA1x02SixFIhiL41a828J1qapOYfcEuyL2zSn%2FfJTN5WVSi01o18x6EAFb4%3D&id=Project%3ARVX-Builds)  
[**Changelogs**](/apps/updates/CHANGELOG.md)

<<<<<<< HEAD
## Credits

- Thanks to [@ReVanced](https://github.com/revanced) for **ReVanced**.
- Thanks to [@inotia00](https://github.com/inotia00) for **ReVanced Extended**.
- Thanks to [@nikhilbadyal](https://github.com/nikhilbadyal/docker-py-revanced) for his amazing work.
- Thanks to [@Spacellary](https://github.com/Spacellary/ReVanced-Extended-Automated-Builds) for his work in making the customized parent fork.
=======
| Env Name                                                    |                        Description                        | Default                        |
|:------------------------------------------------------------|:---------------------------------------------------------:|:-------------------------------|
| [*APP_NAME*_CLI_DL](#global-resources)                      |     DL for CLI to be used for patching **APP_NAME**.      | GLOBAL_CLI_DL                  |
| [*APP_NAME*_PATCHES_DL](#global-resources)                  |   DL for Patches to be used for patching **APP_NAME**.    | GLOBAL_PATCHES_DL              |
| [*APP_NAME*_PATCHES_JSON_DL](#global-resources)             | DL for Patches Json to be used for patching **APP_NAME**. | GLOBAL_PATCHES_JSON_DL         |
| [*APP_NAME*_INTEGRATIONS_DL](#global-resources)             | DL for Integrations to be used for patching **APP_NAME**. | GLOBAL_INTEGRATIONS_DL         |
| [*APP_NAME*_KEYSTORE_FILE_NAME](#global-keystore-file-name) |       Key file to be used for signing **APP_NAME**.       | GLOBAL_KEYSTORE_FILE_NAME      |
| [*APP_NAME*_ARCHS_TO_BUILD](#global-archs-to-build)         |         Arch to keep in the patched **APP_NAME**.         | GLOBAL_ARCHS_TO_BUILD          |
| [*APP_NAME*_EXCLUDE_PATCH**](#custom-exclude-patching)      |     Patches to exclude while patching  **APP_NAME**.      | []                             |
| [*APP_NAME*_INCLUDE_PATCH**](#custom-include-patching)      |     Patches to include while patching  **APP_NAME**.      | []                             |
| [*APP_NAME*_VERSION](#app-version)                          |         Version to use for download for patching.         | Recommended by patch resources |
| [*APP_NAME*_PACKAGE_NAME***](#any-patch-apps)               |           Package name of the app to be patched           | None                           |
| [*APP_NAME*_DL_SOURCE***](#any-patch-apps)                  |     Download source of any of the supported scrapper      | None                           |
| [*APP_NAME*_DL***](#app-dl)                                 |            Direct download Link for clean apk             | None                           |

`**` - By default all patches for a given app are included.<br>
`**` - Can be used to included universal patch.
`***` - Can be used for unavailable apps in the repository (unofficial apps).
>>>>>>> pr/9

## Support

<<<<<<< HEAD
I'll try my best to help you regarding this project. Make sure you've read everything here, repository synced & tasker project up-to-date and outcome is same from multiple reproductions. Still if any issues persist, you're free to open discussions, issues & PRs. Kindly have some patience after creating them.
=======
1. <a id="any-patch-apps"></a>**Officially** Supported values for **APP_NAME**** are :

    - [youtube](https://www.apkmirror.com/apk/google-inc/youtube/)
    - [youtube_music](https://www.apkmirror.com/apk/google-inc/youtube-music/)
    - [twitter](https://www.apkmirror.com/apk/twitter-inc/twitter/)
    - [reddit](https://www.apkmirror.com/apk/redditinc/reddit/)
    - [tiktok](https://www.apkmirror.com/apk/tiktok-pte-ltd/tik-tok-including-musical-ly/)
    - [warnwetter](https://www.apkmirror.com/apk/deutscher-wetterdienst/warnwetter/)
    - [spotify](https://spotify.en.uptodown.com/android)
    - [nyx-music-player](https://nyx-music-player.en.uptodown.com/android)
    - [icon_pack_studio](https://www.apkmirror.com/apk/smart-launcher-team/icon-pack-studio/)
    - [ticktick](https://www.apkmirror.com/apk/appest-inc/ticktick-to-do-list-with-reminder-day-planner/)
    - [twitch](https://www.apkmirror.com/apk/twitch-interactive-inc/twitch/)
    - [hex-editor](https://m.apkpure.com/hex-editor/com.myprog.hexedit)
    - [windy](https://www.apkmirror.com/apk/windy-weather-world-inc/windy-wind-weather-forecast/)
    - [my-expenses](https://my-expenses.en.uptodown.com/android)
    - [backdrops](https://backdrops.en.uptodown.com/android)
    - [expensemanager](https://apksos.com/app/com.ithebk.expensemanager)
    - [tasker](https://www.apkmirror.com/apk/joaomgcd/tasker-crafty-apps-eu/)
    - [irplus](https://irplus.en.uptodown.com/android)
    - [vsco](https://www.apkmirror.com/apk/vsco/vsco-cam/)
    - [meme-generator-free](https://meme-generator-free.en.uptodown.com/android)
    - [nova_launcher](https://www.apkmirror.com/apk/teslacoil-software/nova-launcher/)
    - [netguard](https://www.apkmirror.com/apk/marcel-bokhorst/netguard-no-root-firewall/)
    - [instagram](https://www.apkmirror.com/apk/instagram/instagram-instagram/)
    - [inshorts](https://www.apkmirror.com/apk/inshorts-formerly-news-in-shorts/)
    - [messenger](https://www.apkmirror.com/apk/facebook-/messenger/)
    - [grecorder](https://opnemer.en.uptodown.com/android)
    - [trakt](https://www.apkmirror.com/apk/trakt/trakt/)
    - [candyvpn](https://www.apkmirror.com/apk/liondev-io/candylink-vpn/)
    - [sonyheadphone](https://www.apkmirror.com/apk/sony-corporation/sony-headphones-connect/)
    - [androidtwelvewidgets](https://m.apkpure.com/android--widgets-twelve/com.dci.dev.androidtwelvewidgets)
    - [yuka](https://yuka.en.uptodown.com/android)
    - [relay](https://www.apkmirror.com/apk/dbrady/relay-for-reddit-/)
    - [boost](https://www.apkmirror.com/apk/ruben-mayayo/boost-for-reddit/)
    - [rif](https://www.apkmirror.com/apk/talklittle/reddit-is-fun/)
    - [sync](https://www.apkmirror.com/apk/red-apps-ltd/sync-for-reddit/)
    - [infinity](https://www.apkmirror.com/apk/red-apps-ltd/sync-for-reddit/)
    - [slide](https://www.apkmirror.com/apk/haptic-apps/slide-for-reddit/)
    - [bacon](https://www.apkmirror.com/apk/onelouder-apps/baconreader-for-reddit/)
    - [microg](https://github.com/inotia-/mMicroG/releases)
    - [pixiv](https://www.apkmirror.com/apk/pixiv-inc/pixiv/)
    - [strava](https://www.apkmirror.com/apk/strava-inc/strava-running-and-cycling-gps/)
    - [solidexplorer](https://www.apkmirror.com/apk/neatbytes/solid-explorer-beta/)
    - [lightroom](https://www.apkmirror.com/apk/adobe/lightroom/)
    - [duolingo](https://www.apkmirror.com/apk/duolingo/duolingo-duolingo/)
    - [musically](https://www.apkmirror.com/apk/tiktok-pte-ltd/tik-tok-including-musical-ly/)
    - [photomath](https://www.apkmonk.com/app/com.microblink.photomath/)
    - [joey](https://www.apkmonk.com/app/o.o.joey/)
    - [vanced](https://www.apkmirror.com/apk/team-vanced/youtube-vanced/)
    - [spotify-lite](https://www.apkmonk.com/app/com.spotify.lite/)
    - [digitales](https://www.apkmonk.com/app/at.gv.oe.app/)
    - [scbeasy](https://www.apkmonk.com/app/com.scb.phone/)
    - [reddit-news](https://m.apkpure.com/relay-for-reddit/reddit.news)
    - [finanz-online](https://apksos.com/app/at.gv.bmf.bmf2go)
    <br>`**` - You can also patch any other app which is **not** supported officially.To do so, you need to provide
   few more inputs to the tool which are mentioned below.
   ```ini
   <APP_NAME>_DL_SOURCE=<apk-link-to-any-of-the-suppored-scrapper>
   <APP_NAME>_PACKAGE_NAME=<package-name-of-the-application>
   ```
   You can also provide DL to the clean apk instead of providing DL_SOURCES as mentioned in this [note](#app-dl).
   Supported Scrappers are:
   1. APKMIRROR - Supports downloading any available version
        1. Link Format - https://www.apkmirror.com/apk/<organisation-name>/app-name/
        2. Example Link - https://www.apkmirror.com/apk/google-inc/youtube/
   2. UPTODOWN - Supports downloading any available version
        1. Link Format - https://<app-name>.en.uptodown.com/android
        2. Example Link - https://spotify.en.uptodown.com/android
   3. APKSOS - Supports downloading any available version
       1. Link Format - https://apksos.com/download-app/<package-name>
       2. Example Link - https://apksos.com/download-app/com.expensemanager
   4. APKPURE - Supports downloading only latest version
       1. Link Format - https://d.apkpure.com/b/APK/<package-name>?version=latest
       2. Example Link - https://d.apkpure.com/b/APK/com.google.android.youtube?version=latest
   5. APKMonk - Supports downloading any available version
       1. Link Format - https://www.apkmonk.com/app/<package-name>/
       2. Example Link - https://www.apkmonk.com/app/<package-name>/

   <br>Please verify the source of original APKs yourself with links provided. I'm not responsible for any damage
    caused.If you know any better/safe source to download clean. Open a discussion.

2. By default, script build the latest version mentioned in `patches.json` file.
3. Remember to download the **_Microg_**. Otherwise, you may not be able to open YouTube/YouTube Music.
4. <a id="patch-apps"></a>By default, tool will build only `youtube,youtube_music`. To build other apps supported by patching
   resources.Add the apps you want to build in `.env` file or in `ENVS` in `GitHub secrets` in the format
   ```ini
   PATCH_APPS=<APP_NAME>
   ```
   Example:
   ```ini
   PATCH_APPS=youtube,twitter,reddit
   ```
5. <a id="existing-downloaded-apks"></a>If APKMirror or other apk sources are blocked in your region or script
   somehow is unable to download from apkmirror. You can download apk manually from any source. Place them in
   `/apks` directory and provide environment variable in `.env` file or in `ENVS` in `GitHub secrets`(Recommended)
   in the format.
   ```dotenv
    EXISTING_DOWNLOADED_APKS=<Comma,Seperate,App,Name>
   ```
   Example:
   ```dotenv
    EXISTING_DOWNLOADED_APKS=youtube,youtube_music
   ```
   If you add above. Script will not download the `youtube` & `youtube_music`apk from internet and expects an apk in
   `/apks` folder with **same** name.
6. <a id="personal-access-token"></a>If you run script again & again. You might hit GitHub API limit. In that case
   you can provide your Personal GitHub Access Token in `.env` file or in `ENVS` in `GitHub secrets` (Recommended)
   in the format -
   ```dotenv
    PERSONAL_ACCESS_TOKEN=<PAT>
   ```
7. <a id="global-resources"></a>You can provide Direct download to the resource to used for patching apps `.env` file
   or in `ENVS` in `GitHub secrets` (Recommended) in the format -
   ```dotenv
    GLOBAL_CLI_DL=https://github.com/revanced/revanced-cli
    GLOBAL_PATCHES_DL=https://github.com/revanced/revanced-patches
    GLOBAL_PATCHES_JSON_DL=https://github.com/revanced/revanced-patches
    GLOBAL_INTEGRATIONS_DL=local://integrations.apk
   ```
   Resources downloaded from envs and will be used for patching for any **APP_NAME**.
   Unless provided different resource for the individual app.<br><br>
   Tool also support resource config at app level. You can patch A app with X resources while patching B with Y
   resources.
   This can be done by providing Direct download link for resources for app.<br>
   Example:
   ```dotenv
    YOUTUBE_CLI_DL=https://github.com/inotia00/revanced-cli
    YOUTUBE_PATCHES_DL=https://github.com/inotia00/revanced-patches
    YOUTUBE_PATCHES_JSON_DL=https://github.com/inotia00/revanced-patches
    YOUTUBE_INTEGRATIONS_DL=https://github.com/inotia00/revanced-integrations
   ```
   With the config tool will try to patch YouTube with resources from inotia00 while other global resource will used
   for patching other apps.<br>
   If you have want to provide resource locally in the apks folder. You can specify that by mentioning filename
   prefixed with `local://`.
   *Note* - The link provided must be DLs. Unless they are from GitHub.
8. <a id="global-keystore-file-name"></a>If you don't want to use default keystore. You can provide your own by
   placing it inside `apks` folder. And adding the name of `keystore-file` in `.env` file or in `ENVS` in `GitHub
   secrets` (Recommended) in the format
   ```dotenv
    GLOBAL_KEYSTORE_FILE_NAME=revanced.keystore
   ```
   Tool also support providing secret key at app level. You can sign A app with X key while signing B with Y
   key.<br>
    Example:
   ```dotenv
    YOUTUBE_KEYSTORE_FILE_NAME=youtube.keystore
   ```
9. <a id="global-archs-to-build"></a>You can build only for a particular arch in order to get smaller apk files.This
   can be done with by adding comma separated `ARCHS_TO_BUILD` in `ENVS` in `GitHub secrets` (Recommended) in the
   format.
   ```dotenv
    GLOABAL_ARCHS_TO_BUILD=arm64-v8a,armeabi-v7a
   ```
   Tool also support configuring at app level.<br>

   Example:
   ```dotenv
    YOUTUBE_ARCHS_TO_BUILD=arm64-v8a,armeabi-v7a
   ```
   *Note* -
   1. Possible values are: `armeabi-v7a`,`x86`,`x86_64`,`arm64-v8a`
   2. Make sure the patching resource(CLI) support this feature.
10. <a id="extra-files"></a>If you want to include any extra file to the Github upload. Set comma arguments
     in `.env` file or in `ENVS` in `GitHub secrets` (Recommended) in the format
    ```ini
    EXTRA_FILES=<url>@<appName>.apk
    ```
    Example:
    ```dotenv
     EXTRA_FILES=https://github.com/inotia00/mMicroG/releases/latest@mmicrog.apk,https://github.com/revanced/revanced-integrations@integrations.apk
    ```
11. <a id="custom-exclude-patching"></a>If you want to exclude any patch. Set comma separated patch in `.env` file
    or in `ENVS` in `GitHub secrets` (Recommended) in the format
    ```ini
    <APP_NAME>_EXCLUDE_PATCH=<PATCH_TO_EXCLUDE-1,PATCH_TO_EXCLUDE-2>
    ```
    Example:
    ```dotenv
     YOUTUBE_EXCLUDE_PATCH=custom-branding,hide-get-premium
     YOUTUBE_MUSIC_EXCLUDE_PATCH=yt-music-is-shit
    ```
    Note -
    1. **All** the patches for an app are **included** by default.<br>
    2. Revanced patches are provided as space separated, make sure you type those **-** separated here.
    It means a patch named _**Hey There**_ must be entered as **_hey-there_** in the above example.
12. <a id="custom-include-patching"></a>If you want to include any universal patch. Set comma separated patch in `.env`
    file or in `ENVS` in `GitHub secrets` (Recommended) in the format
    ```ini
    <APP_NAME>_INCLUDE_PATCH=<PATCH_TO_EXCLUDE-1,PATCH_TO_EXCLUDE-2>
    ```
    Example:
    ```dotenv
     YOUTUBE_INCLUDE_PATCH=remove-screenshot-restriction
    ```
    Note -
    1. Revanced patches are provided as space separated, make sure you type those **-** separated here.
       It means a patch named _**Hey There**_ must be entered as **_hey-there_** in the above example.
13. <a id="app-version"></a>If you want to build a specific version or latest version. Add `version` in `.env` file
    or in `ENVS` in `GitHub secrets` (Recommended) in the format
    ```ini
    <APP_NAME>_VERSION=<VERSION>
    ```
    Example:
    ```ini
    YOUTUBE_VERSION=17.31.36
    YOUTUBE_MUSIC_VERSION=X.X.X
    TWITTER_VERSION=latest
    ```
14. <a id="app-dl"></a>If you have your personal source for apk to be downloaded. You can also provide that and tool
    will not scarp links from apk sources.Add `dl` in `.env` file or in `ENVS` in `GitHub secrets` (Recommended) in
    the format
    ```ini
    <APP_NAME>_DL=<direct-app-download>
    ```
    Example:
    ```ini
    YOUTUBE_DL=https://d.apkpure.com/b/APK/com.google.android.youtube?version=latest
    ```
15. <a id="telegram-support"></a>For Telegram Upload.
     1. Set up a telegram channel, send a message to it and forward the message to
        this telegram [bot](https://t.me/username_to_id_bot)
     2. Copy `id` and save it to `TELEGRAM_CHAT_ID`<br>
        <img src="https://i.imgur.com/22UiaWs.png" width="300" style="left"><br>
     3. `TELEGRAM_BOT_TOKEN` - Telegram provides BOT_TOKEN. It works as sender. Open [bot](https://t.me/BotFather) and
        create one copy api key<br>
        <img src="https://i.imgur.com/A6JCyK2.png" width="300" style="left"><br>
     4. `TELEGRAM_API_ID` - Telegram API_ID is provided by telegram [here](https://my.telegram.org/apps)<br>
        <img src="https://i.imgur.com/eha3nnb.png" width="300" style="left"><br>
     5. `TELEGRAM_API_HASH` - Telegram API_HASH is provided by telegram [here](https://my.telegram.org/apps)<br>
        <img src="https://i.imgur.com/7n5k1mp.png" width="300" style="left"><br>
     6. After Everything done successfully a part of the actions secrets of the repository may look like<br>
        <img src="https://i.imgur.com/Cjifz1M.png" width="400">
16. Configuration defined in `ENVS` in `GitHub secrets` will override the configuration in `.env` file. You can use this
    fact to define your normal configurations in `.env` file and sometimes if you want to build something different just
    once. Add it in `GitHub secrets`.<br>
17. Sample Envs<br>
    <img src="https://i.imgur.com/FxOtiGs.png" width="600" style="left">
18. Make sure your Action has write access. If not click
    [here](https://github.com/nikhilbadyal/docker-py-revanced/settings/actions).
    In the bottom give read and write access to Actions.
    <img src="https://i.imgur.com/STSv2D3.png" width="400">
>>>>>>> pr/9
