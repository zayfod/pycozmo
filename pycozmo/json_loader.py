"""

JSON reading functions for files containing non-standard comments

"""

import json
import os
from typing import Dict, List


def load_json_file(filename: str) -> Dict:
    with open(filename, 'r') as f:
        filtered_json = ''
        for line in f.readlines():
            # ignore urls (don't know what they might be used for)
            if '\"url\":' not in line:
                # get all characters before '//'
                filtered_json += line.split('//')[0]
        return json.loads(filtered_json)


def get_json_files(resource_dir: str, base_names: List[str]) -> List[str]:
    file_addr = []

    for name in base_names:
        if name[0] == '/':
            name = name[1:]
        addr = os.path.join(resource_dir, name)
        if os.path.isdir(addr):
            for root, _, files in os.walk(addr):
                for name in files:
                    if name.endswith('.json'):
                        file_addr.append(os.path.join(root, name))

        elif addr.endswith('.json'):
            file_addr.append(addr)

    return file_addr


def find_file(directory: str, name: str) -> str:
    for root, _, files in os.walk(directory):
        if name in files:
            return os.path.join(root, name)
