# scp-rsync

scp wrapper by rsync.

[At OpenSSH 8.0 release](http://www.openssh.com/txt/release-8.0), scp is not recommended(the protocol is outdated). This is a wrapper script of scp written in Python3 with rsync.

This wrapper is written to use in interactive shell, not mission critical shell scripts because it is impossible to behave in the same way perfectly using rsync.
