from enum import Enum
from typing import Any


class Actions(str, Enum):
    ADD = "$add"
    UPDATE = "$update"
    REMOVE = "$remove"


ID = "_id"
SUB_DOCS = ["mentions", "posts"]


def find_index(
    document: dict[str, Any], path: list[str], doc: dict[str, Any]
) -> int:
    """Find a document position give its current path"""
    if len(path) == 0:
        for idx, item in enumerate(document):
            if ID not in doc:
                return -1
            if doc[ID] == item[ID]:
                return idx
    _p = int(path[0]) if path[0].isnumeric() else path[0]
    return find_index(document[_p], path[1:], doc)


def search(
    document: dict[str, Any], node: dict[str, Any], path: list[str]
) -> list[str]:
    """Search document recursively to determine action"""
    if ID in node:
        idx = find_index(document, path, node)
        path.append(str(idx))

    if isinstance(node, dict) and (
        "value" in node or "text" in node or "_delete" in node
    ):
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
        return path

    for k, v in node.items():
        if k in SUB_DOCS:
            path.append(k)
        if isinstance(v, list):
            search(document, v[0], path)
    return path


def generate_update_statement(
    document: dict[str, Any], input: dict[str, Any]
) -> dict[str, dict[str, str]]:
    """generate update statement for given edit actions"""
    result = {}

    for k, cmds in input.items():
        for cmd in cmds:
            path = search(document, cmd, [k])
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
