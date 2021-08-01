class Error(Exception):
    '''Base class for other exceptions'''
    pass

class RemoteNotExistsError(Error):
    '''Raised when trying to change a remote that doesn't exist'''

    def __init__(self, remote, message="Cannot alter remote that does not exist"):
        self.remote = remote
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.remote} -> {self.message}'

class RemoteAlreadyExistsError(Error):
    '''Raised when trying to add a remote that already exists'''

    def __init__(self, remote, message="Cannot add a remote that already exists"):
        self.remote = remote
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.remote} -> {self.message}'

class BranchNotExistsError(Error):
    '''Raised when trying to checkout a branch that doesn't exist'''

    def __init__(self, branch, message="Cannot change to a branch that doesn't exist"):
        self.branch = branch
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.branch} -> {self.message}'

class BranchAlreadyExistsError(Error):
    '''Raised when trying to checkout a new branch that already exists'''

    def __init__(self, branch, message="Cannot create a new branch where one with the same name already exists"):
        self.branch = branch
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.branch} -> {self.message}'

class CannotDeleteBranchError(Error):
    '''Raised when deleting a branch fails'''

    def __init__(self, branch, message="Failed to delete the specified branch"):
        self.branch = branch
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.branch} -> {self.message}'

class NoCommitsError(Error):
    '''Raised when trying to view a log for a branch that has no commits'''

    def __init__(self, message="Cannot view log for an empty branch"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class UnknownRevisionError(Error):
    '''Raised when a reset fails due to commit not existing'''

    def __init__(self, commit, message="Cannot reset to a commit that does not exist"):
        self.commit = commit
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.commit} -> {self.message}'

class PushError(Error):
    '''Raised when pushing to a remote fails'''

    def __init__(self, remote, branch, message="Pushing to remote on specified branch failed"):
        self.remote = remote
        self.branch = branch
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.remote}, branch {self.branch} -> {self.message}'

class MergeError(Error):
    '''Raised when trying to merge two branches fails'''

    def __init__(self, branch, message="Merging the specified branch failed"):
        self.branch = branch
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.branch} -> {self.message}'

class PullError(Error):
    '''Raised when pulling from the remote fails'''

    def __init__(self, message="Pulling from remote failed"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class RemoveFailureError(Error):
    '''Raised when trying to remove a file fails'''

    def __init__(self, message="Removing specified file(s) failed"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'

class NotRepositoryError(Error):
    '''Raised when trying to perform git operations in a folder that is not a repository'''

    def __init__(self, path, message="Folder is not a git repository"):
        self.path = path
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.path} -> {self.message}'

class ConflictError(Error):
    '''Raised when a merge conflict occurs'''

    def __init__(self, message="Merge conflict occurred. Fix conflict or use abort_merge"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}'