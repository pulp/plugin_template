# coding=utf-8
"""Constants for Pulp PluginTemplate plugin tests."""
from urllib.parse import urljoin

from pulp_smash.constants import PULP_FIXTURES_BASE_URL
from pulp_smash.pulp3.constants import (
    BASE_PUBLISHER_PATH,
    BASE_REMOTE_PATH,
    CONTENT_PATH
)

# FIXME: list any download policies supported by your plugin type here.
# If your plugin supports all download policies, you can import this
# from pulp_smash.pulp3.constants instead.
# DOWNLOAD_POLICIES = ['immediate', 'streamed', 'on_demand']
DOWNLOAD_POLICIES = ['immediate']

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
PLUGIN_TEMPLATE_CONTENT_NAME = 'plugin_template.unit'

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
PLUGIN_TEMPLATE_CONTENT_PATH = urljoin(CONTENT_PATH, 'plugin_template/units/')

PLUGIN_TEMPLATE_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, 'plugin_template/plugin-template/')

PLUGIN_TEMPLATE_PUBLISHER_PATH = urljoin(BASE_PUBLISHER_PATH, 'plugin_template/plugin-template/')

# FIXME: replace this with your own fixture repository URL and metadata
PLUGIN_TEMPLATE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'plugin_template/')
"""The URL to a plugin_template repository."""

# FIXME: replace this with the actual number of content units in your test fixture
PLUGIN_TEMPLATE_FIXTURE_COUNT = 3
"""The number of content units available at :data:`PLUGIN_TEMPLATE_FIXTURE_URL`."""

PLUGIN_TEMPLATE_FIXTURE_SUMMARY = {
    PLUGIN_TEMPLATE_CONTENT_NAME: PLUGIN_TEMPLATE_FIXTURE_COUNT,
}
"""The desired content summary after syncing :data:`PLUGIN_TEMPLATE_FIXTURE_URL`."""

# FIXME: replace this with the location of one specific content unit of your choosing
PLUGIN_TEMPLATE_URL = urljoin(PLUGIN_TEMPLATE_FIXTURE_URL, '')
"""The URL to an plugin_template file at :data:`PLUGIN_TEMPLATE_FIXTURE_URL`."""

# FIXME: replace this with your own fixture repository URL and metadata
PLUGIN_TEMPLATE_INVALID_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'plugin_template-invalid/')
"""The URL to an invalid plugin_template repository."""

# FIXME: replace this with your own fixture repository URL and metadata
PLUGIN_TEMPLATE_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'plugin_template_large/')
"""The URL to a plugin_template repository containing a large number of content units."""

# FIXME: replace this with the actual number of content units in your test fixture
PLUGIN_TEMPLATE_LARGE_FIXTURE_COUNT = 25
"""The number of content units available at :data:`PLUGIN_TEMPLATE_LARGE_FIXTURE_URL`."""
