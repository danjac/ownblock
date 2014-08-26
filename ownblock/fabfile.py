from fabric import api

api.env.hosts = ['178.79.185.15']
api.env.user = 'deploy'
api.env.directory = "$HOME/sites/ownblock/ownblock"
api.env.activate = "source $HOME/.virtualenvs/ownblock/bin/activate"


@api.task
def deploy():
    with api.cd(api.env.directory),\
            api.prefix(api.env.activate):

        api.run("git pull")
        api.run("./manage.py check")
        api.run("./manage.py collectstatic --noinput")
        api.run("./manage.py syncdb --migrate")
        api.sudo("supervisorctl restart webapp")
