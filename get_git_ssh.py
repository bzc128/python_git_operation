#!/usr/bin/env python3
#coding:utf-8

import json
import requests
import re
import sys


group_list = sys.argv[2].split(",")
for g in group_list:
    print(type(g),g)

# 根据groups_list遍历，找出所有ssh_url_to_repo
def get_ssh_url_list(private_token=token,per_page=per_page):
    projects_list = []
    for g in group_list:
        url = "%s/groups/%s/projects?private_token=%s&per_page=%s" % (base_url, g, private_token, per_page)
        r = requests.get(url)
        projects = json.loads(str(r.content, 'utf-8'))
        for p in projects:
            print(type(p),p)
            projects_list.append(p["ssh_url_to_repo"])

    return projects_list

# 根据repo_name匹配，找到对应的ssh_url_to_repo
def get_ssh_url(repo_name):
    name = repo_name
    repo_url = get_ssh_url_list()
    for i in range(len(repo_url)):
        if re.search(name,repo_url[i]) is not None:
            return repo_url[i]

def main():
    name = sys.argv[1]
    ssh_url = get_ssh_url(name)
    return ssh_url

if __name__ == '__main__':

    a = main()
    print(a)
