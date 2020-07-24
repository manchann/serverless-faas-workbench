aws lambda update-function-configuration --function-name efs-test --handler random.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler random.lambda_handler

sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5

aws lambda update-function-configuration --function-name efs-test --handler sequence.lambda_handler
aws lambda update-function-configuration --function-name tmp-test --handler sequence.lambda_handler

sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
sleep 5
python3 ./request.py
