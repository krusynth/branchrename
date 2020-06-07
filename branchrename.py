from github import Github, GithubException

import settings


g = Github(settings.GITHUB_TOKEN)


existing_branch_name = 'master'
new_branch_name = settings.BRANCH

ulogin = g.get_user().login

# We only want repos that we own and are not forks.
for repo in g.get_user().get_repos():
  if ulogin == repo.owner.login and repo.fork == False:

    try:
      branch = repo.get_branch(branch=existing_branch_name)

    except GithubException:
      continue # We expect this if there's no master branch.

    print(repo.owner.login + "/" + repo.name, end=" ")

    if repo.archived:
      print('Repository is archived so branch name cannot be changed.')
      continue

    # If we already have a branch named after the new branch, skip this repo.
    try:
      branch = repo.get_branch(branch=new_branch_name)
      if branch:
        print('Branch "%s" already exists, skipping' % new_branch_name)
        continue

    except GithubException:
      pass # We expect this.

    if branch.protected:
      print('Branch "%s" is protected, skipping' % existing_branch_name)
      continue

    src = repo.get_git_ref('heads/%s' % existing_branch_name)

    print(src.object.sha, existing_branch_name, "=>", new_branch_name)

    # Create a new brach that points to the same commit as the existing branch.
    repo.create_git_ref('refs/heads/%s' % new_branch_name, sha=src.object.sha)

    # Delete the old branch.
    src.delete()
