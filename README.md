# branchrename

This script goes through all repo that you own on GitHub that are not forks and renames any branches named `master` to a new name (defaults to `release`).

Usage:

1. [Create an auth token for GitHub](https://github.com/settings/tokens), with the `repo` privileges enabled.

1. Rename `settings.example.py` to `settings.py`. Enter the token and your user or organization. You can customize the new branch name.

1. Install the dependencies: `pip3 install -r requirements.txt`

1. Run the script: `python3 branchrename.py`

1. After you've run this script, you'll need to rename any repos that are checked out locally. Run this command from the directory of any repo you have checked out locally to rename the branch and track from origin.

`git checkout master && git fetch && git branch -m release && git branch release -u origin/release`
