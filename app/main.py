from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor
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
    futures = []
    try:
        with ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            while True:
                chunk = file.file.read(settings.CHUNK_SIZE)
                if not chunk:
                    break
                future = executor.submit(upload_chunk_to_s3, chunk, file.filename, len(futures) + 1)
                futures.append(future)
        for future in futures:
            future.result()
    except ClientError as e:
        return {"success": False}
    return {"success": True}


def upload_chunk_to_s3(chunk, filename, chunk_number):
    key = f"{filename}.part{chunk_number}"
    s3.upload_fileobj(BytesIO(chunk), settings.AWS_S3_BUCKET_NAME, key)
