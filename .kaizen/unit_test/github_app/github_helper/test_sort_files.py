import pytest

def sort_files(files):
    sorted_files = []
    for file in files:
        min_index = len(sorted_files)
        file_name = file["filename"]
        for i, sorted_file in enumerate(sorted_files):
            if file_name < sorted_file["filename"]:
                min_index = i
                break
        sorted_files.insert(min_index, file)
    return sorted_files

@pytest.mark.parametrize("input_files, expected_output", [
    # Normal Cases
    ([{"filename": "file3.txt"}, {"filename": "file1.txt"}, {"filename": "file2.txt"}],
     [{"filename": "file1.txt"}, {"filename": "file2.txt"}, {"filename": "file3.txt"}]),
    
    ([{"filename": "file2.txt"}, {"filename": "file1.txt"}, {"filename": "file2.txt"}],
     [{"filename": "file1.txt"}, {"filename": "file2.txt"}, {"filename": "file2.txt"}]),
    
    ([{"filename": "file1.txt"}],
     [{"filename": "file1.txt"}]),
    
    ([{"filename": "file1.txt"}, {"filename": "file2.txt"}, {"filename": "file3.txt"}],
     [{"filename": "file1.txt"}, {"filename": "file2.txt"}, {"filename": "file3.txt"}]),
    
    # Edge Cases
    ([],
     []),
    
    ([{"filename": "file.txt"}, {"filename": "file.txt"}, {"filename": "file.txt"}],
     [{"filename": "file.txt"}, {"filename": "file.txt"}, {"filename": "file.txt"}]),
    
    ([{"filename": "File.txt"}, {"filename": "file.txt"}, {"filename": "FILE.txt"}],
     [{"filename": "FILE.txt"}, {"filename": "File.txt"}, {"filename": "file.txt"}]),
    
    # Error Handling
    ([{"filename": 123}, {"filename": "file1.txt"}],
     [{"filename": 123}, {"filename": "file1.txt"}]),  # Assuming non-string filenames are sorted as is
    
    ([{"name": "file1.txt"}, {"filename": "file2.txt"}],
     [{"filename": "file2.txt"}]),  # Assuming missing 'filename' key files are ignored
    
    # Boundary Conditions
    ([{"filename": "a" * 1000}, {"filename": "b" * 1000}],
     [{"filename": "a" * 1000}, {"filename": "b" * 1000}]),
    
    ([{"filename": "file@!.txt"}, {"filename": "file#.txt"}, {"filename": "file$.txt"}],
     [{"filename": "file#.txt"}, {"filename": "file$.txt"}, {"filename": "file@!.txt"}])
])
def test_sort_files(input_files, expected_output):
    assert sort_files(input_files) == expected_output

def test_large_list_performance():
    large_list = [{"filename": f"file{i}.txt"} for i in range(1000, 0, -1)]
    sorted_large_list = [{"filename": f"file{i}.txt"} for i in range(1, 1001)]
    assert sort_files(large_list) == sorted_large_list

if __name__ == "__main__":
    pytest.main()