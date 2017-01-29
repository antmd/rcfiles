
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Source the contents of the ~/profile.d directory

ProfileDir="${HOME}/profile.d"
for f in $( ls  -1H "${ProfileDir}" ) ; do
    if [[ -f "${ProfileDir}/$f" && $f =~ ^[[:digit:]]+-[[:alnum:]]+$ ]]; then
        source "${ProfileDir}/$f"
    fi
done

# Source the contents of the ~/profile.d/Local directory

LocalDir="${HOME}/profile.d/Local"
for f in $( ls  -1H "${LocalDir}" ) ; do
    if [[ -f "${LocalDir}/$f" && $f =~ [[:digit:]]+-[[:alnum:]]+ ]]; then
        source "${LocalDir}/$f"
    fi
done

# If we are an interactive shell, source the contents of ~/profile.d/Interactive
if [[ $- == *i*  ]]; then
    # Interactive shell only
    # To test for a 'login shell' use if shopt -q login_shell; then...
    InteractiveDir="${HOME}/profile.d/Interactive"
    for f in $( ls  -1H "${InteractiveDir}" ) ; do
        if [[ -f "${InteractiveDir}/$f" && $f =~ [[:digit:]]+-[[:alnum:]]+ ]]; then
            source "${InteractiveDir}/$f"
        fi
    done
fi

export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting
