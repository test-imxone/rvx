# Changelog

The changelogs listed here are combined from both this repository and the **RVX-Builds** tasker project. The versions are just release dates with format `YY.MM.DD`.

>> Here's the [**RVX-Builds**](https://taskernet.com/shares/?user=AS35m8k0QSchKA1x02SixFIhiL41a828J1qapOYfcEuyL2zSn%2FfJTN5WVSi01o18x6EAFb4%3D&id=Project%3ARVX-Builds) taskernet link.

## List of Versions

<details><summary>Click to expand</summary>

- [v23.10.04](#v231004)
- [v23.08.04](#v230804)

</details>

## v23.10.04

### ⭐ Custom Patch Resources

The Tool now supports resource config at app level. You can patch A app with X resources while patching B with Y resources. This can be done by providing supported download links for resources for the app. Another new major addition is to be able patch any supported app in the `patches.json`, irrespective of the official apps present in the repository configs. [**Read more...**](/auto/docs/customize-patches.md)

### Changes

- Renamed `/apps` to `/auto` folder and changed some folder structures.
- Removed `BUILD_EXTENDED` from both repository & tasker project.
- Added `CUSTOM_DLs` to source patch resources from GitHub, Locally (in `/apks` folder) and direct links.
- Removed `ALTERNATIVE_PATCHES` from both repository & tasker project.
- Added `PACKAGE_NAME` and `APK_DL` to patch any available app in sourced `patches.json` and apk is provided using either from supported (scraped) sources or direct download links.
- Removed `MicroG` auto-release by default due to different sources.
- Added `EXTRA_FILES` to release any user-defined apks from GitHub or link sources without patching.

- Added `RVX-Builds - Sources` task to help users save their favorite resources like *app_dl (`APK_DL`), extra (`EXTRA_FILES`), cli, patches, integrations (`CUSTOM_DLs`)*.
- Added `RVX-Builds - Resources` task to select desired resources from the set of sources (saved or currently being used) for global or app level config.
- Renamed task `RVX-Builds - Apps` to `RVX-Builds - Builder` and disintegrated app level config to a separate task `RVX-Builds - App Builder`.
- Added `RVX-Builds - Loading` to show a loading scene.
- Fixed `RVX-Builds - Project Updates` profile due to above changes and increased schedule period from `15 min` to `25 min`.
- Increase `RVX-Builds - Check For Updates` profile schedule period from `15 min` to `30 min`.
- Improved the **Update Checker** (`/.github/workflows/update.yml`) workflow to use a python script (`/scripts/check_updates.py`).
- Improved rest of scripting in both repository and in tasker project.

### Notes

- With `PACKAGE_NAME` and `APK_DL`, alternative builds of same packages can also be released. See an [example](/.env.example).
- With `EXTRA_FILES`, any number of microg builds (apks provided by different organisations) can be released. See an [example](/.env.example).
- In Tasker, users might experience some delays at some parts due to a large sequence of actions majorly depending on internet connection to fetch patch sources. I'll look for improvements.

## v23.08.04

- Initial Release of **rvx-builds** repository.
- Initial Release of **RVX-Builds** Tasker project.
