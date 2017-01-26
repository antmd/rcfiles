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

RcFiles=$(find . -maxdepth 1 -name '.*' | tail -n +2)

cd $HOME

for f in ${RcFiles}; do
    RcFile=${f#./}

	[[ "$RcFile" = ".git" ]] && continue
	
    if [[ -e "$f" ]]; then
        echo "Moving ~/$RcFile to ~/$RcFile.moved"
        mv "$RcFile" "$RcFile.moved"
    fi

    ln -s "$ScriptDir/$RcFile" $RcFile
done

if [[ ! -d "profile.d" ]]; then
    ln -s "$ScriptDir/profile.d" .
fi

# vim:sts=4:ts=4:sw=4:
