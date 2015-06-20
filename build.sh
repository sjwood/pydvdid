#!/usr/bin/env bash
#
# Compiles python to check for syntactic correctness


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

# is globstar option already set?
shopt -q globstar
GLOBSTAR_SET=$?

# set globstar option (if it has not already been)
if [ $GLOBSTAR_SET -ne 0 ]
then
    shopt -s globstar
fi

# invoke compileall module for all python files in the directory
python -m compileall -f $SCRIPT_DIRECTORY/**/*.py
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]
then
    __echo_to_stderr "Python compileall returned exit code $EXIT_CODE"
fi

# reset globstar option (if it was not originally set)
if [ $GLOBSTAR_SET -ne 0 ]
then
    shopt -u globstar
fi

# exit with appropriate code
if [ $EXIT_CODE -ne 0 ]
then
    exit 1
fi
exit 0
