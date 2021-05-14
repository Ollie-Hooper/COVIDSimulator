def get_bottom_lvl_keys(d, keys, input_names):
    """Recursive function to return a flat dictionary"""
    for k, v in d.items():
        if isinstance(v, dict):
            get_bottom_lvl_keys(v, [*keys, str(k)], input_names)
        else:
            input_names.append("-".join([*keys, str(k)]))
    return input_names


def unflatten_dict(d):
    """Function to unflatten kwargs dictionary, works in unison with split_key"""
    nested_d = {}
    for k, v in d.items():
        split_key(k, v, nested_d)
    return nested_d


def split_key(k, v, nested_d):
    """Function to unflatten kwargs dictionary, works in unison with unflatten_dict"""
    k, *k_rest = k.split("-", 1)
    if k_rest:
        split_key(k_rest[0], v, nested_d.setdefault(k, {}))
    else:
        nested_d[k] = v


def parse_measures(kwargs):
    """Function which parses the measures inputs into a properly formatted dictionary"""
    for measure, values in kwargs["measures"].items():
        if values["enabled"]:
            kwargs["measures"][measure]["starts"] = eval(f"[{kwargs['measures'][measure]['starts']}]")
            kwargs["measures"][measure]["ends"] = eval(f"[{kwargs['measures'][measure]['ends']}]")
        else:
            kwargs["measures"][measure]["starts"] = []
            kwargs["measures"][measure]["ends"] = []
        del kwargs["measures"][measure]["enabled"]
    return kwargs
