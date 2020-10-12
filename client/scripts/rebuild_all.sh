#!/bin/bash

echo "${BASH_SOURCE[0]}"

scripts=$(cd -P "$(dirname $0)" > /dev/null;pwd)
page_dir="${scripts}/../src/pages"
base="${scripts}/../.."

echo "Scripts dir ${scripts}"

# Find the virtualenv dir
if [[ -d "${base}/.venv3" ]];then
    venv="${base}/.venv3"
    python_app="${venv}/bin/python"
elif [[ -d "${base}/.venv" ]];then
    venv="${base}/.venv"
    python_app="${venv}/bin/python"
else
    echo "Unable to determine virtualenv dir."
    python_app=$(which python3)
fi

echo "Pages are at ${page_dir}"
echo "Using Python from ${venv}/bin/python"

pushd ${page_dir} > /dev/null
for d in `ls -d */`
do
    pushd ${d} > /dev/null
    if [[ -a 'modules_used.json' ]];then
        echo "Building in $d"
        #${venv}/bin/python ${scripts}/make_modules.py modules_used.json
        ${python_app} ${scripts}/make_modules.py modules_used.json
    fi
    popd > /dev/null
done
popd > /dev/null
