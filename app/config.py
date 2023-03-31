from pydantic import BaseSettings


class Settings(BaseSettings):

    MAX_WORKERS = 4
    CHUNK_SIZE = 1024 * 1024
    AWS_ACCESS_KEY_ID: str = 'AKIAXTD25Q6VOFW55JJZ'
    AWS_SECRET_KEY: str = '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'
    AWS_S3_BUCKET_NAME: str = 'bauka'
    AWS_S3_REGION_NAME: str = 'eu-west-2'
    AWS_S3_URL_PROTOCOL: str = 'http'

    class Config:
        case_sensitive = True


settings = Settings()
