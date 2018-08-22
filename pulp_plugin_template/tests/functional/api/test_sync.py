# coding=utf-8
"""Tests that sync plugin_template plugin repositories."""
import unittest

from pulp_smash import api, config
from pulp_smash.pulp3.constants import REPO_PATH
from pulp_smash.pulp3.utils import (
    gen_repo,
    get_content,
    get_added_content,
    sync,
)

from pulp_plugin_template.tests.functional.constants import (
    PLUGIN_TEMPLATE_FIXTURE_COUNT,
    PLUGIN_TEMPLATE_REMOTE_PATH
)
from pulp_plugin_template.tests.functional.utils import gen_plugin_template_remote
from pulp_plugin_template.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


# Implement sync support before enabling this test.
@unittest.skip("FIXME: plugin writer action required")
class BasicSyncPluginTemplateRepoTestCase(unittest.TestCase):
    """Sync repositories with the plugin_template plugin."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()

    def test_sync(self):
        """Sync repositories with the plugin_template plugin.

        In order to sync a repository a remote has to be associated within
        this repository. When a repository is created this version field is set
        as None. After a sync the repository version is updated.

        Do the following:

        1. Create a repository, and a remote.
        2. Assert that repository version is None.
        3. Sync the remote.
        4. Assert that repository version is not None.
        5. Sync the remote one more time.
        6. Assert that repository version is different from the previous one.
        """
        client = api.Client(self.cfg, api.json_handler)

        repo = client.post(REPO_PATH, gen_repo())
        self.addCleanup(client.delete, repo['_href'])

        body = gen_plugin_template_remote()
        remote = client.post(PLUGIN_TEMPLATE_REMOTE_PATH, body)
        self.addCleanup(client.delete, remote['_href'])

        # Sync the repository.
        self.assertIsNone(repo['_latest_version_href'])
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertIsNotNone(repo['_latest_version_href'])
        self.assertEqual(len(get_content(repo)), PLUGIN_TEMPLATE_FIXTURE_COUNT)
        self.assertEqual(len(get_added_content(repo)), PLUGIN_TEMPLATE_FIXTURE_COUNT)

        # Sync the repository again.
        latest_version_href = repo['_latest_version_href']
        sync(self.cfg, remote, repo)
        repo = client.get(repo['_href'])

        self.assertNotEqual(latest_version_href, repo['_latest_version_href'])
        self.assertEqual(len(get_content(repo)), PLUGIN_TEMPLATE_FIXTURE_COUNT)
        self.assertEqual(len(get_added_content(repo)), 0)
