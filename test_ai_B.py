import pytest
from load_scores import load_scores


def write_csv(tmp_path, text):
    path = tmp_path / "scores.csv"
    path.write_text(text, encoding="utf-8-sig")
    return path


def test_valid_scores(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"김,하나", 0 \n 민지 ,100\n')
    kept, notes = load_scores(path)
    assert kept == [("김,하나", 0), ("민지", 100)]
    assert notes == []


@pytest.mark.parametrize("row", [
    "민지,-1", "민지,101", "민지,88.5", "민지,", ",70", "민지,80,추가",
])
def test_invalid_row(tmp_path, row):
    path = write_csv(tmp_path, f"name,score\n{row}\n하나,80\n")
    kept, notes = load_scores(path)
    assert kept == [("하나", 80)]
    assert len(notes) == 1
    assert notes[0][0] == 2
    assert notes[0][-1]


def test_duplicate_is_reported(tmp_path):
    path = write_csv(tmp_path, "name,score\n민지,70\n민지,90\n")
    kept, notes = load_scores(path)
    assert kept == [("민지", 70), ("민지", 90)]
    assert any(note[0] == 3 for note in notes)


def test_wrong_header(tmp_path):
    path = write_csv(tmp_path, "name,age\n민지,20\n")
    with pytest.raises(ValueError):
        load_scores(path)


def test_header_only(tmp_path):
    path = write_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


def test_missing_file(tmp_path):
    path = tmp_path / "missing.csv"
    with pytest.raises(FileNotFoundError) as error:
        load_scores(path)
    assert str(path) in str(error.value)