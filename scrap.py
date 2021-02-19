#!/usr/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from lxml import html
from selenium.webdriver.common.keys import Keys
import re
import os, sys, stat

print("Notes: This script only works for projects including one directory \nFor the first use of this script you will have to enter your credentials directly in the script")
lg_dict = {"python": "#!/usr/bin/python3\n", "javascript": "#!/usr/bin/node\n", "c":"", "bash": "#!/usr/bin/env bash\n"}
driver = webdriver.Firefox()
driver.get("https://intranet.hbtn.io/auth/sign_in")
username = driver.find_element_by_id("user_login")
password = driver.find_element_by_id("user_password")
username.send_keys("") # here goes your email
password.send_keys("") # here goes your password
driver.find_element_by_class_name("btn.btn-primary").click()
link = input("Enter the link of the project: ")
lg = input("Enter the programming language: ")
driver.get(link)
content = driver.page_source
soup = BeautifulSoup(content, features="lxml")
directory = soup.body.find_all(text=re.compile("Directory: "), limit=1)
di = os.mkdir(str(directory[0].next_element.text))
os.chdir(str(directory[0].next_element.text))
readme = open("README.md", "w+")
for direc in directory:
    readme.write(str(direc.next_element.text))
readme.close()
listy = soup.body.find_all(text=re.compile("File:"))
for name in listy:
    f_name = name.next_element.text
    f = open(f_name,"w+")
    os.chmod(str(f_name), stat.S_IRWXU)
    if lg_dict[lg]:
        f.write(lg_dict[lg])
    f.close()
