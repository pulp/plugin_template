import argparse
import yaml

# Parse the command-line argument
parser = argparse.ArgumentParser()
parser.add_argument('value_name', help='Name of the value to extract')
args = parser.parse_args()

# Read the YAML file
with open('template_config.yml') as file:
    data = yaml.safe_load(file)

# Extract the value based on the provided name
value = data.get(args.value_name)

# Output the value
if value is not None:
    print(value)
else:
    print("")
