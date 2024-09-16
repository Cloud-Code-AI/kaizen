def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def set_nested(data, keys, value):
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value
