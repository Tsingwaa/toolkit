###############################################################################
# Copyright (C) 2022 All rights reserved.
# Filename: fetch_filename_list.py
# Author: Tsingwaa
# Email: zengchh3@gmail.com
# Created Time : 2022-01-25 21:49 Tuesday
# Last modified: 2022-01-25 21:49 Tuesday
# Description: Fetch filename list for images stored by folder
#
###############################################################################

import json
import os
import os.path as osp


def fetch_filename_list(root):
    """Fetch filename list and sort by cardinality in decreasing order.

    Args:
        root: the root directory of data.
    """

    dir2fnames = dict()

    print("Getting filenames from root...")

    for root, dirs, files in os.walk(root):
        for dir_name in dirs:
            dir_path = osp.join(root, dir_name)
            fnames = [
                osp.join(dir_name, fname) for fname in os.listdir(dir_path)

                if osp.splitext(fname)[1] in ['.jpeg', '.jpg']
            ]
            dir2fnames[dir_name] = fnames

    dir2fnum = {
        dir_name: len(fnames)

        for dir_name, fnames in dir2fnames.items()
    }

    print(f"Number of directories:\n {dir2fnum}")

    sorted_dir_list = sorted(dir2fnum[0], key=lambda d: d[1], reverse=True)

    print(f"Sorted directory list: {sorted_dir_list}")

    label2fnames = {}

    for i, dir_name in enumerate(sorted_dir_list):
        fnames = dir2fnames[dir_name]
        label2fnames[i] = fnames

    print(f"label2fnames:\n{label2fnames}")

    return label2fnames


if __name__ == "__main__":
    root = "~/Datasets/Xray14/Data/"
    save_path = "~/Datasets/Xray14/label2fnames.json"

    label2fnames = fetch_filename_list(root)

    print(f"Writing into '{save_path}'...")
    with open(save_path, 'w') as f:
        json.dump(label2fnames, f)
