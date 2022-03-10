import collections

# Python2/Python3 support
try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in list(overrides.items()):
        if isinstance(value, collectionsAbc.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]

    return source