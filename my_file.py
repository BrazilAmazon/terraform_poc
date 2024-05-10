import sys, os, subprocess

cmd='echo "TEST=AB" >> $GITHUB_OUTPUT'
subprocess.call([str(cmd)], shell=False)
first_name = sys.argv[1]
last_name = sys.argv[2]
print("Hello " + first_name + " " + last_name)
