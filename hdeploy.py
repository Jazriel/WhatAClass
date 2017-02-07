import subprocess

res = subprocess.Popen('coverage run test.py', shell=True, stdout=subprocess.PIPE)
res.communicate(input='\n')

if res.returncode is 0:
    subprocess.Popen('gunicorn start:app -p wac.pid -D', shell=True)


