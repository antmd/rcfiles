# On most unixes, .bash_profile is skipped for a new terminal window, so we put
# all terminal customisation in .bashrc, but put guards around to check for logon shell
if [ -f ~/.bashrc  ]; then
   source ~/.bashrc
fi

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
