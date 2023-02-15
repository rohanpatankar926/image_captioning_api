import boto3
from botocore.exceptions import NoCredentialsError,NoRegionError,DataNotFoundError
import os
import base64
from dotenv import load_dotenv
load_dotenv()
def available_objects():
    s3=boto3.resource("s3",aws_access_key_id=os.getenv("ACCESS_KEY"),aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    try:
        my_bucket = s3.Bucket('imagetotext98866')
        objects=[obj.key for obj in my_bucket.objects.all()]
        return objects
    except Exception as e:
        print(e)
available_objects()