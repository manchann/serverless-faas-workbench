#!/bin/bash

#lambda_functions="random-read random-write sequence-read sequence-write dd"
concurrency="1 10 20 50 100 200"
newline=$'\n'
count="200"
bs="1024"
test="test1"
for es in $concurrency; do
  echo $newline'---------------' $es '개 진행중 -----------------'$newline
  loop=$(seq 1 $es)
  for l in $loop; do
    curl 'https://jgfunc.azurewebsites.net/api/HttpExample/'$bs'/'$count'/'$es'/'$test'?code=tRkE7ZKLwuOWlB4/MDIkfh8a/lblE/fBpHZ1Tpkd6FRPYGfVHwcWsA==' &
  done
  sleep 30
done

exit
