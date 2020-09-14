#!/usr/bin/env bash

base=$(cd $(dirname $0) > /dev/null;pwd)

snapshot=$(${base}/copy_prod_db_to_local.sh | grep snapshot| sed 's/snapshot: \(.*\)/\1/ ')
echo "Snapshot name is ${snapshot}"
${base}/reset_local_from_snapshot ${snapshot}




