#!/bin/bash

while read -r line
do
    array+=($line)
    done < api_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        launch_cmd="source ~/.bash_profile; nohup python /grad/users/cx28/scienceograhy/crawlers/run_worker.py < /dev/null 2>&1 &"
        ssh "${array[i]}" "$launch_cmd"
    done