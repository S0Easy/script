import gitlab
import datetime
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
gitlab_url = "http://10.10.10.22/"
token = "-xxVsB6xy4ayF-YmsYh4"
gitlab.Gitlab(gitlab_url, token).projects.get("2")

