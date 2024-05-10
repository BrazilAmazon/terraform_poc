import sys, os
os.environ['Test'] = "Ab"
first_name = sys.argv[1]
last_name = sys.argv[2]
print("Hello " + first_name + " " + last_name)
