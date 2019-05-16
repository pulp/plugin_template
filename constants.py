TEMPLATE_SNAKE = 'pulp_plugin_template'
TEMPLATE_SNAKE_SHORT = 'plugin_template'
TEMPLATE_CAPS = 'PULP_PLUGIN_TEMPLATE'
TEMPLATE_CAPS_SHORT = 'PLUGIN_TEMPLATE'
TEMPLATE_CAMEL = 'PulpPluginTemplate'
TEMPLATE_CAMEL_SHORT = 'PluginTemplate'
TEMPLATE_DASH = 'pulp-plugin-template'
TEMPLATE_DASH_SHORT = 'plugin-template'
IGNORE_FILES = (
    'LICENSE',
    'COMMITMENT',
    'pep8speaks.yml',
    'bootstrap.py',
    'Vagrantfile.example'
)
IGNORE_COPYTREE = ('.git', '*.pyc', '*.egg-info', 'bootstrap.py', '__pycache__', 'meta-docs',
                   'constants.py', 'generate_travis_config.py', 'templates')
