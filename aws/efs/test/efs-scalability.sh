#remove dynamodb datas
python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
sleep 10
#change lambda_function sequence -> random
aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
sleep 40

#start random access work
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

#change lambda_function random -> sequence
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

#change lambda_function sequence -> dd
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

#export dynamodb data to local json file
sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/efs-scalablity
