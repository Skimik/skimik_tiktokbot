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

def upload_video(browser, description = 'заголовок по умолчанию'):
	i = 0
	i+=1
	print(i)
	path = str(pathlib.Path(__file__).parent.absolute())
	i+=1
	print(i)
	WebDriverWait(browser, 100).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'upload-wrapper'))) 
	upload_button = browser.find_element_by_class_name('upload-wrapper') 
	i+=1
	print(i)
	upload_button.click()
	WebDriverWait(browser, 100).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'jsx-3829822639'))) 
	i+=1
	print(i)
	video_upload_button = browser.find_element_by_class_name('jsx-3829822639')
	#video_upload_button.click()
	#video_upload_button.send_keys(path + 'test2.mp4')
	video_upload_button.drop_files(path + '\\test2.mp4')

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

	post_button = browser.find_element_by_class_name('btn-post') 
	i+=1
	print(i)
	#post_button.click()
	i+=1
	print(i)



username = 'Profile 2'

options = Options()
options.add_argument(f'user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\{username}_user')
options.add_argument(f'--profile-directory={username}')
options.add_argument('Cache-Control=no-cache')
options.add_argument('--no-sandbox')
options.add_argument('--dns-prefetch-disable') 
options.add_argument('--disable-dev-shm-usage')
#options.add_extension('crx/protect.crx')
options.add_extension('u.crx')
options.add_argument('--disable-web-security') 
options.add_argument('--ignore-certificate-errors')
options.page_load_strategy = 'none'
options.add_argument('--ignore-certificate-errors-spki-list') 
options.add_argument('--ignore-ssl-errors')

options.add_experimental_option(
	"excludeSwitches", ['enable-automation']) 
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')


chrome_options = Options()
#chrome_options.add_argument("--user-data-dir=~/Library/Caches/Google/Chrome")
#chrome_options.add_argument("--profile-directory=Profile 2")
#chrome_options.add_argument("--user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
#chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")
PATH = "chromedriver3.exe"
#PATH = "geckodriver.exe"
#PATH = 'IEDriverServer.exe'

browser = webdriver.Chrome(PATH, options = options)

time.sleep(randint(1,3))

browser.header_overrides = {
							'method': 'GET',
							'accept-encoding': 'gzip, deflate, br', 
							'referrer': 'https://www.tiktok.com/trending',
							'upgrade-insecure-requests': '1'
							}

browser.get('https://www.tiktok.com/')

isExistLogin = isElementExist(browser, '.login-button')

if isExistLogin:
	login_button = browser.find_element_by_class_name('login-button')
	login_button.click()
	print('Ты новенький? У тебя есть 1 минута чтобы стать смешариком')
	browser.get('https://www.tiktok.com/login/phone-or-email/email')
	#time.sleep(randint(1,3))
	#WebDriverWait(browser, 100).until(
	#	EC.presence_of_element_located((By.CLASS_NAME, 'channel-item-wrapper-2gBWB'))) 
	#log_with_email = browser.find_element_by_class_name('channel-item-wrapper-2gBWB') 
	#time.sleep(randint(1,3))
	#print(log_with_email)
	#log_with_email[1].click()



	time.sleep(60)
	browser.exit()
else:
	print('Ты уже смешарик')


upload_video(browser)

time.sleep(240)
browser.exit()