#!/usr/bin/env python3

import argparse
import os
import stat
import sys
import tempfile
import textwrap

import utils

from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Generate a .travis.yml and .travis directory'
                                                 'for a specified plugin')
    parser.add_argument('plugin_name', type=str,
                        help=textwrap.dedent('''\
                            Update this plugin's' Travis config

                            A plugin with this name must already exist.

                        '''))
    parser.add_argument('--pypi-username', type=str,
                        help=textwrap.dedent('''\
                            The username that should be used when uploading packages to PyPI. It
                            is required unless --exclude-deploy-client-to-pypi and
                            --exclude-deploy-daily-client-to-pypi and --exclude-deploy-to-pypi are
                            specified.

                        '''))
    parser.add_argument('--exclude-docs-test', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis build for testing the 'make html' command for sphinx
                            docs

                        '''))
    parser.add_argument('--exclude-mariadb-test', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis build for testing against MariaDB.

                        '''))
    parser.add_argument('--exclude-deploy-to-pypi', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that publishes builds to PyPI

                            This stage only executes when a tag is associated with the commit being
                            built. When enabling this stage, the user is expected to provide a
                            secure environment variable called PYPI_PASSWORD. The variable can
                            be added in the travis-ci.com settings page for the project[0]. The PYPI
                            username is specified using --pypi-username option.

                        '''))
    parser.add_argument('--exclude-test-bindings', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that runs a script to test generated client
                            library.

                            This stage requires the plugin author to include a 'test_bindings.py'
                            script in the .travis directory of the plugin repository. This script
                            is supposed to exercise the generated client library.

                        '''))
    parser.add_argument('--exclude-deploy-client-to-pypi', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that publishes a client library to PyPI.

                            This stage only executes when a tag is associated with the commit being
                            built. When enabling this stage, the user is expected to provide a
                            secure environment variable called PYPI_PASSWORD. The variable can
                            be added in the travis-ci.com settings page for the project[0]. The PYPI
                            username is specified using --pypi-username option.

                            This stage uses the OpenAPI schema for the plugin to generate a Python
                            client library using openapi-generator-cli.

                        '''))
    parser.add_argument('--exclude-deploy-client-to-rubygems', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that publishes a client library to RubyGems.org.

                            This stage only executes when a tag is associated with the commit being
                            built. When enabling this stage, the user is expected to provide a
                            secure environment variable called RUBYGEMS_API_KEY. The variable can
                            be added in the travis-ci.com settings page for the project.

                        '''))
    parser.add_argument('--exclude-deploy-daily-client-to-pypi', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that publishes a client library to PyPI.

                            This stage only executes when a tag is associated with the commit being
                            built. When enabling this stage, the user is expected to provide a
                            secure environment variable called PYPI_PASSWORD. The variable can
                            be added in the travis-ci.com settings page for the project[0]. The PYPI
                            username is specified using --pypi-username option.

                            This stage uses the OpenAPI schema for the plugin to generate a Python
                            client library using openapi-generator-cli.

                            [0] https://docs.travis-ci.com/user/environment-variables/
                            #defining-variables-in-repository-settings

                        '''))
    parser.add_argument('--exclude-deploy-daily-client-to-rubygems', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude a Travis stage that publishes a client library to RubyGems.org
                            with each CRON build.

                            This stage only executes on builds trigerred by CRON. When enabling
                            this stage, the user is expected to provide a secure environment
                            variable called RUBYGEMS_API_KEY. The variable can be added in the
                            travis-ci.com settings page for the project.

                        '''))
    parser.add_argument('--exclude-check-commit-message', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude inspection of commit message for a reference to an issue in
                            pulp.plan.io.

                        '''))
    parser.add_argument('--exclude-coverage', action='store_true',
                        help=textwrap.dedent('''\
                            Exclude collection of coverage and reporting to coveralls.io
                            pulp.plan.io.

                        '''))
    args = parser.parse_args()
    config = {}
    for name, value in args._get_kwargs():
        config[name] = value

    if config['plugin_name'] == 'pulpcore':
        config['plugin_snake_name'] = 'pulpcore'
        config['plugin_dash_name'] = 'pulpcore'
    else:
        config['plugin_snake_name'] = 'pulp_' + config['plugin_name']
        config['plugin_dash_name'] = 'pulp-' + config['plugin_name']

    if not utils.is_valid(config['plugin_name']):
        parser.print_help()
        return 2

    if not config['pypi_username'] and not config['exclude_deploy_client_to_pypi'] and \
            not config['exclude_deploy_to_pypi']:
        parser.print_help()
        return 2

    orig_root_dir = os.path.dirname(os.path.abspath(parser.prog))
    dst_root_dir = os.path.join(os.path.dirname(orig_root_dir), config['plugin_snake_name'])

    if not config['exclude_test_bindings']:
        if not os.path.isfile(os.path.join(dst_root_dir, '.travis', 'test_bindings.py')):
            parser.print_help()
            return 2

    templates = ['.travis.yml']
    templates += ['.travis/' + f for f in os.listdir(orig_root_dir + '/templates/.travis/')]
    for template in templates:
        write_file_to_plugin_dir(template, config, dst_root_dir)

    return 0


def write_file_to_plugin_dir(template_name, config, dst_dir):
    """
    Create a file in the plugin directory by rendering a template with config passed in.

    Args:
        template_name (str): path to the template relative to the 'template' directory
        config (dict): dictionary with all parameters for the template
        dst_dir (str): path to the root of plugin being updated
    """
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name)
    with tempfile.NamedTemporaryFile(mode='w', dir=dst_dir, delete=False) as fd_out:
        tempfile_path = fd_out.name
        fd_out.write(template.render(**config))
        fd_out.write('\n')
    file_path = os.path.join(dst_dir, template_name)
    os.rename(tempfile_path, file_path)
    if file_path.endswith('.sh'):
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | \
            stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    else:
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH
    os.chmod(file_path, mode)
    print(file_path)


if __name__ == '__main__':
    sys.exit(main())
