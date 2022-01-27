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

import os
import os.path as osp

import yaml


def fetch_filename_list(data_root):
    """Fetch filename list and sort by cardinality in decreasing order.

    Args:
        root: the root directory of data.
    """

    print("Getting filenames from root directory...")

    class_names = os.listdir(data_root)
    class2fnames = dict()
    class2fnum = dict()

    for class_name in class_names:
        dir_path = osp.join(data_root, class_name)
        fnames = [
            osp.join(class_name, fname) for fname in os.listdir(dir_path)

            if osp.splitext(fname)[1] in ['.jpeg', '.jpg']
        ]
        class2fnames[class_name] = fnames
        class2fnum[class_name] = len(fnames)

    sorted_class2fnum = sorted(class2fnum.items(),
                               key=lambda kv: kv[1],
                               reverse=True)

    label2fnames = dict()
    label2class = dict()

    for i, (class_name, fnum) in enumerate(sorted_class2fnum):
        print(f"{i:>2}: {class_name:>4} : {fnum:>5}")
        label2fnames[i] = class2fnames[class_name]
        label2class[i] = class_name

    return label2fnames, label2class


if __name__ == "__main__":
    root_dir = osp.expanduser("~/Datasets/ISIC2019/Data")
    label2fnames_path = osp.expanduser("~/Datasets/ISIC2019/label2fnames.yaml")
    label2class_path = osp.expanduser("~/Datasets/ISIC2019/label2class.yaml")

    label2fnames, label2class = fetch_filename_list(root_dir)

    print(f"Writing label2fnames into '{label2fnames_path}'...")
    with open(label2fnames_path, 'w') as f1:
        yaml.dump(
            label2fnames,
            f1,
            allow_unicode=True,
            default_flow_style=False,
        )

    print(f"Writing label2class into '{label2class_path}'...")
    with open(label2class_path, 'w') as f2:
        yaml.dump(
            label2class,
            f2,
            allow_unicode=True,
            default_flow_style=False,
        )
