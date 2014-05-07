#!/bin/bash

while read -r line
do
    array+=($line)
    done < api_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        echo "${array[i]}"
        current_path=$PWD
        echo "current path = $current_path"
        launch_cmd="source ~/.bash_profile; nohup python /grad/users/cx28/scienceograhy/crawlers/run_worker.py > /.freespace/cx28/logs < /dev/null 2>&1 &"
        echo "cmd = $launch_cmd"
        ssh "${array[i]}" "$launch_cmd" 
    done