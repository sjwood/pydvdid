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

# where is this script executing?
SCRIPT_DIRECTORY=$(readlink -f "$(dirname "$0")")
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot determine where script is running from."
    exit 1
fi

# construct packaged code location
CODE_DIRECTORY="$SCRIPT_DIRECTORY/pydvdid"
if [ $? -ne 0 ]
then
    __echo_to_stderr "Cannot construct code directory."
    exit 1
fi

# invoke compileall module for code location
python -m compileall $CODE_DIRECTORY
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]
then
    __echo_to_stderr "Python compileall returned exit code $EXIT_CODE."
    exit 1
fi
