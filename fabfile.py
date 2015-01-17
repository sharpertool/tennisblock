import re
import os

from fabric.api import *
from fabric.contrib.files import *
from fabric.network import ssh

env.use_ssh_config = True
env.disable_known_hosts = True
env.skip_bad_hosts = True

env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'gardenbuzz.pem')]

ssh.util.log_to_file("paramiko.log", 10)

@hosts('ec2-user@gardenbuzz.com')
def dev_release():
    with cd("/var/www/sites/dev.tennisblock.com"):
        run("./siteupdate.sh")


@hosts('ec2-user@gardenbuzz.com')
def prod_release():
    with cd("/var/www/sites/tennisblock.com"):
        run("./siteupdate.sh")


@hosts('ec2-user@gardenbuzz.com')
def get_prod_dump():
    with cd("backups"):
        out = run("dbbackup tennisblock")
        m = re.search(r'backups/(.*)', out)
        if m:
            backup_file = m.group(1).strip()
            files = get(backup_file)
            if len(files) == 1:
                return files [0]
        return None

@hosts('ec2-user@gardenbuzz.com')
def sync_prod(dbname=None):
    if not dbname:
        raise Exception("Cannot work my magic if you don't give me names!")

    dumpfile = get_prod_dump()
    print("Downloaded dumpfile {}".format(dumpfile))
    local('./resetdb.sh {}'.format(dbname))
    local('gzcat {} | mysql {}'.format(dumpfile, dbname))

