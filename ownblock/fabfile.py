from fabric import api

api.env.hosts = ['178.79.185.15']
api.env.user = 'deploy'
api.env.directory = "$HOME/sites/ownblock/ownblock"
api.env.activate = "source $HOME/.virtualenvs/ownblock/bin/activate"
api.env.manage = "dotenv %s/manage.py" % api.env.directory


def manage(cmd):
    return api.run("%s %s" % (api.env.manage, cmd))


@api.task
def deploy():
    with api.cd(api.env.directory),\
            api.prefix(api.env.activate):

        api.run("git pull")
        api.run("pip install -r ../requirements/production.txt")

        manage("check")
        manage("collectstatic --noinput")
        manage("migrate")

        api.sudo("supervisorctl restart webapp")
