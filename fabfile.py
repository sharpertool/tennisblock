from fabric.api import run,env,hosts,cd,get,local

env.use_ssh_config = True

@hosts('ec2-user@gardenbuzz.com')
def dev_release():
    with cd("/var/www/sites/dev.tennisblock.com"):
        run("./siteupdate.sh")


@hosts('ec2-user@gardenbuzz.com')
def prod_release():
    with cd("/var/www/sites/tennisblock.com"):
        run("./siteupdate.sh")

