import pytest
from bug3_logic import find_max


@pytest.mark.parametrize("scores, expected", [
    ([95, 70, 60], 95),
    ([70, 95, 60], 95),
    ([70, 85, 60, 95], 95),
    ([-8, -2, -5], -2),
])
def test_maximum(scores, expected):
    assert find_max(scores) == expected


def test_single_score():
    assert find_max([42]) == 42


def test_empty_list():
    with pytest.raises(IndexError):
        find_max([])