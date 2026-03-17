#!/usr/bin/python
#
# List all files that have ever been committed in this repository, in any
# commit in any branch.

import pygit2
import stat

def list_all_files(repo_path):
    repo = pygit2.Repository(repo_path)
    walker = repo.walk(repo.head.hex, pygit2.GIT_SORT_NONE)
    files = {}
    for ref in repo.listall_references():
        if not ref.startswith('refs/heads'):
            continue
        walker.push(repo.lookup_reference(ref).hex)
    for ref in walker:
        add_tree(repo, ref.tree, '', files)
    files = files.keys()
    files.sort()
    return files

def add_tree(repo, tree, prefix, files):
    for file in tree:
        fullname = '%s/%s' % (prefix, file.name)
        if stat.S_ISDIR(file.filemode):
            add_tree(repo, file.to_object(), fullname, files)
        else:
            files[fullname] = 1

print "\n".join(list_all_files('.'))
