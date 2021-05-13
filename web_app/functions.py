def get_bottom_lvl_keys(d, keys, input_names):
    for k, v in d.items():
        if isinstance(v, dict):
            get_bottom_lvl_keys(v, [*keys, str(k)], input_names)
        else:
            input_names.append("-".join([*keys, str(k)]))
    return input_names


def unflatten_dict(d):
    n_d = {}
    for k, v in d.items():
        split_key(k, v, n_d)
    return n_d


def split_key(k, v, n_d):
    k, *k_rest = k.split("-", 1)
    if k_rest:
        split_key(k_rest[0], v, n_d.setdefault(k, {}))
    else:
        n_d[k] = v
