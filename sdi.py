import unittest,os,sys,time
import generictests, runner
from generictests import Tests
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
import requests

open('c:\selenium\Logs\sdiemptyheader1.txt', 'w').close() # blank file



# if len(sys.argv) > 3:
#     base_url = sys.argv[3]
# else:
#     base_url = "http://www.sdi.co.uk"
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

base_url = "http://www.sdi.co.uk"
generictests.base_url = "http://www.sdi.co.uk"
site = "SDI"

class SDITests(unittest.TestCase):
    def test_functional_error_page_404(self):
        url = base_url + "/404yo"
        tests = Tests()
        self.assertEqual(tests.get_status_code_and_page_title(url, "This page cannot be found", "404", site + '404Page', generictests.screenshot_path),True)

    def test_functional_error_page_500(self):
        url = base_url + "/|"
        tests = Tests()
        self.assertEqual(tests.get_status_code_and_page_title(url, "Illegal characters in path.", "500", site + '500Page', generictests.screenshot_path),True)

    def test_analytics1_Google_CheckGaScriptLoaded(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r'ga.js', 'Google Analytics JavaScript file not present on homepage', site + '-Analytics-GA-check', generictests.screenshot_path),True)

    def test_analytics2_Google_CheckTrackingCodeIsCorrect(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r'UA-4023792-1', 'Google Analytics UA code not correct', site + '-Analytics-UACode-check', generictests.screenshot_path),True)

    def test_analytics3_Omniture_checkOmnitureScriptLoaded(self):
        url = base_url + "/"
        tests = Tests()
        self.assertEqual(tests.text_search(url, r's_code_sdi.js', 's_code_sdi.js not present on page', site + '-Analytics-OmnitureScript-check', generictests.screenshot_path),True)
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
        url = base_url + "/help/sitemap"
        tests = Tests()
        self.assertEqual(tests.check_title_and_link_text(url, "Sitemap", "Why Scotland?", site + "-Sitemap-HTML", generictests.screenshot_path), True)

    def test_functional_robots_not_blocking(self):
        url = base_url + "/robots.txt"
        tests = Tests()
        self.assertEqual(tests.robots_not_blocking(url, True, site + "-Robots", generictests.screenshot_path),True)

    def test_security_ssl_valid(self):
        url = base_url + "/login"
        tests = Tests()
        self.assertEqual(tests.check_ssl_certificate(url, site + "-SSL", generictests.screenshot_path),True)

    # def test_accessibility_header1s(self):
    #     url = base_url
    #     tests = Tests()
    #     self.assertEqual(tests.accessibility_page_has_h1(url, 'c:\selenium\URLlists\urllistsdi.txt', 'c:\selenium\Logs\sdiemptyheader1.txt' ),True)

    #Note probably not worth running.  Better to use an actual spider for this.
    # def test_seo_returncodes(self):
    #     tests = Tests()
    #     self.assertEqual(tests.seo_redirects('200','redirect-fails',generictests.screenshot_path, 'c:\selenium\URLlists\urllistse2.txt'),True)

    def test_functional_homepage1_confirm_logo_present_and_image_loaded(self):
        tests = Tests()
        self.assertEqual(tests.functional_confirm_logo_present_and_image_loaded('//header/div/div/div/div/a/img','/~/media/Shared/Logos/sdi-logo.ashx','src',site + '-homepage-logo&image',generictests.screenshot_path),True)

    def test_site_search_query_string_based(self):
        url = base_url + "/search?q=scotland"
        tests = Tests()
        self.assertEqual(tests.functional_site_search_query_string_based(url,r'All results','//a[@id="plmain_0_RepeaterAll_lnkArticle_0"]',"issue",site + '-search_results'),True)



######################Non Generic Tests#######################
    def test_project_visuliser_downloadPDF(self):
        driver = generictests.driver
        try:
            url = base_url + "/invest/investment-services/inward-investment-visualiser"
            driver.get(url)
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/main/article/section[2]/div/div[4]/p/a").click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/main/article/section[3]/div/div[3]/section/nav/ul/li/a").click()
            time.sleep(5)
            driver.find_element_by_xpath("/html/body/main/article/section[3]/div/div[4]/p/a").click()
            time.sleep(5)
            driver.find_element_by_xpath("/html/body/main/article/section[4]/div/div[4]/p/a").click()
            time.sleep(5)
            generictests.inputfield_value_byid(identifier="Administration0", fieldvalue="1");  #Office service assistant = 1
            time.sleep(2)
            generictests.inputfield_value_byid(identifier="General Management0", fieldvalue="1");  #General Manager = 1
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/main/article/section[5]/div/div[3]/div[3]/a").click()
            time.sleep(5)
            generictests.inputfield_value_byid(identifier="firstName", fieldvalue="Darren");  #First name
            time.sleep(1)
            generictests.inputfield_value_byid(identifier="lastName", fieldvalue="McMillan");  #Last name
            time.sleep(1)
            generictests.inputfield_value_byid(identifier="emailAddress", fieldvalue="dogdigital1996@outlook.com");  #Email address
            time.sleep(1)
            generictests.inputfield_value_byid(identifier="telephone", fieldvalue="1234");  #Telephone
            time.sleep(1)
            driver.find_element_by_id("Checkbox2").click()
            time.sleep(1)
            driver.find_element_by_id("Checkbox7").click()
            time.sleep(1)
            driver.find_element_by_xpath("//div/div[2]/form/fieldset/button").click()
            time.sleep(1)
            driver.get("https://login.live.com")
            time.sleep(2)
            generictests.inputfield_value_byid(identifier="i0116", fieldvalue="dogdigital1996@outlook.com");  #Email address
            time.sleep(1)
            generictests.inputfield_value_byid(identifier="i0118", fieldvalue="Jimbob12");  #Email address
            time.sleep(1)
            driver.find_element_by_id("idSIButton9").click()
            time.sleep(2)#30)
            driver.get("https://bay181.mail.live.com")
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="messageListControl72fmessageListInnerContainer"]/div/div[2]/ul/li/span[4]/a').click()
            time.sleep(5)
            driver.find_element_by_partial_link_text('http://www.sdi.co.uk/invest/').click()
            time.sleep(5)
            driver.implicitly_wait(2)
            driver.switch_to.window("Office space")
            #self.assertIsNotNone(driver.find_element_by_link_text('Download PDF'),'Link not present')
            driver.implicitly_wait(2)
            driver.find_element_by_link_text('Download PDF').click()
            time.sleep(10)
            #self.assertIsNotNone(driver.find_element_by_tag_name("embed"), "PDF will not load")
        except:
            timestamp = generictests.get_timestamp()
            error = "Could not complete the test.  Screenshot captured: " + generictests.server_url + "CapturedScreenshots/SDIVisuliserPDFDownload" + timestamp + '.png'
            generictests.take_screenshot(driver, generictests.screenshot_path + 'SDIVisuliserPDFDownload' + timestamp + '.png')
            try:
                driver.switch_to.window("Office space")
            except:
                do = "nothing"
            raise Exception(error)

    def test_z_close(self):
        generictests.driver.close()

if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)


