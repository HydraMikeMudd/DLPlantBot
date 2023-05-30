import io
import uuid

def load_image_path(filepath: str) -> io.BytesIO:
    """Loads an image from a filepath into a BytesIO object.

    Args:
        filepath (str): The filepath to the image.

    Returns:
        io.BytesIO: The image as a BytesIO object.
    """
    with open(filepath, "rb") as f:
        data = f.read()
    return io.BytesIO(data)


def write_image_path(filepath: str, data: io.BytesIO) -> str:
    """Writes an image from a BytesIO object to a filepath.

    Args:
        filepath (str): The filepath to write the image to.
        data (io.BytesIO): The image as a BytesIO object.
    """
    if filepath is None:
        filename = str(uuid.uuid4())
        filepath = f"res/{filename}.png"
    
    data.seek(0)
    with open(filepath, "wb") as f:
        f.write(data.read())
    
    return filepath