import requests
from bs4 import BeautifulSoup




class image_catcher(object):
	def __init__(self, email, password):
		self.email = email
		self.password = password
		self.s = None
		self.s = self.login_user()
	
	 def login_user():
		s = requests.session()
		login_data = {'email': self.email, 'password': self.password}
		s.post('http://www.zhihu.com/login', login_data)
		return s
	
	def get_image_contents(url):
		r = self.s.get(url)
		content = r.content
		soup = BeautifulSoup(content, 'lxml')
		images = soup.find_all('img')
		i = 0
		for image in images:
			image_path = image.get('data-original')
			name = './image/' + str(i) + '.jpg'
			save_image(image_path, name)
			i += 1

	def save_image(image_path, name):
		if image_path:
			image_response = requests.get(image_path)
			if not image_response.status == 200: return
			image_content = image_response.content
			if image_content and i%2 == 0:
				with(open(name, 'wb')) as f:
					f.write(image_content)
				print 'write iamge done, %s' %name
