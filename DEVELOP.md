Development
===========

Introduction
------------
This project uses a combination of virtualenv and zc.buildout to setup a self
contained development environment. It's designed so I can basically go to any
of my computers, clone the upstream repository, source the bootstrap script,
and begin working.

Also, git-flow is being used to manage the general workflow of the repository,
so please install it and stick with it.


Bootstrapping
-------------
With virtualenv and zc.buildout:
% source bootstrap
% buildout

With zc.buildout only:
% python bootstrap.py -d
% bin/buildout


Web Resources
-------------
Project website, bug database, and GIT repository is at:
http://github.com/mvillalba/python-ant

Project documentation (Sphinx) is at:
NOT-HOSTED-ANYWHERE-YET

Backup GIT repositories:
https://gitorious.org/python-ant/python-ant
http://repo.or.cz/w/python-ant.git


Release Checklist
-----------------
 * Deactivate virtualenv environment, if active
 * Clone upstream to clean directory (setup all remotes!)
 * Bootstrap environment
 * Start release branch (git-flow)
 * Set/check version number (setup.py, project's __init__.py, docs)
 * Run pylint
 * Run importchecker
   % importchecker src
 * Run pep8
   % pep8 -r src --count --statistics
 * Run test suite and check test coverage
   % nosetests --with-coverage --cover-inclusive --cover-erase
 * Freeze dependencies' version numbers in buildout.cfg and setup.py
 * Check bug database for open issues/bugs
 * Build documentation
 * Check documentation (coverage, grammar, contents, etc)
 * Update CHANGES.md
 * Update copyright statements if new year
 * Update setup.py
 * Create distribution bundles
   % buildout setup . sdist bdist_egg
 * Check dist/* files (no nuclear launch codes, all files present, do they work
   in a separate virtualenv with pip?)
 * Upload to PyPI
   % buildout setup . sdist bdist_egg register upload
 * Check package page in PyPI (readme, download links)
 * If first release, delete dummy "develop" version from PyPI
 * Re-test release in a clean environment, installing from the cheeseshop
 * Finish git-flow release and add release tag and commit release
 * Push upstream (GitHub master, gitorious backup, odin backup)
   % git push --all all && git push --tags all
 * Close old feature branches (GitHub)
   % git push origin :feature/{NAME-HERE}
 * Upload dist files to GitHub and download them to check integrity
 * Unfreeze version numbers from setup.py and buildout.cfg
 * Set version number to "develop" (setup.py, project's __init__.py, docs)
 * Go back to old development repo and update everything
   % git checkout develop && git pull origin develop
   % git checkout master && git pull origin master
 * Upload built documentation
 * Make public announcement, if necessary


Release Notes
-------------
If releasing anything but a final version, skip registering and uploading to
the cheeseshop.

If releasing a .devX version, some steps may be skipped from the release
checklist. In particular, .devX versions should be treated mostly as an
internal thing and thus, should generally not be published nor uploaded to
GitHub.

