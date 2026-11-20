import pytest
from load_scores import load_scores


def read_csv(tmp_path, rows):
    path = tmp_path / "scores.csv"
    path.write_text("name,score\n" + rows, encoding="utf-8-sig")
    return load_scores(path)


def test_names_and_boundaries(tmp_path):
    rows = ' 민지 ,0\n\n"김,하나",70\n민지,100\n'
    kept, skipped = read_csv(tmp_path, rows)
    assert kept == [("민지", 0), ("김,하나", 70), ("민지", 100)]
    assert skipped == []


@pytest.mark.parametrize("row, reason", [
    ("민지,10,추가", "열 개수가 2가 아님"),
    (",50", "이름이 비어 있음"),
    ("민지,", "점수가 비어 있음"),
    ("민지,88.5", "점수가 정수가 아님"),
    ("민지,-1", "점수가 0~100 밖"),
    ("민지,101", "점수가 0~100 밖"),
])
def test_invalid_row_is_recorded(tmp_path, row, reason):
    kept, skipped = read_csv(tmp_path, row + "\n하나,80\n")
    assert kept == [("하나", 80)]
    assert skipped == [(2, row, reason)]


def test_header_only(tmp_path):
    assert read_csv(tmp_path, "") == ([], [])


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")