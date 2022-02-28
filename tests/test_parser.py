import pytest

from src.document import generate_update_statement


@pytest.mark.parametrize(
    "input,output",
    [
        ({"posts": [{"_id": 2, "value": "too"}]}, {"$update": {"posts.0.value": "too"}}),
        ({"posts": [{"_id": 3, "mentions": [{"_id": 5, "text": "pear"}]}]}, {"$update": {"posts.1.mentions.0.text": "pear"}}),
        ({"posts": [{"_id": 2, "_delete": "true"}]}, {"$remove": {"posts.0": "true"}}),
        ({"posts": [{"_id": 3, "mentions": [{"_id": 6, "_delete": "true"}]}]}, {"$remove": {"posts.1.mentions.1": "true"}}),
        ({"posts": [{"value": "four"}]}, {"$add": {"posts": [{"value": "four"}]}}),
        ({"posts": [{"_id": 3, "mentions": [{"text": "banana"}]}]}, {"$add": {"posts.1.mentions": [{"text": "banana"}]}}),
        ({
            "posts": [
                {"_id": 2, "value": "too"},
                {"value": "four"},
                {"_id": 4, "_delete": "true"}
            ]
        }, {
            "$update": {"posts.0.value": "too"},
            "$add": {"posts": [{"value": "four"}]},
            "$remove": {"posts.2": "true"}
        })
    ]
)
def test_parse(sample_document, input, output):
    assert generate_update_statement(sample_document, input) == output
