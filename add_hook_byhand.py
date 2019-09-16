#!/usr/bin/env python3
#coding:utf-8

import json
import requests
import time
import sys


# project_name = "zhenai-cupid-login"
project_name = sys.argv[1]    # gitlab_name
# job = sys.argv[2]
job = "http://jenkins.com/project/%s" %(sys.argv[2])
# group_list = ["cupid"]
# group_list = ["cupid", "crm", "crm-web", "crm_pad"]
# group_list = sys.argv[1].split(",")

# 获取所有工程，工程较多，分页获取
def get_project_list(page, private_token=token, per_page=per_page):
    page = page
    projects_dict = {}
    url = "%s/projects?private_token=%s&per_page=%s&page=%s" % (base_url, private_token, per_page, page)
    r = requests.get(url)
    projects = json.loads(str(r.content, 'utf-8'))
    # print(projects)
    for p in projects:
        # print(type(p),p)
        projects_dict[p["name"]] = p['id']

    return projects_dict

# 统计所有工程
def get_project_id(name=project_name):
    projects_dict = {}
    page = 6
    project_name = name
    for i in range(1,page):
        project = get_project_list(i)
        projects_dict.update(project)

    project_id = projects_dict[project_name]

    return project_id

def add_hook(private_token=token):
    project_id = get_project_id()
    url = "%s/projects/%s/hooks?private_token=%s" % (base_url, project_id, private_token)
    r = requests.get(url)
    hooks = json.loads(str(r.content, 'utf-8'))
    # print(hooks)
    hooks_list = []
    hooks_id = []
    for h in hooks:
        hooks_list.append(h['url'])
        hooks_id.append(h['id'])
    # print('hook_list:',hooks_list)
    # print('hook_id:',hooks_id)
    if job in hooks_list:
        print("hook is exist...")
    elif len(hooks_list) == 0:
        id = 1000
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split()
        d = '%sT%sZ' % (t[0], t[-1])
        hook_info = {
            "id": id,
            "url": job,
            "project_id": p,
            "push_events": 'true',
            "issues_events": 'false',
            "merge_requests_events": 'false',
            "tag_push_events": 'false',
            "note_events": 'false',
            "job_events": 'false',
            "pipeline_events": 'false',
            "wiki_page_events": 'false',
            "enable_ssl_verification": 'true',
            "created_at": d
        }

        hook_url = "%s/projects/%s/hooks?private_token=%s" % (base_url, p, private_token)
        r = requests.post(hook_url, hook_info)
        result = json.loads(str(r.content, 'utf-8'))
        print('结果', result)
    else:
        id = sorted(hooks_id)[-1] + 1
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split()
        d = '%sT%sZ' % (t[0], t[-1])
        hook_info = {
            "id": id,
            "url": job,
            "project_id": p,
            "push_events": 'true',
            "issues_events": 'false',
            "merge_requests_events": 'false',
            "tag_push_events": 'false',
            "note_events": 'false',
            "job_events": 'false',
            "pipeline_events": 'false',
            "wiki_page_events": 'false',
            "enable_ssl_verification": 'true',
            "created_at": d
        }

        hook_url = "%s/projects/%s/hooks?private_token=%s" % (base_url, p, private_token)
        r = requests.post(hook_url, hook_info)
        result = json.loads(str(r.content, 'utf-8'))
        print('结果', result)

def main():
    add_hook()

if __name__ == '__main__':
    main()
