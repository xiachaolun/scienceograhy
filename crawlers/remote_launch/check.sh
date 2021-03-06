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
        launch_cmd="source ~/.bash_profile; nohup python /grad/users/cx28/scienceograhy/crawlers/remote_launch/maintain_worker.py > /.freespace/citybeat_logs/sci.txt < /dev/null 2>&1 &"
        echo "cmd = $launch_cmd"
        ssh "${array[i]}" "$launch_cmd"
    done