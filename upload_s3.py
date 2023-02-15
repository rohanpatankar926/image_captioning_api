import boto3
from botocore.exceptions import NoCredentialsError,NoRegionError,DataNotFoundError
import os
import base64
from dotenv import load_dotenv
load_dotenv()
def upload_img_s3(uploaded,s3_upload):
    s3=boto3.resource("s3",aws_access_key_id=os.getenv("ACCESS_KEY"),aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    print(s3)
    try:
        with open(uploaded, 'rb') as f:
            encoded_image = base64.b64encode(f.read())
        s3.Bucket(os.getenv("BUCKET_NAME")).put_object(Key=s3_upload,Body=encoded_image)
        print("uploaded to s3")
        return True
    except Exception as e:
        print(e)


upload_img_s3("image/images.jpg","imageas.jpg")