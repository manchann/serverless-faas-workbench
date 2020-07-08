import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table('EFS')

scan = table.scan()
with table.batch_writer() as batch:
    for each in scan['Items']:
        batch.delete_item(Key={
            'id': each['id'],
            'type': each['type']
        })
