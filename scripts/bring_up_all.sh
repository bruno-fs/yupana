#!/bin/bash
set -x
export SCRIPT_HOME=$PWD/scripts
SESSION_NAME=yupana-stack

byobu new-session -d -s ${SESSION_NAME}
# upload-svc
byobu select-window -t ${SESSION_NAME}:0
byobu rename-window -t ${SESSION_NAME}:0 'ingress'
byobu send-keys "cd ${SCRIPT_HOME}" C-m
byobu send-keys "./bring_up_upload_svc.sh" C-m
${SCRIPT_HOME}/countdown.sh 'Waiting for ingress services to startup' 60 'Services are ready!'

# upload consumer
byobu new-window -t ${SESSION_NAME}:1 -n 'upload-consumer'
byobu send-keys "cd ${SCRIPT_HOME}" C-m
byobu send-keys "./bring_up_upload_consumer.sh" C-m

# test hi consumer
byobu new-window -t ${SESSION_NAME}:2 -n 'hi-consumer'
byobu send-keys "cd ${SCRIPT_HOME}" C-m
byobu send-keys "./bring_up_test_hi_consumer.sh" C-m

# yupana
byobu new-window -t ${SESSION_NAME}:3 -n 'yupana'
byobu send-keys "cd ${SCRIPT_HOME}" C-m
byobu send-keys "./bring_up_yupana.sh" C-m
${SCRIPT_HOME}/countdown.sh 'Waiting for host inventory db to be ready.' 15 'Services are ready!'

# host inventory
byobu new-window -t ${SESSION_NAME}:4 -n 'host-inventory-svc'
byobu send-keys "cd ${SCRIPT_HOME}" C-m
byobu send-keys "./bring_up_host_inventory_svc.sh" C-m
