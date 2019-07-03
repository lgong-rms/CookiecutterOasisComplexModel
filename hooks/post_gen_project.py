#!/usr/bin/env python3

import os
import time

from subprocess import (
    check_call,
    check_output,
)

SUBMODULES = {
    'oasis_keys_server': 'git+ssh://git@github.com/OasisLMF/oasis_keys_server'

}

def setup_git_user():
    check_call(['git', 'config', '--global', 'user.name', '"{{cookiecutter.project_maintainer}}"'])
    check_call(['git', 'config', '--global', 'user.email', '"{{cookiecutter.project_maintainer_email}}"'])


def create_git_repo():
    check_call(['git', 'init'])
    check_call(['git', 'add', '.'])
    check_call(['git', 'commit', '-m', 'Post-project creation initialisation'])


def add_git_submodules():
    for name, url in SUBMODULES.items():
        check_call(
            [
                'git', 'submodule', 'add', '-f', url, name,
                'git', 'checkout', 'master'
            ]
        )


def commit_git_submodules():
    check_call(['git', 'add', '-A'])
    check_call(['git', 'commit', '-m', 'Commit for Git submodules'])


if __name__ == '__main__':
    cwd = os.getcwd()

    print('\nSetting up Git user and email in global config.')
    time.sleep(2)
    setup_git_user()
    print('\n\tuser={}, email={}'.format(check_output(['git', 'config', '--global', 'user.name']), check_output(['git', 'config', '--global', 'user.email'])))
    time.sleep(3)

    print('\nCreating Git repo in {}.\n'.format(cwd))
    time.sleep(2)
    create_git_repo()

    print('\nAdding Oasis repositories as Git submodules in {}.\n'.format(os.path.join(cwd, 'src')))
    time.sleep(2)
    add_git_submodules()

    print('\nCommitting Git submodules.\n')
    time.sleep(2)
    commit_git_submodules()
