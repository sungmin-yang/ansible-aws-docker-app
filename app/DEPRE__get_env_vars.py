#!/usr/bin/python3
# Read a credential file when using python scripts directly

import os, sys
import argparse

# Get three args {{POSTGRES_USER}} {{POSTGRES_PASSWORD}} {{POSTGRES_DB}}
parser = argparse.ArgumentParser()
parser.add_argument("-U", "--user", help="Type your DB user", required=True)
parser.add_argument("-P", "--password", help="Type your DB user\'s password", required=True)
parser.add_argument("-D", "--db", help="show program version", required=True)
args = parser.parse_args()


# with open('../.env', 'r') as f:
#     text = f.readlines()

# for line in text:
#     env_key, env_val = line.strip().split('=')
#     os.environ[env_key] = env_val
#     print(os.environ.get(env_key))

print(args.user)
print(args.password)

if __name__ == '__main__':
    print(123)