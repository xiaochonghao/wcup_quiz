#!/usr/bin/env bash
dev_mode=test

if [ $# -ge 1 ]; then
    if [ $1 != 'pro' ] && [ $1 != 'test' ]; then
        echo 'usage: sh run_clear_match_result.sh [pro|test]'
        exit
    fi
    if [ $1 == 'pro' ]; then
        dev_mode=pro
    fi
fi
echo "dev_mode=${dev_mode}"

cat > /var/spool/cron/clear_result <<EOF
*/5 * * * * /data/wcup_quiz/manage_${dev_mode}.py clear_result
EOF
crontab /var/spool/cron/clear_result
service crond restart

chmod -R 777 /data/wcup_quiz/logs/

tailf /data/wcup_quiz/bin/run_task.sh