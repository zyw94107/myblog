from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://github.com/zyw94107/myblog.git"

env.user = 'yiwei'
env.password = 'z9940107'

# 填写你自己的主机对应的域名
env.hosts = ['35.229.149.208']
env.key_filename = '~/.ssh/my-ssh-key'
# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '22'


def deploy():
    source_folder = '/home/yiwei/sites/www.zhouyw.top/myblog'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('systemctl restart gunicorn')
    sudo('service nginx reload')
