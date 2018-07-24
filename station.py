from selenium import webdriver
import time


def huace_restart(host):
    url = 'http://' + host

    # for test
    browser = webdriver.Chrome(r'C:\Users\wangyichuan\Desktop\test\test-pkg\chromedriver.exe')
    # browser = webdriver.PhantomJS(r'C:\Users\wangyichuan\Desktop\test\test-pkg\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    browser.get(url)
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="ipAccount"]').send_keys('admin')
    browser.find_element_by_xpath('//*[@id="ipPassword"]').send_keys('password')
    login = browser.find_element_by_xpath('//*[@id="btnLogin"]')
    login.click()
    # 点击接收机设置
    web = browser.find_element_by_xpath('//*[@id="accordionLeftMenu"]/div[3]/div[1]/div[1]')
    web.click()
    time.sleep(1)
    # 点击接收机重置
    web = browser.find_element_by_xpath('//*[@id="accordionLeftMenu"]/div[3]/div[2]/ul/li[4]/div/a')
    web.click()
    time.sleep(1)
    # 点击重启
    frame = browser.find_element_by_xpath('//*[@id="mainPanle"]/iframe')
    browser.switch_to.frame(frame)
    web = browser.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[1]/td[2]/span/a')
    web.click()
    time.sleep(1)
    # 点击确认
    web = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[4]/a[1]')
    web.click()
    browser.quit()
    print("%s has been restarted" % host)


def sinan_restart(host):
    url = 'http://' + host

    # for test
    browser = webdriver.Chrome(r'C:\Users\wangyichuan\Desktop\test\test-pkg\chromedriver.exe')
    # browser = webdriver.PhantomJS(r'C:\Users\wangyichuan\Desktop\test\test-pkg\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    browser.get(url)
    time.sleep(2)
    # 点击接收机设置
    browser.find_element_by_xpath('//*[@id="btn_account"]').send_keys('admin')
    browser.find_element_by_xpath('//*[@id="btn_Password"]').send_keys('admin')
    # 新版本
    login = browser.find_element_by_xpath('//*[@id="login"]/form/div/p[2]/input')
    # 老版本
    # login = browser.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[9]/td/input[1]')
    login.click()
    time.sleep(1)
    # 点击主机控制
    web = browser.find_element_by_xpath('//*[@id="menupanel"]/h3[2]')
    web.click()
    time.sleep(1)
    web = browser.find_element_by_xpath('//*[@id="menupanel"]/ul[2]/li[5]/a')
    web.click()
    # 点击重启
    frame = browser.find_element_by_xpath('//*[@id="mainFrame"]')
    browser.switch_to.frame(frame)
    web = browser.find_element_by_xpath('//*[@id="btn_restart"]')
    web.click()
    alert = browser.switch_to.alert
    alert.accept()
    browser.quit()
    print("%s has been restarted" % host)


def hexin_restart(host):
    username = 'admin'
    password = 'password'
    url = 'http://' + username + ':' + password + '@' + host

    browser = webdriver.Chrome(r'C:\Users\wangyichuan\Desktop\test\test-pkg\chromedriver.exe')
    # browser = webdriver.PhantomJS(r'C:\Users\wangyichuan\Desktop\test\test-pkg\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    browser.get(url)
    frame = browser.find_element_by_xpath('//*[@id="leftFrame"]')
    browser.switch_to.frame(frame)
    web = browser.find_element_by_xpath('//*[@id="admin_elem4"]/li/a')
    web.click()
    time.sleep(1)

    browser.switch_to.parent_frame()
    frame = browser.find_element_by_xpath('//*[@id="mainFrame"]')
    browser.switch_to.frame(frame)
    web = browser.find_element_by_xpath('//*[@id="_Reset_Device"]')
    web.click()
    browser.quit()
    print("%s has been restarted" % host)


def main():
    start = time.time()

    huace_host = '172.19.248.52'
    sinan_host = '172.19.248.55'
    hexin_host = '172.19.248.53'

    host = hexin_host

    # huace_restart(host)
    # hexin_restart(host)
    sinan_restart(host)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()