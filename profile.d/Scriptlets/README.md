Scriptlets
----------

Scriptlets are small scripts that can be

* Sourced to set themselves up
* Run as binaries to do some action

These scripts get sourced automatically by 30-Scriptlets

They must not have any extension

** WARNING: Scriptlets *MUST* check for being 'sourced' or 'run', as follows: **


    if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
        #--------------------------------------------------------------------------------
        # The script is being sourced: set up completion
        #--------------------------------------------------------------------------------

        <SET UP THE COMMAND>

    else
        #--------------------------------------------------------------------------------
        # The script is being run from the command-line... do the delete
        #--------------------------------------------------------------------------------

        <RUN THE COMMAND>
    fi
