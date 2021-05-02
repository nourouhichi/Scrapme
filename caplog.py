#!/usr/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from lxml import html
from selenium.webdriver.common.keys import Keys
import re
import os, sys, stat

driver = webdriver.Firefox()
driver.get("https://intranet.hbtn.io/auth/sign_in")
username = driver.find_element_by_id("user_login")
password = driver.find_element_by_id("user_password")
username.send_keys("") # here goes your email
password.send_keys("") # here goes your password
driver.find_element_by_class_name("btn.btn-primary").click()
content = driver.page_source
soup = BeautifulSoup(content, features="lxml")
cap = soup.find_all(href=re.compile("/captain_logs"))
path = str(cap[0]["href"])
driver.get('https://intranet.hbtn.io{}'.format(path))
driver.find_element_by_id("captain_log_smiley_1").click()
who_helped = driver.find_element_by_id("who_helped_you-tokenfield")
who_you_helped = driver.find_element_by_id("who_you_helped-tokenfield")
curriculum = driver.find_element_by_id("captain_log_think_about_curriculum")
env = driver.find_element_by_id("captain_log_think_about_workspace")
exp = driver.find_element_by_id("captain_log_think_about_experience")
listy = [who_helped, who_you_helped, exp, env, curriculum]
for item in listy:
    item.send_keys("Nothing")
driver.find_element_by_class_name("btn.btn-primary").click()
os.remove("geckodriver.log")
