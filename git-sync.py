#!/usr/bin/env python
import os
import argparse
from git import Repo
from git.repo.fun import is_git_dir


def check_arg():
    """Make the parsing of CLI call

    Returns:
        [tupla] -- [Namespaces of the parameters passed to the cli]
    """
    parse = argparse.ArgumentParser(prog='git-sync',
                                    usage='%(prog)s [-h|--help] ',
                                    description='keep sync remote git repo with a local repo',
                                    epilog='',
                                    allow_abbrev=False)
    parse.add_argument('-r', '--remote',
                       type=str,
                       help='Remote git repo to sync',
                       required=True)
    parse.add_argument('-b', '--branch',
                       type=str,
                       help='Branch to sync',
                       required=True)
    parse.add_argument('-u', '--username',
                       type=str,
                       help='Username to authenticate with remote git repo',
                       required=True)
    parse.add_argument('-t', '--token',
                       type=str,
                       help='Token to authenticate with remote git repo',
                       required=True)
    parse.add_argument('-d', '--dst',
                       type=str,
                       help='Directory where local repo will reside',
                       required=True)
    args = parse.parse_args()
    return args


class GitOperations:
    """ Class with the operations necessary to clone or update the remote repository with a local directory
    """
    def __init__(self, repourl, branch, username, token, path):
        """Constructor of the class

        :param repourl: Remote URL Repository
        :param branch: Branch to work with
        :param username: username with read permission
        :param token: token bellowing to the username param
        :param path: local destinations of the repo in the filesystem
        """
        split_str = str.split(repourl, sep='/')
        self.repourl = 'https://' + username + ':' + token + '@'
        for i in range(2, len(split_str) - 1):
            self.repourl += split_str[i] + '/'
        self.repourl += split_str[len(split_str) - 1]
        self.branch = branch
        self.path = path

    def clone(self):
        """ Proceed to clone or pull the remote repository depending id the repo exists at path parameter for CLI

        :return:
        """
        print('Path destino: ' + self.path)
        if not is_git_dir(self.path + '/.git'):
            # proceed to clone the repo
            print('Clonando el repositorio ' + self.repourl)
            Repo.clone_from(self.repourl, self.path, branch=self.branch)
        else:
            # proceed to update the local directory with a last commit
            print('Haciendo un pull del repositorio ' + self.repourl)
            repo = Repo(self.path)
            self.update(repo)

    def update(self, repo):
        """ Make a pull from the remote repository

        :param repo: Instance of Repo Class of GitPython package pointing to local repo
        :return:
        """
        o = repo.remotes.origin
        o.pull(self.branch)


def initialize():
    """ Initialization of GitOperation Class instance and others tasks necessaries

    :return: An instance of GitOperation Class
    """
    try:
        args = check_arg()

        git_ope = GitOperations(
            args.remote,
            args.branch,
            args.username,
            args.token,
            os.path.abspath(args.dst)
        )

        # create the destination directory if not exists
        if not os.path.exists(git_ope.path):
            os.mkdir(git_ope.path, mode=0o777)
            # os.chown(git_ope.path, -1, 0)

        return git_ope
    except Exception as e:
        print(e.args)


# for script execution use
if __name__ == '__main__':
    try:
        gitinst = initialize()
        gitinst.clone()
    except Exception as e:
        print(e.args)
    finally:
        print("¡Script finalizado!")
