python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
sleep 10

aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
sleep 40

python3 ./efs_scalablity/request1.py
sleep 15
python3 ./efs_scalablity/request10.py
sleep 20
python3 ./efs_scalablity/request20.py
sleep 20
python3 ./efs_scalablity/request50.py
sleep 50
python3 ./efs_scalablity/request100.py
sleep 100
python3 ./efs_scalablity/request200.py
sleep 100

aws lambda update-function-configuration --function-name efs-test --handler sequence.lambda_handler
sleep 60

python3 ./efs_scalablity/request1.py
sleep 15
python3 ./efs_scalablity/request10.py
sleep 20
python3 ./efs_scalablity/request20.py
sleep 20
python3 ./efs_scalablity/request50.py
sleep 50
python3 ./efs_scalablity/request100.py
sleep 100
python3 ./efs_scalablity/request200.py
sleep 100

aws lambda update-function-configuration --function-name efs-test --handler dd.lambda_handler
sleep 40

python3 ./efs_scalablity/request1.py
sleep 15
python3 ./efs_scalablity/request10.py
sleep 20
python3 ./efs_scalablity/request20.py
sleep 20
python3 ./efs_scalablity/request50.py
sleep 50
python3 ./efs_scalablity/request100.py
sleep 100
python3 ./efs_scalablity/request200.py
sleep 100
sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/efs-scalablity
