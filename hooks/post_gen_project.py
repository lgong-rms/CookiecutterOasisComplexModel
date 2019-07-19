#!/usr/bin/env python3

import os
import time

from subprocess import (
    check_call,
    check_output,
)


def setup_git_user():
    check_call(['git', 'config', '--global', 'user.name', '"{{cookiecutter.project_maintainer}}"'])
    check_call(['git', 'config', '--global', 'user.email', '"{{cookiecutter.project_maintainer_email}}"'])


def create_git_repo():
    check_call(['git', 'init'])
    check_call(['git', 'add', '.'])
    check_call(['git', 'commit', '-m', 'Post-project creation initialisation'])

if __name__ == '__main__':
    cwd = os.getcwd()

    print('\nSetting up Git user and email in global config.')
    time.sleep(2)
    setup_git_user()
    print('\n\tuser={}, email={}'.format(check_output(['git', 'config', '--global', 'user.name']), check_output(['git', 'config', '--global', 'user.email'])))
    time.sleep(3)

    print('\nCreating local Git repository in {}.\n'.format(cwd))
    time.sleep(2)
    create_git_repo()

    print(
        '\nLocal Git repository {{cookiecutter.project_name}} set up. '
        'Please create a remote repository on GitHub (or some other hosting service) '
        'and link via `git remote add origin <remote URI>`'
    )
