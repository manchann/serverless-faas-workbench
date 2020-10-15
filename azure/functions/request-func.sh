#!/bin/bash

#lambda_functions="random-read random-write sequence-read sequence-write dd"
concurrency="200 100 50 20 10 1"
newline=$'\n'
count="200"
bs="1024"
test="dedicated_test-1"

jgfunc_url=('https://jgfunc.azurewebsites.net/api/HttpExample/' '?code=tRkE7ZKLwuOWlB4/MDIkfh8a/lblE/fBpHZ1Tpkd6FRPYGfVHwcWsA==')
dedicated_function_url=('https://dedicated-plan-test.azurewebsites.net/api/HttpExample/' '?code=P1TpmaR/iH/t1b0sbyIMFgABnBWhctA4ktX20vf6EvBpnkBVRZ/TYA==')

for es in $concurrency; do
  echo $newline'---------------' $es '개 진행중 -----------------'$newline
  loop=$(seq 1 $es)
  for l in $loop; do
    curl ${dedicated_function_url[0]}$bs'/'$count'/'$es'/'$test${dedicated_function_url[1]} &
  done
  sleep 40
done

exit
