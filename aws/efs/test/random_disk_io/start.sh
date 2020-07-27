python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py

aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random.lambda_handler

sleep 30
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 10

aws lambda update-function-configuration --function-name efs-test --handler sequence.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler sequence.lambda_handler

sleep 30
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sleep 120
python3 ./request.py
sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/disk_io_test
