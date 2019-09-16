#!/usr/bin/env python3
#coding:utf-8

import json
import requests
import time
import sys

job = "http://jenkins.com/project/crm-merge-master-to-bugfix"
# group_list = ["cupid"]
# group_list = ["cupid", "crm", "crm-web", "crm_pad"]
group_list = sys.argv[1].split(",")

def get_hooks_list(private_token=token,per_page=per_page):
    projects_list = []  # 存projects的id
    for g in group_list:
        url = "%s/groups/%s/projects?private_token=%s&per_page=%s" % (base_url, g, private_token, per_page)
        r = requests.get(url)
        projects = json.loads(str(r.content, 'utf-8'))
        # print(projects)
        # print("project数：",len(projects))
        for p in projects:
            if p['path_with_namespace'].split('/')[0] in group_list:
                print(p['id'])
                projects_list.append(p["id"])
            # if p['path_with_namespace'].split('/')[0] not in group_list:
            #     projects_list.remove(p)

            # print('p:',p)

    return projects_list

def get_hooks(private_token=token):
    projects_list = get_hooks_list()
    # print(projects_list)
    for p in projects_list:
        print(p)
        url = "%s/projects/%s/hooks?private_token=%s" %(base_url, p, private_token)
        r = requests.get(url)
        hooks = json.loads(str(r.content, 'utf-8'))
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
            id = sorted(hooks_id)[-1]+1
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

            hook_url = "%s/projects/%s/hooks?private_token=%s" %(base_url, p, private_token)
            r = requests.post(hook_url,hook_info)
            result = json.loads(str(r.content, 'utf-8'))
            print('结果',result)

#    return hooks

def main():
    get_hooks()

if __name__ == '__main__':
    main()
