from fabric import api

api.env.hosts = ['178.79.185.15']
api.env.user = 'deploy'
api.env.directory = "$HOME/sites/ownblock/ownblock"
api.env.activate = "source $HOME/.virtualenvs/ownblock/bin/activate"


def manage(cmd):
    return api.run("dotenv %s/manage.py %s" % (api.env.directory, cmd))


@api.task
def bower_update():

    with api.cd(api.env.directory):
        api.run("bower update")
        with api.cd(api.env.directory +
                    "/static/bower_components/openlayers/build"):

            api.run("python build.py")
            api.run("ln -s ../img .")
            api.run("ln -s ../theme .")


@api.task
def deploy():
    with api.cd(api.env.directory):

        api.run("git pull")

        with api.prefix(api.env.activate):

            api.run("pip install -r ../requirements/production.txt")

            manage("check")
            manage("collectstatic --noinput")
            manage("migrate")

    bower_update()
    api.sudo("supervisorctl restart webapp")
