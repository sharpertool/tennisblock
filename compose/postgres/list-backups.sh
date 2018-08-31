#!/bin/bash
echo "listing available backups"
echo "-------------------------"
backup_dir=${1:-/backups}
ls ${backup_dir}/ /local_backups

