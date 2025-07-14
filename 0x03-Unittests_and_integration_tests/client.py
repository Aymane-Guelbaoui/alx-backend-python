
"""Client module to interact with GitHub organizations."""
from typing import List, Dict
from utils import get_json


class GithubOrgClient:
    """GitHub Organization Client."""
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Retrieve org info."""
        return get_json(self.ORG_URL.format(org=self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Retrieve public repos URL."""
        return self.org["repos_url"]

    def public_repos(self, license: str = None) -> List[str]:
        """Get list of public repos, optionally filter by license."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [repo["name"] for repo in repos if self.has_license(repo, license)]

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if repo has given license."""
        return repo.get("license", {}).get("key") == license_key
