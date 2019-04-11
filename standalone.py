from selenium import webdriver


def test():
    desired_capabilities = {'platform': 'WINDOWS', 'browserName': 'chrome'}
    driver = webdriver.Remote(
        '127.0.0.1:4444/wd/hub',
        desired_capabilities=desired_capabilities)
    driver.implicitly_wait(10)
    driver.get('https://www.baidu.com/')
    driver.quit()


if __name__ == '__main__':
    test()
