#efs export json format

table_name=$1
file_name=$2
aws dynamodb scan --table-name ${table_name} --region ap-northeast-2 \
  --output json >${file_name}.json
