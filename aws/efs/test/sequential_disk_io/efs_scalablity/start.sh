aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random.lambda_handler

python3 ./request1.py
sleep 120
python3 ./request10.py
sleep 120
python3 ./request20.py
sleep 120
python3 ./request50.py
sleep 120
python3 ./request100.py
sleep 120
python3 ./request200.py

aws lambda update-function-configuration --function-name efs-test --handler sequence.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler sequence.lambda_handler

python3 ./request1.py
sleep 120
python3 ./request10.py
sleep 120
python3 ./request20.py
sleep 120
python3 ./request50.py
sleep 120
python3 ./request100.py
sleep 120
python3 ./request200.py

aws lambda update-function-configuration --function-name efs-test --handler dd.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler dd.lambda_handler

python3 ./request1.py
sleep 120
python3 ./request10.py
sleep 120
python3 ./request20.py
sleep 120
python3 ./request50.py
sleep 120
python3 ./request100.py
sleep 120
python3 ./request200.py