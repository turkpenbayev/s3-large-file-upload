from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, UploadFile
from app.config import settings

app = FastAPI()

s3 = boto3.client(
    service_name='s3',
    region_name=settings.AWS_S3_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    chunk_count = 0
    try:
        while True:
            chunk = file.file.read(settings.SHUNK_SIZE)
            if not chunk:
                break
            chunk_count += 1
            s3.upload_fileobj(
                BytesIO(chunk),
                settings.AWS_S3_BUCKET_NAME,
                f"{file.filename}.part{chunk_count}"
            )
    except ClientError as e:
        return {"success": False}
    return {"success": True}
