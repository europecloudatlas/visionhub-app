"""
S3/MinIO storage utilities
"""
import os
import uuid
from botocore.exceptions import ClientError
import boto3
from botocore.client import Config

from .config import get_settings

settings = get_settings()

# S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)


def ensure_bucket_exists():
    """Create S3 bucket if it doesn't exist"""
    try:
        s3_client.head_bucket(Bucket=settings.s3_bucket)
        print(f"✅ S3 bucket '{settings.s3_bucket}' exists")
    except ClientError:
        try:
            s3_client.create_bucket(Bucket=settings.s3_bucket)
            print(f"✅ Created S3 bucket '{settings.s3_bucket}'")
        except ClientError as e:
            print(f"❌ Failed to create bucket: {e}")
            raise


def upload_image(file, original_filename: str) -> tuple:
    """
    Upload image to S3/MinIO
    
    Args:
        file: File object (from UploadFile.file)
        original_filename: Original filename
    
    Returns:
        (image_url, stored_filename)
    """
    # Generate unique filename
    ext = os.path.splitext(original_filename)[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    
    try:
        # Determine content type
        content_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        content_type = content_type_map.get(ext, 'image/jpeg')
        
        # Upload to S3
        s3_client.upload_fileobj(
            file,
            settings.s3_bucket,
            filename,
            ExtraArgs={
                'ContentType': content_type,
                'ACL': 'public-read'
            }
        )
        
        # Generate public URL
        image_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{filename}"
        
        print(f"✅ Uploaded image: {filename}")
        return image_url, filename
    
    except ClientError as e:
        print(f"❌ S3 upload failed: {e}")
        raise


def delete_image(filename: str):
    """
    Delete image from S3/MinIO
    
    Args:
        filename: Filename to delete
    """
    try:
        s3_client.delete_object(Bucket=settings.s3_bucket, Key=filename)
        print(f"✅ Deleted image: {filename}")
    except ClientError as e:
        print(f"⚠️ Failed to delete image: {e}")
        # Don't raise - deletion failure shouldn't break the flow