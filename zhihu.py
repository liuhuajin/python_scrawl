import requests

s = requests.session()
login_data = {'email':'liuhuajinbenton@163.com', 'password':'7443923555'}
s.post('http://www.zhihu.com/login', login_data)
r = s.get('http://zhihu.com')
print r.status_code
