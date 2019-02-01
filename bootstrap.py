#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import sys
import tempfile
import textwrap

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
IGNORE_COPYTREE = ('.git', '*.pyc', '*.egg-info', 'bootstrap.py', '__pycache__', 'meta-docs')


def is_valid(name):
    """
    Check if specified name is compliant with requirements for it.

    The max length of the name is 16 characters. It seems reasonable to have this limitation
    because the plugin name is used for directory name on the file system and it is also used
    as a name of some Python objects, like class names, so it is expected to be relatively short.
    """
    return bool(re.match(r'^[a-z][0-9a-z_]{2,15}$', name))


def to_camel(name):
    """
    Convert plugin name from snake to camel case
    """
    return name.title().replace('_', '')


def to_caps(name):
    """
    Convert plugin name from snake to upper snake case
    """
    return name.upper()


def to_dash(name):
    """
    Convert plugin name from snake case to dash representation
    """
    return name.replace('_', '-')


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='rename template data to a specified plugin name')
    parser.add_argument('plugin_name', type=str,
                        help=textwrap.dedent('''\
                            set plugin name to this one

                            Requirements for plugin name:
                             - specified in the snake form: your_new_plugin_name
                             - consists of 3-16 characters
                             - possible characters are letters [a-z], numbers [0-9], underscore [_]
                             - first character should be a letter [a-z]
                        '''))
    args = parser.parse_args()
    plugin_name = args.plugin_name

    if not is_valid(plugin_name):
        parser.print_help()
        return 2

    pulp_plugin_name = 'pulp_' + plugin_name
    replace_map = {
        TEMPLATE_SNAKE: pulp_plugin_name,
        TEMPLATE_SNAKE_SHORT: plugin_name,
        TEMPLATE_CAPS: to_caps(pulp_plugin_name),
        TEMPLATE_CAPS_SHORT: to_caps(plugin_name),
        TEMPLATE_CAMEL_SHORT: to_camel(plugin_name),
        TEMPLATE_CAMEL: to_camel(pulp_plugin_name),
        TEMPLATE_DASH_SHORT: to_dash(plugin_name),
        TEMPLATE_DASH: to_dash(pulp_plugin_name),
    }

    # copy template directory
    orig_root_dir = os.path.dirname(os.path.abspath(parser.prog))
    dst_root_dir = os.path.join(os.path.dirname(orig_root_dir), pulp_plugin_name)
    try:
        shutil.copytree(orig_root_dir, dst_root_dir,
                        ignore=shutil.ignore_patterns(*IGNORE_COPYTREE))
    except FileExistsError:
        print(textwrap.dedent('''
              It looks like plugin with such name already exists!
              Please, choose another name.
              '''))
        return 1

    # rename python package directory
    listed_dir = os.listdir(dst_root_dir)
    if TEMPLATE_SNAKE in listed_dir:
        os.rename(os.path.join(dst_root_dir, TEMPLATE_SNAKE),
                  os.path.join(dst_root_dir, pulp_plugin_name))

    # replace text
    for dir_path, dirs, files in os.walk(dst_root_dir):
        for file in files:
            # skip files which don't need any text replacement
            if file in IGNORE_FILES:
                continue

            file_path = os.path.join(dir_path, file)

            # write substituted text to temporary file
            with open(file_path) as fd_in, tempfile.NamedTemporaryFile(mode='w', dir=dir_path,
                                                                       delete=False) as fd_out:
                tempfile_path = fd_out.name
                text = fd_in.read()
                for old, new in replace_map.items():
                    text = text.replace(old, new)
                # discard anything between TEMPLATE_REMOVE_START and TEMPLATE_REMOVE_END tags
                if text.count('TEMPLATE_REMOVE_START') and text.count('TEMPLATE_REMOVE_END'):
                    lines = text.splitlines()
                    # get the indexes of our template start and end tags
                    start_indexes = [
                        l[0] for l in enumerate(lines) if l[1].count('TEMPLATE_REMOVE_START')
                    ]
                    end_indexes = [
                        l[0] + 1 for l in enumerate(lines) if l[1].count('TEMPLATE_REMOVE_END')
                    ]
                    # zip those two lists together and make a range using the start and end indexes
                    # turn the list of ranges into a list of lists e.g.
                    # [[0, 1, 2, 4, 5], [10, 11, 12, 13]]
                    skip_lines = [
                        list(range(*x)) for x in zip(start_indexes, end_indexes)
                    ]
                    # flatten the list to have one list of lines to skip
                    skip_lines = [idx for seq in skip_lines for idx in seq]
                    # rebuild the text from the lines but exclude the indexes between the tags
                    new_lines = [l[1] for l in enumerate(lines) if l[0] not in skip_lines]
                    text = "\n".join(new_lines)

                fd_out.write(text)

            # overwrite existing file by renaming the temporary one
            os.rename(tempfile_path, file_path)

    return 0


if __name__ == '__main__':
    sys.exit(main())
