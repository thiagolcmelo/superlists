import random
import string

from fabric import Connection
from fabric import task

LOWERS = string.ascii_lowercase
UPPERS = string.ascii_uppercase
DIGITS = string.digits
OTHERS = "!@#$%^&*(-_=+)"
REPO_URL = 'https://github.com/thiagolcmelo/superlists.git'

@task
def deploy(c):
    site_folder = '/home/%s/sites/%s' % (c.user, c.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(c, site_folder)
    _get_latest_source(c, source_folder)
    _update_settings(c, source_folder, c.host)
    _update_virtualenv(c, source_folder)
    _update_static_files(c, source_folder)
    _update_database(c, source_folder)

def _create_directory_structure_if_necessary(c, site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run("""
            if [ ! -d "{site_folder}/{subfolder}" ];
            then
                mkdir -p "{site_folder}/{subfolder}";
            fi
            """.format(site_folder=site_folder,
                       subfolder=subfolder))

def _get_latest_source(c, source_folder):
    c.run("""
        if [ -d "{source_folder}/.git" ];
        then
            cd "{source_folder}" && git fetch && git pull;
            CURRENT_COMMIT=$(git log -n 1 --format=%H)
            git reset --hard $CURRENT_COMMIT
        else
            git clone "{repo_url}" "{source_folder}";
        fi
    """.format(source_folder=source_folder,
               repo_url=REPO_URL))

def _update_settings(c, source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    secret_key_file = source_folder + '/superlists/secret_key.py'
    chars = LOWERS + DIGITS + OTHERS
    secret = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    c.run("""
        sed -i -e 's/DEBUG\ =\ True/DEBUG\ =\ False/g' {settings_path}
        sed -i -e 's/ALLOWED_HOSTS =.*$/ALLOWED_HOSTS = ["{site_name}"]/g' {settings_path}
        if [ ! -f {secret_key_file} ];
        then
            echo "SECRET_KEY = '{secret}'" >> {secret_key_file};
        fi
        echo "from .secret_key import SECRET_KEY" >> {settings_path}
    """.format(settings_path=settings_path,
               site_name=site_name,
               secret_key_file=secret_key_file,
               secret=secret))

def _update_virtualenv(c, source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    c.run("""
        if [ ! -f "{virtualenv_folder}/bin/pip" ];
        then
            virtualenv --python=python3 {virtualenv_folder}
        fi
        {virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt
    """.format(
        virtualenv_folder=virtualenv_folder,
        source_folder=source_folder
    ))

def _update_static_files(c, source_folder):
    c.run("""
        cd "{source_folder}"
        ../virtualenv/bin/python3 manage.py collectstatic --noinput
    """.format(source_folder=source_folder))

def _update_database(c, source_folder):
    c.run("""
        cd "{source_folder}"
        ../virtualenv/bin/python3 manage.py migrate --noinput
    """.format(source_folder=source_folder))
