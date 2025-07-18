import sys
flash = 'flashplayer_sa.exe'

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [url]')
    sys.stdin.read(1)

script = f'\"{flash}\" {sys.argv[1]}'

import subprocess
proc = subprocess.Popen(script, start_new_session=True)
proc.detach()
