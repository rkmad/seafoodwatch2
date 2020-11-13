from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json

driver = webdriver.Chrome()

# save group titles and overviews to dictionary:
# get links to all group pages
driver.get("https://www.seafoodwatch.org/seafood-recommendations/seafood-a-z")
groupURLS = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'image-grid-item')))

groupNames = driver.find_elements_by_class_name('image-grid-item-title')
#groupURLS = driver.find_elements_by_class_name('image-grid-item')
groupsNamesURL_d = {}

# for group, url in zip(groupNames[:2], groupURLS[:2]):
for group, url in zip(groupNames, groupURLS):
    groupsNamesURL_d[str(group.get_attribute("innerText"))] = str(url.get_attribute("href"))


# iterate through groupsNamesURL_d to use urls to get group title overview text description, make new dictionary
urls_scraped_tracker_l =[]

with open ('groupOverview_l.json', 'a+') as fout, open ('urls_scraped_tracker_l.json', 'a+') as fout_u:

    for index, (group, url) in enumerate(groupsNamesURL_d.items()):
        groupOverview_l=[]
        driver.get(url)

        lis_0 = [group]
        lis_1 = [str(driver.find_element_by_xpath("//div/div/div/p[@class='centered ng-binding']").get_attribute("innerText"))]

        # change to specific url for group
        driver.get(url.replace('/overview', ''))

        # # to get Best, Good, Avoid text: as list. Not all groups have these groups, so when not present: pass
        lis_2=[]
        try:
            groupCategories = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//div/div/div/div/div/span[@class='color-description ng-binding']")))
            for ele in groupCategories:
                lis_2.append(ele.get_attribute("innerText"))
        except TimeoutException:
            print("Timed out waiting for load of Best, Good, Avoid text.")
            pass

        # # to get group information: Type, Method, Location. ALl groups must have this information, so when not present: continue
        lis_3=[]
        try:
            groupInfoTextOnly = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH,"//div/div/div/div[@class='rec-details']")))
            for ele in groupInfoTextOnly:
                lis_3.append(ele.get_attribute("innerText"))
        except TimeoutException:
            print("Timed out waiting for load of group information: Type, Method, Location.")
            continue

        # # to get all Overall scores on page:
        lis_4=[]
        scoresOverall = driver.find_elements_by_xpath("//div/div/div/h3[@class='ng-binding']")
        for ele in scoresOverall:
            lis_4.append(ele.get_attribute("innerText"))

        # # to get all subscore names: 
        # # subscores subgroups always begin with either 'Data' for 10 subgroups or 'Target Species' for 4 subgroups
        lis_5=[]
        subscoreNames = driver.find_elements_by_xpath("//div/div/div/label[@class='equalize ng-binding']")
        for ele in subscoreNames:
            lis_5.append(ele.get_attribute("innerText"))

        # # to get all subscores on page:
        lis_6=[]
        subscores = driver.find_elements_by_xpath("//span/span[@class='ng-binding']")
        for ele in subscores:
            lis_6.append(ele.get_attribute("innerText"))

        # # to get all group short text:
        # only this returns Eco-certification text but will need to remove this extraneous text from final result: 
            # Cookie Settings    
            # Always Active
            # All Recommendations for XXXNameOfFishXXX      
            # Please try again with broader search terms.
        lis_7=[]
        groupShortText = driver.find_elements_by_xpath("//div/div/div/div/p")
        for ele in groupShortText:
            lis_7.append(ele.get_attribute("innerText"))


        groupOverview_l = [lis_0, lis_1, lis_2, lis_3, lis_4, lis_5, lis_6, lis_7]
        json.dump(groupOverview_l, fout)

        # to keep running list of urls successfully scraped if needed
        urls_scraped_tracker_l.append(url)
        json.dump(urls_scraped_tracker_l, fout_u)
        print("Done scraping: " + str(url))


driver.close()



#########################################################################################
#########################################################################################
#########################################################################################