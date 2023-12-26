import os
from typing import List, Mapping

from ruamel.yaml import YAML

import json

yaml = YAML()

def run():
    variables = {}
    rules = []

    for root, dirs, files in os.walk("variables"):
        for name in files:
            file_name = os.path.join(root, name)
            print(file_name)
            variables.update(get_vars(file_name))
    for root, dirs, files in os.walk("rules"):
        for name in files:
            file_name = os.path.join(root, name)
            print(file_name)
            rules.extend(get_rules(file_name))
    for rule in rules:
        for k, v in rule.items():
            # could be more things, but in practice only list and string
            if isinstance(v, str):
                rule[k] = v.format(**variables)
            elif isinstance(v, list):
                rule[k] = [x.format(**variables) for x in v]
            else:
                raise NotImplementedError(f"unknown type for {k}: {type(v)}")

    rule_group = {
        "name": "combined list",
        "description": "combination of rules",
        "rules":  rules,
    }
    with open("output/rules.json", "w") as fh:
        json.dump(rule_group, fh, indent=2)
        fh.write("\n")  # Add newline at the end of the file


def get_rules(file_name: str) -> List[Mapping]:
    with open(file_name) as fh:
        rules = yaml.load(fh)
        assert isinstance(rules, list)
        return rules


def get_vars(file_name: str) -> Mapping:
    with open(file_name) as fh:
        vars = yaml.load(fh)
        assert isinstance(vars, dict)
        return vars


if __name__ == '__main__':
    run()
