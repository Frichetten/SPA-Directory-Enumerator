#!/usr/bin/python3
# Written by Nick Frichette
# I take no responsibility for what you do with this tool
# Intended for security research only
import requests
import re # Regular Expressions
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Incorrect usage! Try: ./enumerator.py https://website.com")
    exit()

link = sys.argv[1]
r = requests.get(link)

# This will grab all the bundles for inspection
a = re.findall(r'src=("|\')(.*?)js("|\')', r.text)

for i, item in enumerate(a):
    if item[1].find('http') != 0:
        a[i] = link + '/' + item[1] + 'js'
    else:
        a[i] = item[1] + 'js'

print("Enumerating Bundles")
print("-------------------")
for item in a:
    print(item)

if '-s' in sys.argv:
    strings = []
    for item in a:
        r = requests.get(item)
        c = re.findall(r'\[("|\')(.*?)("|\')\]', r.text)
        for string in c:
            strings.append(string[1])

    strings = list(set(strings))
    
    for item in strings:
        print(item)
else:
    # For each of these bundles lets scan for directories
    directories = []
    #directories.append("/")
    for item in a:
        r = requests.get(item)
        c = re.findall(r'("|\')/(.*?)("|\')', r.text)
        for direc in c:
            if len(direc[1]) > 0:
                if direc[1][0] == '/':
                    directories.append(direc[1])
                else:
                    directories.append("/"+direc[1])

    directories = list(set(directories))

    print("")
    print("Enumerating Routes")
    print("------------------")
    for item in directories:
        print(item)
