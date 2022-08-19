#!/bin/bash

# .env -> AWS_S3_CERTIFICATE_BUCKET_NAME
# .env -> AWS_S3_CERTIFICATE_KEY
awslocal s3api create-bucket --bucket nanuri-secret-bucket
wget https://github.com/aryansbtloe/resources/raw/master/Certificate/certificate.p12 -O /tmp/certificate.p12
awslocal s3api put-object --bucket nanuri-secret-bucket --key certificate.p12 --body /tmp/certificate.p12
