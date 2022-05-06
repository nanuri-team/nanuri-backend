from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    location = 'static'


class MediaStorage(S3Boto3Storage):
    querystring_auth = False
    location = 'media'
