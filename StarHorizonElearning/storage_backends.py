from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    aws_access_key_id= settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY
