#!/usr/bin/python3
"""Archive webstatic"""
from fabric.api import local, put, run, env
from time import strftime
from datetime import date
from os import path

env.hosts = ["52.91.121.78", "18.234.168.42"]


def do_pack():
    """ A script that generates archive the contents of web_static folder"""
    file_name = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(file_name))

        return "versions/web_static_{}.tgz".format(file_name)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes
    an archive to your web server"""

    if not path.exists(archive_path):
        return False
    try:
        tgzfile = archive_path.split("/")[-1]
        filename = tgzfile.split(".")[0]
        pathname = "/data/web_static/releases/" + filename
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".format(filename))
        run("tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgzfile, filename))
        run("rm /tmp/{}".format(tgzfile))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        return True
    except Exception as e:
        return False


def deploy():
    """Runs do_pack the do_deploy"""
    a_path = do_pack()
    if not a_path:
        return False

    do_deploy(a_path)
