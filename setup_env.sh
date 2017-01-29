#!/bin/bash - 
#===============================================================================
#
#          FILE: setup_env.sh
# 
#   DESCRIPTION: Create the env from the rcfiles in this directory by symlinks
# 
#       CREATED: 2014-10-21
#
#        AUTHOR: Anthony Dervish
#
#===============================================================================

set -o nounset                              # Treat unset variables as an error

ScriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
cd "$ScriptDir"

if ! [[ -d bin/stow ]]; then
    cd bin
    tar zxvf stow.tgz
    cd ..
fi

Stow=bin/stow/stow

RcFiles=$(find . -maxdepth 1 -type d -name '*-config')

for ConfigDir in ${RcFiles}; do
    ConfigDir=${ConfigDir#./}
    echo "Install ${ConfigDir}"
    $Stow -v --target="${HOME}" -S "${ConfigDir}"
done

# vim:sts=4:ts=4:sw=4:
