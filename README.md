# python_git_operation
使用python来调取gitlab的api做一些简单操作。

#add_hook_auto.py
自动为git的上的指定的项目组下所有项目添加webhook。
python add_hook_auto.py groups_list 

#add_hook_byhand.py
为指定的项目添加webhook
python add_hook_byhand.py project_name

#get_git_ssh.py
获取项目的ssh_url
python get_git_ssh.py repo_name groups_list

#settings.py
