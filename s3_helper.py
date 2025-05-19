# recipe-app/s3_helper.py
import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='ap-northeast-1'
    )

def test_s3_connection():
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        return f"Connection successful. Found {len(response.get('Contents', []))} objects"
    except Exception as e:
        return f"Connection failed: {str(e)}"