# coding=utf-8
# 自动合并dev到其他分支， 当合并失败删除merge请求
import sys
import datetime
import urllib.request
import requests
import gitlab   
from requests.api import head, request

#项目名和项目ID
project_name = "java01"
project_list = [2]

#生成gitlab对象
gitlab_url = "http://10.10.10.22"
token = "52qzzWMCs12noYNUoFLV"
old_branch='hotfix'
new_branchs=["DEV"]
# new_branchs=["DEV", "prod", "produce", "master"]
# 验证登录
gl = gitlab.Gitlab(gitlab_url, token)
print(gl)

for project_id in project_list:
    project = gl.projects.get(project_id)
    print(f"-----------------------{project_id}")
    for proj in new_branchs:
        print(f"正在合并的项目：{project_name}的{old_branch}分支到{proj}")
        # mr合并请求的对象
        mr = None
 #       try:
            # 创建mr
        print("++++++++++++++++++开始处理合并请求++++++++++++++++++++++=")
        mr = project.mergerequests.create({
                'source_branch': old_branch, 
                'target_branch': proj,
                'title': f"{old_branch} to {proj}" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        # 接受合并请求
        print("---------------------------------"*20)
        url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr.id}/merge"
        print(f'url: {url}')
        headers = {
            "PRIVATE-TOKEN":token
        }
        
        req = urllib.request.Request(url=url, headers=headers, method="PUT")
        # print()
        resp = urllib.request.urlopen(req)
        # print("************************************"*20)
        # resp = requests.put(url=url, headers=headers)
        print(resp)
        print(f"合并到分支{proj}成功,结束...\r\n")
        # except Exception as e:
        #     print(f"合并出错,可能有冲突未解决或者{old_branch}分支并没有更新,异常信息：\r\n")
        #     print(e)
        #     # 把刚创建的mr请求删除
        #     # v4版本支持 project.mergerequests.delete(mr.id)
