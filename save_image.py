from fastapi import UploadFile
import uuid


async def save(file: UploadFile, path):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    file_path = f"{path}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(contents)
    return file_path
