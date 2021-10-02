# gitcode

**gitcode** is a Python package aimed at allowing users to perform *Git* commands from Python scripts and the Python shell. There are alternative packages that perform the same function, but I found them awkward and difficult to use. I decided to develop **gitcode** so that users, either new to or experienced with *Git*, could find it easy and accessible to interface with it from their Python projects.

> Note: gitcode is currently at v1.0.0 (the first initial build). There are obviously improvements to be made, but I've decided that I'm going to first rework the authentication in the various functions that require Git authentication, due to GitHub [deprecating password authentication](https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/). v1.0.1 with token-based authentication and other improvements is currently in development.

## Instructions for installation

- **gitcode** requires Python versions greater than 3.5. All packages used in the source code are found within a default Python install, but one of them requires Python >=3.5.
- *Git* also needs to be installed on your system. You can download it from the [Git website](https://git-scm.com/downloads)
- Once Python and *Git* are installed, it is recommended (but not required) to set up a virtual environment to install **gitcode** into. See [here](https://docs.python.org/3/library/venv.html) for instructions on how to setup and activate a virtual environment
- Once complete, run the below command to install **gitcode**
```
pip install git+https://github.com/WindJackal/gitcode.git@stable-release
```
- If the above doesn't work, run `pip3` instead of `pip`

## Documentation

There are two modules in the **gitcode** package: [git](gitcode/git.py) and [exceptions](gitcode/exceptions.py). Most of the time, you will only be using the git module; the exceptions module will only be used if you want to implement your own custom error handling.

### The 'git' module

Import the git module using `from gitcode import git`.

#### Initialising a repository
There are three ways to initialise a repository: `git.init()`, `git.Repo()` and `git.clone()`

##### git.init()
The structure of `git.init()` is as follows:
```
git.init(path)
```
- the `path` argument is a string specifying where you want the local repository on your machine to be. The folder you specify doesn't have to exist; `git.init()` will create it for you if necessary.
- On Linux/Mac, the path would look something like this `'/home/user/Documents/repository'`
- On Windows, the same would look like `'C:\Users\user\Documents\folder'`
- set `git.init(path)` equal to a variable, since it return an object that allows you to perform *Git* operations

##### git.Repo()
`git.Repo()` is the main object that allows you to perform Git operations. Further detail is provided below, but you can instantiate this if you don't want to re-initialise an existing repo. `git.Repo()` has a structure as follows:
`git.Repo(path, origin=None, descriptor=None)`
- The first argument, `path`, is required. It specifies the path to the repository you wish to interact with. The rest of the arguments are optional, and the values can be set later.
- The second argument, `origin`, represents the remote repository your local repository is linked to.
- The third argument, `descriptor`, is a human friendly name you can call your repository. Note that you can not refer to your repository object in this way.

##### git.clone()
`git.clone()` allows you to clone an existing repository from a version control hosting site such as GitHub. The structure of the `clone` function is as follows:
```
git.clone(path, remote, username, password, branch=None)
```
- The `path` argument is required, and specifies the directory to which you want to clone the remote repository
- The `remote` argument is required, and specifies what remote repository you are cloning
- The `username` argument is required, and is your GitHub username. This is not stored or sent anywhere, only used to authenticate for GitHub
- The `password` argument is required, and is your GitHub password. This is not stored or sent anywhere, only used to authenticate for GitHub.
- The `branch` argument is optional, and specifies what branch of your local repository the remote repository will be cloned to. If left blank, it will default to the master branch.

**NOTE: IT IS IMPORTANT THAT FOR ANY OF THESE METHODS, WHEN YOU RUN THEM, SET THEM EQUAL TO A VARIABLE SO THAT YOU HAVE A WAY TO CALL THE METHODS OF THE REPO OBJECT THAT IS RETURNED**

#### Working with Git
There are two additional functions you may use to work with *Git*: `git.set_identity` and `git.help()`

##### git.set_identity()
This is used to set your name and email for *Git* to use when committing. The structure of the function is as follows:
```
git.set_identity(name, email, globalreach=False)
```
- The first argument, `name`, is required, and specifies the name *Git* will use during commits.
- The second argument, `email`, is required, and specifies the email address *Git* will use during commits.
- The third argument, `globalreach`, is optional and defaults to False. You can set your info individually for each repository (please make sure you are in the repository's directory when running this command) or globally, which you may have done anyway when installing *Git*. To set your information globally, pass in `globalreach` as `True`.

##### git.help()
If you are unsure of how git works or what to do with *Git*. simply run `git.help()` in a shell. It will give you a rundown of the basic *Git* commands.

#### The Repo object
**gitcode**'s `git` module and functionality is defined by the **Repo** object. Within the **Repo** object are the methods and variables you will use to perform *Git* operations.

To access these, preface all of them with your repo variable, e.g. `repo.variable`

##### Variables
- `name`, a human friendly name you can call your repository
- `path`, the path to your local repository folder
- `origin`, the remote origin of your repository
- `branches`, a list of all the branches present in the repository
- `commits`, a list of all the commits made by the repository
- `current_branch`, the current branch you're working on
- `latest_commit`, the message and hash of the last commit you made

##### Methods

###### description()
Returns a string describing the Repo object with basic information.

###### add_remote()
Adds a remote to your repository. Structured as `add_remote(url, name='origin'`. Returns True if successful.
- `url` is what you wish to set the remote you're adding to.
- `name` is what you wish to call the remote you're adding. Defaults to 'origin'

This will raise a `RemoteAlreadyExistsError` if a remote with  the same name already exists.

###### get_remotes()
Gets a list of the remotes defined in your repository. Takes no arguments. You can use `check_origin()` instead of `get_remotes()` to achieve the same results.

Returns the remotes as a string.

###### set_remote()
Sets an existing remote to a new variable. Structured as `set_remote(url, name='origin')`. Returns True if successful.
- `url` is what you wish the new value of the remote to be.
- `name` is the remote you wish to assign a new value to.

This will raise a `RemoteNotExistsError` if you're trying to set a value to a remote that doesn't exist.

###### branch()
Takes no arguments. Returns the branches in the repository and the current one marked with an asterisk.

###### checkout()
Allows you to change branches or create a new branch. Structured as: `checkout(name, new=False)`. Returns True if successful.
- `new` determines if you're creating a new branch or simply switching to an existing one. Set `new=True` if creating a new branch.
- `name` represents the name of the branch you're switching to or creating.

A `BranchAlreadyExistsError` will be raised if you're trying to create a new branch with the same name as one that already exists. A `BranchNotExistsError` will be raised if you're trying to switch to a branch that doesn't exist.

###### delete_branch()
Allows you to delete branches. Structured as `delete_branch(name)`. Returns True if successful.
- `name` is the name of the branch you're trying to delete.

This will raise a `CannotDeleteBranchError` if the branch does not exist or if the deletion fails for some reason.

###### merge()
Allows you to merge two branches. Structured as `merge(branch, commit=True)`. Returns True if successful.
- `branch` specifies the branch you want to merge to the current branch you're on
- `commit` specifies whether you want to commit after the merge completes. Defaults to True.

This will raise a `MergeError` is the branch cannot be merged due to a generic error, or a `ConflictError` if a merge conflict occurs.

###### abort_merge()
Allows you to abort a merge if a conflict error occurs. Takes no arguments. Returns True if successful.

This will raise a `MergeError` if it fails.

###### continue_merge()
Allows you to continue a merge after fixing a merge conflict. Takes no arguments. Returns True if successful.

This will raise a `ConflictError` if the merge fails again.

###### stage_files()
Allows you to stage files to be committed. Takes no arguments. You can call `add()` instead of `stage_files()` to achieve the same results. Returns True if successful, False if not.

###### remove_files()
Allows you to remove files from the commit stage. Structured as `remove_files(cached=False, pathspec=None, recursive=False)`. Returns True if successful.
- `cached` is optional, defaults to False. If set to true, will remove files that haven't been committed before.
- `pathspec` is optional, defaults to None. Set it to a specific filename to remove a specific file or folder.
- `recursive` is optional, defaults to False. Set it to True if trying to remove a non-empty directory. 

Any failures will raise a `RemoveFailureError`.

###### commit()
Allows you to commit files. Structured as `commit(add=True, message=None)`. Returns True if successful.
- `add` is optional, defaults to True. Will add all untracked/unstaged files prior to committing. Set to False to prevent this.
- `message` is optional, defaults to None. Allows you to specify a commit message when you commit.

Any errors will be printed and False will be returned.

###### log()
Allows you to view the commit log. Structured as `log(limit=None, format=None)`. Returns the commit log if successful.
- `limit` allows you to specify how many commits you want to return. Defaults to None, which will return all the commits.
- `format` allows to specify the format you want the commits in, according to *Git*'s [pretty-format documentation](https://git-scm.com/docs/pretty-formats). Defaults to None, which returns the default format.

This will raise a `NoCommitsError` if no commits have been made on the current branch.

###### status()
Allows you to view the current status of the repository. Structured as `status(short=False, porcelain=False, untracked=False)`. Returns the status as a string.
- `short` returns the status in *Git*'s short format if set to True.
- `porcelain` returns the status in *Git*'s porcelain format if set to True.
- `untracked` returns only the untracked files if set to True.

**NOTE: THESE OPTIONS TAKE PRECEDENCE. IF BOTH SHORT AND UNTRACKED ARE SET TO TRUE, SHORT WILL TAKE PRECEDENCE, AND SO ON.**

###### gitignore()
Allows you to specify files to be ignored by *Git* in a *.gitignore* file. Structured as `gitignore(content=[])`. Returns True if successful, False if not.
- `content` defaults to an empty list, which will return False. Pass in a list of all the files and folders you wish to ignore.

You can call `ignore()` instead of `gitignore()` to achieve the same result.

###### reset()
Allows you to reset to a specific commit. Structured as `reset(mode, commit)`. Returns True if successful.
- `mode` is a choice between 'soft', 'hard', 'keep', 'mixed', and 'merge', which you can read about on the [Git website](https://git-scm.com/docs/git-reset).
- `commit` is a commit hash that you wish to reset to. You can provide the full 40-character hash, but the first 7 characters should be sufficient.

This will raise an `UnknownRevisionError` if the reset fails.

###### push()
Allows you to push to a remote repository. Structured as `push(username, password, remote='origin', branch='master', all=False)`. Returns True if successful.
- `username` is your GitHub username used for authentication.
- `password` is your GitHub password used for authentication.
- `remote` is the remote you wish to push to. Defaults to 'origin'.
- `branch` is the specific branch you wish to push to. Defaults to 'master'.
- `all` decides if you push all branches or just the current one. Defaults to False.

This will raise a `PushError` if it fails.

###### pull()
Allows you to pull changes from a remote repository. Structured as `pull(remote, username, password, branch=None)`. Returns True if successful.
- `remote` is the remote you wish to push to. Defaults to 'origin'
- `username` is your GitHub username used for authentication.
- `password` is your GitHub password used for authentication.
- `branch` is the specific branch you wish to pull from.

This will raise a `PullError` if it fails.

### The 'exceptions' module
This module contains all the errors raised in the `git` module. Basic solutions for each error can be found below. All errors inherit from a base `Error` class.

#### RemoteNotExistsError
This is raised when you are trying to change the value of a remote that doesn't exist. 
- Run the `get_remotes()` method (also known as `check_origin()`) to see what remotes exist. If the remote you're trying to set isn't there, run the `add_remote()` method.
- If the remote is there, the error is elsewhere in your code.

#### RemoteAlreadyExistsError
This is raised when trying to create a remote with the same name as one that already exists.
- If you're trying to change the value of the remote, run the `set_remote()` method.
- Otherwise, choose a new name for the remote you're creating.

#### BranchNotExistsError
This is raised when trying to change to a branch that doesn't exist.
- Run the `branch()` method to see what branches exist. If it isn't there, the error occurred when you created the branch.
- Make sure you're not already on the branch you're trying to change to.

#### BranchAlreadyExistsError
This is raised when trying to create a new branch with the same name as one that already exists.
- If you're trying to change to a branch, make sure to leave `new=False` in the `checkout()` method.
- Otherwise, choose a different name for the branch you're creating.

#### CannotDeleteBranchError
This is raised when trying to delete a branch fails.
- Make sure the branch exists using the `branch()` method or `branches` variable.
- Make sure you're not on the branch you're trying to delete by checking the `current_branch` variable.
- If it still fails, the problem is elsewhere.

#### NoCommitsError
This is raised when trying to view a log with no commits
- You haven't committed any changes to this branch. Run the `stage_files()` and/or `commit()` methods, then try this again.

#### UnknownRevisionError
This is raised when a reset attempt fails.
- You're trying to reset to something that doesn't exist. Make sure the `commit` hash is correct.
- If it still doesn't work, try changing the `mode` to a different option (see the `reset()` method above for details).
- If it still fails, the problem is elsewhere in your code.

#### PushError
This is raised when pushing to the remote fails
- Make sure the `username` and `password` you passed in are correct.
- Make sure the `remote` and optionally, the `branch`, you're trying to push to are both correct.
- If it still fails, the problem is elsewhere in your code.

#### PullError
This is raised when pulling from a remote fails.
- Make the same checks as the `PushError` above.

#### MergeError
This is raised when trying to merge two branches fails.
- Make sure the `branch` you're trying to merge exists by running the `branch()` method.
- If you don't want to commit after the merge is complete, set `commit=True`. 
- If nothing is working, try running the `abort_merge()` method. This will undo it and you can try to fix your code before merging again.

#### ConflictError
This is raised when a merge conflict occurs.
- Fix the merge conflict, then run the `continue_merge()` method.
- Try the no-commit option by setting `commit=False`.
- If you can't fix it, run the `abort_merge()` method to reset to before the merge attempt. 

#### RemoveFailureError
This is raised when trying to remove files fails
- Change `cached`, `pathspec`, and/or `recursive` to their alternate options.
- If it still fails, the problem is elsewhere.

#### NotRepositoryError
This is raised when trying to perform operations in a directory that isn't a *Git* repository.
- Run the `init()` method to create a local repository.
- Run the `clone()` method to clone a remote repository to your local machine.
