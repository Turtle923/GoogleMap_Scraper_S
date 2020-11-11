from bs4 import BeautifulSoup as bs4
import time
from tqdm import tqdm
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import *
import codecs
import csv


#Global Variables declaration
Input_Search = input('Enter name to be searched: ')#
C_UC_Business = input("""
Enter value in 1 or 2
	1) Claimed Business
	2) Unclaimed Business
: 
""")#
Profile_Name = input('Enter Google Profilename: ')
a = []

options =  webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--profile-directory='+Profile_Name+'')
browser = webdriver.Chrome(executable_path = "chromedriver",options=options)#




def Collecting_Urls():
	search_result = []
	#browser = webdriver.Firefox(executable_path = "geckodriver",options=options)
	browser.get('https://www.google.de/maps/search/'+Input_Search+'/')

	print("Scraping Search result Urls...")

	#iterate the loop till Next page button is disabled
	while True:
		time.sleep(4)
		#Get a div containing search results	
		resultdivs = browser.find_elements_by_xpath("//div[@class='section-result-content']")

		for ran in range(len(resultdivs)):
			try:
				#Click on search result div to get Url
				resultdivs[ran].click()
			except StaleElementReferenceException:
				#when you will click on back to result this exception will occur so you will find the search result div again
				resultdivs = browser.find_elements_by_xpath("//div[@class='section-result-content']")
				resultdivs[ran].click()


			#Find a Back to result to result Link button
			time.sleep(3)
			wait = WebDriverWait(browser, 20)

			back_Button =wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Back to results"]')))
			#Get Url of the result and append it to array
			search_result.append(browser.current_url)


			back_Button.click()
			time.sleep(1)


		time.sleep(2)

		try:
			nextbutton = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='n7lv7yjyC35__button-next-icon']")))

			nextbutton.click()
		#If next button is not clickable break the loop
		except:
			print()
			break
	print("Found : "+str(len(search_result))+" Search results")
	return search_result









def Collecting_Data():
	search_result = Collecting_Urls()
	checkdata =[]
	## will open the file and encode it into UTF-16##
	data_file = open('data2.csv','w', newline='', encoding = "utf-16")
	writer = csv.writer(data_file, delimiter='\t')
	Header = ['Business Name','Address','Phone']
	writer.writerow(Header)
	print('Scraping reviews of each URL.....')
	for url in tqdm(search_result):
		browser.get(url)
		time.sleep(5)
			## Getting the Business Name ##
		try:
			Name = browser.find_element_by_class_name('section-hero-header-title-title').text


		except NoSuchElementException:
			continue
		#if user selected claimed business
		if C_UC_Business == "1":
			try:
				cuc = browser.find_element_by_xpath("//button[@data-item-id='merchant']").text


				if cuc.lower().replace(' ','') == "claimthisbusiness":
					pass
				else:
					continue
			except NoSuchElementException:
				continue
		#if user selects a Unclaimed business
		else:
			try:
				cuc = browser.find_element_by_xpath("//button[@data-item-id='merchant']").text


				if cuc.lower().replace(' ','') == "claimthisbusiness":
					continue
				else:
					pass
			except NoSuchElementException:
				pass


		#Find address
		try:
			Address = browser.find_element_by_xpath("//button[@data-item-id='address']").text
		except NoSuchElementException:
			Address = ""


		#Find Phone
		try:
			Phone = browser.find_element_by_xpath("//button[starts-with(@data-item-id,'phone:tel:')]").text
		except NoSuchElementException:
			Phone = ""


		#Create a string concatinate all three var to see if data is being duplicate or not if data is already in the csv then continue
		dt = Name+Address+Phone
		if dt in checkdata:
			continue
		else:
			row = [Name,Address,Phone]

			writer.writerow(row)
		#append to check data when data is being written to csv from record
		checkdata.append(Name+Address+Phone)

	data_file.close()
			






Collecting_Data()
#browser.close()

