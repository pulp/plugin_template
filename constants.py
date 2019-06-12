TEMPLATE_SNAKE = '{{ plugin_snake }}'
TEMPLATE_SNAKE_SHORT = '{{ plugin_snake_short }}'
TEMPLATE_CAPS = '{{ plugin_caps }}'
TEMPLATE_CAPS_SHORT = '{{ plugin_caps_short }}'
TEMPLATE_CAMEL = '{{ plugin_camel }}'
TEMPLATE_CAMEL_SHORT = '{{ plugin_camel_short }}'
TEMPLATE_DASH = '{{ plugin_dash }}'
TEMPLATE_DASH_SHORT = '{{ plugin_dash_short }}'
IGNORE_FILES = (
    'LICENSE',
    'COMMITMENT',
    'pep8speaks.yml',
    'bootstrap.py',
    'Vagrantfile.example'
)
IGNORE_COPYTREE = ('.git', '*.pyc', '*.egg-info', 'bootstrap.py', '__pycache__', 'meta-docs',
                   'constants.py', 'generate_travis_config.py', 'templates')
