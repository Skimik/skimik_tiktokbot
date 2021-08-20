from driver_processor import Driver
from db_processor import Database
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

def up(profile, name, description = '.'):
	username = profile

	options = Options()
	options.add_argument(f'user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\{username}')
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
		
	PATH = "chromedriver3.exe"
		
	browser = webdriver.Chrome(PATH, options = options)

	if Driver('Profile 2',browser).auth():
		Driver('Profile 2',browser).play(name, description)
	else:
                Database('auth').update_db('auth_status','0',f'where username = "{name}"')

	browser.quit()


def auth(profile, email = None, password = None, auth_status = None):
	username = profile

	options = Options()
	options.add_argument(f'user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\{username}')
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
		
	PATH = "chromedriver3.exe"
		
	browser = webdriver.Chrome(PATH, options = options)

	res = Driver('Profile 2',browser).auth(email, password, auth_status, 1)
	
	time.sleep(10)
	
	browser.quit()

	return res



def auth_test(profile, email = None, password = None, auth_status = None):
	username = profile

	options = Options()
	options.add_argument(f'user-data-dir=C:\\Users\\korol\\AppData\\Local\\Google\\Chrome\\User Data\\{username}')
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
		
	PATH = "chromedriver3.exe"
		
	browser = webdriver.Chrome(PATH, options = options)

	res = Driver('Profile 2',browser).auth_test(email, password, auth_status, 0)
	
	time.sleep(10)
	
	browser.quit()

	return res

if __name__ == '__main__':
	up('Profile 3', 'movie_2021-04-20_18_48_13.mp4')
