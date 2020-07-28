python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py

aws lambda update-function-configuration --function-name efs-test --handler random-write.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random-write.lambda_handler

sleep 40
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60

aws lambda update-function-configuration --function-name efs-test --handler sequence-write.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler sequence-write.lambda_handler

sleep 40
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60
python3 ./request.py
sleep 60

aws lambda update-function-configuration --function-name efs-test --handler random-read.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random-read.lambda_handler

sleep 40
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60

aws lambda update-function-configuration --function-name efs-test --handler sequence-read.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler sequence-read.lambda_handler

sleep 40
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60
aws lambda update-function-configuration --function-name efs-test --memory-size 256
aws lambda update-function-configuration --function-name tmp-test --memory-size 256
sleep 5
aws lambda update-function-configuration --function-name efs-test --memory-size 512
aws lambda update-function-configuration --function-name tmp-test --memory-size 512
sleep 30
python3 ./request.py
sleep 60

sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/file_rw_test
