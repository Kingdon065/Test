#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import subprocess

try:
    completed = subprocess.run(
        'echo to stdout; echo to stderr 1>&2; exit 1',
        check=True,
        shell=True,
        stdout=subprocess.PIPE,

    )
except subprocess.CalledProcessError as err:
    print(f'ERROR: {err}')
else:
    print(f'returnCode: {completed.returncode}')
    print('Have {} bytes in stdout: {!r}'.format(
        len(completed.stdout),
        completed.stdout.decode('utf-8')
    ))