#!/bin/bash

BASEDIR=/var/www/sites/dev.tennisblock.com
GITDIR=currentVersion
ENVDIR=/home/ec2-user/Envs
ENVNAME=tennisblockdev

pushd ${BASEDIR} >> /dev/null
cp maintenance.html maintenance_on.html
popd >> /dev/null

echo "Pulling latest code updates.." 
cd ${BASEDIR}/${GITDIR}
git reset --hard HEAD
git checkout develop
git pull
if [ $? -ne 0 ];then
    echo "Pull failed.."
    exit 2
fi

echo -e "\n Collecting updated statics.."
cd ${BASEDIR}
./manage collectstatic --noinput
if [ $? -ne 0 ];then
    echo "Pull failed.."
    exit 2
fi

echo -e "\n Installing updated Python modules.."
echo -e "\n Changing directory to ${BASEDIR}/${GITDIR} .."
cd ${BASEDIR}/${GITDIR}

source ${ENVDIR}/${ENVNAME}/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ];then
    echo "Pull failed.."
    exit 2
fi

echo -e "\n Reloading uWSGI web service.."
cd ${BASEDIR}
touch reload.me

# How can we check uwsgi status and return true if its up and running???

#status= check_uwsgi()
#status=`/usr/lib64/nagios/plugins/check_uwsgi.py -s 127.0.0.1 -p 9191 -t 1`


# Remove maintenance only if it's all good.
#if [ $status == 0 ];then

#    pushd ${BASEDIR} >> /dev/null
#    popd >> /dev/null

#fi
rm maintenance_on.html
