#!/usr/bin/env bash
#
# Discovers and runs tests in the project


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

# test for existence of nose
NOSE_PATH=$(which nosetests)
if [ $? -ne 0 ]
then
    __echo_to_stderr "Nose is not installed"
    exit 1
fi

# test for existence of coverage
COVERAGE_PATH=$(which coverage)
if [ $? -ne 0 ]
then
    __echo_to_stderr "Coverage is not installed"
    exit 1
fi

# where is this script executing?
SCRIPT_DIRECTORY=$(readlink -f "$(dirname "$0")")
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot determine where script is running from"
    exit 1
fi

# set script directory as current directory
cd $SCRIPT_DIRECTORY

# find and execute tests
nosetests --with-coverage --cover-branches --cover-inclusive --cover-erase
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]
then
    __echo_to_stderr "Nose returned exit code $EXIT_CODE"
fi

# exit with appropriate code
if [ $EXIT_CODE -ne 0 ]
then
    exit 1
fi
exit 0
