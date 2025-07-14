
"""Unit and integration tests for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked.url/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "http://mocked.url/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = repos_payload
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://mocked.url"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [
            unittest.mock.Mock(**{"json.return_value": cls.org_payload}),
            unittest.mock.Mock(**{"json.return_value": cls.repos_payload})
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
