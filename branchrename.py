from github import Github, GithubException

import settings


g = Github(settings.GITHUB_TOKEN)


oldrepo = 'master'
newrepo = settings.BRANCH

ulogin = g.get_user().login

# We only want repos that we own and are not forks.
for repo in g.get_user().get_repos():
  if ulogin == repo.owner.login and repo.fork == False:

    try:
      branch = repo.get_branch(branch=oldrepo)

    except GithubException:
      continue # We expect this if there's no master branch.

    print(repo.owner.login + "/" + repo.name, end=" ")

    # If we already have a branch named after the new branch, skip this repo.
    try:
      branch = repo.get_branch(branch=newrepo)
      if branch:
        print('Branch "%s" already exists, skipping' % newrepo)
        continue

    except GithubException:
      pass # We expect this.

    if branch.protected:
      print('Branch "%s" is protected, skipping' % oldrepo)
      continue

    src = repo.get_git_ref('heads/%s' % oldrepo)

    print(src.object.sha, oldrepo, "=>", newrepo)

    # Create a new brach that points to the same commit as the existing branch.
    repo.create_git_ref('refs/heads/%s' % newrepo, sha=src.object.sha)

    # Delete the old branch.
    src.delete()
