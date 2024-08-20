import pytest
from pull_requests import sort_files

# Fixture to generate test data
@pytest.fixture
def files():
    return [
        {"filename": "file3.txt"},
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
        {"filename": "file4.txt"},
    ]

# Normal Cases
def test_sort_files_empty_list():
    assert sort_files([]) == []

def test_sort_files_single_file():
    assert sort_files([{"filename": "file1.txt"}]) == [{"filename": "file1.txt"}]

def test_sort_files_multiple_files(files):
    expected_output = [
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
        {"filename": "file3.txt"},
        {"filename": "file4.txt"},
    ]
    assert sort_files(files) == expected_output

# Edge Cases
def test_sort_files_identical_filenames():
    files = [
        {"filename": "file1.txt"},
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
    ]
    expected_output = [
        {"filename": "file1.txt"},
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
    ]
    assert sort_files(files) == expected_output

def test_sort_files_case_insensitive():
    files = [
        {"filename": "File1.txt"},
        {"filename": "file2.txt"},
        {"filename": "FILE3.txt"},
    ]
    expected_output = [
        {"filename": "FILE3.txt"},
        {"filename": "File1.txt"},
        {"filename": "file2.txt"},
    ]
    assert sort_files(files) == expected_output

# Error Handling
def test_sort_files_non_list_argument():
    with pytest.raises(TypeError):
        sort_files(123)

@pytest.mark.parametrize("invalid_input", [
    [1, 2, 3],
    ["file1.txt", "file2.txt"],
    [{"filename": "file1.txt"}, "file2.txt"],
])
def test_sort_files_invalid_elements(invalid_input):
    with pytest.raises(TypeError):
        sort_files(invalid_input)

# Boundary Conditions
def test_sort_files_max_files():
    files = [{"filename": f"file{i}.txt"} for i in range(1000)]
    sorted_files = sort_files(files)
    assert len(sorted_files) == 1000
    for i in range(len(sorted_files) - 1):
        assert sorted_files[i]["filename"] <= sorted_files[i + 1]["filename"]

def test_sort_files_min_max_filenames():
    files = [
        {"filename": ""},
        {"filename": "a" * 255},
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
    ]
    expected_output = [
        {"filename": ""},
        {"filename": "a" * 255},
        {"filename": "file1.txt"},
        {"filename": "file2.txt"},
    ]
    assert sort_files(files) == expected_output