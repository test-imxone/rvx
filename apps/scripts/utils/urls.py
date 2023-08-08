class GitHubURLs:
    default_repo = "IMXEren/rvx-builds"
    default_branch = "changelogs"

    def __init__(self, repo_full=default_repo, repo_branch=default_branch):
        self.repo = repo_full
        self.branch = repo_branch
    
    def get_env(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/.env"
    
    def get_env_json(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/apps/json/env.json"
    
    def get_apps_json(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/apps/revanced/apps.json"
    
    def get_patches_py(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/src/patches.py"
    
    def get_config_py(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/src/config.py"
    
    def get_extras_json(self):
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/apps/json/extras.json"
    
    def get_rv_json(self):
        return f"https://raw.githubusercontent.com/revanced/revanced-patches/main/patches.json"
    
    def get_rvx_json(self):
        return f"https://raw.githubusercontent.com/inotia00/revanced-patches/revanced-extended/patches.json"
    
    def get_cli_dl(self):
        return f"https://github.com/revanced/revanced-cli"
    
    def get_patches_dl(self):
        return f"https://github.com/revanced/revanced-patches"
    
    def get_patches_json_dl(self):
        return f"https://github.com/revanced/revanced-patches"
    
    def get_integrations_dl(self):
        return f"https://github.com/revanced/revanced-integrations"
