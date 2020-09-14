#!/usr/bin/env bash

scriptdir=$(cd $(dirname $0);pwd)
root=${scriptdir}/..

cd ${root}

mkcert -install

# Clean up first
rm -f *.pem

# Could be more names if desired.
# Make sure these names are in /etc/hosts
mkcert tennisblock.local local.tennisblock.com localhost

pem_files=$(ls *.pem)

pem_file=$(ls *.pem | grep '\d.pem')
key_file=$(ls *.pem | grep '\d-key.pem')

echo "Pem Files: ${pem_files}"
echo "Pem File: ${pem_file}"
echo "Key File: ${key_file}"

mkdir -p ssl
echo "Backup existing files (one time)"
if [[ -f "ssl/private.key" ]]
then
    mkdir -p ssl/backup
    mv ssl/private.* ssl/backup
fi

if [[ -f "${pem_file}" ]]
then
    mv ${pem_file} ssl/private.crt
fi

if [[ -f "${key_file}" ]]
then
    mv ${key_file} ssl/private.key
fi

cat "$(mkcert -CAROOT)/rootCA.pem" >> ./ssl/private.pem

