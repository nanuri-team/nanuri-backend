from datetime import datetime
from decimal import Decimal

import boto3
from django.conf import settings


class GroupMessageTable:
    def __init__(self):
        self.resource = boto3.resource(
            'dynamodb',
            endpoint_url=settings.AWS_DYNAMODB_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_DYNAMODB_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_DYNAMODB_SECRET_ACCESS_KEY,
        )
        self.client = boto3.client(
            'dynamodb',
            endpoint_url=settings.AWS_DYNAMODB_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_DYNAMODB_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_DYNAMODB_SECRET_ACCESS_KEY,
        )
        self.table_name = 'group_message'

        if self.table_name not in self._list_tables():
            self._create_table()

    def _create_table(self):
        return self.resource.create_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'channel_id',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'message_id',
                    'AttributeType': 'N',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'channel_id',
                    'KeyType': 'HASH',
                },
                {
                    'AttributeName': 'message_id',
                    'KeyType': 'RANGE',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            },
            TableClass='STANDARD',
        )

    def _list_tables(self):
        tables = self.client.list_tables()
        return tables['TableNames']

    def insert_row(self, channel_id, message_to, message_from, message):
        table = self.resource.Table(self.table_name)
        now = datetime.utcnow()
        return table.put_item(
            Item={
                'channel_id': channel_id,
                'message_id': Decimal(now.timestamp()),
                'message_to': message_to,
                'message_from': message_from,
                'message': message,
                'created_at': now.strftime('%Y-%m-%d %H:%M:%S.%f'),
            }
        )


group_message_table = GroupMessageTable()
