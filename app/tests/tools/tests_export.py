import os.path

from tools.export import export_to_csv


def test_export_to_csv(clean_tmp_folder: None) -> None:
    file = export_to_csv(headers=["h1", "h2"], data=[{"h1": "test", "h2": "test"}])

    assert os.path.exists(file)
    with open(file) as f:
        assert f.read() == "h1;h2\ntest;test\n"
