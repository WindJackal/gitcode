from subprocess import run, PIPE
import platform
import os
import re
from .exceptions import *

class Repo():
    def __init__(self, path, origin=None, descriptor=None):
        self.name = descriptor
        self.path = path
        self.origin = origin
        self.branches = ['master']
        self.commits = []
        self.current_branch = 'master'
        self.latest_commit = None

    def __str__(self):
        description = f'{self.name}, with the local repository at {self.path} and origin at {self.origin}'
        return description
    
    def set_remote(self, url, name='origin'):
        proc = run(['git', 'remote', 'set-url', f'{name}', f'{url}'], capture_output=True, cwd=self.path)
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise RemoteNotExistsError(name)
        if name == 'origin':
            self.origin = url
        return True
    
    def get_remotes(self):
        try:
            proc = run(['git', 'remote', '-v'], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            remotes = out.decode('utf-8')
            return remotes
        except:
            return None
    
    check_origin = get_remotes

    def add_remote(self, url, name='origin'):
        proc = run(['git', 'remote', 'add', f'{name}', f'{url}'], capture_output=True, cwd=self.path)
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise RemoteAlreadyExistsError(name)
        if name == 'origin':
            self.origin = url
        return True

    def branch(self):
        try:
            proc = run(['git', 'branch'], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            branches = out.decode('utf-8')
            return branches
        except:
            return None
    
    def checkout(self, name, new=False):
        if new == True and name not in self.branches:
            proc = run(['git', 'checkout', '-b', f'{name}'], capture_output=True, cwd=self.path)
            err = proc.stderr
            if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
                raise BranchAlreadyExistsError(name)
            self.branches.append(name)
        elif new == False and name in self.branches:
            proc = run(['git', 'checkout', f'{name}'], capture_output=True, cwd=self.path)
            err = proc.stderr
            if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
                raise BranchNotExistsError(name)
        elif new == True and name in self.branches:
            raise BranchAlreadyExistsError(name)
        elif new == False and name not in self.branches:
            raise BranchNotExistsError(name)
        self.current_branch = name
        return True
    
    change_branch = checkout

    def delete_branch(self, name):
        if name in self.branches:
            proc = run(['git', 'branch', '-D', f'{name}'], capture_output=True, cwd=self.path)
            err = proc.stderr
            if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
                raise CannotDeleteBranchError(name)
            self.branches.remove(name)
            return True
        else:
            raise CannotDeleteBranchError(name)
    
    def merge(self, branch, commit=True):
        self.commit(message=f'About to merge {branch}')
        if commit == False:
            proc = run(['git', 'merge', '--no-commit', branch], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            print(out.decode('utf-8'))
            print(err.decode('utf-8'))
            if 'not something we can merge' in err.decode('utf-8') or 'error:' in err.decode('utf-8') or 'fatal:' in err.decode('utf-8'):
                raise MergeError(branch)
            elif 'Merge conflict' in err.decode('utf-8'):
                raise ConflictError
        else:
            proc = run(['git', 'merge', branch], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            print(out.decode('utf-8'))
            print(err.decode('utf-8'))
            if 'not something we can merge' in err.decode('utf-8') or 'error:' in err.decode('utf-8') or 'fatal:' in err.decode('utf-8'):
                raise MergeError(branch)
            elif 'Merge conflict' in err.decode('utf-8'):
                raise ConflictError
        return True
    
    def abort_merge(self):
        proc = run(['git', 'merge', '--abort'], capture_output=True,cwd=self.path)
        out, err = proc.stdout, proc.stderr
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))
        if 'fatal' in err.decode('utf-8'):
            raise MergeError(branch='No merge to abort')
        return True
    
    def continue_merge(self):
        proc = run(['git', 'merge', '--continue'], capture_output=True, cwd=self.path)
        out, err = proc.stdout, proc.stderr
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))
        if 'Merge conflict' in err.decode('utf-8'):
            raise ConflictError
        return True
        
    def stage_files(self):
        try:
            proc = run(['git', 'add', '-A'], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            files = out.decode('utf-8')
            errors = err.decode('utf-8')
            return True
        except:
            return False
    
    add = stage_files

    def remove_files(self, cached=False, pathspec=None, recursive=False):
        if cached == False and pathspec == None:
            proc = run(['git', 'rm'], capture_output=True,  cwd=self.path)
        elif cached == True and pathspec == None:
            proc = run(['git', 'rm', '--cached'], capture_output=True,  cwd=self.path)
        elif cached == False and pathspec != None and recursive == False:
            proc = run(['git', 'rm', f'{pathspec}'], capture_output=True,  cwd=self.path)
        elif cached == False and pathspec != None and recursive == True:
            proc = run(['git', 'rm', '-r', f'{pathspec}'], capture_output=True,  cwd=self.path)
        elif cached == True and pathspec != None and recursive == False:
            proc = run(['git', 'rm', '--cached', f'{pathspec}'], capture_output=True,  cwd=self.path)
        elif cached == True and pathspec != None and recursive == True:
            proc = run(['git', 'rm', '-r', '--cached', f'{pathspec}'], capture_output=True,  cwd=self.path)
        else:
            return False
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise RemoveFailureError
        files = out.decode('utf-8')
        return True

    def commit(self, add=True, message=None):
        try:
            if add == True and message != None:
                proc = run(['git', 'commit', '-am', f'{message}'], capture_output=True)
            elif add == False and message != None:
                proc = run(['git', 'commit', '-m', f'{message}'], capture_output=True)
            elif add == True and message == None:
                proc = run(['git', 'commit', '-a', '--allow-empty-message'], capture_output=True)
            else:
                proc = run(['git', 'commit', '--allow-empty-message'], capture_output=True)
            commit_hash = re.search('\w{40}', self.log(1)).group()
            ct = {'name': message, 'hash': str(commit_hash)}
            self.commits.append(ct)
            self.latest_commit = ct
            return True
        except Exception as e:
            print(e)
            return False
    
    def log(self, limit=None, format=None):
        if limit == None and format == None:
            proc = run(['git', 'log'], capture_output=True, cwd=self.path)
        elif limit!= None and isinstance(limit, int) and format == None:
            proc = run(['git', 'log', '-n', f'{limit}'], capture_output=True, cwd=self.path)
        elif limit == None and format != None:
            proc = run(['git', 'log', f'--pretty=format:{format}'], capture_output=True, cwd=self.path)
        elif limit != None and isinstance(limit, int) and format != None:
            proc = run(['git', 'log', '-n', f'{limit}', f'--pretty=format:{format}'], capture_output=True, cwd=self.path)
        else:
            return None
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise NoCommitsError
        commits = out.decode('utf-8')
        return commits
    
    def status(self, short=False, porcelain=False, untracked=False):
        try:
            if short:
                proc = run(['git', 'status', '--short'], capture_output=True, cwd=self.path)
            elif porcelain:
                proc = run(['git', 'status', '--porcelain'], capture_output=True, cwd=self.path)
            elif untracked:
                proc = run(['git', 'status', '-u'], capture_output=True, cwd=self.path)
            else:
                proc = run(['git', 'status'], capture_output=True, cwd=self.path)
            out, err = proc.stdout, proc.stderr
            status = out.decode('utf-8')
            return status
        except:
            return None
    
    def gitignore(self, content=[]):
        try:
            if len(content) == 0:
                return False
            
            if platform.system == 'Windows':
                file = open(f'{self.path}\.gitignore', 'a')
            else:
                file = open(f'{self.path}/.gitignore', 'a')
            
            to_write = []
            for i in content:
                to_write.append(i)
                to_write.append('\n')
            
            file.writelines(to_write)
            file.close()
            return True
        except:
            return False
    
    ignore = gitignore

    def reset(self, mode, commit):
        proc = run(['git', 'reset', f'--{mode}', f'{commit}'], capture_output=True, cwd=self.path)
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise UnknownRevisionError(commit)
        for i in self.commits:
            commit_hash = i['hash'][:len(commit)]
            if commit == commit_hash:
                name = i['name']
                new_hash = i['hash']
                break
        ct = {'name': name, 'hash': new_hash}
        self.latest_commit = ct
        index = self.commits.index(ct) + 1
        self.commits = self.commits[:index]
        return True
    
    def push(self, username, password, remote='origin', branch='master', all=False):
        rest = remote.replace(re.search('.*.com', remote).group(), '')
        site = re.search('/.*.com', remote).group()
        site = site.replace('//', '')

        command = remote[:8] + username + ':' + password + '@' + site
        if platform.system == 'Windows':
            file = open(f'{self.path}\.git-credentials', 'a')
        else:
            file = open(f'{self.path}/.git-credentials', 'a')
        
        file.write(f'{command}')
        file.close()

        with open('.gitignore', 'a') as f:
            f.write('.git-credentials')
        

        if all == True:
            proc = run(['git', 'push', '-u', remote, '--all', branch], capture_output=True, cwd=self.path)
        else:
            proc = run(['git', 'push', '-u', remote, f'HEAD:{branch}'], capture_output=True, cwd=self.path)
        
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise PushError(remote, branch)
        
        return True

    def pull(self, remote, username, password, branch=None):
        rest = remote.replace(re.search('.*.com', remote).group(), '')
        site = re.search('/.*.com', remote).group()
        site = site.replace('//', '')

        command = remote[:8] + username + ':' + password + '@' + site + rest
        if branch != None:
            proc = run(['git', 'pull', f'{command}', f'{branch}'], capture_output=True, cwd=self.path)
        else:
            proc = run(['git', 'pull', f'{command}', 'master'], capture_output=True, cwd=self.path)
        out, err = proc.stdout, proc.stderr
        if 'fatal' in err.decode('utf-8') or 'error' in err.decode('utf-8'):
            raise PullError
        return True

def init(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        
        initproc = run(['git', 'init'],  cwd=path)
        repo = Repo(path)
        repo.commit(message="Repository Created")
        return repo
    except:
        return None

def set_identity(name, email, globalreach=False):
    try:
        if globalreach == True:
            name_proc = run(['git', 'config', '--global', 'user.name', f'"{name}"'], capture_output=True)
            email_proc = run(['git', 'config', '--global', 'user.email', f'{email}'], capture_output=True)
            out, err = name_proc.stdout, name_proc.stderr
        elif globalreach == False:
            name_proc = run(['git', 'config', 'user.name', f'"{name}"'], capture_output=True)
            email_proc = run(['git', 'config', 'user.email', f'{email}'], capture_output=True)
            out, err = name_proc.stdout, name_proc.stderr
        return True
    except:
        return False

def clone(path, remote, username, password, branch=None):
    try:
        rest = remote.replace(re.search('.*.com', remote).group(), '')
        site = re.search('/.*.com', remote).group()
        site = site.replace('//', '')

        command = remote[:8] + username + ':' + password + '@' + site + rest
        if branch != None:
            proc = run(['git', 'clone', '-b', f'{branch}', f'{command}'], cwd=path)
        else:
            proc = run(['git', 'clone', f'{command}'], cwd=path)
        repo = Repo(path)
        origin = remote
        return repo
    except:
        return False

def help():
    try:
        proc = run(['git', 'help'], capture_output=True)
        out, err = proc.stdout, proc.stderr
        info = out.decode('utf-8')
        print(info)
        return
    except:
        return None