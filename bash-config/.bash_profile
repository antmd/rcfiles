# On most unixes, .bash_profile is skipped for a new terminal window, so we put
# all terminal customisation in .bashrc, but put guards around to check for logon shell
if [ -f ~/.bashrc  ]; then
   source ~/.bashrc
fi

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"

if [[ -n "$DISPLAY" && -e ~/.Xmodmap ]]; then
    xmodmap ~/.Xmodmap
fi
