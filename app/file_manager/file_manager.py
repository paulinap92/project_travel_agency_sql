import os

class FileManager:
    """A dynamic file manager that supports operations such as reading, writing, and deleting files.

    Attributes:
        operations (list[str]): List of operations to dynamically create methods for. Supported operations: 'read', 'write', 'delete'.
    """

    def __init__(self, operations: list[str]) -> None:
        """Initializes the FileManager and dynamically creates methods based on the provided operations.

        Args:
            operations (list[str]): List of operations to support ('read', 'write', 'delete').

        Raises:
            ValueError: If an unsupported operation is provided.
        """
        for operation in operations:
            method_name = f"{operation}_file"
            method = self._create_file_method(operation)
            setattr(self, method_name, method)

    @staticmethod
    def _create_file_method(operation: str):
        """Creates a file operation method dynamically based on the operation type.

        Args:
            operation (str): The file operation to create ('read', 'write', 'delete').

        Returns:
            function: A method corresponding to the operation.

        Raises:
            ValueError: If an unsupported operation is provided.
        """
        match operation:
            case "write":
                def method(file_path: str, data: str):
                    """Writes data to a file.

                    Args:
                        file_path (str): Path to the file to write to.
                        data (str): The data to write to the file.

                    Raises:
                        IOError: If writing to the file fails.
                    """
                    try:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(data)
                    except Exception as e:
                        raise IOError(f"Failed to write to file: {file_path}. Error: {e}")

            case "read":
                def method(file_path: str):
                    """Reads lines from a file.

                    Args:
                        file_path (str): Path to the file to read from.

                    Returns:
                        list[str]: A list of lines from the file.

                    Raises:
                        FileNotFoundError: If the file does not exist.
                        IOError: If reading the file fails.
                    """
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(f"File not found: {file_path}")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            return [line.rstrip('\n') for line in f]
                    except Exception as e:
                        raise IOError(f"Failed to read file: {file_path}. Error: {e}")

            case "delete":
                def method(file_path: str):
                    """Deletes a file.

                    Args:
                        file_path (str): Path to the file to delete.

                    Raises:
                        FileNotFoundError: If the file does not exist.
                        IOError: If deleting the file fails.
                    """
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(f"File not found: {file_path}")
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        raise IOError(f"Failed to delete file: {file_path}. Error: {e}")

            case _:
                raise ValueError(f"Unsupported operation: {operation}")

        method.__name__ = operation
        return method
