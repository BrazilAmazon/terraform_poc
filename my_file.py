
import os
name = 'my_name'
value = 'my_value'
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'{name}={value}', file=fh)
