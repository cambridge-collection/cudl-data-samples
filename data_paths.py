#!/usr/bin/env python3
"""
Print the path of data files associated with JSON file paths

Usage:
    data_paths [options] [JSON_PATH...]

Arguments:
    JSON_PATH  The path of a JSON file (path must of the form "json/*.json"
               If not specified, paths are read from stdin

Examples:

    $ ls
    data/  json/
    $ python data_paths.py \\
        json/MS-TS-AR-00026-00076.json \\
        json/MS-TS-00006-J-00001-00001.json
    json/MS-TS-AR-00026-00076.json
    data/tei/MS-TS-AR-00026-00076/MS-TS-AR-00026-00076.xml
    json/MS-TS-00006-J-00001-00001.json
    data/tei/MS-TS-00006-J-00001-00001/MS-TS-00006-J-00001-00001.xml

"""

import os
import sys
from collections import defaultdict
from pathlib import Path

from docopt import docopt


def main():
    args = docopt(__doc__)
    base_dir = Path('.')
    json_dir = base_dir / 'json'
    data_dir = base_dir / 'data'

    json_paths = get_json_paths_by_id(json_dir, args['JSON_PATH'] or sys.stdin)
    data_paths = get_data_paths_by_id(data_dir, json_paths.keys())

    for json_id, json_path in json_paths.items():
        print(json_path)
        for data_path in data_paths[json_id]:
            print(data_path)


def get_json_paths_by_id(json_dir, input_lines):
    json_paths = {}
    for line in input_lines:
        json_path = Path(line.rstrip())

        if not json_path.name.endswith('.json'):
            raise ValueError(f'input path does not end with .json: {json_path}')
        if json_dir not in json_path.parents:
            raise ValueError(f'input path is not under {json_dir}: {json_path}')

        json_path_id = json_path.name[:-5]
        if json_path_id in json_paths:
            raise ValueError(f'duplicate input path: {json_path}')
        json_paths[json_path_id] = json_path
    return json_paths


def get_data_paths_by_id(data_dir: Path, json_ids):
    def generate_data_paths():
        for (_dirpath, dirnames, filenames) in os.walk(data_dir):
            dirpath = Path(_dirpath)
            if dirpath == data_dir:
                pass
            elif dirpath.parent == data_dir:
                # Constrain the traversal to only visit data dirs for items
                # we are looking for
                dirnames[:] = [name for name in dirnames if name in json_ids]
            else:
                json_id = dirpath.parts[:len(data_dir.parts) + 2][-1]
                assert json_id in json_ids
                yield from ((json_id, dirpath / fn) for fn in filenames)

    data_paths = defaultdict(list)
    for json_id, data_path in generate_data_paths():
        data_paths[json_id].append(data_path)
    return data_paths


if __name__ == '__main__':
    main()
