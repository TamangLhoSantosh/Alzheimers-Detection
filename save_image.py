from fastapi import UploadFile  # To handle file uploads
import uuid


async def save(file: UploadFile, path):
    """
    Save an uploaded file to the specified path with a unique filename.

    Parameters:
    - file (UploadFile): The file object received from the client.
    - path (str): The directory path where the file will be saved.

    Returns:
    - str: The complete file path where the file is saved.
    """

    # Generate a unique filename using uuid and set the file extension to .jpg
    file.filename = f"{uuid.uuid4()}.jpg"

    # Read the contents of the uploaded file asynchronously
    contents = await file.read()

    # Construct the full path where the file will be saved
    file_path = f"{path}/{file.filename}"

    # Open the file in write-binary mode and save the contents
    with open(file_path, "wb") as f:
        f.write(contents)  # Write the contents to the file

    # Return the path where the file has been saved
    return file_path
