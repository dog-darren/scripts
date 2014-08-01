from selenium import webdriver
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
import unittest, time, re, os, string, random, requests, ConfigParser, sys
import runner


server_url = "http://teamcity.dogstaging.com/"
#Set time stamp for screenshots / logs
dateTimeStamp = time.strftime('%Y%m%d_%H_%M_%S') #todo make function to return correct date time stamp
#Set driver #todo export to function
driver = runner.open("chrome")
#driver = webdriver.Chrome(executable_path='C:\Selenium\chromedriver.exe')
#Set URL to open #todo export to function
base_url = ""
#Set Screenshot URL # todo export to function
screenshot_path = "C:\\selenium\CapturedScreenshots\\"
#Set up config parser for reading / writing data to config files
config = ConfigParser.RawConfigParser()


def take_screenshot(driver, save_location): #Screenshot capture
        path = os.path.abspath(save_location)
        driver.get_screenshot_as_file(save_location)
        return save_location

def id_generator(size=10, chars=string.ascii_uppercase + string.digits): #Random ID generator
    return ''.join(random.choice(chars) for _ in range(size))

def get_timestamp():
    return time.strftime('%Y%m%d_%H_%M_%S')

def inputfield_value_byid(identifier, fieldvalue):
    elem = driver.find_element_by_id(identifier)
    elem.clear()
    elem.send_keys(fieldvalue)

class Tests(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.accept_next_alert = True

    def get_status_code_and_page_title(self,fullurl,pagetitle,code,screenshot_name, screenshot_path):
        #usage generictests.Tests.test_return_status_code('http://www.sdi.co.uk/404yo', "This page cannot be found", "404", 'SDI404Page', screenshot_path )
        def return_code(fullurl,pagetitle,code,screenshot_name, screenshot_path):
            driver.get(fullurl)
            #Confirm page is loaded correctly by asserting the title
            responseCode = "<Response [" + code + "]>"
            try:
                status_code = requests.head(fullurl)
            except:
                timestamp = get_timestamp()
                error = "Failed to connect to " + fullurl + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
            try:
                self.assertEqual(str(status_code), responseCode,)
                return True
            except:
                timestamp = get_timestamp()
                error = "Status code incorrect for: " + fullurl + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
        def page_title(pagetitle,screenshot_name, screenshot_path):
            try:
                assert pagetitle in driver.title #Resource not found is returned by default asp page
                return True
            except:
                timestamp = get_timestamp()
                error = "Expected page title: " + pagetitle + " Got: " + driver.title + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
        code = return_code(fullurl,pagetitle,code,screenshot_name, screenshot_path)
        title = page_title(pagetitle,screenshot_name, screenshot_path)
        value = str(code) + "     " + str(title)
        if (title == True) and (code == True):
            return True # If all good return True with can later be asserted against
        else:
            print value
            return value #If not return errors.

    def get_status_code(self,fullurl, code,screenshot_name, screenshot_path):
        def return_code(fullurl,code,screenshot_name, screenshot_path):
            driver.get(fullurl)
            #Confirm page is loaded correctly by asserting the title
            responseCode = "<Response [" + code + "]>"
            try:
                status_code = requests.head(fullurl)
            except:
                timestamp = get_timestamp()
                error = "Failed to connect to " + fullurl + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
            try:
                error = "Status code incorrect for: " + fullurl + "\n" + "Expected: " + code +" Got: " + str(status_code) + "\n" + "Screenshot: " + server_url + screenshot_name + dateTimeStamp + ".png" + "\n" + "URL: " + fullurl
                self.assertEqual(str(status_code), responseCode, error)
                return True
            except:
                timestamp = get_timestamp()
                error = "Status code incorrect for: " + fullurl + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
        code = return_code(fullurl,code,screenshot_name, screenshot_path)
        if code == True:
            return True # If all good return True with can later be asserted against
        else:
            print code
            return code #If not return errors.



    def text_search(self, fullurl, query, message, screenshot_name, screenshot_path):
        #Usage text_search(r'Piece of text you wish to verify is present', 'Error message to show')
        driver.get(fullurl)
        src = driver.page_source
        text_found = re.search(query, src)
        try:
            self.assertNotEqual(text_found, None, message)
            return True
        except:
            error = "Text search for: " + query + " did not return the expected results. " + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + get_timestamp() + ".png" + "\n" + "URL: " + fullurl
            take_screenshot(driver, screenshot_path + screenshot_name + get_timestamp() + '.png')
            return error

    def get_tag_text(self, fullurl, tag, query, screenshot_name, screenshot_path):
        driver.get(fullurl)
        try:
            lookup = "driver.find_element_by_xpath(\"//" + tag + "[contains(text(),'" + query + "')]" + '").text'
            self.assertNotEqual(eval(lookup), None)
            return True
        except:
            timestamp = get_timestamp()
            error = "Text search for: " + query + " did not return the expected results. " + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
            take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def check_title_and_link_text(self, fullurl, title, linktext, screenshot_name, screenshot_path):
        driver.get(fullurl)
        time.sleep(1)
        def checktitle(title):
            try:
                assert title in driver.title
                return True
            except:
                timestamp = get_timestamp()
                error = "Expected: " + title + " Got: " + driver.title + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
        def checklinktext(linktext):
             try:
                lookup = "driver.find_element_by_link_text('" + linktext + "').text"
                self.assertEqual(eval(lookup), linktext)
                return True
             except:
                timestamp = get_timestamp()
                error = "Link text search for: " + linktext + " did not return the expected results. " + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                return error
        title_value = checktitle(title)
        linktext_value = checklinktext(linktext)
        value = str(title_value) + "     " + str(linktext_value)
        if (title_value == True) and (linktext_value == True):
            return True # If all good return True with can later be asserted against
        else:
            print value
            return value #If not return errors.

    def robots_not_blocking(self, fullurl, livesite, screenshot_name, screenshot_path):
        driver.get(fullurl)
        src = driver.page_source
        if livesite == True:
            query = re.search("(Disallow: /[\s|\<])", src) # Check for "Disallow: /"
        else:
            query = re.search("(Disallow: [\s|\<])", src) # Check for "Disallow: "
        try:
            self.assertIsNone(query)
            return True
        except:
            timestamp = get_timestamp()
            error = "Robots.txt is not configured correctly." + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
            take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def check_ssl_certificate(self, fullurl, screenshot_name, screenshot_path):
        url = str(fullurl).replace("http:", "https:")
        try:
            requests.get(url, verify=True) #Verify url has a valid SSL certificate, otherwise throw an SSL exception
            return True
        except:
            timestamp = get_timestamp()
            error = "SSL certificate not valid." + "\n" + "Screenshot: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + ".png" + "\n" + "URL: " + fullurl
            take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def accessibility_page_has_h1(self, fullurl, urllist, logfile):
        def checkh1(fullurl,urllist,logfile):
            with open(urllist, 'r') as f:
                urllist = [line.strip() for line in f]
            noh1 = [] #List for pages with no h1 tag on the page
            noh1content = [] #List for pages with a h1 tag, but no contents inside it.
            for url in urllist:
                testurl = str(url)
                driver.set_page_load_timeout(60)  # Timeout if page takes more than 1min to load
                driver.get(testurl)
                try:
                    header1 = driver.find_element_by_xpath("//h1")  # store page h1
                    header1text = header1.get_attribute("innerHTML").strip()  # Store  value for H1, stripping out any whitespace
                    strippedtags = re.sub('<[^<]+?>', '', header1text)  # Strip HTML tags from H1
                    #inner = driver.execute_script("return arguments[0].innerHTML;", header1) #alternative way
                    header1LogMessage = "On page: " + url + " the H1 tag has no content. "
                    if strippedtags == "": # If h1 tag has no content
                        noh1content.append(header1LogMessage)
                        fh = open(logfile, 'a')
                        fh.write(header1LogMessage.encode('utf8') + '\n')
                        fh.close
                except: # If h1 tag is missing
                    error = "On page: " + url + " a H1 tag isn't present. "
                    fh = open(logfile, 'a')
                    fh.write(error.encode('utf8') + '\n')
                    fh.close
                    noh1.append(error)
            if not noh1 and not noh1content: #Check if any errors
                return True
            else:
                value = noh1 + noh1content
                print "###Pages with no h1 content###"
                for item in noh1content: print item
                print "###Pages with no h1###"
                for item in noh1: print item
                return value
        h1check = checkh1(fullurl, urllist, logfile)
        if h1check == True:
            return True # If all good return True with can later be asserted against
        else:
            print h1check
            return h1check #If not return errors.

    def seo_redirects(self, code, screenshot_name, screenshot_path, urllist):
        invalid_status_code = []
        str(code)
        with open(urllist, 'r') as f:
            urllist = [line.strip() for line in f]
            for url in urllist:
                fullpath = str(base_url) + str(url)
                driver.set_page_load_timeout(180)  # Timeout if page takes more than 3min to load
                returncode = self.get_status_code(fullpath, code, screenshot_name, screenshot_path)
                if returncode != code:
                    invalid_status_code.append(returncode)
        if not returncode:
            return True
        else:
            print invalid_status_code
            return invalid_status_code

    def functional_confirm_logo_present_and_image_loaded(self, xpath_image, link, attribute, screenshot_name, screenshot_path):
        url = base_url + "/"
        driver.get(url)
        driver.find_element_by_xpath(xpath_image).click()
        try:
            self.assertEqual(base_url + link, driver.find_element_by_xpath(xpath_image).get_attribute(attribute))
            return True
        except:
            timestamp = get_timestamp()
            error = "Homepage logo or image not loaded correctly on " + url + "  Screenshot captured: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png'
            take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
            return error

    def functional_site_search_query_string_based(self, fullurl, query, xpath, message, screenshot_name):
        driver.get(fullurl)
        driver.implicitly_wait(10)
        timestamp = get_timestamp()
        def checkHeader():
            try:
                self.assertEqual(self.text_search(fullurl,query, message, screenshot_name,screenshot_path),True)
                return True
            except:
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                error = "Search result page not loading.  Screenshot captured: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png' + "URL: " + fullurl
                return error
        def checkFirstResult():
            try:
                driver.find_element_by_xpath(xpath)
                return True
            except:
                take_screenshot(driver, screenshot_path + screenshot_name + timestamp + '.png')
                error = "Search results not loading.  Screenshot captured: " + server_url + "CapturedScreenshots/" + screenshot_name + timestamp + '.png' + " URL: " + fullurl
                return error
        header = checkHeader()
        result = checkFirstResult()
        value = []
        for item in header, result:
            if item != True:
                value.append(item)
                print value
        if (header == True) and (result == True):
            return True # If all good return True with can later be asserted against
        else:
            return value #If not return errors.

    def runTest(self):
        #print self.get_tag_text(base_url, "script", "document.write(s_code)", "SDI404Page", screenshot_path )
        #print self.check_title_and_link_text(base_url, "Sitemap", "Why Scotland?", "SDISitemap-HTML", screenshot_path)
        #print get_timestamp()
        if len(sys.argv) > 3:
            print sys.argv[3]
        print len(sys.argv)

    def tearDown(self):
        driver.quit()

if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
