import unittest,os,sys,time
import generictests, runner
from generictests import Tests
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
import requests

open('c:\selenium\Logs\isemptyheader1.txt', 'w').close() # blank file



# if len(sys.argv) > 3:
#     base_url = sys.argv[3]
# else:
#     base_url = "http://www.interactivescotland.com"
#
# if len(sys.argv) > 4:
#     driver = sys.argv[4]
#     print "driver"
# else:
#     driver = runner.open("chrome")
#
# if len(sys.argv) > 5:
#     base_url = sys.argv[5]
# else:
#     site = "SDI"

base_url = "http://www.interactivescotland.com"
generictests.base_url = "http://www.interactivescotland.com"
site = "InteractiveScotland"

class InteractiveScotlandTests(unittest.TestCase):
    def test_functional_error_page_404(self):
        url = base_url + "/404yo"
        tests = Tests()
        self.assertEqual(tests.get_status_code_and_page_title(url, "Page not found", "404", site + '404Page', generictests.screenshot_path),True)

    def test_functional_error_page_500(self):
        url = base_url + "/|"
        tests = Tests()
        self.assertEqual(tests.get_status_code_and_page_title(url, "Error - Something went wrong", "500", site + '500Page', generictests.screenshot_path),True)

    def test_analytics1_Google_CheckGaScriptLoaded(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r'ga.js', 'Google Analytics JavaScript file not present on homepage', site + '-Analytics-GA-check', generictests.screenshot_path),True)

    def test_analytics2_Google_CheckTrackingCodeIsCorrect(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r'UA-51444392-1', 'Google Analytics UA code not correct', site + '-Analytics-UACode-check', generictests.screenshot_path),True)

    def test_analytics3_Omniture_checkOmnitureScriptLoaded(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r's_code_is.js', 's_code_s.js not present on page', site + '-Analytics-OmnitureScript-check', generictests.screenshot_path),True)
        self.assertEqual(tests.get_tag_text(base_url, "script", "document.write(s_code)", site + '-Analytics-OmnitureScript-check', generictests.screenshot_path),True)

    def test_analytics4_Omniture_checkOmniturePropAndVarsWritten(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r's.prop22 = \'EN\'', 's.prop22 not present on homepage, Omniture files might not be functioning correctly.', site + '-Analytics-Omiture-check', generictests.screenshot_path),True)
        self.assertEqual(tests.text_search(url, r's.eVar22 = \'EN\'', 's.eVar22 not present on homepage, Omniture files might not be functioning correctly.', site + '-Analytics-Omiture-check', generictests.screenshot_path),True)

    def test_sitemap1_checkXMLSitemap_And_LoadedWithCorrectDomain(self):
        url = base_url + "/sitemap.xml"
        tests = Tests()
        query = "r'<loc>" + base_url + "/'"
        self.assertEqual(tests.text_search(url, eval(query), 'Sitemap either not present or displaying incorrect URL\'s.', site + '-SitemapXML-check', generictests.screenshot_path),True)

    def test_sitemap2_checkHTMLSitemap(self):
        url = base_url + "/sitemap"
        tests = Tests()
        self.assertEqual(tests.check_title_and_link_text(url, "Sitemap", "Hippotrix", site + "-Sitemap-HTML", generictests.screenshot_path), True)

    def test_functional_robots_not_blocking(self):
        url = base_url + "/robots.txt"
        tests = Tests()
        self.assertEqual(tests.robots_not_blocking(url, True, site + "-Robots", generictests.screenshot_path),True)

    def test_security_ssl_valid(self):
        url = base_url + "/subscribe"
        tests = Tests()
        self.assertEqual(tests.check_ssl_certificate(url, site + "-SSL", generictests.screenshot_path),True)

    # def test_accessibility_header1s(self):
    #     url = base_url
    #     tests = Tests()
    #     self.assertEqual(tests.accessibility_page_has_h1(url, 'c:\selenium\URLlists\urllistsdi.txt', 'c:\selenium\Logs\isemptyheader1.txt' ),True)

    # def test_seo_returncodes(self):
    #     tests = Tests()
    #     self.assertEqual(tests.seo_redirects('200','redirect-fails',generictests.screenshot_path, 'c:\selenium\URLlists\urllistse2.txt'),True)

    def test_functional_homepage1_confirm_logo_present_and_image_loaded(self):
        url = base_url
        tests = Tests()
        self.assertEqual(tests.functional_confirm_logo_present_and_image_loaded('//body/form/div/div/div/header/div/a','/','href',site + '-homepage-logo&image',generictests.screenshot_path),True)

    def test_site_search_query_string_based(self):
        url = base_url + "/search?q=scotland"
        tests = Tests()
        self.assertEqual(tests.functional_site_search_query_string_based(url,r'Key Results','/html/body/form/div[4]/div/main/article/section[2]/article[2]/a',"issue",site + '-search_results'),True)


######################Non Generic Tests#######################


    def test_contactForm_test(self):
        #Load contact form
        try:
            driver = generictests.driver
            tests = Tests()
            url = base_url + "/DoNotDelete/Contactus"
            driver.get(url)
            #Confirm page is loaded correctly by asserting the title
            assert 'Contact Us' in driver.title
        except:
            error = "Expected page title of Contact Us." + "Got: " + driver.title
        try:
            #Populate personal details
            generictests.inputfield_value_byid( identifier = "plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_field_AD2521FB14D4408C936F6A623EE3F6D0", fieldvalue = "Selenium test ignore" ); #full name
            generictests.inputfield_value_byid( identifier = "plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_field_C11995CA89414B65B4BF23D2AD4A8705", fieldvalue = "dtest1@dogdigital.com" ); #email
            generictests.inputfield_value_byid( identifier = "plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_field_D7565F5AD80740AB8EC27B87A77C6D75", fieldvalue = "Test company ignore" ); #company name
            time.sleep(1)
            #Add comment
            generictests.inputfield_value_byid( identifier = "plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_field_BD1B87D75333428483D3D78731963693", fieldvalue = "This is a test comment please ignore" ); #comment field
            time.sleep(1)
            #Tick t&c checkbox and hit submit button
            driver.find_element_by_id("plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_field_177C5DACD5504424AD520E7563877E66").click()
            time.sleep(1)
            driver.find_element_by_id("plmain_0_form_83F545649D3C4CD984EF40518F3BC1CB_form_83F545649D3C4CD984EF40518F3BC1CB_submit").click()
        except:
            error = "Couldn't submit contact us form.  Screenshot: " + generictests.server_url + "CapturedScreenshots/" + "ISContactForm" + generictests.get_timestamp() + '.png'
            generictests.take_screenshot(driver, generictests.screenshot_path + "ISContactForm" + generictests.get_timestamp() + '.png')
            raise Exception(error)
        try:
            time.sleep(3)
            #Assert form has submitted correctly & thank you page loaded
            assert 'Thank you' in driver.title
            tests.text_search(url,"r'Thank you for contacting Interactive Scotland'","error",site + "-ISContactThankYouPage",generictests.screenshot_path)
        except:
            driver.implicitly_wait(10)
            error = "Contact us thank you page did not load.  Screenshot: " + generictests.server_url + "CapturedScreenshots/" + "ISContactThankYouPage" + generictests.get_timestamp() + '.png'
            generictests.take_screenshot(driver, generictests.screenshot_path + "ISContactThankYouPage" + generictests.get_timestamp() + '.png')
            error = "Thank you page didn't load."


    def test_z_close(self):
        generictests.driver.close()


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
