#!flask/bin/python
import click


def make_sure_path_exists(path):
    """Ensure a directory exists."""
    from os import makedirs
    import errno
    try:
        makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def create_db():
    """Simple program that creates the db that is configured in instance/config.py as SQLALCHEMY_DATABASE_URI."""
    from ..WhatAClass import db
    filename = '../../instance/config.py'
    db_uri = None
    click.echo('Searching in instance/config.py')
    with open(filename) as config:
        for line in config:
            if line.find('SQLALCHEMY_DATABASE_URI') is not -1:
                db_uri = line.split('=')[1].strip()

    click.echo('Parsing SQLALCHEMY_DATABASE_URI')
    db_path = db_uri.replace('sqlite:///', '', 1)

    click.echo('Making sure directory exists')
    make_sure_path_exists(db_path)

    click.echo('Creating database')
    db.create_all()


@click.command()
@click.option('--creat_db', is_flag=True, help='Create the database configured in instance/config.py. (SQLALCHEMY_DATABASE_URI)')
def run(creat_db):
    """Handy function to do a bunch of stuff from the command line."""
    if creat_db:
        create_db()


if __name__ == '__main__':
    run()
