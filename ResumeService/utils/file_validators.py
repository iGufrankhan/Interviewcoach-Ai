import os
from utils import apierror, apiresponse




def validate_file_extension(filename: str) -> bool:
    """
    Validates the file extension against a list of allowed extensions.

    Args:
        filename (str): The name of the file to validate.

    Returns:
        bool: True if the file extension is valid, False otherwise.
    """
    
    allowed_extensions = ['pdf', 'docx', 'txt']
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions





def validate_file_size(file_path: str) -> bool:
    """
    Validates the file size against a maximum size limit.

    Args:
        file_path (str): The path to the file to validate.

    Returns:
        bool: True if the file size is within the limit, False otherwise.
    """
    max_size_mb = 5  

    if not os.path.isfile(file_path):
        return False

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    return file_size_mb <= max_size_mb  


def validate_not_empty(file_path: str) -> bool:
    """
    Validates that the file is not empty.

    Args:
        file_path (str): The path to the file to validate.
    Returns:
        bool: True if the file is not empty, False otherwise.
    """
    if not os.path.isfile(file_path):
        return False

    return os.path.getsize(file_path) > 0




