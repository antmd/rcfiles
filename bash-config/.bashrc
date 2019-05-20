
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

#DebugStartup=1
function dlog() {
    if [[ -n "${DebugStartup:-}" ]]; then
        echo "$@" 1>&2
    fi
}

# OS Identification
OS_WIN=
OS_MAC=
OS_LINUX=
CYGWIN=
OsProfileDir=

if [[ $(uname -s) =~ ^CYGWIN*  ]]; then
    CYGWIN=1
    OS_WIN=1
    OsProfileDir=Cygwin
fi
export CYGWIN

os_id=$(echo $OSTYPE | tr '[[:upper:]]' '[[:lower:]]')
if [[ "$os_id" =~ ^darwin*   ]]; then
    export OS_MAC=1
    OsProfileDir=Mac
elif [[ "$os_id" =~ ^linux*   ]]; then
    export OS_LINUX=1
    OsProfileDir=Linux
fi


# Source the contents of the ~/profile.d directory
# Source the contents of the ~/profile.d/Local directory
ProfileDirs="${HOME}/profile.d"
ProfileDirs="${ProfileDirs} ${HOME}/profile.d/Local"
if [[ -n "$OsProfileDir" ]]; then
    ProfileDirs="${ProfileDirs} ${HOME}/profile.d/${OsProfileDir}"
fi
# If we are an interactive shell, source the contents of ~/profile.d/Interactive
if [[ $- == *i*  ]]; then
    ProfileDirs="${ProfileDirs} ${HOME}/profile.d/Interactive"
fi

for ProfileDir in  $ProfileDirs; do 
    if [[ -d "${ProfileDir}" ]]; then
        for f in $( ls  -1H "${ProfileDir}" ) ; do
            if [[ -f "${ProfileDir}/$f" && $f =~ ^[[:digit:]]+-[-_[:alnum:]]+$ ]]; then
                dlog "Sourcing ${ProfileDir}/$f"
                source "${ProfileDir}/$f"
            fi
        done
    else
        dlog "Skipping missing dir ${ProfileDir}"
    fi
done

unset DebugStartup

