import os
import pytest
from app.file_manager.file_manager import FileManager

@pytest.fixture
def file_path(tmp_path):
    return tmp_path / "test_file.txt"

@pytest.fixture
def file_manager():
    return FileManager(operations=["write", "read", "delete"])

def test_write_file(file_manager, file_path):
    file_manager.write_file(file_path, "Test data")
    assert file_path.exists()
    assert file_path.read_text() == "Test data"

def test_read_file(file_manager, file_path):
    file_path.write_text("Line 1\nLine 2\n")
    result = file_manager.read_file(file_path)
    assert result == ["Line 1", "Line 2"]

def test_delete_file(file_manager, file_path):
    file_path.write_text("Test data")
    assert file_path.exists()
    file_manager.delete_file(file_path)
    assert not file_path.exists()

def test_write_file_error(file_manager, tmp_path):
    invalid_path = tmp_path / "non_existent_dir" / "file.txt"
    with pytest.raises(IOError, match="Failed to write to file"):
        file_manager.write_file(invalid_path, "Test data")

def test_read_file_not_found(file_manager):
    with pytest.raises(FileNotFoundError, match="File not found"):
        file_manager.read_file("non_existent_file.txt")

def test_delete_file_not_found(file_manager):
    with pytest.raises(FileNotFoundError, match="File not found"):
        file_manager.delete_file("non_existent_file.txt")

def test_unsupported_operation():
    with pytest.raises(ValueError, match="Unsupported operation"):
        FileManager(operations=["unsupported"])