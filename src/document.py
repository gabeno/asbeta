from enum import Enum
from typing import Any


class Actions(str, Enum):
    ADD = "$add"
    UPDATE = "$update"
    REMOVE = "$remove"


ID = "_id"
SUB_DOCS = ["mentions", "posts"]
FIELDS = ["value", "text"]


def find_index(document, path, doc):
    if len(path) == 0:
        for idx, item in enumerate(document):
            if ID not in doc:
                return -1
            if doc["_id"] == item["_id"]:
                return idx
    _p = int(path[0]) if path[0].isnumeric() else path[0]
    return find_index(document[_p], path[1:], doc)


def search(document, node, path):
    if isinstance(node, dict) and ("value" in node or "text" in node or "_delete" in node):
        if "value" in node:
            if ID in node:
                path.append(f"{Actions.UPDATE}:value:{node['value']}")
            else:
                path.append(f"{Actions.ADD}:value:{node['value']}")
        if "text" in node:
            if ID in node:
                path.append(f"{Actions.UPDATE}:text:{node['text']}")
            else:
                path.append(f"{Actions.ADD}:text:{node['text']}")
        if "_delete" in node:
            path.append(f"{Actions.REMOVE}::true")
        return
    for k, v in node.items():
        if k in SUB_DOCS:
            path.append(k)
        if isinstance(v, list):
            idx = find_index(document, path, v[0])
            if idx >= 0:
                path.append(str(idx))
            search(document, v[0], path)

    return path


def generate_update_statement(document: dict[str, Any], input: dict[str, Any]):
    result = {}

    for cmd in input["posts"]:
        path = search(document, {"posts": [cmd]}, [])
        action, field, value = path[-1].split(":")

        if action == Actions.UPDATE:
            full_path = ".".join(path[:-1] + [field])
            result.update({action: {full_path: value}})
        elif action == Actions.REMOVE:
            full_path = ".".join(path[:-1])
            result.update({action: {full_path: value}})
        elif action == Actions.ADD:
            full_path = ".".join(path[:-1])
            result.update({action: {full_path: [{field: value}]}})
    return result
