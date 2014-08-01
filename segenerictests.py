__author__ = 'darren.mcmillan'
from selenium import webdriver
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
import unittest, time, re, os, string, random, requests, ConfigParser, sys
import generictests
from generictests import Tests
import runner

check = Tests()

class SETests(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.accept_next_alert = True

    def knowledge_hub_load_first_content_item(self, fullurl, xpath, screenshot_name, screenshot_path):
        driver = generictests.driver
        driver.get(fullurl)
        try:
            driver.find_element_by_xpath(xpath).click()
            driver.implicitly_wait(10)
            return True
        except:
            timestamp = generictests.get_timestamp()
            error = "Could not load 1st knowledge hub article. Screenshot: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def knowledge_hub_filter(self, fullurl, xpath, filterid, filteritemid, donelink, screenshot_name, screenshot_path):
        driver = generictests.driver
        driver.get(fullurl)
        try:
            filtervalue = driver.find_element_by_xpath(xpath).text
            driver.find_element_by_id(filterid).click()
            driver.implicitly_wait(10)
            driver.find_element_by_id(filteritemid).click()
            driver.find_element_by_xpath(donelink).click()
            time.sleep(1)
            newfiltervalue = driver.find_element_by_xpath(xpath).text
            if int(newfiltervalue) < int(filtervalue) :
               return True
            else:
               raise
        except:
            timestamp = generictests.get_timestamp()
            error = "Knowledge hub filter appears to not be working. Screenshot: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def knowledge_hub_side_pod(self, fullurl, xpath, query, screenshot_name, screenshot_path):
        driver = generictests.driver
        driver.get(fullurl)
        try:
            driver.find_element_by_xpath(xpath).click()
        except:
            timestamp = generictests.get_timestamp()
            error = "Knowledge side pod doesn't exist: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
            return error
        try:
            driver.implicitly_wait(10)
            if check.text_search(driver.current_url,query,"error",screenshot_name,screenshot_path) == True:
                return True
            else:
                raise
        except:
            timestamp = generictests.get_timestamp()
            error = "Knowledge side pod page failed to load: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def login(self, fullurl, loginid, username, password, usernameid, passwordid, loginbuttonxpath, profilexpath, screenshot_name, screenshot_path):
        try:
            driver = generictests.driver
            driver.get(fullurl)
            driver.find_element_by_id(loginid).click()
            driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
            generictests.inputfield_value_byid(usernameid, username)
            generictests.inputfield_value_byid(passwordid, password)
            driver.find_element_by_xpath(loginbuttonxpath).click()
        except:
            timestamp = generictests.get_timestamp()
            error = "Failed to login: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
            return error
        # try:
        #     driver.switch_to_default_content()
        #     driver.find_element_by_link_text(profilexpath).click()
        #     return True
        # except:
        #     timestamp = generictests.get_timestamp()
        #     error = "Failed to login: " + generictests.server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
        #     driver.get_screenshot_as_file(screenshot_path + screenshot_name + timestamp + '.png')
        #     return error
        time.sleep(1)
        #driver.switch_to_default_content()
        driver.get_screenshot_as_file(screenshot_path + screenshot_name + generictests.get_timestamp() + '.png')
        print generictests.server_url + "CapturedScreenshots/" + screenshot_name + generictests.get_timestamp() + '.png'
        print profilexpath
        driver.find_element_by_xpath(profilexpath).click()


    def runTest(self):
        pass


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
