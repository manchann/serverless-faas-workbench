aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random.lambda_handler

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
aws lambda update-function-configuration --function-name tmp-test --handler sequence.lambda_handler

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
aws lambda update-function-configuration --function-name tmp-test --handler dd.lambda_handler

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
