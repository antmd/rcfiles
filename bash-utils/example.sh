#!/usr/bin/env bash

read -r -d '' __usage <<-'EOF'
  -f --file  [arg] Filename to process. Required.
  -t --temp  [arg] Location of tempfile. Default="/tmp/bar"
EOF

read -r -d '' __helptext <<-'EOF'
This program does some stuff then exits.
EOF

# Optional cleanup function -- delete if not needed
function __cleanup() {
    info "Cleaning up!"
}

# Copy main.sh into your bash scripts folder
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/main.sh"


### Validation. Error out if the things required for your script are not present
##############################################################################

#[[ "${arg_f:-}" ]]     || help      "Setting a filename with -f or --file is required"


### MAIN
##############################################################################

info "Starting ${__base}"
