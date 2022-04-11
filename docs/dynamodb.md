## Create table

### group message

```shell
$ aws dynamodb create-table \
    --table-name group_message \
    --attribute-definitions \
        AttributeName=channel_id,AttributeType=S \
        AttributeName=message_id,AttributeType=N \
    --key-schema \
        AttributeName=channel_id,KeyType=HASH \
        AttributeName=message_id,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --table-class STANDARD \
    --endpoint-url http://localhost:8000
```

## List table

```shell
$ aws dynamodb list-tables --endpoint-url http://localhost:8000
```


## Delete table

```shell
$ aws dynamodb delete-table --table-name group_message --endpoint-url http://localhost:8000
```
