#!/bin/bash

# TO-DO(Eddie): replace this whole remote executing thing with some sort of python library such that we could write a configure file and don't have to hard code any shit
while read -r line
do
    array+=($line)
    done < api_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        current_path=$PWD
        launch_cmd="source ~/.bash_profile; nohup python /grad/users/cx28/scienceograhy/crawler/distributed_crawler/start_crawling_job.py > crawl_log &"
        # echo "cmd = $launch_cmd"
        ssh "${array[i]}" "$launch_cmd" 
    done

