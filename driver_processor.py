from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.common.keys import Keys
import time
import pathlib
from random import randint
from selenium.webdriver.remote.webelement import WebElement
import os.path

from selenium.webdriver.common.action_chains import ActionChains



import numpy as np
import scipy.interpolate as si



class Driver():
	def __init__(self, profile, browser):
		self.profile = profile
		self.browser = browser

	def play(self, file, description = '.'):
		JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

		def drop_files(element, files, offsetX=0, offsetY=0):
			driver = element.parent
			isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
			paths = []
    
			# ensure files are present, and upload to the remote server if session is remote
			for file in (files if isinstance(files, list) else [files]) :
				if not os.path.isfile(file) :
					raise FileNotFoundError(file)
				paths.append(file if isLocal else element._upload(file))
    
			value = '\n'.join(paths)
			elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
			elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

		WebElement.drop_files = drop_files



		def isElementExist(browser, element):
			flag = True
			try:
				browser.find_element_by_css_selector(element)
				return flag
			except:
				flag = False
				return flag

		def upload_video(browser, description = description):
			i = 0
			i+=1
			print(i)
			path = str(pathlib.Path(__file__).parent.absolute())
			i+=1
			print(i)
			try:
				WebDriverWait(browser, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, 'upload-wrapper'))) 
				upload_button = browser.find_element_by_class_name('upload-wrapper') 
				i+=1
				print(i)
				upload_button.click()
			except:
				#WebDriverWait(browser, 10).until(
				#	EC.presence_of_element_located((By.CLASS_NAME, 'UploadContainer'))) 
				#upload_button = browser.find_element_by_class_name('UploadContainer') 
				#i+=1
				#print(i)
				#upload_button.click()

				self.browser.get('https://www.tiktok.com/upload?lang=ru-RU')

			WebDriverWait(browser, 100).until(
				EC.presence_of_element_located((By.CLASS_NAME, 'jsx-3829822639'))) 
			i+=1
			print(i)
			video_upload_button = browser.find_element_by_class_name('jsx-3829822639')
			#video_upload_button.click()
			#video_upload_button.send_keys(path + 'test2.mp4')
			video_upload_button.drop_files(path + f'\\{file}')

			i+=1
			print(i)

			#WebDriverWait(browser, 100).until(
			#	EC.presence_of_element_located((By.CLASS_NAME, 'jsx-2053310055 preview')))
			try:
				print('b')
				WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'progress-container'))) 
				print('b')
			except: print('d')	
			print('s')
			WebDriverWait(browser, 100).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'progress-container')))
			print('s')
			i+=1
			print(i)
			time.sleep(1)
			video_title_input = browser.find_element_by_class_name('public-DraftEditor-content') 
			video_title_input.send_keys(description)
			time.sleep(1.2)
			post_button = browser.find_element_by_class_name('btn-post') 
			i+=1
			print(i)
			post_button.click()
			i+=1
			print(i)



		time.sleep(randint(1,3))

		self.browser.header_overrides = {
									'method': 'GET',
									'accept-encoding': 'gzip, deflate, br', 
									'referrer': 'https://www.tiktok.com/trending',
									'upgrade-insecure-requests': '1'
									}

		self.browser.get('https://www.tiktok.com/')

		upload_video(self.browser)

		time.sleep(15)
		



	def auth(self, email = None, password = None, auth_status = None, triggerauth = 0):

		def isElementExist(browser, element):
			flag = True
			try:
				browser.find_element_by_css_selector(element)
				return flag
			except:
				flag = False
				return flag

		

		time.sleep(randint(1,3))

		self.browser.header_overrides = {
									'method': 'GET',
									'accept-encoding': 'gzip, deflate, br', 
									'referrer': 'https://www.tiktok.com/trending',
									'upgrade-insecure-requests': '1'
									}

		self.browser.get('https://www.tiktok.com/')
		time.sleep(randint(1,3))
		isExistLogin = isElementExist(self.browser, '.login-button')

		if isExistLogin:
			#login_button = self.browser.find_element_by_class_name('login-button')
			#time.sleep(0.5)
			#login_button.click()
			print('Ты новенький? У тебя есть 1 минута чтобы стать смешариком')
			self.browser.get('https://www.tiktok.com/login/phone-or-email/email')
			time.sleep(30)
			#if email != None:


				
			#	email_input = self.browser.find_elements_by_tag_name('input') 
			#	time.sleep(randint(2,20)/10)
			#	print(email_input)
			#	email_input[0].send_keys(email)
			#	time.sleep(randint(2,20)/10)
			#	password_input = self.browser.find_elements_by_tag_name('input') 
			#	time.sleep(randint(2,20)/10)
			#	print(password_input)
			#	password_input[1].send_keys(password)
			#	time.sleep(20)
			#else:
			#	time.sleep(60)


			if triggerauth == 1:
				time.sleep(80)
				
			self.browser.get('https://www.tiktok.com/')
			time.sleep(randint(1,3))
		
			isExistLogin = isElementExist(self.browser, '.login-button')
			if isExistLogin:
				auth_status = False
			else:
				auth_status = True
		else:
			print('Ты уже смешарик')
			if triggerauth == 1:
				time.sleep(60)
			#if email != None:
			#	time.sleep(45)
			auth_status = True

		return auth_status






	def auth_test(self, email = None, password = None, auth_status = None, triggerauth = 0):

		def isElementExist(browser, element):
			flag = True
			try:
				self.browser.find_element_by_css_selector(element)
				return flag
			except:
				flag = False
				return flag

		

		time.sleep(randint(1,3))

		self.browser.header_overrides = {
									'method': 'GET',
									'accept-encoding': 'gzip, deflate, br', 
									'referrer': 'https://www.tiktok.com/trending',
									'upgrade-insecure-requests': '1'
									}

		self.browser.get('https://www.tiktok.com/')
		time.sleep(randint(1,3))
		isExistLogin = isElementExist(self.browser, '.login-button')

		if isExistLogin:

			#login_button = self.browser.find_element_by_class_name('login-button')
			#time.sleep(0.5)
			#login_button.click()
			print('Ты новенький? У тебя есть 1 минута чтобы стать барбариком')
			self.browser.get('https://www.tiktok.com/login/phone-or-email/email')
			time.sleep(2)
			if (email != None) and (triggerauth == 0):
				print('aboba')
				


				points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]];
				points = np.array(points)

				x = points[:,0]
				y = points[:,1]


				t = range(len(points))
				ipl_t = np.linspace(0.0, len(points) - 1, 100)

				x_tup = si.splrep(t, x, k=3)
				y_tup = si.splrep(t, y, k=3)

				x_list = list(x_tup)
				xl = x.tolist()
				x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

				y_list = list(y_tup)
				yl = y.tolist()
				y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

				x_i = si.splev(ipl_t, x_list) # x interpolate values
				y_i = si.splev(ipl_t, y_list)






				#startElement = driver.find_element_by_id('drawer')

				email_input = self.browser.find_elements_by_tag_name('input') 
				time.sleep(randint(2,20)/10)
				print('abobasss')

				WebDriverWait(self.browser, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, 'input-field-3x_mo'))) 
				email_button = self.browser.find_element_by_class_name('input-field-3x_mo')

				action =  ActionChains(self.browser);
			
				action.move_to_element(email_button);
				action.perform();

				print(zip(x_i, y_i))


				for mouse_x, mouse_y in zip(x_i, y_i):
					action.move_by_offset(mouse_x,mouse_y);
					action.perform();
					print(mouse_x, mouse_y)

				
				
				email_button.click()
				print('abobaaaa')
				

				print(email_input)
				email_input[0].send_keys(email)
				time.sleep(randint(2,20)/10)
				print('abobafff')
				


				password_input = self.browser.find_elements_by_tag_name('input') 
				time.sleep(randint(2,20)/10)
				print('abobaddd')
				WebDriverWait(self.browser, 10).until(
					EC.presence_of_element_located((By.CLASS_NAME, 'move-warning-2Xqmt'))) 
				email_button = self.browser.find_element_by_class_name('move-warning-2Xqmt') 
				
				
				print('abobarrr')

				time.sleep(3)

				action =  ActionChains(self.browser);

				action.move_to_element(email_button);
				action.perform();

				for mouse_x, mouse_y in zip(x_i, y_i):
					action.move_by_offset(mouse_x,mouse_y);
					action.perform();
					print(mouse_x, mouse_y)

				email_button.click()
				print('abobaggg')

				time.sleep(3)

				print(password_input)
				password_input[1].send_keys(password)
				time.sleep(20)
			else:
				time.sleep(60)


			if triggerauth == 1:
				time.sleep(120)
			isExistLogin = isElementExist(self.browser, '.login-button')
			if isExistLogin:
				auth_status = False
			else:
				auth_status = True
		else:
			print('Ты уже смешарик')
			if triggerauth == 1:
				time.sleep(120)
			#if email != None:
			#	time.sleep(45)
			auth_status = True

		return auth_status




























	#def __init__(self, profile):
	#	self.profile = profile
	#	self.JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

	#def drop_files(self, element, files, offsetX=0, offsetY=0):
	#	driver = element.parent
	#	isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
	#	paths = []
    
	#	# ensure files are present, and upload to the remote server if session is remote
	#	for file in (files if isinstance(files, list) else [files]) :
	#		if not os.path.isfile(file) :
	#			raise FileNotFoundError(file)
	#		paths.append(file if isLocal else element._upload(file))
    
	#	value = '\n'.join(paths)
	#	elm_input = driver.execute_script(self.JS_DROP_FILES, element, offsetX, offsetY)
	#	elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

	



	#def isElementExist(self, browser, element):
	#	flag = True
	#	try:
	#		browser.find_element_by_css_selector(element)
	#		return flag
	#	except:
	#		flag = False
	#		return flag

	#def upload_video(self, browser, description = 'заголовок по умолчанию'):
	#	WebElement.drop_files = self.drop_files
	#	i = 0
	#	i+=1
	#	print(i)
	#	path = str(pathlib.Path(__file__).parent.absolute())
	#	i+=1
	#	print(i)
	#	WebDriverWait(browser, 100).until(
	#		EC.presence_of_element_located((By.CLASS_NAME, 'upload-wrapper'))) 
	#	upload_button = browser.find_element_by_class_name('upload-wrapper') 
	#	i+=1
	#	print(i)
	#	upload_button.click()
	#	WebDriverWait(browser, 100).until(
	#		EC.presence_of_element_located((By.CLASS_NAME, 'jsx-3829822639'))) 
	#	i+=1
	#	print(i)
	#	video_upload_button = browser.find_element_by_class_name('jsx-3829822639')
	#	#video_upload_button.click()
	#	#video_upload_button.send_keys(path + 'test2.mp4')
	#	video_upload_button.drop_files(self, path + '\\test2.mp4')

	#	i+=1
	#	print(i)

	#	#WebDriverWait(browser, 100).until(
	#	#	EC.presence_of_element_located((By.CLASS_NAME, 'jsx-2053310055 preview')))
	#	try:
	#		print('b')
	#		WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'progress-container'))) 
	#		print('b')
	#	except: print('d')	
	#	print('s')
	#	WebDriverWait(browser, 100).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'progress-container')))
	#	print('s')
	#	i+=1
	#	print(i)
	#	time.sleep(1)
	#	video_title_input = browser.find_element_by_class_name('public-DraftEditor-content') 
	#	video_title_input.send_keys(description)

	#	post_button = browser.find_element_by_class_name('btn-post') 
	#	i+=1
	#	print(i)
	#	#post_button.click()
	#	i+=1
	#	print(i)


	#def play(self):
	#	username = self.profile

	#	options = Options()
	#	options.add_argument(f'user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\{username}_user')
	#	options.add_argument(f'--profile-directory={username}')
	#	options.add_argument('Cache-Control=no-cache')
	#	options.add_argument('--no-sandbox')
	#	options.add_argument('--dns-prefetch-disable') 
	#	options.add_argument('--disable-dev-shm-usage')
	#	#options.add_extension('crx/protect.crx')
	#	options.add_extension('u.crx')
	#	options.add_argument('--disable-web-security') 
	#	options.add_argument('--ignore-certificate-errors')
	#	options.page_load_strategy = 'none'
	#	options.add_argument('--ignore-certificate-errors-spki-list') 
	#	options.add_argument('--ignore-ssl-errors')

	#	options.add_experimental_option(
	#		"excludeSwitches", ['enable-automation']) 
	#	options.add_experimental_option('useAutomationExtension', False)
	#	options.add_argument('--disable-blink-features=AutomationControlled')


	#	chrome_options = Options()
	#	#chrome_options.add_argument("--user-data-dir=~/Library/Caches/Google/Chrome")
	#	#chrome_options.add_argument("--profile-directory=Profile 2")
	#	#chrome_options.add_argument("--user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
	#	#chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
	#	#chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	#	PATH = "chromedriver3.exe"
	#	#PATH = "geckodriver.exe"
	#	#PATH = 'IEDriverServer.exe'

	#	browser = webdriver.Chrome(PATH, options = options)

	#	time.sleep(randint(1,3))

	#	browser.header_overrides = {
	#								'method': 'GET',
	#								'accept-encoding': 'gzip, deflate, br', 
	#								'referrer': 'https://www.tiktok.com/trending',
	#								'upgrade-insecure-requests': '1'
	#								}

	#	browser.get('https://www.tiktok.com/')

	#	isExistLogin = self.isElementExist(browser, '.login-button')

	#	if isExistLogin:
	#		login_button = browser.find_element_by_class_name('login-button')
	#		login_button.click()
	#		print('Ты новенький? У тебя есть 1 минута чтобы стать смешариком')
	#		browser.get('https://www.tiktok.com/login/phone-or-email/email')
	#		#time.sleep(randint(1,3))
	#		#WebDriverWait(browser, 100).until(
	#		#	EC.presence_of_element_located((By.CLASS_NAME, 'channel-item-wrapper-2gBWB'))) 
	#		#log_with_email = browser.find_element_by_class_name('channel-item-wrapper-2gBWB') 
	#		#time.sleep(randint(1,3))
	#		#print(log_with_email)
	#		#log_with_email[1].click()



	#		time.sleep(60)
	#		browser.exit()
	#	else:
	#		print('Ты уже смешарик')


	#	self.upload_video(browser)

	#	time.sleep(240)
	#	browser.exit()
