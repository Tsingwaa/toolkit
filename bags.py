"""Bags of utility in the toolbox."""


def json_load(load_path, mode='r'):
    """Convenient json load tool"""
    import json
    with open(load_path, mode) as f:
        return json.load(f)


def json_dump(var, dump_path, mode='w', ensure_ascii=False):
    import json
    with open(dump_path, mode) as f:
        json.dump(var, f, ensure_ascii=ensure_ascii, indent=4)


def sort_dict(src_dict, sort_key='key', do_print=False):
    """Sort dict by value, save dict as OrderedDict.
    ARGS:
        src_dict(dict): source dictionary, build-in dict type without order.
        sort_key(str): 'key' or 'value'. Default: 'value'.
        do_print(bool): whether print the sorted ordered dict.

        return(OrderedDict): sorted ordered dict. 
    """
    import collections

    dict_sorted2list = sorted(src_dict.items(), key=lambda kv: (kv[1], kv[0]))
    sorted_ordered_dict = collections.OrderedDict(dict_sorted2list)

    if do_print:
        print(sorted_ordered_dict)

    return sorted_ordered_dict
