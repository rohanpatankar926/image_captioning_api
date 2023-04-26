import boto3
from botocore.exceptions import NoCredentialsError,NoRegionError,DataNotFoundError
import os
import base64
from dotenv import load_dotenv
load_dotenv()
def available_objects():
    s3=boto3.resource("s3",aws_access_key_id="e203e5b14fda08deca1a9d65d1fb7c39",aws_secret_access_key="d8f4d62a7a73e8ade87b0971436c2b0a98c1f1565ab1dd6caf366a09cd465551")
    try:
        # my_bucket = s3.Bucket('imagetotext98866')
        # objects=[obj.key for obj in my_bucket.objects.all()]
        # return objects
        for bucket in s3.buckets.all():
            print(bucket.name)
    except Exception as e:
        print(e)
available_objects()