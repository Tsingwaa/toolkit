#!/usr/bin/env python
# coding=utf-8

def redesign_ctg(confuse_ctgs_list_fpath, redesign_ctg_map_fpath):
    """Redesign categories, mainly merge category
    Args:
        confuse_ctgs_list_fpath(str): save a dict(e.g. 'cm0.1_iou0.6':[[ctg1,ctg2], [ctg3,ctg4,ctg5]])
        redesign_ctg_map_fpath(str): to save a dict('old_ctg':'new_ctg')
    """
    import json

    confuse_ctgs_list = []
    high_iou_misclsf_rate = 0.
    with open(confuse_ctgs_list_fpath, 'r') as f_1:
        d = json.load(f_1) 
        for key, value in d.items():
            if 'high_iou' in key:
                high_iou_misclsf_rate = value
            else:
                confuse_ctgs_list = value

    ctg_map = dict()
    
    for confuse_ctgs in confuse_ctgs_list:
        
        


