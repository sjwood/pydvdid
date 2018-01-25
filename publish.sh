#!/usr/bin/env bash
#
# Publishes the project to PyPI and GitHub


# utility function for writing to stderr
function __echo_to_stderr() {
    if [ $? -ne 0 ]
    then
        return 1
    fi

    echo "$@" 1>&2
}

# test for existence of python
PYTHON_PATH=$(which python)
if [ $? -ne 0 ]
then
    __echo_to_stderr "Python is not installed"
    exit 1
fi

# where is this script executing?
SCRIPT_DIRECTORY=$(readlink -f "$(dirname "$0")")
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot determine where script is running from"
    exit 1
fi

# what version are we publishing?
VERSION=$(cat setup.py | sed -n 's/^[ ]*version=\"\([0-9]\.[0-9]\)\".*/\1/p')
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot determine version to publish"
    exit 1
fi
if [ -z "$VERSION" ]
then
    __echo_to_stderr "Version needs to be of the format [0-9].[0-9]"
    exit 1
fi

# package distributions
python "$SCRIPT_DIRECTORY/setup.py" sdist
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot package source distribution"
    exit 1
fi
python "$SCRIPT_DIRECTORY/setup.py" bdist_wheel --universal
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot package wheel distribution"
    exit 1
fi

# upload to PyPI test site
twine upload -r pypitest dist/*
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot upload to PyPI test"
    exit 1
fi

# upload to PyPI
twine upload -r pypi dist/*
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot upload to PyPI"
    exit 1
fi

# publish to git
git tag --annotate v$VERSION --message="v$VERSION released to PyPI"
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot tag release in git"
    exit 1
fi
git push origin v$VERSION
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot push release to git origin"
    exit 1
fi

exit 0
