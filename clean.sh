#!/usr/bin/env bash
#
# cleans all generated code in the project


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
    __echo_to_stderr "Cannot determine where script is running from"
    exit 1
fi

# find and delete the compiled files
COMPILED_FILES=$(find "$SCRIPT_DIRECTORY" -type f | grep "^.*\.pyc$")
IFS=$'\n'$'\r'
for COMPILED_FILE in $COMPILED_FILES
do
    rm --force "$COMPILED_FILE"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete compiled file $COMPILED_FILE"
        exit 1
    fi
done

# find and delete any python3 cached directories
PYCACHE_DIRECTORIES=$(find "$SCRIPT_DIRECTORY" -type d | grep "^.*\__pycache__\$")
IFS=$'\n'$'\r'
for PYCACHE_DIRECTORY in $PYCACHE_DIRECTORIES
do
    rm --recursive --force "$PYCACHE_DIRECTORY"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete pycache directory $PYCACHE_DIRECTORY"
        exit 1
    fi
done

# find and delete the package directories
PACKAGE_DIRECTORIES=$(find "$SCRIPT_DIRECTORY" -type d | grep "^.*\.egg-info\$")
IFS=$'\n'$'\r'
for PACKAGE_DIRECTORY in $PACKAGE_DIRECTORIES
do
    rm --recursive --force "$PACKAGE_DIRECTORY"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete package directory $PACKAGE_DIRECTORY"
        exit 1
    fi
done

# delete the distribution directory
if [ -d "$SCRIPT_DIRECTORY/dist" ]
then
    rm --recursive --force "$SCRIPT_DIRECTORY/dist"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete distribution folder"
        exit 1
    fi
fi

# delete the coverage file
if [ -f "$SCRIPT_DIRECTORY/.coverage" ]
then
    rm --force "$SCRIPT_DIRECTORY/.coverage"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete coverage file .coverage"
        exit 1
    fi
fi

# delete the coverage report
if [ -d "$SCRIPT_DIRECTORY/cover" ]
then
    rm --recursive --force "$SCRIPT_DIRECTORY/cover"
    if [ $? -ne 0 ]
    then
        __echo_to_stderr "Cannot delete coverage report folder cover"
        exit 1
    fi
fi

# exit with appropriate code
exit 0
