__author__ = 'darren.mcmillan'
from selenium import webdriver

def open(version):
    types = {'firefox' : 'webdriver.Firefox()', 'chrome' : 'webdriver.Chrome()', 'ie' : 'webdriver.Ie()', 'opera' : 'webdriver.Opera()', 'phantomjs' : 'webdriver.PhantomJS()', 'safari' : 'webdriver.Safari()', 'remote' : 'webdriver.Remote()'}
    if version == "chrome":
        selection = "webdriver.Chrome(executable_path='C:\Selenium\chromedriver.exe')"
    else:
        selection = types[version]
    return eval(selection)
