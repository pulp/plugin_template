#!/usr/bin/env python3

import argparse
import os
import shutil
import stat
import sys
import tempfile
import textwrap
import utils
import yaml

from jinja2 import Environment, FileSystemLoader


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Generate a .travis.yml and .travis directory'
                                                 'for a specified plugin')
    parser.add_argument('plugin_name', type=str,
                        help=textwrap.dedent('''\
                            Create or update this plugin.

                        '''))
    parser.add_argument('--bootstrap', action='store_true',
                        help=textwrap.dedent('''\
                            Create a new plugin and template boilerplate code.

                        '''))
    parser.add_argument('--test', action='store_true',
                        help=textwrap.dedent('''\
                            Generate or update functional and unit tests.

                        '''))
    parser.add_argument('--travis', action='store_true',
                        help=textwrap.dedent('''\
                            Generate or update travis configuration files.

                        '''))
    parser.add_argument('--docs', action='store_true',
                        help=textwrap.dedent('''\
                            Generate or update plugin documentation.

                        '''))
    parser.add_argument('--all', action='store_true',
                        help=textwrap.dedent('''\
                            Create a new plugin and template all non-excluded files.

                        '''))
    parser.add_argument('--verbose', action='store_true',
                        help=textwrap.dedent('''\
                            Include more output.

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
        config['plugin_snake'] = 'pulpcore'
    else:
        config['plugin_snake'] = 'pulp_' + config['plugin_name']

    config['plugin_snake_short'] = config['plugin_name']
    config['plugin_caps'] = utils.to_caps(config['plugin_snake'])
    config['plugin_caps_short'] = utils.to_caps(config['plugin_name'])
    config['plugin_camel_short'] = utils.to_camel(config['plugin_snake'])
    config['plugin_camel'] = utils.to_camel(config['plugin_name'])
    config['plugin_dash_short'] = utils.to_dash(config['plugin_name'])
    config['plugin_dash'] = utils.to_dash(config['plugin_snake'])

    here = os.path.dirname(os.path.abspath(__file__))
    plugin_root_dir = os.path.join(os.path.dirname(here), config['plugin_snake'])

    if config['travis']:
        if not config['pypi_username'] and not config['exclude_deploy_client_to_pypi'] and \
                not config['exclude_deploy_to_pypi']:
            print("If PyPI scripts are included, PyPI username is required.")
            return 2

        if not config['exclude_test_bindings']:
            if not os.path.isfile(os.path.join(plugin_root_dir, '.travis', 'test_bindings.py')):
                print("If bindings are not excluded, `test_bindings.py` must exist.")
                return 2

    if not utils.is_valid(config['plugin_name']):
        print("Invalid plugin name")
        return 2

    for section in ['bootstrap', 'travis', 'docs', 'test']:
        if config.get(section) or config.get('all'):
            write_template_section(config, section, plugin_root_dir)

    with open(os.path.join(plugin_root_dir, 'template_config.yml'), 'w') as outfile:
        outfile.write("# This config represents the latest values used when running the "
                      "template.\n\n")
        yaml.dump(config, outfile, default_flow_style=False)


def write_template_section(config, name, plugin_root_dir):
    """
    Template or copy all files for the section.
    """
    section_template_dir = "{name}_templates".format(name=name)
    env = Environment(
        loader=FileSystemLoader(section_template_dir)
    )

    files_templated = 0
    files_copied = 0
    for relative_path in generate_relative_path_set(section_template_dir):
        necessary_dir_structure = os.path.dirname(os.path.join(plugin_root_dir, relative_path))
        if not os.path.exists(necessary_dir_structure):
            os.makedirs(necessary_dir_structure)

        if relative_path.endswith('.j2'):
            template = env.get_template(relative_path)
            destination = relative_path[:-len('.j2')]
            write_template_to_file(template, plugin_root_dir, destination, config)
            files_templated += 1
            if config.get('verbose'):
                print(f"Templated file: {relative_path}")
        else:
            shutil.copyfile(
                os.path.join(section_template_dir, relative_path),
                os.path.join(plugin_root_dir, relative_path)
            )
            files_copied += 1
            if config.get('verbose'):
                print(f"Copied file: {relative_path}")

    print(f"Section: {name} \n    templated: {files_templated}\n    copied: {files_copied}")
    return 0


def generate_relative_path_set(root_dir):
    """
    Create a set of relative paths within the specified directory.
    """
    applicable_paths = set()
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for file_name in files:
            template_abs_path = os.path.join(root, file_name)
            template_relative_path = os.path.relpath(template_abs_path,
                                                     root_dir)
            applicable_paths.add(template_relative_path)
    return applicable_paths


def write_template_to_file(template, plugin_root_dir, relative_path, config):
    """
    Render template with values from the config and write it to the target plugin directory.
    """

    with tempfile.NamedTemporaryFile(mode='w', dir=plugin_root_dir, delete=False) as fd_out:
        tempfile_path = fd_out.name
        fd_out.write(template.render(**config))
        fd_out.write('\n')

        destination_path = os.path.normpath(os.path.join(plugin_root_dir, relative_path))
        os.rename(tempfile_path, destination_path)

        if destination_path.endswith('.sh'):
            mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | \
                stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
        else:
            mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH
        os.chmod(destination_path, mode)


if __name__ == '__main__':
    sys.exit(main())
