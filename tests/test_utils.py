import pytest

from onstrodb.core.utils import generate_hash_id


@pytest.mark.parametrize(
    "test_input,output",
    [
        (["Hello", "World"], "872e4e50"),
        (["ad", "4", "high school"], "1199e3f8"),
        (["python", "test", "param", "3"], "411996b0")
    ]
)
def test_generate_hash_id(test_input, output):
    assert generate_hash_id(test_input) == output
