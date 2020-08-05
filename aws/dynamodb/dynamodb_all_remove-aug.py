import boto3

table_name = 'aug2'
region_name = 'ap-northeast-2'
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)

scan = table.scan()
with table.batch_writer() as batch:
    for each in scan['Items']:
        batch.delete_item(Key={
            'id': each['id'],
            'type': each['type']
        })
