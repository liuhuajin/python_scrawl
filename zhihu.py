import requests
from bs4 import BeautifulSoup

s = requests.session()
login_data = {'email':'liuhuajinbenton@163.com', 'password':'7443923555'}
s.post('http://www.zhihu.com/login', login_data)
r = s.get('http://zhihu.com/question/23978389')
content = r.content
soup = BeautifulSoup(content, 'lxml')
images = soup.find_all('img')
i = 0
for image in images:
	image_path = image.get('data-original')
	if image_path:
		image_response = requests.get(image_path)
		print image_response.status_code
		image_content = image_response.content
		if image_content:
			with(open('./image/image_'+str(i)+'.jpg', 'wb')) as f:
				f.write(image_content)
			print 'write iamge done, %s' %i
			i += 1
