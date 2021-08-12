#!/usr/bin/env python3

import argparse
import subprocess

# -3, -T, -S is not supported in rsync


def colon(path: str):
    flag = False

    if path.startswith(':'):
        return None
    if path.startswith('['):
        flag = True


    limit = len(path)
    for c in range(limit):
        if c < limit:
            if path[c] == '@' and path[c + 1] == '[':
                flag = True
            if path[c] == ']' and path[c + 1] == ':' and flag:
                return c + 1
        if path[c] == ':' and not flag:
            return c
        if path[c] == '/':
            return None

    return None


def make_cmd(path):
    n = colon(path)
    if n:
        cmd = ['ssh', path[0:n], 'test -d ' + "'" + path[n + 1:] + "'"]
    else:
        cmd = ['test', '-d', path]

    return cmd


if __name__ == '__main__':
    ssh_options = ''
    rsync_options = ['--copy-links', '--progress']
    recursive = False
    skip_dir_check = False

    parser = argparse.ArgumentParser()

    parser.add_argument('--skip-dir-check', action='store_true')

    parser.add_argument('-4', action='store_true')
    parser.add_argument('-6', action='store_true')
    parser.add_argument('-A', action='store_true')
    parser.add_argument('-B', action='store_true')
    parser.add_argument('-C', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-r', action='store_true')
    parser.add_argument('-q', action='store_true')
    parser.add_argument('-v', action='store_true')

    parser.add_argument('-c', nargs=1, type=str)
    parser.add_argument('-F', nargs=1, type=str)
    parser.add_argument('-i', nargs=1, type=str)
    parser.add_argument('-J', nargs=1, type=str)
    parser.add_argument('-l', nargs=1, type=int)
    parser.add_argument('-o', nargs=1, type=str)
    parser.add_argument('-P', nargs=1, type=int)

    parser.add_argument('srcs', nargs='+', type=str)
    parser.add_argument('dst', nargs=1, type=str)

    args = vars(parser.parse_args())

    if args['skip_dir_check']:
        skip_dir_check = True

    if args['4']:
        ssh_options += ' -4'
    if args['6']:
        ssh_options += ' -6'
    if args['A']:
        ssh_options += ' -o FowardAgent=Yes'
    if args['B']:
        ssh_options += ' -o BatchMode=Yes'
    if args['C']:
        ssh_options += ' -C'
    if args['p']:
        rsync_options += ['-p', '-t', '-U']
    if args['q']:
        rsync_options += ['-q']
    if args['r']:
        rsync_options += ['-r']
        recursive = True
    if args['v']:
        rsync_options += ['-v']

    if args['c']:
        ssh_options += f' -c {args["c"][0]}'
    if args['F']:
        ssh_options += f' -F {args["F"][0]}'
    if args['i']:
        ssh_options += f' -i {args["i"][0]}'
    if args['J']:
        ssh_options += f' -J {args["J"][0]}'
    if args['l']:
        bw = args["l"][0]
        if bw != 0:
            bw = bw // 8
            if bw == 0:
                bw = 1
        rsync_options += [f'--bwlimit={bw}']
    if args['o']:
        ssh_options += f' -o {args["o"][0]}'
    if args['P']:
        ssh_options += f' -p {args["P"][0]}'

    srcs = args['srcs']
    dst = args['dst']


    if not skip_dir_check:
        exist_dst = False
        cmd = make_cmd(dst[0])
        if cmd:
            try:
                subprocess.run(cmd, check=True)
                exist_dst = True
            except subprocess.CalledProcessError:
                pass

        for i, src in enumerate(srcs):
            if recursive:
                src = src.rstrip('/')
                srcs[i] = src
            if not src.endswith('/') and not exist_dst:
                cmd = make_cmd(src)
                try:
                    subprocess.run(cmd, check=True)
                    srcs[i] = src + '/'
                except subprocess.CalledProcessError:
                    pass

    rsync_cmd = ['rsync'] + rsync_options + ['-e'] + [f'ssh {ssh_options}'] + srcs + dst
    subprocess.run(rsync_cmd)
