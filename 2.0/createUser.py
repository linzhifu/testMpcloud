from selenium import webdriver
import config
from pop_email import get_email
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from time import sleep

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if config.debug:
    logging.disable(logging.DEBUG)


def createUser(driver, user):

    try:
        url = config.URL
        email = user['EMAIL']
        password = user['PSW']
        server = user['SERVER']
        name = user['NAME']
        login = user['LOGIN']

        driver.get(url)

        # 等待时间
        wait = WebDriverWait(driver, 10)
        # 全屏
        # driver.set_window_size(1366, 768)
        driver.maximize_window()

        logging.info('新建用户：' + name)

        # 输入email
        inputEmail = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.capture-login .el-input__inner')),
            message='找不到 EMAIL输入栏')
        inputEmail.clear()
        inputEmail.send_keys(email)

        # 获取验证码
        captchaBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.send-captcha')),
            message='找不到 获取验证码按键')
        captchaBtn.click()
        logging.debug('邮箱登录-获取验证码：' + captchaBtn.text)
        time.sleep(30)

        captcha = get_email(email, password, server)

        # 输入验证码
        inputCap = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.capture .el-input__inner')),
            message='找不到 验证码输入栏')
        inputCap.clear()
        inputCap.send_keys(captcha)

        # 登录
        loginBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.login')),
            message='找不到 登陆按键')
        logging.debug('邮箱登录-登录：' + loginBtn.text)
        loginBtn.click()
        time.sleep(0.5)

        # 获取登录状态
        online = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.online')),
            message='找不到 登录-状态(在线)')

        username = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.username')),
            message='找不到 登录-用户')

        sleep(config.timeout)

        logging.info('登录成功：' + username.text + ' ' + online.text)
        '''
        # 修改密码
        setPswBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.psw')),
            message='找不到 修改密码按键')
        logging.debug('个人资料-设置密码：' + setPswBtn.text)
        setPswBtn.click()
        '''

        inputPsw = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.el-dialog__wrapper .el-input__inner')),
            message='找不到 修改密码输入栏')
        inputPsw.clear()
        inputPsw.send_keys(login)

        checkBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.el-dialog__wrapper .el-button--primary')),
            message='找不到 确定密码按键')
        logging.debug('设置密码-确定：' + checkBtn.text)
        checkBtn.click()
        time.sleep(0.5)

        # 修改用户名称
        inputName = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '.info-item:nth-of-type(2) .el-input__inner')),
            message='找不到 用户名输入栏')
        inputName.send_keys(Keys.CONTROL + 'a')
        inputName.send_keys(name)

        setInfoBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.change-info')),
            message='找不到 修改资料按键')
        logging.debug('个人资料-修改资料：' + setInfoBtn.text)
        setInfoBtn.click()
        sleep(1)

        # 退出
        logoutBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginout')),
            message='找不到 退出按键')
        logoutBtn.click()
        sleep(1)

        # # 申请权限
        # permissionBtn = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, '.apply-permission')),
        #     message='找不到 申请权限按键')
        # permissionBtn.click()
        # sleep(1)

        # # 填写资料
        # infoInputs = wait.until(
        #     EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
        #                                            '.submit-info-input')),
        #     message='找不到 信息输入栏')
        # for infoInput in infoInputs:
        #     infoInput.send_keys(name)

        driver.quit()
        return True

    except Exception as E:
        logging.info(E)
        driver.quit()
        return False


if __name__ == '__main__':
    driver = webdriver.Chrome()
    createUser(driver, config.USER_PRO_PM)
