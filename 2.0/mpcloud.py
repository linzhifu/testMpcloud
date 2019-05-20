import logging
import os
import time
import requests
# import shutil
# import get_video
from time import sleep
# from datetime import datetime
# from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import config

# DEBUG LOG
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if config.debug:
    logging.disable(logging.DEBUG)

# admin
admin = {
    'userid': '',
    'token': '',
}

# 用户登陆配置
loginCase = {
    'method': 'post',
    'url': '/api/v1/user/login',
    'params': {},
    'json': {
        'email': 'linzhifu221@163.com',
        'pswmd5': 'c313b271b06b2b50ad9a3e93e8744029',
        'timestamp': int(time.time())
    },
    'response': {
        'errcode': '0',
        'errmsg': 'ok'
    }
}

# 操作等待时间
sleepTime = 1

# 是否修改过密码
isNewPsw = False

# TEAM成员
teamUsers = config.teamUsers

# TEAM
testTeam = config.testTeam

# 是否修改过产品
isModifyPro = False

# 是否修改过型号
isModifyMod = False

# 产品-型号
proMod = config.proMod

# 测试软件
software = config.software

# 测试文件下载路径
filePath = config.filePath()


# API请求，默认获取管理员token
def doTest(case=loginCase, RESTAPI_DOMAIN=config.URL):
    start = time.time()
    response = ''
    error = None
    try:
        response = requests.request(
            method=case['method'],
            url=RESTAPI_DOMAIN + case['url'],
            params=case['params'],
            json=case['json'],
            verify=False)
    except requests.exceptions.ConnectionError:
        error = "ConnectionError"
    except requests.exceptions.HTTPError:
        error = "HTTPError"
    except requests.exceptions.URLRequired:
        error = "URLRequired"
    except requests.exceptions.TooManyRedirects:
        error = "TooManyRedirects"
    except requests.exceptions.ReadTimeout:
        error = "ReadTimeout"
    except requests.exceptions.InvalidURL:
        error = "InvalidURL"
    timeval = time.time() - start

    rev = ''
    if error is None:
        # rev = json.loads(r.text)
        try:
            rev = response.json()
        except Exception as e:
            error = '返回数据不是JSON对象'

    if error is None:
        if not case['response']:
            error = 'response为空'

    if error is None:
        if str(rev.get('errcode')) != case['response'].get('errcode'):
            error = 'errcode不一致'

    # 记录userId和token
    if error is None:
        if rev.get('data'):
            if rev['data'].get('userid') and rev['data'].get('token'):
                admin['userid'] = rev['data'].get('userid')
                admin['token'] = rev['data'].get('token')
    result = {'time': str(round(timeval, 2)), 'error': error}
    return result


# 将滚动条移动到页面的顶部
def goTop(driver):
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    sleep(sleepTime)


# 拖动到可见的元素去
def goToElement(element, driver):
    js = 'arguments[0].scrollIntoView();'
    driver.execute_script(js, element)
    sleep(sleepTime)


# 用户通过邮箱和密码登录
def login(wait, **kwargs):
    # 获取登陆邮箱和密码
    email = kwargs.get('email')
    password = kwargs.get('password')
    if not email:
        raise Exception('邮箱不能为空')
    if not password:
        raise Exception('密码不能为空')
    # 点击密码登录
    loginTabView = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.way li:nth-of-type(2)')),
        message='找不到 密码登陆TAB')
    logging.debug('登录-Tab项(密码登录)：' + loginTabView.text)
    loginTabView.click()
    sleep(sleepTime)

    # 输入email
    inputEmail = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .mail .el-input__inner')),
        message='找不到 EMALI输入栏')
    inputEmail.send_keys(email)

    # 输入password
    inputPsw = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .password .el-input__inner')),
        message='找不到 密码输入栏')
    inputPsw.send_keys(password)

    # 点击登录
    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.password-login .login')),
        message='找不到 登陆按键')
    logging.debug('登录-按钮(登录/注册)：' + loginBtn.text)
    loginBtn.click()
    sleep(sleepTime)

    # 获取登录状态
    online = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.online')),
        message='找不到 登录-状态(在线)')

    # 获取用户名
    username = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.username')),
        message='找不到 登录-用户')

    logging.info('用户登录成功：' + username.text + ' ' + online.text)
    sleep(sleepTime)

    return True


# 点击退出
def logout(driver, wait, user):
    logoutBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginout')),
        message='找不到退出按键')
    logoutBtn.click()
    sleep(sleepTime)


# 修改用户资料
def updateUserInfo(driver, wait, user):
    # 用户名
    inputName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(1) .el-input__inner')),
        message='找不到 用户名输入栏')
    inputName.send_keys(Keys.CONTROL + 'a')
    inputName.send_keys(user['userName'])

    # QQ
    inputQQ = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(3) .el-input__inner')),
        message='找不到 QQ输入栏')
    inputQQ.send_keys(Keys.CONTROL + 'a')
    inputQQ.send_keys(user['qq'])

    # IM
    inputIM = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(4) .el-input__inner')),
        message='找不到 IM输入栏')
    inputIM.send_keys(Keys.CONTROL + 'a')
    inputIM.send_keys(user['im'])

    # PHONE
    inputPhone = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(5) .el-input__inner')),
        message='找不到 PHONE输入栏')
    inputPhone.send_keys(Keys.CONTROL + 'a')
    inputPhone.send_keys(user['phone'])

    # 确认修改
    setInfoBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.change-info')),
        message='找不到 修改资料按键')
    logging.debug('个人资料-修改资料：' + setInfoBtn.text)
    setInfoBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 核对用户资料
def checkUserInfo(driver, wait, user):
    # 判断是否有多余的测试team未删除（上一次测试失败的）
    # 点击查看我的team
    # 查看我的team
    myTeamBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.watch-myteam')),
        message='找不到 查看我的群组按键')
    logging.debug('个人中心-我的资料：' + myTeamBtn.text)
    myTeamBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 核对team
    getTeams = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody tr')),
        message='找不到 team列表')
    if len(getTeams) != 1:
        # 删除team
        deleteTeam(wait)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回上一级按键')
    logging.debug('查看我的team-查看：' + backBtn.text)
    goTop(driver)
    backBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 用户名
    inputName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(1) .el-input__inner')),
        message='找不到 用户名输入栏')
    userName = inputName.get_attribute('value')
    if userName != user['userName']:
        raise Exception('个人资料：userName有误：' + userName)

    # Email
    inputEmail = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(2) .el-input__inner')),
        message='找不到 Email输入栏')
    email = inputEmail.get_attribute('value')
    if email != user['EMAIL']:
        raise Exception('个人资料：Email有误')

    # QQ
    inputQQ = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(3) .el-input__inner')),
        message='找不到 QQ输入栏')
    qq = inputQQ.get_attribute('value')
    if qq != user['qq']:
        raise Exception('个人资料：QQ有误')

    # IM
    inputIM = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(4) .el-input__inner')),
        message='找不到 IM输入栏')
    im = inputIM.get_attribute('value')
    if im != user['im']:
        raise Exception('个人资料：IM有误')

    # PHONE
    inputPhone = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(5) .el-input__inner')),
        message='找不到 PHONE输入栏')
    phone = inputPhone.get_attribute('value')
    if phone != user['phone']:
        raise Exception('个人资料：phone有误')

    # team
    teams = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(6) .teamlist div')),
        message='找不到 Team输入栏')
    if len(teams) != len(user['TEAM']):
        raise Exception('个人资料：team数量有误')
    for team in teams:
        teamName = team.get_attribute('innerText')
        if teamName not in user['TEAM']:
            raise Exception('个人资料：team显示有误')

    # role
    roles = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.info-item-last .teamlist div')),
        message='找不到 用户角色')
    if len(roles) != len(user['ROLE']):
        raise Exception('个人资料：role数量有误')
    for role in roles:
        roleName = role.get_attribute('innerText')
        if roleName not in user['ROLE']:
            raise Exception('个人资料：role显示有误')


# 修改密码
def updatePassword(driver, wait, user):
    global isNewPsw

    # 设置密码按键
    setPswBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.psw')),
        message='找不到 个人资料-设置密码按键')
    logging.debug('个人资料-设置密码：' + setPswBtn.text)
    setPswBtn.send_keys(Keys.ENTER)

    # 密码输入栏
    inputPsw = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.el-dialog__wrapper .el-input__inner')),
        message='找不到 password输入栏')
    inputPsw.clear()
    # 修改密码测试完后，需要修改回123，方便后续自动化测试
    if isNewPsw:
        inputPsw.send_keys('123')
    else:
        inputPsw.send_keys(user['passWord'])

    # 确认修改按键
    checkBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-dialog__wrapper .el-button--primary')),
        message='找不到 设置密码-确定按键')
    logging.debug('设置密码-确定：' + checkBtn.text)
    checkBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 标记密码已经修改过
    isNewPsw = not isNewPsw


# 还原用户名，方便后续测试
def resUserName(driver, wait, user):
    # 用户名
    inputName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.info-item:nth-of-type(1) .el-input__inner')),
        message='找不到 用户名输入栏')
    inputName.send_keys(Keys.CONTROL + 'a')
    inputName.send_keys(user['NAME'])

    # 确认修改
    setInfoBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.change-info')),
        message='找不到 修改资料按键')
    logging.debug('个人资料-修改资料：' + setInfoBtn.text)
    goToElement(setInfoBtn, driver)
    setInfoBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 获取team功能：删除、查看、修改
def getTeamFunction(wait, row, column):
    teamFunctionBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(%d)'
            % (row, column))),
        message='获取Team功能失败')

    logging.debug('查看我的team：' + teamFunctionBtn.text)
    return teamFunctionBtn


# 获取team列表信息，row行1开始，colunm列1开始
def getTeamInfo(wait, row, column):
    teamItem = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(%d) td:nth-of-type(%d)' % (row, column))),
        message='获取team列表信息失败')

    return teamItem.text


# 添加Team
def addTeam(driver, wait, user):
    # 创建Team按键
    createTeamBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-team')),
        message='找不到 创建Team按键')
    logging.debug('个人资料-查看我的team：' + createTeamBtn.text)
    createTeamBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 群组名称
    inputTeamName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper form .el-form-item:nth-of-type(1) input')),
        '找不到 群组名称输入栏')
    inputTeamName.send_keys(user['teamName'])

    # 群组介绍
    inputTeamDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper form .el-form-item:nth-of-type(2) input')),
        '找不到 群组介绍输入栏')
    inputTeamDes.send_keys(user['teamDes'])

    # 创建
    createBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-dialog div:nth-of-type(3) button:nth-of-type(2)')),
        message='找不到 创建按键')
    logging.debug('查看我的team-创建team：' + createBtn.text)
    createBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 核对TestTeam
def checkTeamInfo(driver, wait, user):
    if getTeamInfo(wait, 1, 2) != testTeam['NAME']:
        raise Exception(testTeam['NAME'] + ' 名字不对：' + getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != config.USER_ADMIN['NAME']:
        raise Exception(testTeam['NAME'] + ' 创建者不对：' + getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 5) != testTeam['DES']:
        raise Exception(testTeam['NAME'] + ' 描述不对：' + getTeamInfo(wait, 1, 5))

    # 核对Temp test team
    if getTeamInfo(wait, 2, 2) != user['teamName']:
        raise Exception(user['teamName'] + ' 名字不对：' + getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != user['NAME']:
        raise Exception(user['teamName'] + ' 创建者不对：' + getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 5) != user['teamDes']:
        raise Exception(user['teamName'] + ' 描述不对：' + getTeamInfo(wait, 2, 4))


# 测试修改team信息
def testModifyTeam(driver, wait, user, row=2, column=3):
    # 获取修改按键
    modifyTeamBtn = getTeamFunction(wait, row, column)
    modifyTeamBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 修改名称
    modifyTeamName = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            'div.el-dialog__wrapper:nth-of-type(4) .el-form-item:nth-of-type(1) input'
        )),
        message='找不到 修改team名称输入栏')
    modifyTeamName.send_keys(user['modifyTeamName'])

    # 修改描述
    modifyTeamDes = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            'div.el-dialog__wrapper:nth-of-type(4) .el-form-item:nth-of-type(2) input'
        )),
        message='找不到 修改team描述输入栏')
    modifyTeamDes.send_keys(user['modifyTeamDes'])

    # 确定修改
    confirmBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'div.el-dialog__wrapper:nth-of-type(4) button.el-button:nth-of-type(2)'
        )),
        message='找不到 确认修改按键')
    logging.debug('查看我的team-修改：' + confirmBtn.text)
    confirmBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 核对修改后信息
    teamName = getTeamInfo(wait, 2, 2)
    if teamName != user['modifyTeamName']:
        raise Exception(user['modifyTeamName'] + ' 修改后team名称不对：' + teamName)
    teamDes = getTeamInfo(wait, 2, 5)
    if teamDes != user['modifyTeamDes']:
        raise Exception(user['modifyTeamDes'] + ' 修改后team描述不对不对：' + teamDes)


# 测试TestTeam查看功能
def test_TestTeam(driver, wait, user):
    # 查看
    teamUserBtn_TestTeam = getTeamFunction(wait, 1, 1)
    teamUserBtn_TestTeam.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # Team名称
    teamName = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.container .title')),
        message='找不到 Team名称')
    if '群组名称：%s' % (testTeam['NAME']) not in teamName.text:
        raise Exception('群组名称不对：' + teamName.text)

    # 核对TEAM成员
    users = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'tbody tr td:nth-of-type(2) .cell')),
        message=testTeam['NAME'] + ' 获取用户信息失败')

    for teamUser in teamUsers:
        for user in users:
            if teamUser == user.text:
                users.remove(user)
                break
            if user == users[len(users) - 1]:
                raise Exception(testTeam['NAME'] + ' 找不到用户：' + teamUser)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回上一级按键')
    logging.debug('查看我的team-查看：' + backBtn.text)
    goTop(driver)
    backBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 测试TempTeam查看功能
def test_TempTeam(driver, wait, user):
    # 查看
    teamUserBtn_TestTeam = getTeamFunction(wait, 2, 2)
    teamUserBtn_TestTeam.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # Team名称
    teamName = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.container .title')),
        message='找不到 Team名称')
    if '群组名称：%s' % (user['modifyTeamName']) not in teamName.text:
        raise Exception('群组名称不对：' + teamName.text)

    # 删除成员
    deleteUserBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-icon-delete')),
        message='找不到 删除用户按键')
    deleteUserBtn.click()
    sleep(sleepTime)

    confirmDelBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定删除用户按键')
    logging.debug('查看我的team-查看：' + confirmDelBtn.text)
    confirmDelBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 添加用户到team
    addUserToTeam(driver, wait, user)

    # 核对TEAM成员
    users = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'tbody tr td:nth-of-type(2) .cell')),
        message=testTeam['NAME'] + ' 获取用户信息失败')

    for teamUser in teamUsers:
        for user in users:
            if teamUser == user.text:
                users.remove(user)
                break
            if user == users[len(users) - 1]:
                raise Exception(testTeam['NAME'] + ' 找不到用户：' + teamUser)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回上一级按键')
    logging.debug('查看我的team-查看：' + backBtn.text)
    goTop(driver)
    backBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 添加成员
def addUserToTeam(driver, wait, user):
    # 添加用户
    # logging.info('添加：' + username)
    # 点击用户下拉栏
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-input__inner')),
        message='找不到 用户列表下拉栏')
    userListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取所有user，users
    users = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 用户列表')

    # 添加按钮
    sureAddUserBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.sure-add')),
        message='找不到 添加用户按键')

    if len(users) != len(teamUsers):
        raise Exception('添加team用户列表显示异常')

    for user in users:
        if user != users[0]:
            userListBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)
        userName = user.get_attribute('innerText')
        if userName in teamUsers:
            logging.debug('team查看-添加用户：' + sureAddUserBtn.text + ' ' +
                          userName)
            goToElement(user, driver)
            user.click()
            sleep(sleepTime)

            goTop(driver)
            sureAddUserBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)

        else:
            raise Exception('team以外的用户存在team列表中')


# 删除team
def deleteTeam(wait, row=2, column=1):
    # 获取删除team按键
    deleteTeamBtn = getTeamFunction(wait, row, column)
    deleteTeamBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '[aria-label=提示] button.el-button:nth-of-type(2)')))
    logging.debug('查看我的team-删除：' + confirmBtn.text)
    confirmBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 确定删除成功
    teams = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'tbody tr')),
        message='找不到team列表')
    if len(teams) != 1:
        raise Exception('Team删除失败')


# 测试team查看用户等功能
def testTeamUser(driver, wait, user):
    # 测试TestTeam
    test_TestTeam(driver, wait, user)

    # 测试TempTeam
    test_TempTeam(driver, wait, user)


# 测试team 修改、查看、删除
def testTeamFunction(driver, wait, user):
    # 测试修改team信息
    testModifyTeam(driver, wait, user)
    # 测试team用户功能
    testTeamUser(driver, wait, user)
    # 测试删除team
    deleteTeam(wait)


# 添加产品类型
def addMod(driver, wait, user):
    # 产品列表下拉按钮
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(1) .el-input__inner')),
        message='不知道 产品列表下拉按键')
    proLisBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取产品列表，并判断是否存在产品名：TestProduct
    proLis = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.el-select-dropdown__list li')),
        message='找不到 下拉产品列表')

    for pro in proLis:
        proName = pro.get_attribute('innerText')
        # logging.info(proName)
        if proName == proMod['PRONAME_1']:
            logging.debug('新增产品-选择产品：' + proName)
            pro.click()
            break

        if pro == proLis[len(proLis) - 1]:
            raise Exception(proMod['PRONAME_1'] + ' 不存在')

    # 输入产品类型名称
    inputModuleName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(2) .el-input__inner')),
        message='找不到 产品类型输入栏')
    inputModuleName.send_keys(user['modName'])

    # 输入产品类型描述
    inputModuleDes = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'textarea.el-textarea__inner')),
        message='找不到 产品类型描述输入栏')
    inputModuleDes.send_keys(user['modDes'])

    # 点击创建按钮
    createModBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(4) .el-button:nth-of-type(1)')),
        message='找不到 创建产品类型按键')
    logging.debug('新增产品-立即创建：' + createModBtn.text)
    createModBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 前往添加成员页面
    gotoAddBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box .el-button:nth-of-type(2)')),
        message='找不到 前往添加成员页面按键')
    logging.debug('新增产品-立即前往：' + gotoAddBtn.text)
    gotoAddBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取产品-型号名称，确定是否创建成功
    isCreateName = wait.until(
        EC.text_to_be_present_in_element(
            ((By.CSS_SELECTOR, '.container .title')),
            proMod['PRONAME_1'] + '-' + user['modName']),
        message='找不到 产品-型号名称')
    if not isCreateName:
        raise Exception('型号创建失败 ' + proMod['PRONAME_1'] + '-' +
                        user['modName'])

    if '产品-产品经理' in user['NAME']:
        # 获取产品-型号创建人，确定是否创建成功
        isCreateUser = wait.until(
            EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                             '创建人：' + user['NAME']),
            message='找不到 产品-型号创建人')
        if not isCreateUser:
            raise Exception('型号创建失败 ' + '创建人：' + user['NAME'])
    else:
        # 获取产品-型号创建人，确定是否创建成功
        isCreateUser = wait.until(
            EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                             '创建人：Administrator'),
            message='找不到 产品-型号创建人')
        if not isCreateUser:
            raise Exception('型号创建失败: ' + '创建人：Administrator')

    # 获取产品-型号描述，确定是否创建成功
    isCreateDes = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.product-des')),
                                         '项目描述：' + user['modDes']),
        message='找不到 产品-型号描述')
    if not isCreateDes:
        raise Exception('型号创建失败 ' + '项目描述：' + user['modDes'])


# 添加角色
def addRole(driver, wait, user):
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-0')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    try:
        userListBtn.click()
    except Exception:
        userListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 添加角色按钮
    addRoleBtn = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.add-role-btn')),
        message='找不到 添加角色按键')
    logging.debug('用户列表-添加角色：' + addRoleBtn.text)

    if '产品-产品经理' in user['NAME']:
        # 角色列表下拉框
        roleListBtn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.add-rolelist .el-input__inner')),
            message='找不到 角色列表下拉按键')
        try:
            roleListBtn.click()
        except Exception:
            roleListBtn.send_keys(Keys.ENTER)
        sleep(sleepTime)

        # 获取所有角色
        roleList = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 '[x-placement] li')),
            message='找不到 下拉列表角色')

        # 添加角色
        if len(roleList) != 6:
            raise Exception('添加角色总数有误(6)：' + str(len(roleList)))
        for i in range(len(roleList)):
            logging.debug('添加角色总数：' + str(len(roleList)))
            if i:
                roleListBtn.click()
                sleep(sleepTime)

            role = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '[x-placement] li')),
                message='找不到 角色列表')
            logging.debug('用户列表-添加角色：' + role.get_attribute('innerText'))
            if role:
                role.click()
                sleep(sleepTime)
                try:
                    addRoleBtn.click()
                except Exception:
                    addRoleBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

    # 用户列表下拉按钮
    userRoleListBtn = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '.add-user .el-input__inner')),
        message='找不到 用户列表下拉按键')
    try:
        userRoleListBtn.click()
    except Exception:
        userRoleListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取所有用户
    userRoleList = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             '[x-placement] li')),
        message='找不到 下拉列表用户')

    if len(userRoleList) != len(teamUsers):
        raise Exception('用户列表显示异常')

    # 添加用户按钮
    addUserBtn = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.add-user-btn')),
        message='找不到 添加用户按键')

    sleep(sleepTime)
    # 已添加角色列表按钮
    roleAddListBtn = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '.add-role .el-input__inner')),
        message='找不到 已添加角色下拉列表按键')
    try:
        roleAddListBtn.click()
    except Exception:
        roleAddListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取所有添加的角色
    roleAddList = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             '[x-placement] li')),
        message='找不到 已添加角色')

    if len(roleAddList) != 6:
        raise Exception('已添加角色总数有误(6)：' + str(len(roleAddList)))

    # 列表行，获取显示用户角色
    row = 0

    if '产品-产品经理' in user['NAME']:
        for i in range(len(roleAddList)):
            logging.debug('已添加角色总数：' + str(len(roleAddList)))
            if i:
                # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
                test = roleAddListBtn.get_attribute('value')
                # logging.info(test)
                if test != '':
                    ActionChains(driver).move_to_element(
                        roleAddListBtn).perform()
                    clearUserBtn = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '.add-role .el-select__caret')))
                    try:
                        clearUserBtn.click()
                    except Exception:
                        clearUserBtn.send_keys(Keys.ENTER)
                    sleep(sleepTime)

                try:
                    roleAddListBtn.click()
                except Exception:
                    roleAddListBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

            role = roleAddList[i]
            roleName = role.text
            logging.debug('赋予角色：' + roleName)
            role.click()

            # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
            test = userRoleListBtn.get_attribute('value')
            # logging.info(test)
            if test != '':
                ActionChains(driver).move_to_element(userRoleListBtn).perform()
                clearUserBtn = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '.add-user .el-select__caret')))
                try:
                    clearUserBtn.click()
                except Exception:
                    clearUserBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

            try:
                userRoleListBtn.click()
            except Exception:
                userRoleListBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)

            for j in range(len(userRoleList)):
                userRole = userRoleList[j]
                userName = userRole.get_attribute('innerText')
                logging.debug(str(j) + ':' + userName)

                if userName not in teamUsers:
                    raise Exception('用户异常-用户：' + userName + ' 不在team里面')

                # 添加所有角色用户
                if roleName in userName:
                    logging.debug('用户列表-添加用户：' + addUserBtn.text + ' ' +
                                  userName)
                    goToElement(userRole, driver)
                    userRole.click()
                    sleep(sleepTime)
                    try:
                        addUserBtn.click()
                    except Exception:
                        addUserBtn.send_keys(Keys.ENTER)
                    sleep(sleepTime)

                    # 刷新用户列表
                    sleep(sleepTime + 1)

                    row += 1
                    # 获取列表显示是否正确
                    if getTeamInfo(wait, row, 2) != userName and getTeamInfo(
                            wait, row, 4) != roleName:
                        raise Exception('用户角色显示异常')

                    if getTeamInfo(wait, row, 4) == '产品经理' or getTeamInfo(
                            wait, row, 4) == '测试工程师':
                        deleteBtn = wait.until(
                            EC.element_to_be_clickable((
                                By.CSS_SELECTOR,
                                'tbody tr:nth-of-type(%d) td:nth-of-type(5) button'
                                % (row))),
                            message='找不到 删除按键')
                        try:
                            deleteBtn.click()
                        except Exception:
                            deleteBtn.send_keys(Keys.ENTER)
                        sleep(sleepTime)

                        # 确定删除按键
                        confirmDelBtn = wait.until(
                            EC.element_to_be_clickable((
                                By.CSS_SELECTOR,
                                '[aria-label=提示] .el-message-box__btns button:nth-of-type(2)'
                            )),
                            message='找不到 确定删除按键')
                        logging.debug('添加用户-删除：' + confirmDelBtn.text)
                        try:
                            confirmDelBtn.click()
                        except Exception:
                            confirmDelBtn.send_keys(Keys.ENTER)
                        sleep(sleepTime)
                        row -= 1

                        # 刷新用户列表
                        sleep(sleepTime)

                    break

    if '项目-产品经理' in user['NAME']:
        addProRole(driver, wait, user)


# 测试查询、修改
def searchPro(driver, wait, user):
    # 获取所有产品
    products = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品列表')

    # 所有产品总个数
    allPro = len(products)
    if allPro != 2:
        raise Exception('产品列表总数错误：' + str(allPro))

    # 判断列表显示是否正确
    if getTeamInfo(wait, 1, 2) != proMod['PRONAME_1']:
        raise Exception(proMod['PRONAME_1'] + ' 显示错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != proMod['PRODES_1']:
        raise Exception(proMod['PRONAME_1'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['PRONAME_1'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 1, 4))

    if getTeamInfo(wait, 2, 2) != proMod['PRONAME_2']:
        raise Exception(proMod['PRONAME_2'] + ' 显示错误' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != proMod['PRODES_2']:
        raise Exception(proMod['PRONAME_2'] + ' 描述显示错误' +
                        getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['PRONAME_2'] + ' 创建人显示错误' +
                        getTeamInfo(wait, 2, 4))

    global isModifyPro
    if '产品-产品经理' in user['NAME']:
        # 修改'TestProduct'产品信息
        for i in range(len(products)):
            proName = getTeamInfo(wait, i + 1, 2)
            if proMod['PRONAME_1'] == proName:
                # 点击修改
                modifyProBtn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         '.el-table__row:nth-of-type(%d) button:nth-of-type(2)'
                         % (i + 1))),
                    message='找不到 产品-修改按键')
                logging.debug('产品管理-产品列表：' +
                              modifyProBtn.get_attribute('innerText'))
                try:
                    modifyProBtn.click()
                    sleep(sleepTime)
                except Exception:
                    modifyProBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)
                # 修改信息
                modifyProInfo(driver, wait, user)

        # 查询输入栏
        searchInput = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '.search-product-input input')),
            message='找不到 产品查询输入栏')
        searchInput.send_keys(user['modifyPro'])

        # 根据产品名查询
        searchBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.search-project-btn')),
            message='找不到 按产品查询按键')
        logging.debug('产品管理-产品列表：' + searchBtn.text)
        try:
            searchBtn.click()
        except Exception:
            searchBtn.send_keys(Keys.ENTER)
        sleep(sleepTime)

        products = wait.until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                                   '.el-table__row')),
            message='找不到 产品列表')
        # 修改user['modifyPro']产品信息
        for i in range(len(products)):
            htmlText = products[i].get_attribute('innerHTML')
            if user['modifyPro'] in htmlText:
                # 点击修改
                modifyProBtn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         '.el-table__row:nth-of-type(%d) button:nth-of-type(2)'
                         % (i + 1))),
                    message='找不到 产品-修改按键')
                logging.debug('产品管理-产品列表：' +
                              modifyProBtn.get_attribute('innerText'))
                try:
                    modifyProBtn.click()
                    sleep(sleepTime)
                except Exception:
                    modifyProBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)
                # 修改信息
                modifyProInfo(driver, wait, user)

    else:
        # 查询输入栏
        searchInput = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '.search-product-input input')),
            message='找不到 产品查询输入栏')
        searchInput.send_keys(proMod['PRONAME_1'])

        # 根据产品名查询
        searchBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.search-project-btn')),
            message='找不到 按产品查询按键')
        logging.debug('产品管理-产品列表：' + searchBtn.text)
        try:
            searchBtn.click()
        except Exception:
            searchBtn.send_keys(Keys.ENTER)
        sleep(sleepTime)

        products = wait.until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                                   '.el-table__row')),
            message='找不到 产品列表')
        # 修改user['modifyPro']产品信息
        for i in range(len(products)):
            htmlText = products[i].get_attribute('innerHTML')
            if proMod['PRONAME_1'] not in htmlText:
                raise Exception('按产品线查询产品失败')

    # 所有产品
    allProBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-all')),
        message='找不到 所有产品按键')
    logging.debug('产品管理-产品列表：' + allProBtn.text)
    try:
        allProBtn.click()
        sleep(sleepTime)
    except Exception:
        allProBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    products = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品列表')

    # 判断列表显示是否正确
    if getTeamInfo(wait, 1, 2) != proMod['PRONAME_1']:
        raise Exception(proMod['PRONAME_1'] + ' 显示错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != proMod['PRODES_1']:
        raise Exception(proMod['PRONAME_1'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['PRONAME_1'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 1, 4))

    if getTeamInfo(wait, 2, 2) != proMod['PRONAME_2']:
        raise Exception(proMod['PRONAME_2'] + ' 显示错误' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != proMod['PRODES_2']:
        raise Exception(proMod['PRONAME_2'] + ' 描述显示错误' +
                        getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['PRONAME_2'] + ' 创建人显示错误' +
                        getTeamInfo(wait, 2, 4))

    if len(products) != allPro:
        raise Exception('全部产品查询失败')

    # 查看型号
    i = 1
    for pro in products:
        htmlText = pro.get_attribute('innerHTML')
        if proMod['PRONAME_1'] in htmlText:
            break
        i += 1
    searchTestProBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-table__row:nth-of-type(%d) .el-button--primary' % (i))),
        message='找不到 产品-查看按键')
    logging.debug('产品管理-产品列表：' + searchTestProBtn.get_attribute('innerText'))
    try:
        searchTestProBtn.click()
        sleep(sleepTime)
    except Exception:
        searchTestProBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取所有产品类型
    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')

    if '产品-产品经理' in user['NAME']:
        # 所有产品类型总个数
        allMod = len(modules)
        if allMod != 3:
            raise Exception('型号总数错误：' + str(allMod))

        if getTeamInfo(wait, 3, 2) != user['modName']:
            raise Exception(user['modName'] + ' 显示错误：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 3, 3) != user['modDes']:
            raise Exception(user['modName'] + ' 描述显示错误：' +
                            getTeamInfo(wait, 3, 3))
        if getTeamInfo(wait, 3, 4) != user['NAME']:
            raise Exception(user['modName'] + ' 创建人显示错误：' +
                            getTeamInfo(wait, 3, 4))

    else:
        # 所有产品类型总个数
        allMod = len(modules)
        if allMod != 2:
            raise Exception('型号总数错误：' + str(allMod))

    # 判断列表显示是否正确
    if getTeamInfo(wait, 1, 2) != proMod['MODNAME_1']:
        raise Exception(proMod['MODNAME_1'] + ' 显示错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != proMod['MODDES_1']:
        raise Exception(proMod['MODNAME_1'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['MODNAME_1'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 1, 4))

    if getTeamInfo(wait, 2, 2) != proMod['MODNAME_2']:
        raise Exception(proMod['MODNAME_2'] + ' 显示错误：' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != proMod['MODDES_2']:
        raise Exception(proMod['MODNAME_2'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['MODNAME_2'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 2, 4))

    # 查询输入栏
    searchInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-product-input input')),
        message='找不到 产品类型查询输入栏')
    searchInput.send_keys(proMod['MODNAME_1'])

    # 产品列表-查看:查询
    searchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-project-btn')),
        message='找不到 按产品类型查询按键')
    logging.debug('产品列表-查看：' + searchBtn.text)
    try:
        searchBtn.click()
    except Exception:
        searchBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')
    for mod in modules:
        htmlText = mod.get_attribute('innerHTML')
        if proMod['MODNAME_1'] not in htmlText:
            raise Exception('根据产品类型名查询失败')

    # 所有产品类型
    allModBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-all')),
        message='找不到 所有产品类型按键')
    logging.debug('产品管理-产品列表：' + allModBtn.text)
    try:
        allModBtn.click()
    except Exception:
        allModBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')
    if len(modules) != allMod:
        raise Exception('全部产品查询失败')

    # 判断列表显示是否正确
    if getTeamInfo(wait, 1, 2) != proMod['MODNAME_1']:
        raise Exception(proMod['MODNAME_1'] + ' 显示错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != proMod['MODDES_1']:
        raise Exception(proMod['MODNAME_1'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['MODNAME_1'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 1, 4))

    if getTeamInfo(wait, 2, 2) != proMod['MODNAME_2']:
        raise Exception(proMod['MODNAME_2'] + ' 显示错误：' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != proMod['MODDES_2']:
        raise Exception(proMod['MODNAME_2'] + ' 描述显示错误：' +
                        getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 4) != config.USER_ADMIN['NAME']:
        raise Exception(proMod['MODNAME_2'] + ' 创建人显示错误：' +
                        getTeamInfo(wait, 2, 4))

    if '产品-产品经理' in user['NAME']:
        if getTeamInfo(wait, 3, 2) != user['modName']:
            raise Exception(user['modName'] + ' 显示错误：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 3, 3) != user['modDes']:
            raise Exception(user['modName'] + ' 描述显示错误：' +
                            getTeamInfo(wait, 3, 3))
        if getTeamInfo(wait, 3, 4) != user['NAME']:
            raise Exception(user['modName'] + ' 创建人显示错误：' +
                            getTeamInfo(wait, 3, 4))


# 修改产品信息
def modifyProInfo(driver, wait, user):
    global isModifyPro
    # 产品名称输入栏
    inputProName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper .el-form-item:nth-of-type(1) input')),
        message='找不到 产品名称输入栏')
    if isModifyPro:
        inputProName.send_keys(Keys.CONTROL + 'a')
        inputProName.send_keys(proMod['PRONAME_1'])
    else:
        inputProName.send_keys(Keys.CONTROL + 'a')
        inputProName.send_keys(user['modifyPro'])

    # 产品描述输入栏
    inputProDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper .el-form-item:nth-of-type(2) input')),
        message='找不到 产品描述输入栏')
    if isModifyPro:
        inputProName.send_keys(Keys.CONTROL + 'a')
        inputProDes.send_keys(proMod['PRODES_1'])
    else:
        inputProName.send_keys(Keys.CONTROL + 'a')
        inputProDes.send_keys(user['modifyProDes'])

    # 确定修改
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-dialog__wrapper button:nth-of-type(2)')),
        message='找不到 确定修改按键')
    logging.debug('产品列表-修改：' + confirmBtn.text)
    try:
        confirmBtn.click()
    except Exception:
        confirmBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    isModifyPro = not isModifyPro


# 添加产品类型
def test_addProMod(driver, wait, user):
    # 输入类型名称
    inputModName = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.add-module-name input')),
        message='找不到 产品类型名称输入栏')
    inputModName.send_keys(user['tempMod'])

    # 输入类型描述
    inputModDes = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.add-mudule-des input')),
        message='找不到 产品类型描述输入栏')
    inputModDes.send_keys(user['tempModDes'])

    # 添加
    addProModBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add')),
        message='找不到 添加产品类型按键')
    logging.debug('产品列表-查看：' + addProModBtn.text)
    try:
        addProModBtn.click()
        sleep(sleepTime)
    except Exception:
        addProModBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)


# 修改产品类型
def modifyMod(driver, wait, user):
    if '产品-产品经理' in user['NAME']:
        # 输入产品类型名称
        inputProModName = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.el-dialog__wrapper .el-form-item:nth-of-type(1) input')),
            message='找不到 产品类型名称输入栏')
        inputProModName.send_keys(Keys.CONTROL + 'a')
        inputProModName.send_keys(user['modifyMod'])

        # 输入产品类型描述
        inputProModDes = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.el-dialog__wrapper .el-form-item:nth-of-type(2) input')),
            message='找不到 产品类型描述输入栏')
        inputProModName.send_keys(Keys.CONTROL + 'a')
        inputProModDes.send_keys(user['modifyModDes'])

        # 确认修改
        confirmBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'div.el-dialog__wrapper .el-dialog__footer button:nth-of-type(2)'
            )),
            message='找不到 确认修改产品类型按键')
        logging.debug('产品列表-查看：' + confirmBtn.text)
        try:
            confirmBtn.click()
            sleep(sleepTime)
        except Exception:
            confirmBtn.send_keys(Keys.ENTER)
        sleep(sleepTime)

    if '项目-产品经理' in user['NAME']:
        global isModifyMod
        # 输入产品类型名称
        inputProModName = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.el-dialog__wrapper .el-form-item:nth-of-type(1) input')),
            message='找不到 产品类型名称输入栏')
        if isModifyMod:
            inputProModName.send_keys(Keys.CONTROL + 'a')
            inputProModName.send_keys(proMod['MODNAME_1'])
        else:
            inputProModName.send_keys(Keys.CONTROL + 'a')
            inputProModName.send_keys(user['modifyMod'])

        # 输入产品类型描述
        inputProModDes = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.el-dialog__wrapper .el-form-item:nth-of-type(2) input')),
            message='找不到 产品类型描述输入栏')
        if isModifyMod:
            inputProModDes.send_keys(proMod['MODDES_1'])
        else:
            inputProModDes.send_keys(user['modifyModDes'])

        # 确认修改
        confirmBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'div.el-dialog__wrapper .el-dialog__footer button:nth-of-type(2)'
            )),
            message='找不到 确认修改产品类型按键')
        logging.debug('产品列表-查看：' + confirmBtn.text)
        confirmBtn.click()

        isModifyMod = not isModifyMod

        sleep(sleepTime)


# 测试查看-添加角色
def test_addRole(driver, wait, user):
    # 添加角色用户

    # 获取产品-型号名称，确定是否加载成功
    isCreateName = wait.until(
        EC.text_to_be_present_in_element(
            ((By.CSS_SELECTOR, '.container .title')),
            '项目名称：' + proMod['PRONAME_1'] + '-' + user['modifyMod']),
        message='找不到 产品-型号名称')
    if not isCreateName:
        raise Exception('型号创建失败 项目名称：' + proMod['PRONAME_1'] + '-' +
                        user['modifyMod'])

    if '产品-产品经理' in user['NAME']:
        # 获取产品-型号创建人，确定是否创建成功
        isCreateUser = wait.until(
            EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                             '创建人：' + user['NAME']),
            message='找不到 产品-型号创建人')
        if not isCreateUser:
            raise Exception('型号创建失败 ' + '创建人：' + user['NAME'])
    else:
        # 获取产品-型号创建人，确定是否创建成功
        isCreateUser = wait.until(
            EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                             '创建人：Administrator'),
            message='找不到 产品-型号创建人')
        if not isCreateUser:
            raise Exception('型号创建失败: ' + '创建人：Administrator')

    # 获取产品-型号描述，确定是否加载成功
    isCreateDes = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.product-des')),
                                         '项目描述：' + user['modifyModDes']),
        message='找不到 产品-型号描述')
    if not isCreateDes:
        raise Exception('型号创建失败 项目描述：' + user['modifyModDes'])

    # 添加角色
    addRole(driver, wait, user)


# 测试修改
def test_modifyProMod(driver, wait, user):
    # 获取所有产品类型
    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')

    # 找出新添加的产品型号，并修改
    for i in range(len(modules)):
        # 产品型号名称
        proModName = getTeamInfo(wait, i + 1, 2)
        # 产品型号描述
        proModDes = getTeamInfo(wait, i + 1, 3)
        # 产品型号创建者
        proModUser = getTeamInfo(wait, i + 1, 4)

        if '产品-产品经理' in user['NAME']:
            if proModName == user['modName'] and proModDes == user[
                    'modDes'] and proModUser == user['NAME']:
                #  修改产品类型按键
                modifyModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(2)'
                        % (i + 1))),
                    message='找不到 修改产品类型按键')
                logging.debug('产品列表-查看：' + modifyModBtn.text)
                try:
                    modifyModBtn.click()
                    sleep(sleepTime)
                except Exception:
                    modifyModBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

                # 修改产品类型
                modifyMod(driver, wait, user)

            if proModName == user['tempMod'] and proModDes == user[
                    'tempModDes'] and proModUser == user['NAME']:
                #  修改产品类型按键
                modifyModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(2)'
                        % (i + 1))),
                    message='找不到 修改产品类型按键')
                logging.debug('产品列表-查看：' + modifyModBtn.text)
                try:
                    modifyModBtn.click()
                    sleep(sleepTime)
                except Exception:
                    modifyModBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

                # 修改产品类型
                modifyMod(driver, wait, user)

                #  查看产品类型按键
                addRoleModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(1)'
                        % (i + 1))),
                    message='找不到 查看产品类型按键')
                logging.debug('产品列表-查看：' + addRoleModBtn.text)
                try:
                    addRoleModBtn.click()
                    sleep(sleepTime)
                except Exception:
                    addRoleModBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

                # 测试添加用户角色
                test_addRole(driver, wait, user)

                # 返回上一级
                backBtn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
                    message='找不到 返回上一级按键')
                logging.debug('产品列表-查看：' + backBtn.text)
                goTop(driver)
                try:
                    backBtn.click()
                except Exception:
                    backBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

        elif '项目-产品经理' in user['NAME']:
            if proModName == proMod['MODNAME_1']:
                #  修改产品类型按键
                modifyModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(2)'
                        % (i + 1))),
                    message='找不到 修改产品类型按键')
                logging.debug('产品列表-查看：' + modifyModBtn.text)
                modifyModBtn.click()

                # 修改产品类型
                modifyMod(driver, wait, user)

                #  查看产品类型按键
                addRoleModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(1)'
                        % (i + 1))),
                    message='找不到 查看产品类型按键')
                logging.debug('产品列表-查看：' + addRoleModBtn.text)
                try:
                    addRoleModBtn.click()
                    sleep(sleepTime)
                except Exception:
                    addRoleModBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

                # 测试添加用户角色
                test_addRole(driver, wait, user)

                # 返回上一级
                backBtn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
                    message='找不到 返回上一级按键')
                logging.debug('产品列表-查看：' + backBtn.text)
                goTop(driver)
                try:
                    backBtn.click()
                except Exception:
                    backBtn.send_keys(Keys.ENTER)
                sleep(sleepTime)

            if proModName == user['modifyMod']:
                #  修改产品类型按键
                modifyModBtn = wait.until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(2)'
                        % (i + 1))),
                    message='找不到 修改产品类型按键')
                logging.debug('产品列表-查看：' + modifyModBtn.text)
                modifyModBtn.click()

                # 修改产品类型
                modifyMod(driver, wait, user)

                # 查看产品成员是否为空
                # 点击用户列表按钮
                userListBtn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
                    message='找不到 用户列表tab按键')
                logging.debug('产品型号-用户列表：' + userListBtn.text)
                userListBtn.click()
                sleep(sleepTime)

                empytText = wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.el-table__empty-block'), '暂无数据'),
                    message='产品成员可见(应该不可见)')

                if empytText is False:
                    raise Exception('产品成员可见(应该不可见)')

                break

        else:
            # 产品型号-查看
            searchTestProBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     '.el-table__row:nth-of-type(1) .el-button--primary')),
                message='找不到 产品-查看按键')
            logging.debug('产品管理-产品列表：' +
                          searchTestProBtn.get_attribute('innerText'))
            searchTestProBtn.click()
            sleep(sleepTime)

            # 获取产品-型号名称，确定是否加载成功
            isCreateName = wait.until(
                EC.text_to_be_present_in_element(
                    ((By.CSS_SELECTOR, '.container .title')),
                    '项目名称：' + proMod['PRONAME_1'] + '-' + proMod['MODNAME_1']),
                message='找不到 产品-型号名称')
            if not isCreateName:
                raise Exception('型号创建失败 项目名称：' + proMod['PRONAME_1'] + '-' +
                                proMod['MODNAME_1'])

            # 获取产品-型号创建人，确定是否加载成功
            isCreateUser = wait.until(
                EC.text_to_be_present_in_element(
                    ((By.CSS_SELECTOR, '.creator')),
                    '创建人：' + config.USER_ADMIN['NAME']),
                message='找不到 产品-型号创建人')
            if not isCreateUser:
                raise Exception('型号创建失败 创建人:' + config.USER_ADMIN['NAME'])

            # 获取产品-型号描述，确定是否加载成功
            isCreateDes = wait.until(
                EC.text_to_be_present_in_element(
                    ((By.CSS_SELECTOR, '.product-des')),
                    '项目描述：' + proMod['MODDES_1']),
                message='找不到 产品-型号描述')
            if not isCreateDes:
                raise Exception('型号创建失败 项目描述：' + proMod['MODDES_1'])
            sleep(sleepTime)

            if '产品' in user['NAME']:
                users = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         '[aria-labelledby=tab-0] tbody tr td:nth-child(2)')),
                    message='找不到项目成员')
                if len(users) != 6:
                    raise Exception('项目成员数量不对')
                for _user in users:
                    name = _user.get_attribute('innerText').strip('\n')
                    if name not in config.teamUsers:
                        raise Exception('项目成员显示不对')

            # 返回上一级
            backBtn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
                message='找不到 返回上一级按键')
            logging.debug('产品列表-查看：' + backBtn.text)
            goTop(driver)
            backBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)

            # 点击用户列表按钮
            userListBtn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
                message='找不到 用户列表tab按键')
            logging.debug('产品型号-用户列表：' + userListBtn.text)
            try:
                userListBtn.click()
            except Exception:
                userListBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)

            if '产品' in user['NAME']:
                users = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         '[aria-labelledby=tab-1] tbody tr td:nth-child(2)')),
                    message='找不到项目成员')
                if len(users) != 6:
                    raise Exception('项目成员数量不对')
                for _user in users:
                    name = _user.get_attribute('innerText').strip('\n')
                    if name not in config.teamUsers:
                        raise Exception('项目成员显示不对')

            if '项目' in user['NAME'] and '产品-项目工程师' not in user['NAME']:
                empytText = wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.el-table__empty-block'), '暂无数据'),
                    message='产品成员可见(应该不可见)')

                if empytText is False:
                    raise Exception('产品成员可见(应该不可见)')
            break


# 测试删除
def test_deleteProMod(driver, wait, user):
    global admin
    # 获取所有产品类型
    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')

    # 定位产品类型
    row = 1
    # 找出新添加的产品型号，并修改
    for _ in range(len(modules)):

        # 产品型号名称
        proModName = getTeamInfo(wait, row, 2)
        # 产品型号描述
        proModDes = getTeamInfo(wait, row, 3)
        # 产品型号创建者
        proModUser = getTeamInfo(wait, row, 4)

        if proModName == user['modifyMod'] and proModDes == user[
                'modifyModDes'] and proModUser == user['NAME']:
            model_id = getTeamInfo(wait, row, 1)
            doTest()
            admin['moduleid'] = int(model_id)
            # 用户登陆配置
            deleteCase = {
                'method': 'delete',
                'url': '/api/v1/middleware/module',
                'params': admin,
                'json': {},
                'response': {
                    'errcode': '0',
                    'errmsg': 'ok'
                }
            }
            result = doTest(deleteCase)
            if result.get('error'):
                raise Exception(result['error'])

        row += 1


# 添加角色
def addProRole(driver, wait, user):
    if '产品-产品经理' in user['NAME']:
        # 点击用户列表按钮
        userListBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
            message='找不到 用户列表tab按键')
        logging.debug('产品型号-用户列表：' + userListBtn.text)
        try:
            userListBtn.click()
        except Exception:
            userListBtn.send_keys(Keys.ENTER)

    # 用户列表下拉按钮
    userRoleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-user .el-input__inner')),
        message='找不到 用户列表下拉按键')
    try:
        userRoleListBtn.click()
    except Exception:
        userRoleListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 获取所有用户
    userRoleList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 下拉列表用户')

    if len(userRoleList) != len(teamUsers):
        raise Exception('用户列表显示异常')

    # 添加用户按钮
    addUserBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-user-btn')),
        message='找不到 添加用户按键')

    sleep(sleepTime)
    # 已添加角色列表按钮
    roleAddListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-role .el-input__inner')),
        message='找不到 已添加角色下拉列表按键')
    roleAddListBtn.click()
    sleep(sleepTime)

    # 获取所有添加的角色
    roleAddList = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 已添加角色')

    if len(roleAddList) != 6:
        raise Exception('已添加角色总数有误(6)：' + str(len(roleAddList)))

    for i in range(len(roleAddList)):
        logging.debug('已添加角色总数：' + str(len(roleAddList)))
        '''
        if i:
            # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
            test = roleAddListBtn.get_attribute('value')
            # logging.info(test)
            if test != '':
                ActionChains(driver).move_to_element(roleAddListBtn).perform()
                clearUserBtn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '.add-role .el-select__caret')))
                clearUserBtn.click()

            roleAddListBtn.click()
            sleep(time)
        '''
        role = roleAddList[i]
        roleName = role.text

        # 添加测试工程师
        if roleName == '测试工程师':
            logging.debug('赋予角色：' + roleName)
            role.click()

            # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
            test = userRoleListBtn.get_attribute('value')
            # logging.info(test)
            if test != '':
                ActionChains(driver).move_to_element(userRoleListBtn).perform()
                clearUserBtn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '.add-user .el-select__caret')))
                clearUserBtn.send_keys(Keys.ENTER)

            userRoleListBtn.send_keys(Keys.ENTER)
            sleep(sleepTime)

            for j in range(len(userRoleList)):
                user_ = userRoleList[j]
                userName = user_.get_attribute('innerText')
                logging.debug(str(j) + ':' + userName)

                if userName not in teamUsers:
                    raise Exception('用户异常-用户：' + userName + ' 不在team里面')

                # 添加所有角色用户
                if userName == user['NAME']:
                    logging.debug('用户列表-添加用户：' + addUserBtn.text + ' ' +
                                  userName)
                    goToElement(user_, driver)
                    user_.click()
                    sleep(sleepTime)
                    try:
                        addUserBtn.click()
                        sleep(sleepTime)
                    except Exception:
                        addUserBtn.send_keys(Keys.ENTER)

                    sleep(sleepTime)

                    break
            break

    # 删除新添加的测试工程师
    for i in range(1, 7):
        if '产品-产品经理' in user['NAME']:
            user_ = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    '[aria-labelledby="tab-1"] tbody tr:nth-of-type(%d) td:nth-of-type(%d)'
                    % (i, 2))),
                message='获取用户列表信息失败').text
            role = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    '[aria-labelledby="tab-1"] tbody tr:nth-of-type(%d) td:nth-of-type(%d)'
                    % (i, 4))),
                message='获取角色列表信息失败').text
        else:
            user_ = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    '[aria-labelledby="tab-0"] tbody tr:nth-of-type(%d) td:nth-of-type(%d)'
                    % (i, 2))),
                message='获取用户列表信息失败').text
            role = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    '[aria-labelledby="tab-0"] tbody tr:nth-of-type(%d) td:nth-of-type(%d)'
                    % (i, 4))),
                message='获取角色列表信息失败').text
        if user_ == user['NAME'] and role == '测试工程师':
            deleteBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%d) td:nth-of-type(5) button' %
                     (i))),
                message='找不到 删除按键')
            try:
                deleteBtn.click()
            except Exception:
                deleteBtn.send_keys(Keys.ENTER)

            # 确定删除按键
            confirmDelBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '[aria-label=提示] .el-message-box__btns button:nth-of-type(2)'
                )),
                message='找不到 确定删除按键')
            logging.debug('添加用户-删除：' + confirmDelBtn.text)
            try:
                confirmDelBtn.click()
            except Exception:
                confirmDelBtn.send_keys(Keys.ENTER)
            break

        if i == 6:
            raise ('新添加：' + user['NAME'] + ' 测试工程师 不存在')

    # 刷新用户列表
    sleep(sleepTime)


# 测试项目功能：添加、修改、删除
def test_proModFuc(driver, wait, user):
    # 测试添加产品类型
    if '产品-产品经理' in user['NAME']:
        test_addProMod(driver, wait, user)

    # 测试修改
    test_modifyProMod(driver, wait, user)

    if '产品-产品经理' in user['NAME']:
        # 测试删除
        test_deleteProMod(driver, wait, user)
        # 测试产品添加删除角色(未完成)
        addProRole(driver, wait, user)

    if '项目-产品经理' in user['NAME']:
        # 修改回原来名字
        test_modifyProMod(driver, wait, user)


# 按订单号查询
def searchByOrderNum(driver, wait, user):
    # 订单号查询输入栏
    inputOrderNum = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-input input')),
        message='找不到 订单号查询输入')
    if '产品-产线工程师' in user['NAME']:
        inputOrderNum.send_keys(config.ORDER_2['NUM'])
    else:
        inputOrderNum.send_keys(config.ORDER_1['NUM'])

    # 按订单号查询
    ordNumSearchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'button.sure:nth-of-type(3)')),
        message='找不到 按订单号查询按键')
    logging.debug('订单列表-查询：' + ordNumSearchBtn.text)
    try:
        ordNumSearchBtn.click()
        sleep(sleepTime)
    except Exception:
        ordNumSearchBtn.send_keys(Keys.ENTER)
    if '产品-产线工程师' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + ' 订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 1, 5) != config.ORDER_2['FACTORY']:
            raise Exception(config.ORDER_2['FACTORY'] + ' 工厂不对：' +
                            getTeamInfo(wait, 1, 5))
        if getTeamInfo(wait, 1, 6) != str((datetime(2019, 11, 1) - datetime.now()).days):
            raise Exception(str((datetime(2019, 11, 1) - datetime.now()).days) + ' 有效时间不对：' +
                            getTeamInfo(wait, 1, 6))
    else:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + ' 订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 1, 5) != config.ORDER_1['FACTORY']:
            raise Exception(config.ORDER_1['FACTORY'] + ' 工厂不对：' +
                            getTeamInfo(wait, 1, 5))
        if getTeamInfo(wait, 1, 6) != str((datetime(2019, 11, 1) - datetime.now()).days):
            raise Exception(str((datetime(2019, 11, 1) - datetime.now()).days) + ' 有效时间不对：' +
                            getTeamInfo(wait, 1, 6))


# 按产品类型查询
def searchByProMod(driver, wait, user):
    # 选择产品
    prolistBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-select:nth-of-type(1) input')),
        message='找不到 产品列表下拉按键')
    try:
        prolistBtn.click()
        sleep(sleepTime)
    except Exception:
        prolistBtn.send_keys(Keys.ENTER)

    proList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品列表')
    for i in range(len(proList)):
        pro = proList[i].get_attribute('innerText')
        if pro == proMod['PRONAME_1']:
            proList[i].click()
            sleep(sleepTime)
            break

        if i == len(proList) - 1:
            raise Exception(proMod['PRONAME_1'] + ' 不存在')

    # 选择型号
    modlistBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-select:nth-of-type(2) input')),
        message='找不到 产品类型列表下拉按键')
    try:
        modlistBtn.click()
        sleep(sleepTime)
    except Exception:
        modlistBtn.send_keys(Keys.ENTER)

    modList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品类型列表')
    for i in range(len(modList)):
        mod = modList[i].get_attribute('innerText')
        if mod == proMod['MODNAME_1']:
            modList[i].click()
            sleep(sleepTime)
            break

        if i == len(modList) - 1:
            raise Exception(proMod['MODNAME_1'] + ' 不存在')

    # 按产品类型查询
    proModSearchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'button.sure:nth-of-type(1)')),
        message='找不到 按产品类型查询按键')
    logging.debug('订单列表-查询：' + proModSearchBtn.text)
    try:
        proModSearchBtn.click()
        sleep(sleepTime)
    except Exception:
        proModSearchBtn.send_keys(Keys.ENTER)
    if 'pmc' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != '20181111':
            raise Exception('20181111' + '订单号不对：' + getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))
        if getTeamInfo(wait, 3, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 3, 2))

    elif '项目-产线工程师' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))

    elif '产品-产线工程师' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))

    else:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))


# 创建订单
def createOrder(wait, product, module, order, pe, user, driver):
    # 点击订单列表
    orderList = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(4) .el-menu-item:nth-of-type(2)'
        )),
        message='找不到 订单列表')
    logging.debug('订单管理：' + orderList.text)
    orderList.click()
    sleep(sleepTime)

    # 获取订单号
    orders = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'tbody tr td:nth-child(2) div')),
        message='找不到 订单号')

    for i in range(len(orders)):
        if order['NUM'] == orders[i].text:
            logging.debug('订单已存在')
            # 删除订单
            btn = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%s) td:nth-child(1) div' % (i + 1))),
                message='找不到 订单信息扩展按键')
            btn.click()
            sleep(sleepTime)

            order_id = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%s) td:nth-child(1) div div span' %
                     (i + 2))),
                message='找不到 订单ID').get_attribute('innerText')

            doTest()
            admin['orderid'] = int(order_id)
            # 删除配置
            deleteCase = {
                'method': 'delete',
                'url': '/api/v1/middleware/order',
                'params': admin,
                'json': {},
                'response': {
                    'errcode': '0',
                    'errmsg': 'ok'
                }
            }
            result = doTest(deleteCase)
            if result.get('error'):
                raise Exception(result['error'])
            break

    # 点击创建订单
    createOrderBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(4) ul li:nth-child(1)')),
        message='找不到 创建订单项')
    logging.debug('订单管理-创建订单：' + createOrderBtn.text)
    createOrderBtn.click()
    sleep(sleepTime)

    # 选择产品
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(1) .el-input__inner')),
        message='找不到 产品列表下拉按键')
    proLisBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    proList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 产品列表')
    for pro in proList:
        proName = pro.get_attribute('innerText')
        if proName == product:
            logging.debug('创建订单-选择产品：' + proName)
            pro.click()
            sleep(sleepTime)
            break
        if pro == proList[len(proList) - 1]:
            raise Exception('上传软件-选择产品：产品不存在')

    # 选择型号
    modLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(2) .el-input__inner')),
        message='找不到 型号列表下拉按键')
    modLisBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    modList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 型号列表')
    for mod in modList:
        modName = mod.get_attribute('innerText')
        if modName == module:
            logging.debug('创建订单-选择型号：' + modName)
            mod.click()
            sleep(sleepTime)
            break
        if mod == modList[len(modList) - 1]:
            raise Exception('上传软件-选择产品：型号不存在')

    # 输入订单号
    inputOrderNum = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(3) .el-input__inner')),
        message='找不到 订单号输入栏')
    inputOrderNum.send_keys(order['NUM'])
    logging.debug('创建订单-订单：' + order['NUM'])

    # 生产数量
    outLineNum = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.order-item:nth-of-type(4) div .el-input__inner')),
        message='找不到 生产数量输入栏')
    outLineNum.send_keys(1000)
    logging.debug('创建订单-生产数量：1000')

    # 生产工厂
    factoryName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(5) .el-input__inner')),
        message='找不到 生产工厂输入栏')
    factoryName.send_keys(Keys.ENTER)
    sleep(sleepTime)

    factorys = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li')),
        message='找不到 工厂列表')
    for factory in factorys:
        factory_name = factory.text
        if factory_name == order['FACTORY']:
            factory.click()
            sleep(sleepTime)
            break

        if factory == factorys[len(factorys) - 1]:
            raise Exception('找不到工厂 ' + order['FACTORY'])
    logging.debug('创建订单-生产工厂：' + order['FACTORY'])

    # 申请者
    applicantListBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(6) .el-input__inner')),
        message='找不到 申请人列表下拉按键')
    applicantListBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    applicantList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 申请人列表')
    if len(applicantList):
        for applicant in applicantList:
            appName = applicant.get_attribute('innerText')
            if appName == pe:
                logging.debug('创建订单-申请者：' + appName)
                applicant.click()
                sleep(sleepTime)
                break
            if applicant == applicantList[len(applicantList) - 1]:
                raise Exception(pe + ' 申请者不存在')

    # 证书有效时间
    inputDate = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(7) .el-input__inner')),
        message='找不到 证书时间输入栏')
    inputDate.send_keys(order['TIME'])
    inputDate.send_keys(Keys.ENTER)
    logging.debug('创建订单-证书有效时间：' + order['TIME'])

    # 订单介绍
    inputOrderDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(8) .el-input__inner')),
        message='找不到 订单介绍输入栏')
    inputOrderDes.send_keys(order['DES'])
    logging.debug('创建订单-订单介绍：' + order['DES'])

    # 创建订单
    createBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-order')),
        message='找不到 创建订单按键')
    logging.debug('创建订单：' + createBtn.text)
    createBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    upOK = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.page-finish'),
                                         '成功创建'),
        message='创建订单失败')

    if upOK is False:
        raise Exception('创建订单失败')

    sleep(sleepTime)


# 查询所有订单
def searchAllOrder(driver, wait, user):
    allOrderBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-all')),
        message='找不到 查询所有订单按键')
    logging.debug('订单列表-查询：' + allOrderBtn.text)
    try:
        allOrderBtn.click()
        sleep(sleepTime)
    except Exception:
        allOrderBtn.send_keys(Keys.ENTER)

    if 'pmc' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != '20181111':
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))
        if getTeamInfo(wait, 3, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 4, 2) != config.ORDER_3['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 4, 2))
        if getTeamInfo(wait, 5, 2) != config.ORDER_4['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 5, 2))
        if getTeamInfo(wait, 6, 2) != config.ORDER_5['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 6, 2))
        if getTeamInfo(wait, 7, 2) != config.ORDER_6['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 7, 2))
        if getTeamInfo(wait, 8, 2) != config.ORDER_7['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 8, 2))
        if getTeamInfo(wait, 9, 2) != config.ORDER_8['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 9, 2))
    elif '项目-产线工程师' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_3['NUM']:
            raise Exception(config.ORDER_3['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))
        if getTeamInfo(wait, 3, 2) != config.ORDER_5['NUM']:
            raise Exception(config.ORDER_5['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 4, 2) != config.ORDER_7['NUM']:
            raise Exception(config.ORDER_7['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 4, 2))

    elif '产品-产线工程师' in user['NAME']:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_4['NUM']:
            raise Exception(config.ORDER_4['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))
        if getTeamInfo(wait, 3, 2) != config.ORDER_6['NUM']:
            raise Exception(config.ORDER_6['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 4, 2) != config.ORDER_8['NUM']:
            raise Exception(config.ORDER_8['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 4, 2))

    else:
        # 检查查询结果
        if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 1, 2))
        if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
            raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 2, 2))
        if getTeamInfo(wait, 3, 2) != config.ORDER_3['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 3, 2))
        if getTeamInfo(wait, 4, 2) != config.ORDER_4['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 4, 2))
        if getTeamInfo(wait, 5, 2) != config.ORDER_5['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 5, 2))
        if getTeamInfo(wait, 6, 2) != config.ORDER_6['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 6, 2))
        if getTeamInfo(wait, 7, 2) != config.ORDER_7['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 7, 2))
        if getTeamInfo(wait, 8, 2) != config.ORDER_8['NUM']:
            raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                            getTeamInfo(wait, 8, 2))


# 订单查询
def searchOrder(driver, wait, user):
    # 刷新
    sleep(sleepTime)

    # 按订单号查询
    searchByOrderNum(driver, wait, user)

    # 按产品型号查询
    searchByProMod(driver, wait, user)

    # 查询所有订单
    searchAllOrder(driver, wait, user)


# 关联软件
def relatedMptool(driver, wait, user):
    # 添加关联
    addSoftBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.addsoft')),
        message='找不到 增加关联按键')
    logging.debug('关联量产工具：' + addSoftBtn.text)
    try:
        addSoftBtn.click()
    except Exception:
        addSoftBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 软件类型
    inputSoftMod = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .relate-item:nth-of-type(1) input')),
        message='找不到 软件类型输入栏')
    try:
        inputSoftMod.click()
        sleep(sleepTime)
    except Exception:
        inputSoftMod.send_keys(Keys.ENTER)

    softMods = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 软件类型列表')
    for i in range(len(softMods)):
        softMod = softMods[i].get_attribute('innerText')
        if softMod == software['type']:
            softMods[i].click()
            sleep(sleepTime)
            break

        if i == len(softMods) - 1:
            raise Exception('Test software 不存在')

    # 软件
    inputSoft = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .relate-item:nth-of-type(2) input')),
        message='找不到 软件输入栏')
    try:
        inputSoft.click()
    except Exception:
        inputSoft.send_keys(Keys.ENTER)
    sleep(sleepTime)

    softs = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')))
    for i in range(len(softs)):
        soft = softs[i].get_attribute('innerText')
        if soft == software['soft']:
            softs[i].click()
            sleep(sleepTime)
            break

        if i == len(softs) - 1:
            raise Exception('softFile.txt(1.00) 不存在')

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-dialog__body .relate-item:nth-of-type(3) button:nth-of-type(2)'
        )),
        message='找不到 确定关联按键')
    logging.debug('关联量产工具-关联软件：' + confirmBtn.text)
    try:
        confirmBtn.click()
    except Exception:
        confirmBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 确定关联是否成功
    if getTeamInfo(wait, 1, 1) != software['version']:
        raise Exception('量产工具版本错误')
    if getTeamInfo(wait, 1, 2) != software['name']:
        raise Exception('量产工具软件名错误')
    if getTeamInfo(wait, 1, 3) != software['type']:
        raise Exception('量产工具软件类型错误')
    if getTeamInfo(wait, 1, 4) != software['des']:
        raise Exception('量产工具介绍错误')


# 取消关联
def cancleRelated(driver, wait, user):
    # 取消关联按键
    cancleBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'tbody tr td:nth-of-type(7) div .download-url')),
        message='找不到 取消关联按键')
    logging.debug('关联量产工具-关联软件：' + cancleBtn.text)
    try:
        cancleBtn.click()
    except Exception:
        cancleBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    okBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定取消关联按键')
    logging.debug('关联量产工具-关联软件：' + okBtn.text)
    try:
        okBtn.click()
    except Exception:
        okBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 确定取消成功
    checkText = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.el-table__empty-text')),
        message='找不到 数据显示')
    if checkText.text != '暂无数据':
        raise Exception('取消关联失败')


# 订单关联量产工具
def addOrderTool(driver, wait, user):
    # 软件列表
    relatedBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'tbody .el-table__row:nth-of-type(3) td:nth-of-type(8) span:nth-child(2)'
        )),
        message='找不到 软件列表')
    logging.debug('订单管理-量产工具：' + relatedBtn.text)
    try:
        relatedBtn.click()
    except Exception:
        relatedBtn.send_keys(Keys.ENTER)
    sleep(sleepTime)

    # 关联软件
    relatedMptool(driver, wait, user)

    # 取消关联
    cancleRelated(driver, wait, user)


# 追加授权
def addAuthor(driver, wait, user, str, num):
    # 获取追加授权按键
    auhtorBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(1) .download-url:nth-child(3)')),
        message='找不到 追加授权按键')
    goToElement(auhtorBtn, driver)
    logging.debug('订单管理-订单列表：' + auhtorBtn.text)
    goToElement(auhtorBtn, driver)
    auhtorBtn.click()
    sleep(sleepTime)

    # 添加在线授权
    selectBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-form>div:nth-child(1) input')),
        message='找不到 离线|在线选择输入栏')
    selectBtn.click()
    sleep(sleepTime)

    # 选择str
    selects = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li')),
        message='找不到 选择列表')
    for select in selects:
        if select.text == str:
            select.click()
            break

        if select == selects[-1]:
            raise Exception('找不到 ' + str)
    sleep(sleepTime)

    numInput = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-form>div:nth-child(2) input')),
        message='找不到 离线|在线选择输入栏')
    numInput.send_keys(num)

    # 确定
    okBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.dialog-footer button:nth-child(2)')),
        message='找不到 确定按键')
    logging.debug('追加授权：' + okBtn.text)
    okBtn.click()
    sleep(sleepTime)

    # 确定是否成功
    if str == '在线':
        allNum = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 'tbody tr:nth-child(1) td:nth-child(3) div')),
            message='找不到 在线授权数量')
        if allNum.text != '3200 / 3200':
            raise Exception('追加在线授权失败')
    else:
        allNum = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 'tbody tr:nth-child(1) td:nth-child(4) div')),
            message='找不到 离线授权数量')
        if allNum.text != '1200 / 1200':
            raise Exception('追加离线授权失败')


# 删除订单
def deleteOrder(driver, wait, user):
    order = user['tempOrder']
    # 获取订单号
    orders = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'tbody tr td:nth-child(2) div')),
        message='找不到 订单号')

    for i in range(len(orders)):
        if order['NUM'] == orders[i].text:
            logging.debug('订单已存在')
            # 删除订单
            btn = wait.until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%s) td:nth-child(1) div' % (i + 1))),
                message='找不到 订单信息扩展按键')
            btn.click()
            sleep(sleepTime)

            order_id = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%s) td:nth-child(1) div div span' %
                     (i + 2))),
                message='找不到 订单ID').get_attribute('innerText')

            doTest()
            admin['orderid'] = int(order_id)
            # 删除配置
            deleteCase = {
                'method': 'delete',
                'url': '/api/v1/middleware/order',
                'params': admin,
                'json': {},
                'response': {
                    'errcode': '0',
                    'errmsg': 'ok'
                }
            }
            result = doTest(deleteCase)
            if result.get('error'):
                raise Exception(result['error'])
            break


# 软件列表功能
def test_softFuc(driver, wait, user):
    if '产线工程师' in user['NAME'] or '研发工程师' in user['NAME']:
        # 软件列表
        downloadSoftBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.download-url')),
            message='找不到 软件列表按键')
        logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    else:
        # 软件列表
        downloadSoftBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.download-url:nth-of-type(2)')),
            message='找不到 软件列表按键')
        logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    downloadSoftBtn.click()
    sleep(sleepTime)

    # 下载
    downloadSoftBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.download-url')),
        message='找不到 下载软件按键')
    logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    downloadSoftBtn.click()
    sleep(sleepTime + 2)

    # 核对下载的软件是否正确
    myfile = filePath + '\\' + software['name']
    if os.path.exists(myfile):
        # 删除文件
        os.remove(myfile)

    else:
        raise Exception('下载软件失败')

    if os.path.exists(myfile):
        raise Exception('删除下载软件失败')


# 新增样品
def newSampe(driver, wait, user, sample):
    # 样品列表
    sampleBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(5) li:nth-child(1)'
        )),
        message='找不到 样品列表按键')
    logging.debug('样品管理：' + sampleBtn.text)
    sampleBtn.click()

    # 点击产品线输入栏
    prosBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-module input')),
        message='找不到 产品线输入栏')
    prosBtn.click()
    sleep(sleepTime)

    # 获取产品线列表
    pros = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 产品线列表')
    sleep(sleepTime)

    # 选择产品线
    for i in range(len(pros)):
        if pros[i].text == sample['PRO']:
            pros[i].click()
            break

        if i == (len(pros) - 1):
            raise Exception('找不到：' + sample['PRO'])
    sleep(sleepTime)

    # 检查样品编码是否已经存在
    try:
        numbers = wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'tbody tr td:nth-child(1)')),
            message='找不到 样品编码')
        for num in numbers:
            if sample['NUM'] in num.text:
                logging.debug(sample['NUM'] + '：已经存在')
                return
    except Exception:
        # 判断是否真的为空
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '.el-table__empty-text'), '暂无数据'),
            message='样品编码不为空')

    # 添加样品按键
    addSampleBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-sample')),
        message='找不到 添加样品按键')
    logging.debug('样品列表：' + addSampleBtn.text)
    addSampleBtn.click()
    sleep(sleepTime)

    addSampleInfo(driver, wait, user, sample)


# 新增不良品样品
def newNgSampe(driver, wait, user, sample):
    # 样品列表
    sampleBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(5) li:nth-child(2)'
        )),
        message='找不到 样品列表按键')
    logging.debug('样品管理：' + sampleBtn.text)
    sampleBtn.click()

    # 点击产品线输入栏
    prosBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-module input')),
        message='找不到 产品线输入栏')
    prosBtn.click()
    sleep(sleepTime)

    # 获取产品线列表
    pros = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 产品线列表')
    sleep(sleepTime)

    # 选择产品线
    for i in range(len(pros)):
        if pros[i].text == sample['PRO']:
            pros[i].click()
            break

        if i == (len(pros) - 1):
            raise Exception('找不到：' + sample['PRO'])
    sleep(sleepTime)

    # 检查样品编码是否已经存在
    try:
        numbers = wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'tbody tr td:nth-child(1)')),
            message='找不到 样品编码')
        for num in numbers:
            if sample['NUM'] in num.text:
                logging.debug(sample['NUM'] + '：已经存在')
                return
    except Exception:
        # 判断是否真的为空
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '.el-table__empty-text'), '暂无数据'),
            message='样品编码不为空')

    # 添加样品按键
    addSampleBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-sample')),
        message='找不到 添加样品按键')
    logging.debug('样品列表：' + addSampleBtn.text)
    addSampleBtn.click()
    sleep(sleepTime)

    addSampleInfo(driver, wait, user, sample)


# 添加样品信息
def addSampleInfo(driver, wait, user, sample):
    # 样品编码
    numInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(1) input')),
        message='找不到 样品编码输入栏')
    numInput.send_keys(sample['NUM'])

    # 产品类型
    typeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(2) input')),
        message='找不到 产品类型输入栏')
    typeInput.click()
    sleep(sleepTime)

    types = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 型号列表')

    for i in range(len(types)):
        if sample['TYPE'] == types[i].text:
            types[i].click()
            sleep(sleepTime)
            break

        if i == len(types) - 1:
            raise Exception('型号不存在：' + sample['TYPE'])

    # 项目
    modInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(3) input')),
        message='找不到 项目输入栏')
    modInput.click()
    sleep(sleepTime)

    mods = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 项目列表')

    for i in range(len(mods)):
        if sample['MOD'] == mods[i].text:
            mods[i].click()
            sleep(sleepTime)
            break

        if i == len(mods) - 1:
            raise Exception('项目不存在：' + sample['MOD'])

    # 订单
    orderInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(4) div input')),
        message='找不到 订单输入栏')
    orderInput.click()
    sleep(sleepTime)

    orders = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 订单列表')

    for i in range(len(orders)):
        if sample['ORDER'] == orders[i].text:
            orders[i].click()
            sleep(sleepTime)
            break

        if i == len(orders) - 1:
            raise Exception('订单不存在：' + sample['ORDER'])

    # 客户
    clientInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(5) input')),
        message='找不到 客户输入栏')
    clientInput.send_keys(sample['CLIENT'])

    # 工厂
    factoryInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(6) input')),
        message='找不到 工厂输入栏')
    factoryInput.click()
    sleep(sleepTime)

    factorys = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 工厂列表')

    for i in range(len(factorys)):
        if sample['FACTORY'] == factorys[i].text:
            factorys[i].click()
            sleep(sleepTime)
            break

        if i == len(factorys) - 1:
            raise Exception('工厂不存在：' + sample['FACTORY'])

    # 激光码
    codeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(7) input')),
        message='找不到 激光码输入栏')
    codeInput.send_keys(sample['CODE'])

    # 资源
    resInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(8) input')),
        message='找不到 资源输入栏')
    resInput.click()
    sleep(sleepTime)

    res = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 资源列表')

    for i in range(len(res)):
        if sample['RES'] == res[i].text:
            res[i].click()
            sleep(sleepTime)
            break

        if i == len(res) - 1:
            raise Exception('资源不存在：' + sample['RES'])

    # wafer
    waferInput = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-info-form>div:nth-child(9) input')),
        message='找不到 容量输入栏')

    waferInput.click()
    sleep(sleepTime)
    wafers = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 容量列表')

    for i in range(len(wafers)):
        if sample['WAFER'] == wafers[i].text:
            wafers[i].click()
            sleep(sleepTime)
            break

        if i == len(wafers) - 1:
            raise Exception('容量不存在：' + sample['WAFER'])

    # 料号
    sizeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(10) input')),
        message='找不到 容量输入栏')
    sizeInput.send_keys(sample['PARTNO'])
    sleep(sleepTime)

    # DIE
    DIEInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(11) input')),
        message='找不到 DIE输入栏')
    DIEInput.click()
    sleep(sleepTime)

    DIEs = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 DIE列表')

    for i in range(len(DIEs)):
        if sample['DIE'] == DIEs[i].text:
            DIEs[i].click()
            sleep(sleepTime)
            break

        if i == len(DIEs) - 1:
            raise Exception('DIE不存在：' + sample['DIE'])

    # 容量
    sizeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(12) input')),
        message='找不到 容量输入栏')
    sizeInput.click()
    sleep(sleepTime)

    sizes = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 容量列表')

    for i in range(len(sizes)):
        if sample['SIZE'] == sizes[i].text:
            sizes[i].click()
            sleep(sleepTime)
            break

        if i == len(sizes) - 1:
            raise Exception('容量不存在：' + sample['SIZE'])

    # 位宽
    bitInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(13) input')),
        message='找不到 位宽输入栏')
    bitInput.click()
    sleep(sleepTime)

    bits = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 位宽列表')

    for i in range(len(bits)):
        if sample['BITWID'] == bits[i].text:
            bits[i].click()
            sleep(sleepTime)
            break

        if i == len(bits) - 1:
            raise Exception('位宽不存在：' + sample['BITWID'])

    # 封装
    packageInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(14) input')),
        message='找不到 封装输入栏')
    packageInput.click()
    sleep(sleepTime)

    packages = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 封装列表')

    for i in range(len(packages)):
        if sample['PACKAGE'] == packages[i].text:
            packages[i].click()
            sleep(sleepTime)
            break

        if i == len(packages) - 1:
            raise Exception('封装不存在：' + sample['PACKAGE'])

    # 基板
    subInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(15) input')),
        message='找不到 基板输入栏')
    subInput.send_keys(sample['SUB']),
    sleep(sleepTime)

    # 尺寸
    areaInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(16) input')),
        message='找不到 尺寸输入栏')
    areaInput.send_keys(sample['AREA'])

    # 工艺
    processInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(17) input')),
        message='找不到 工艺输入栏')
    processInput.send_keys(sample['PROCESS'])

    # 生产时间
    timeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(18) input')),
        message='找不到 生产时间输入栏')
    timeInput.send_keys(sample['TIME'])
    timeInput.send_keys(Keys.ENTER)

    # 简述
    ngInput = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(19) input')),
        message='找不到 不良描述输入栏')
    ngInput.send_keys('简述')

    # 不良描述
    ngInput = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(20) input')),
        message='找不到 不良描述输入栏')
    ngInput.send_keys(sample['NG'])

    # 备注
    noteInput = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(21) input')),
        message='找不到 备注描述输入栏')
    noteInput.send_keys(sample['NOTE'])

    # 添加
    addBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add')),
        message='找不到 添加按键')
    logging.debug('样品列表：' + addBtn.text)
    addBtn.click()
    sleep(sleepTime)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回按键')
    goTop(driver)
    backBtn.click()
    sleep(sleepTime)


# 添加样品记录
def newRecord(driver, wait, user):
    # 添加样品记录
    addRecordBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'tbody button:nth-child(2) span')),
        message='找不到 添加记录按键')
    logging.info('样品列表：' + addRecordBtn.text)
    addRecordBtn.click()
    sleep(sleepTime)

    # platform = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'input')),
    #     message='找不到 平台输入栏')
    # platform.send_keys('TEST')

    testTime = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.el-date-editor--datetime input')),
        message='找不到 测试时间')
    testTime.click()
    sleep(sleepTime)

    now = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'div[x-placement] .el-picker-panel__footer button:nth-child(1)')),
        message='找不到 此刻')
    now.click()
    sleep(sleepTime)

    # 添加信息
    infos = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               '.two-level-item-inner-input')),
        message='找不到 信息输入栏')
    for i in range(len(infos)):
        infos[i].send_keys(i)

    # # 不良描述
    # ngInput = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR,
    #                                       'div:nth-child(11) input')),
    #     message='找不到 不良描述输入栏')
    # ngInput.send_keys('不良描述')

    # 简述
    inconInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(12) input')),
        message='找不到 结论述输入栏')
    inconInput.send_keys('简述')

    # 结论
    inconInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(13) input')),
        message='找不到 结论述输入栏')
    inconInput.send_keys('结论')

    # 备注
    noteInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(14) input')),
        message='找不到 备注述输入栏')
    noteInput.send_keys('备注')

    # 添加
    addBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add')),
        message='找不到 添加按键')
    addBtn.click()
    sleep(sleepTime)


# 我的资料
def userInfo(driver, wait, user):
    if user['updateUserInfoEnable']:
        # 修改个人资料
        logging.info('测试修改用户资料')
        updateUserInfo(driver, wait, user)
        checkUserInfo(driver, wait, user)
        logging.info('测试修改资料PASS')

        # 将滚动条移动到页面的顶部
        goTop(driver)

        # 修改密码
        logging.info('测试修改密码')
        updatePassword(driver, wait, user)
        logout(driver, wait, user)
        login(wait, email=user['EMAIL'], password=user['passWord'])
        checkUserInfo(driver, wait, user)
        updatePassword(driver, wait, user)
        logging.info('测试修改密码PASS')

        # 还原用户名，方便后续测试
        resUserName(driver, wait, user)

        # 将滚动条移动到页面的顶部
        goTop(driver)

    if user['teamEnable']:
        # team功能
        myTeamBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.watch-myteam')),
            message='找不到 查看我的群组按键')
        logging.debug('个人中心-我的资料：' + myTeamBtn.text)
        try:
            myTeamBtn.click()
            sleep(sleepTime)
        except Exception:
            myTeamBtn.send_keys(Keys.ENTER)
        sleep(sleepTime)

        # 添加Team
        logging.info('添加Team')
        addTeam(driver, wait, user)
        logging.info('添加Team PASS')
        # 核对Team列表
        logging.info('核对Team列表')
        checkTeamInfo(driver, wait, user)
        logging.info('核对Team列表PASS')
        # 测试team功能：查看、修改、删除
        logging.info('测试Team功能')
        testTeamFunction(driver, wait, user)
        logging.info('测试Team功能PASS')

    return True


# 产品线和项目管理
def productManager(driver, wait, user):
    # 点击选择产品线和项目管理
    proManagerBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(2) .el-submenu__title'
        )),
        message='找不到 产品线和项目管理')
    logging.debug('产品线和项目管理：' + proManagerBtn.text)
    proManagerBtn.click()
    sleep(sleepTime)

    return True


# 新增项目
def addProduct(driver, wait, user):
    if user['addModEnable']:
        # 打开添加产品项
        addNewProModBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'ul:nth-child(1)>li:nth-child(2) li:first-child')),
            message='找不到 新增项目')
        logging.debug('产品管理-新增产品：' + addNewProModBtn.text)
        addNewProModBtn.click()
        sleep(sleepTime)

        logging.info('测试添加项目')
        addMod(driver, wait, user)
        logging.info('测试添加项目成功')

        logging.info('测试添加项目角色成员')
        addRole(driver, wait, user)
        logging.info('测试添加项目角色成员成功')

    return True


# 产品列表
def proList(driver, wait, user):
    if user['proLisEnable']:
        # 打开产品列表项
        proLisBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'ul:nth-child(1)>li:nth-child(2) li:last-child')),
            message='找不到 产品列表项')
        logging.debug('产品管理-产品列表：' + proLisBtn.text)
        proLisBtn.click()
        sleep(sleepTime)

        # 产品线列表查询
        logging.info('测试产品线列表查询')
        searchPro(driver, wait, user)
        logging.info('测试产品线列表查询成功')

        # 测试项目功能：添加、修改、删除
        logging.info('测试项目功能(添加、修改、删除)')
        test_proModFuc(driver, wait, user)
        logging.info('测试产品类型功能(添加、修改、删除) PASS')


# 订单管理
def orderManager(driver, wait, user):
    # 点击选择产品管理项
    orderManagerBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'li.el-submenu:nth-of-type(4) div.el-submenu__title')),
        message='找不到 订单管理')
    logging.debug('订单管理：' + orderManagerBtn.text)
    orderManagerBtn.click()
    sleep(sleepTime)


# 创建订单
def newOrder(driver, wait, user, applicant):
    if user['createOrderEnable']:
        logging.info('测试创建订单')
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_1'],
                    user['tempOrder'], applicant, user['tempOrder'], driver)
        logging.info('测试创建订单成功')


# 订单列表
def orderList(driver, wait, user):
    if user['orderListEnable']:
        # 订单列表按键
        orderListsBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'ul:nth-child(1)>li:nth-child(4) ul li:nth-child(2)')),
            message='找不到 订单列表按键')
        logging.debug('订单管理-量产工具：' + orderListsBtn.text)
        orderListsBtn.click()
        sleep(sleepTime)

        logging.info('测试订单查询功能')
        searchOrder(driver, wait, user)
        logging.info('测试订单查询功能成功')

        if '产品经理' in user['NAME']:
            logging.info('测试订单关联量产工具')
            addOrderTool(driver, wait, user)
            logging.info('测试订单关联量产工具成功')

        if 'pmc' in user['NAME']:
            logging.info('追加授权')
            addAuthor(driver, wait, user, '在线', '1000')
            addAuthor(driver, wait, user, '离线', '1000')
            logging.info('追加授权成功')

            logging.info('删除订单')
            deleteOrder(driver, wait, user)
            logging.info('删除订单成功')

        if '产线工程师' in user['NAME'] or '测试工程师' in user[
                'NAME'] or '研发工程师' in user['NAME']:
            # 测试下载功能
            logging.info('测试下载功能')
            test_softFuc(driver, wait, user)
            logging.info('测试下载功能成功')


# 样品管理
def sampleManage(driver, wait, user):
    sampleManage = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(5) .el-submenu__title'
        )),
        message='找不到 样品管理')
    logging.debug('样品管理：' + sampleManage.text)
    sampleManage.click()


# 添加样品
def addSampe(driver, wait, user):
    if user['createSampleEnable']:
        # 添加样品
        newSampe(driver, wait, user, config.SAMPLE)
        # 添加记录
        newRecord(driver, wait, user)


# 添加不良品样品
def addNgSampe(driver, wait, user):
    if user['createSampleEnable']:
        # 添加样品
        newNgSampe(driver, wait, user, config.SAMPLE)
        # 添加记录
        newRecord(driver, wait, user)


if __name__ == '__main__':
    print(doTest())
    print(admin)
