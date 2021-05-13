def get_bottom_lvl_keys(d, keys, input_names):
    for k, v in d.items():
        if isinstance(v, dict):
            get_bottom_lvl_keys(v, [*keys, str(k)], input_names)
        else:
            input_names.append("_".join([*keys, str(k)]))
    return input_names
