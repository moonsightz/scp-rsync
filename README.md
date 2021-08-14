# scp-rsync

scp-rsync wrapper script.

[At OpenSSH 8.0 release](http://www.openssh.com/txt/release-8.0), scp has been declared as not recommended(the protocol is outdated). This is a script which behave like scp written in Python3 with rsync.

This script is written to use in interactive shell, not mission critical shell scripts because it is impossible to behave in the same way perfectly using rsync.

scp -3/-T/-S options are not supported.

In simple copy case, you can alias scp by this script.
```sh
# alias example
alias scp='~/local/bin/scp-rsync.py' # (sh-variant)
```

To behave like scp, commands to check whether sources/destination are directory or not may be issued.  If you want to skip, set `--skip-dir-check` (but the directory handling may differ from scp).
