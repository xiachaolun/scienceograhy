
while read -r line
do
    array+=($line)
    done < api_host.txt
    for ((i=0; i < ${#array[*]}; i++))
    do
        echo "${array[i]}"
            # pkill -9 -f kills a job with partial name. So *make sure* that the name here is what you want to kill
            ssh "${array[i]}" "pkill -9 -f '/grad/users/cx28/scienceograhy/crawlers/run_worker.py'"
done