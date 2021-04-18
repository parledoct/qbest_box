from flask import g

from minio import Minio
from minio.error import S3Error

def get_client():
    client = getattr(g, '_minio', None)
    if client is None:
        client = g._minio = Minio(
            # Use 127.0.0.1:9000 if you have launched manually
            # network name 'minio' is available only when
            # you use docker-compose up (see docker-compose.yml)
            "minio:9000",
            access_key="minio",
            secret_key="minio123",
            secure=False
        )

        # Make buckets if they don't exist.
        [ client.make_bucket(b) for b in ["audio", "features"] if not client.bucket_exists(b) ]

    return client

def upload_file(bucket, path, data, size):
    client = get_client()

    client.put_object(bucket, path, data, size)
