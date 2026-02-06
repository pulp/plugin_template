# /// script
# dependencies = [
#     "pyyaml>=6.0.3,<6.1.0",
# ]
#
# ///

import sys

import argparse
import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("value_name", help="Name of the value to extract")
    args = parser.parse_args()

    with open("template_config.yml") as file:
        data = yaml.safe_load(file)

    try:
        value = data.get(args.value_name)
    except KeyError:
        sys.exit(1)

    # Output the value
    if value is not None:
        print(value)
    else:
        print("")
