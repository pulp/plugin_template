# coding=utf-8
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

# FIXME: replace this with the actual number of content units in your test fixture
PLUGIN_TEMPLATE_FIXTURE_COUNT = 3

PLUGIN_TEMPLATE_FIXTURE_SUMMARY = {
    PLUGIN_TEMPLATE_CONTENT_NAME: {'count': PLUGIN_TEMPLATE_FIXTURE_COUNT}
}

# FIXME: replace this with the location of one specific content unit of your choosing
PLUGIN_TEMPLATE_URL = urljoin(PLUGIN_TEMPLATE_FIXTURE_URL, '')

# FIXME: replace this iwth your own fixture repository URL and metadata
PLUGIN_TEMPLATE_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'plugin_template_large/')

# FIXME: replace this with the actual number of content units in your test fixture
PLUGIN_TEMPLATE_LARGE_FIXTURE_COUNT = 25
