import time
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import smtplib, ssl

driver = webdriver.Chrome('D:\chromedriver.exe')
driver.maximize_window()

port = 587  # For starttls
smtp_server = "smtp.live.com"
sender_email = "email@hotmail.com"
password = "azerty"
message = """\
Subject: Check PREFECTURE

This message is sent from Python."""

while True:
	driver.get("http://www.essonne.gouv.fr/booking/create/13185/1")

	time.sleep(10)

	bad_gateway = 0
	indispo = 0

	try:
		bad_gateway = driver.find_element_by_xpath("//*[contains(text(), 'Bad Gateway')]")
	except NoSuchElementException:
		True

	try:
		elem = driver.find_element_by_id('planning14167').click()
	except NoSuchElementException:
		True

	time.sleep(1)

	try:
		elem = driver.find_element_by_name('nextButton').click()
	except NoSuchElementException:
		True

	time.sleep(10)

	try:
		indispo = driver.find_element_by_xpath("//*[contains(text(), 'existe plus de plage horaire')]")
	except NoSuchElementException:
		True

	try:
		bad_gateway = driver.find_element_by_xpath("//*[contains(text(), 'Bad Gateway')]")
	except NoSuchElementException:
		True

	f = open('D:\prefecture.txt', 'a+')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	if indispo != 0:
		print("indisponible")
		f.write(st + " : indisponible" + "\n")
	if bad_gateway != 0:
		print("Bad Gateway")
		f.write(st + " : Bad Gateway" + "\n")
	if indispo == 0 and bad_gateway == 0:
		print("OK !!")
		f.write(st + " : OK !!" + "\n")
		context = ssl.create_default_context()
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()  # Can be omitted
			server.starttls(context=context)
			server.ehlo()  # Can be omitted
			server.login(sender_email, password)
			server.sendmail(sender_email, "receiver1@laposte.net", message)
			server.sendmail(sender_email, "receiver2@googlemail.com", message)
	f.close()
	time.sleep(60)
