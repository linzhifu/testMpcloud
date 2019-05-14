from selenium import webdriver
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import config
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
# from selenium.webdriver.common.action_chains import ActionChains
import os
import get_video
import shutil

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if config.debug:
    logging.disable(logging.DEBUG)

currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 是否修改过密码
isNewPsw = False

# 是否修改过产品
isModifyPro = False

# TEAM成员
teamUsers = config.teamUsers

# TEAM
testTeam = config.testTeam

# 睡眠时间
time = config.timeout

# 产品-型号
proMod = config.proMod

# 测试软件
software = config.software

# 测试文件下载路径
filePath = config.filePath


# 将滚动条移动到页面的顶部
def goTop(driver):
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    sleep(time)


# 拖动到可见的元素去
def goToElement(element, driver):
    js = 'arguments[0].scrollIntoView();'
    driver.execute_script(js, element)
    sleep(time)


# 页面加载
def pageFinish(driver):
    # 加载时间最大为10s
    i = 10
    STR_READY_STATE = ''
    while STR_READY_STATE != 'complete':
        if i:
            sleep(time)
            STR_READY_STATE = driver.execute_script(
                'return document.readyState')
        else:
            raise Exception('页面加载失败')


def updatePro(wait):
    pass


# 登录
def login(user, wait):
    # 点击密码登录
    loginTabView = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.way li:nth-of-type(2)')),
        message='找不到 登录-Tab项(密码登录)')
    logging.debug('登录-Tab项(密码登录)：' + loginTabView.text)
    loginTabView.click()

    # 输入email
    inputEmail = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .mail .el-input__inner')),
        message='找不到 Email输入栏')
    inputEmail.send_keys(user['EMAIL'])

    # 输入password
    inputPsw = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .password .el-input__inner')),
        message='找不到 password输入栏')
    if isNewPsw:
        inputPsw.send_keys(user['passWord'])
    else:
        inputPsw.send_keys('123')

    # 点击登录
    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.password-login .login')),
        message='找不到 登录-按钮(登录/注册)')
    logging.debug('登录-按钮(登录/注册)：' + loginBtn.text)
    # send_keys(Keys.ENTER)代替click(),避免无界面模式点击不了
    loginBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 获取登录状态
    online = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.online')),
        message='找不到 登录-状态(在线)')

    username = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.username')),
        message='找不到 登录-用户')

    sleep(time)
    logging.info('登录成功：' + username.text + ' ' + online.text)


# 修改用户资料
def updateUserInfo(user, wait):
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


# 还原用户名，方便后续测试
def resUserName(user, wait, driver):
    # 判断是否有多余的team未删除（上一次测试失败的）
    # 点击查看我的team
    # 查看我的team
    myTeamBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.watch-myteam')),
        message='找不到 查看我的群组按键')
    logging.debug('个人中心-我的资料：' + myTeamBtn.text)
    myTeamBtn.send_keys(Keys.ENTER)
    sleep(time)

    pageFinish(driver)

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
    sleep(time)

    pageFinish(driver)

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


# 核对用户资料
def checkUserInfo(user, wait):
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
def updatePassword(user, wait):
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
    sleep(time)

    # 标记密码已经修改过
    isNewPsw = not isNewPsw


# 添加Team
def addTeam(user, wait):
    # 创建Team按键
    createTeamBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-team')),
        message='找不到 创建Team按键')
    logging.debug('个人资料-查看我的team：' + createTeamBtn.text)
    createTeamBtn.send_keys(Keys.ENTER)
    sleep(time)

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
    sleep(time)


# 获取team列表信息，row行1开始，colunm列1开始
def getTeamInfo(wait, row, column):
    teamItem = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(%d) td:nth-of-type(%d)' % (row, column))),
        message='获取team列表信息失败')

    return teamItem.text


# 获取team功能：删除、查看、修改
def getTeamFunction(wait, row, column):
    teamFunctionBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(%d)'
            % (row, column))),
        message='获取Team功能失败')

    logging.debug('查看我的team-修改：' + teamFunctionBtn.text)
    return teamFunctionBtn


# 核对TestTeam
def checkTeamInfo(user, wait):
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
def testModifyTeam(user, wait, row=2, column=3):
    # 获取修改按键
    modifyTeamBtn = getTeamFunction(wait, row, column)
    modifyTeamBtn.send_keys(Keys.ENTER)
    sleep(time)

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
    sleep(time)

    # 核对修改后信息
    teamName = getTeamInfo(wait, 2, 2)
    if teamName != user['modifyTeamName']:
        raise Exception(user['modifyTeamName'] + ' 修改后team名称不对：' + teamName)
    teamDes = getTeamInfo(wait, 2, 5)
    if teamDes != user['modifyTeamDes']:
        raise Exception(user['modifyTeamDes'] + ' 修改后team描述不对不对：' + teamDes)


# 删除team
def deleteTeam(wait, row=2, column=1):
    # 获取删除team按键
    deleteTeamBtn = getTeamFunction(wait, row, column)
    deleteTeamBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '[aria-label=提示] button.el-button:nth-of-type(2)')))
    logging.debug('查看我的team-删除：' + confirmBtn.text)
    confirmBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 确定删除成功
    teams = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'tbody tr')),
        message='找不到team列表')
    if len(teams) != 1:
        raise Exception('Team删除失败')


# 测试TestTeam查看功能
def test_TestTeam(wait, driver):
    # 查看
    teamUserBtn_TestTeam = getTeamFunction(wait, 1, 1)
    teamUserBtn_TestTeam.send_keys(Keys.ENTER)
    sleep(time)

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
    sleep(time)


# 测试TempTeam查看功能
def test_TempTeam(user, wait, driver):
    # 查看
    teamUserBtn_TestTeam = getTeamFunction(wait, 2, 2)
    teamUserBtn_TestTeam.send_keys(Keys.ENTER)
    sleep(time)

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
    sleep(time)

    confirmDelBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定删除用户按键')
    logging.debug('查看我的team-查看：' + confirmDelBtn.text)
    confirmDelBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 添加用户到team
    addUserToTeam(wait, driver)

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
    sleep(time)


# 添加成员
def addUserToTeam(wait, driver):
    # 添加用户
    # logging.info('添加：' + username)
    # 点击用户下拉栏
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-input__inner')),
        message='找不到 用户列表下拉栏')
    userListBtn.send_keys(Keys.ENTER)
    sleep(time)

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
            sleep(time)
        userName = user.get_attribute('innerText')
        if userName in teamUsers:
            logging.debug('team查看-添加用户：' + sureAddUserBtn.text + ' ' +
                          userName)
            goToElement(user, driver)
            user.click()
            sleep(time)

            goTop(driver)
            sureAddUserBtn.send_keys(Keys.ENTER)
            sleep(time)

        else:
            raise Exception('team以外的用户存在team列表中')


# 测试team查看用户等功能
def testTeamUser(user, wait, driver):
    # 测试TestTeam
    test_TestTeam(wait, driver)

    # 测试TempTeam
    test_TempTeam(user, wait, driver)


# 测试team 修改、查看、删除
def testTeamFunction(user, wait, driver):
    # 测试修改team信息
    testModifyTeam(user, wait)
    # 测试team用户功能
    testTeamUser(user, wait, driver)
    # 测试删除team
    deleteTeam(wait)


# 核对项目成员
def check_user(wait, users):
    if len(users) != 6:
        raise Exception('项目成员数量不对')
    for user in users:
        name = user.get_attribute('innerText').strip('\n')
        if name not in config.teamUsers:
            raise Exception('项目成员显示不对')


# 产品线列表功能测试
def searchPro(user, wait, driver):
    pageFinish(driver)
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

    # 查询输入栏
    searchInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-product-input input')),
        message='找不到 产品查询输入栏')
    searchInput.send_keys(proMod['PRONAME_1'])

    # 根据产品名查询
    searchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-project-btn')),
        message='找不到 按产品查询按键')
    logging.debug('产品管理-产品列表：' + searchBtn.text)
    searchBtn.click()
    sleep(time)

    products = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品列表')
    # 修改user['modifyPro']产品信息
    for i in range(len(products)):
        htmlText = products[i].get_attribute('innerHTML')
        if proMod['PRONAME_1'] not in htmlText:
            raise Exception('按产品名查询失败')

    # 所有产品
    allProBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-all')),
        message='找不到 所有产品按键')
    logging.debug('产品管理-产品列表：' + allProBtn.text)
    allProBtn.click()
    sleep(time)

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
    searchTestProBtn.click()
    sleep(time)

    # 获取所有产品类型
    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')

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

    # 根据产品类型名查询
    searchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-project-btn')),
        message='找不到 按产品类型查询按键')
    logging.debug('产品列表-查看：' + searchBtn.text)
    searchBtn.click()
    sleep(time)

    pageFinish(driver)

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
    allModBtn.click()
    sleep(time)

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

    # 产品型号-查看
    searchTestProBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-table__row:nth-of-type(1) .el-button--primary')),
        message='找不到 产品-查看按键')
    logging.debug('产品管理-产品列表：' + searchTestProBtn.get_attribute('innerText'))
    searchTestProBtn.click()
    sleep(time)

    pageFinish(driver)

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
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                         '创建人：' + config.USER_ADMIN['NAME']),
        message='找不到 产品-型号创建人')
    if not isCreateUser:
        raise Exception('型号创建失败 创建人:' + config.USER_ADMIN['NAME'])

    # 获取产品-型号描述，确定是否加载成功
    isCreateDes = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.product-des')),
                                         '项目描述：' + proMod['MODDES_1']),
        message='找不到 产品-型号描述')
    if not isCreateDes:
        raise Exception('型号创建失败 项目描述：' + proMod['MODDES_1'])

    # 检查订单显示
    # ORDER1
    # if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
    #     raise Exception(config.ORDER_1['NUM'] + ' 订单号显示错误：' +
    #                     getTeamInfo(wait, 1, 2))
    # if getTeamInfo(wait, 1, 3) != config.ORDER_1['ONLINE']:
    #     raise Exception(config.ORDER_1['ONLINE'] + ' 在线数量显示错误：' +
    #                     getTeamInfo(wait, 1, 3))
    # if getTeamInfo(wait, 1, 4) != config.ORDER_1['OFFLINE']:
    #     raise Exception(config.ORDER_1['OFFLINE'] + ' 离线数量显示错误：' +
    #                     getTeamInfo(wait, 1, 4))
    # if getTeamInfo(wait, 1, 5) != config.ORDER_1['FACTORY']:
    #     raise Exception(config.ORDER_1['FACTORY'] + ' 工厂显示错误：' +
    #                     getTeamInfo(wait, 1, 5))
    # if getTeamInfo(wait, 1, 6) != config.authTime:
    #     raise Exception(config.authTime + ' 有效时间显示错误：' +
    #                     getTeamInfo(wait, 1, 6))
    # # if getTeamInfo(wait, 1, 7) != config.USER_PRO_PE['NAME']:
    # #     raise Exception(config.USER_PRO_PE['NAME'] + ' 创建人显示错误：' +
    # #                     getTeamInfo(wait, 1, 7))

    # # ORDER2
    # if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
    #     raise Exception(config.ORDER_2['NUM'] + ' 订单号显示错误：' +
    #                     getTeamInfo(wait, 2, 2))
    # if getTeamInfo(wait, 2, 3) != config.ORDER_2['ONLINE']:
    #     raise Exception(config.ORDER_2['ONLINE'] + ' 在线数量显示错误：' +
    #                     getTeamInfo(wait, 2, 3))
    # if getTeamInfo(wait, 2, 4) != config.ORDER_2['OFFLINE']:
    #     raise Exception(config.ORDER_2['OFFLINE'] + ' 离线数量显示错误：' +
    #                     getTeamInfo(wait, 2, 4))
    # if getTeamInfo(wait, 2, 5) != config.ORDER_2['FACTORY']:
    #     raise Exception(config.ORDER_2['FACTORY'] + ' 工厂显示错误：' +
    #                     getTeamInfo(wait, 2, 5))
    # if getTeamInfo(wait, 2, 6) != config.authTime:
    #     raise Exception(config.authTime + '有效时间显示错误：' +
    #                     getTeamInfo(wait, 2, 6))
    # # if getTeamInfo(wait, 2, 7) != config.USER_MOD_PE['NAME']:
    # #     raise Exception(config.USER_MOD_PE['NAME'] + ' 创建人显示错误：' +
    # #                     getTeamInfo(wait, 2, 7))

    # 点击用户列表按钮
    # userListBtn = wait.until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
    #     message='找不到 用户列表tab按键')
    # logging.debug('产品型号-用户列表：' + userListBtn.text)
    # try:
    #     userListBtn.click()
    # except Exception:
    #     userListBtn.send_keys(Keys.ENTER)
    # sleep(time)

    users = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR,
             '[aria-labelledby=tab-0] tbody tr td:nth-child(2)')),
        message='找不到项目成员')
    check_user(wait, users)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回上一级按键')
    logging.debug('产品列表-查看：' + backBtn.text)
    goTop(driver)
    backBtn.send_keys(Keys.ENTER)
    sleep(time)

    pageFinish(driver)

    # 查看产品成员是否为空
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    try:
        userListBtn.click()
    except Exception:
        userListBtn.send_keys(Keys.ENTER)
    sleep(time)

    empytText = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '.el-table__empty-block span')),
        message='产品成员可见(应该不可见)-找不到‘暂无数据’')

    if empytText.get_attribute('innerText') != '暂无数据':
        raise Exception('产品成员可见(应该不可见)')


# 按订单号查询
def searchByOrderNum(wait):
    # 订单号查询输入栏
    inputOrderNum = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-input input')),
        message='找不到 订单号查询输入')
    inputOrderNum.send_keys(config.ORDER_1['NUM'])

    # 按订单号查询
    ordNumSearchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'button.sure:nth-of-type(3)')),
        message='找不到 按订单号查询按键')
    logging.debug('订单列表-查询：' + ordNumSearchBtn.text)
    ordNumSearchBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 检查查询结果
    if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + ' 订单号不对：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 5) != config.ORDER_1['FACTORY']:
        raise Exception(config.ORDER_1['FACTORY'] + ' 工厂不对：' +
                        getTeamInfo(wait, 1, 5))
    if getTeamInfo(wait, 1, 6) != config.authTime:
        raise Exception(config.authTime + ' 有效时间不对：' + getTeamInfo(wait, 1, 6))


# 点击退出
def logout(user, wait, driver):
    logoutBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginout')),
        message='找不到退出按键')
    logoutBtn.click()
    sleep(time)


# 用户资料
def userInfo(user, wait, driver):
    # 修改个人资料和修改密码 测试
    if user['updateUserInfoEnable']:
        logging.info('修改用户资料')
        updateUserInfo(user, wait)
        checkUserInfo(user, wait)
        logging.info('修改资料PASS')

        # 将滚动条移动到页面的顶部
        goTop(driver)

        # 修改密码
        logging.info('修改密码')
        updatePassword(user, wait)
        logout(user, wait, driver)
        login(user, wait)
        checkUserInfo(user, wait)
        updatePassword(user, wait)
        logging.info('修改密码PASS')

        # 还原用户名，方便后续测试
        resUserName(user, wait, driver)

        # 将滚动条移动到页面的顶部
        goTop(driver)

    # 测试TEAM功能
    if user['teamEnable']:
        # 查看我的team
        myTeamBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.watch-myteam')),
            message='找不到 查看我的群组按键')
        logging.debug('个人中心-我的资料：' + myTeamBtn.text)
        myTeamBtn.send_keys(Keys.ENTER)
        sleep(time)

        # 添加Team
        logging.info('添加Team')
        addTeam(user, wait)
        logging.info('添加Team PASS')

        # 核对Team列表
        logging.info('核对Team列表')
        checkTeamInfo(user, wait)
        logging.info('核对Team列表PASS')

        # 测试team功能：查看、修改、删除
        logging.info('测试Team功能')
        testTeamFunction(user, wait, driver)
        logging.info('测试Team功能PASS')


# 按产品类型查询
def searchByProMod(wait):
    # 选择产品
    prolistBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-select:nth-of-type(1) input')),
        message='找不到 产品列表下拉按键')
    prolistBtn.send_keys(Keys.ENTER)
    sleep(time)

    proList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品列表')
    for i in range(len(proList)):
        pro = proList[i].get_attribute('innerText')
        if pro == proMod['PRONAME_1']:
            proList[i].click()
            sleep(time)
            break

        if i == len(proList) - 1:
            raise Exception(proMod['PRONAME_1'] + ' 不存在')

    # 选择型号
    modlistBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-select:nth-of-type(2) input')),
        message='找不到 产品类型列表下拉按键')
    modlistBtn.click()
    sleep(time)

    modList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品类型列表')
    for i in range(len(modList)):
        mod = modList[i].get_attribute('innerText')
        if mod == proMod['MODNAME_1']:
            modList[i].click()
            sleep(time)
            break

        if i == len(modList) - 1:
            raise Exception(proMod['MODNAME_1'] + ' 不存在')

    # 按产品类型查询
    proModSearchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'button.sure:nth-of-type(1)')),
        message='找不到 按产品类型查询按键')
    logging.debug('订单列表-查询：' + proModSearchBtn.text)
    proModSearchBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 检查查询结果
    if getTeamInfo(wait, 1, 2) != '20181111':
        raise Exception(config.ORDER_1['NUM'] + ' 订单号不对：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 2, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 3, 2) != config.ORDER_2['NUM']:
        raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                        getTeamInfo(wait, 3, 2))


# 产品列表
def proList(user, wait, driver):
    if user['proLisEnable']:
        # 打开产品列表项
        proLisBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'ul:nth-child(1)>li:nth-child(2) li:last-child')))
        logging.debug('产品管理-产品列表：' + proLisBtn.text)
        proLisBtn.click()
        sleep(time)

        # 查询功能
        logging.info('查询产品列表')
        searchPro(user, wait, driver)
        logging.info('查询产品列表成功')


# 产品管理
def productManager(user, wait, driver):
    # 点击选择产品管理项
    proManagerBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(2) .el-submenu__title'
        )),
        message='找不到 产品管理')
    logging.debug('产品管理：' + proManagerBtn.text)
    proManagerBtn.click()


# 查询所有订单
def searchAllOrder(wait):
    allOrderBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-all')),
        message='找不到 查询所有订单按键')
    logging.debug('订单列表-查询：' + allOrderBtn.text)
    allOrderBtn.send_keys(Keys.ENTER)
    sleep(time)

    # 检查查询结果
    if getTeamInfo(wait, 1, 2) != '20181111':
        raise Exception(config.ORDER_1['NUM'] + ' 订单号不对：' +
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


# 订单查询
def searchOrder(user, wait):
    # 刷新
    sleep(time)
    pageFinish(driver)

    # 按订单号查询
    searchByOrderNum(wait)

    # 按产品型号查询
    searchByProMod(wait)

    # 查询所有订单
    searchAllOrder(wait)


# 订单管理
def orderManager(user, wait, driver):
    # 点击选择产品管理项
    orderManagerBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'li.el-submenu:nth-of-type(4) div.el-submenu__title')),
        message='找不到 订单管理')
    logging.debug('订单管理：' + orderManagerBtn.text)
    orderManagerBtn.click()


# 创建订单
def newOrder(wait, user, driver):
    if user['createOrderEnable']:
        logging.info('创建订单')
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_1'],
                    user['tempOrder'], config.USER_MOD_PE['NAME'], user,
                    driver)
        logging.info('创建订单成功')


# 删除订单
def deleteOrder(user, wait, driver):
    # 获取删除按键
    deleteBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(9) .download-url:nth-child(2)')),
        message='找不到 删除按键')
    logging.debug('订单管理-订单列表：' + deleteBtn.text)
    goToElement(deleteBtn, driver)
    deleteBtn.click()

    # 确定删除
    okBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '[aria-label=提示] .el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定删除按键')
    logging.debug('订单管理-订单列表：' + okBtn.text)
    okBtn.click()

    # 等待列表刷新
    sleep(time)

    # 确定删除是否成功
    orders = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             'tbody td:nth-of-type(2)')),
        message='找不到 订单列表')
    for order in orders:
        if order.text == user['tempOrder']['NUM']:
            raise Exception('删除订单失败')


# 订单管理-订单列表
def orderList(user, wait, driver):
    # 点击订单列表
    if user['orderListEnable']:
        orderListBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'ul:nth-child(1)>li:nth-child(4) ul li:nth-child(2)')),
            message='找不到 创建订单项')
        logging.debug('订单管理-创建订单：' + orderListBtn.text)
        orderListBtn.click()
        sleep(time)

        logging.info('查询订单')
        searchOrder(user, wait)
        logging.info('查询订单成功')

        logging.info('追加授权')
        addAuthor(user, wait, driver, '在线', '1000')
        addAuthor(user, wait, driver, '离线', '1000')
        logging.info('追加授权成功')

        # logging.info('删除订单')
        # deleteOrder(user, wait, driver)
        # logging.info('删除订单成功')


# 追加授权
def addAuthor(user, wait, driver, str, num):
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
    sleep(time)

    # 添加在线授权
    selectBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-form>div:nth-child(1) input')),
        message='找不到 离线|在线选择输入栏')
    selectBtn.click()
    sleep(time)

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
    sleep(time)

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
    sleep(time)

    # 确定是否成功
    if str == '在线':
        allNum = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 'tbody tr:nth-child(1) td:nth-child(3) div')),
            message='找不到 在线授权数量')
        print(allNum.text)
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
    sleep(time)

    pageFinish(driver)

    # 获取订单号
    orders = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'tbody tr td:nth-child(2) div')),
        message='找不到 订单号')

    for i in range(len(orders)):
        if order['NUM'] == orders[i].text:
            logging.debug('订单已存在')
            return

    # 点击创建订单
    createOrderBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(4) ul li:nth-child(1)')),
        message='找不到 创建订单项')
    logging.debug('订单管理-创建订单：' + createOrderBtn.text)
    createOrderBtn.click()
    sleep(time)

    # 选择产品
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(1) .el-input__inner')),
        message='找不到 产品列表下拉按键')
    proLisBtn.send_keys(Keys.ENTER)
    sleep(time)

    proList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 产品列表')
    for pro in proList:
        proName = pro.get_attribute('innerText')
        if proName == product:
            logging.debug('创建订单-选择产品：' + proName)
            pro.click()
            sleep(time)
            break
        if pro == proList[len(proList) - 1]:
            raise Exception('上传软件-选择产品：产品不存在')

    # 选择型号
    modLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(2) .el-input__inner')),
        message='找不到 型号列表下拉按键')
    modLisBtn.send_keys(Keys.ENTER)
    sleep(time)

    modList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 型号列表')
    for mod in modList:
        modName = mod.get_attribute('innerText')
        if modName == module:
            logging.debug('创建订单-选择型号：' + modName)
            mod.click()
            sleep(time)
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

    # 授权数量
    outLineNum = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
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
    sleep(time)

    factorys = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li')),
        message='找不到 工厂列表')
    for factory in factorys:
        factory_name = factory.text
        if factory_name == order['FACTORY']:
            factory.click()
            sleep(time)
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
    sleep(time)

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
                sleep(time)
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
    sleep(time)

    upOK = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.page-finish'),
                                         '成功创建'),
        message='创建订单失败')

    if upOK is False:
        raise Exception('创建订单失败')

    sleep(time)


def main(driver, user=config.USER_MOD_PMC):
    # user :USER_PRO_PM
    startTime = datetime.now()

    # 测试目录
    logData = datetime.now().strftime('%Y-%m-%d')
    LOGDIR = logData + '\\' + user['NAME']

    # 检查目录
    if os.path.exists(logData):
        pass
    else:
        os.mkdir(logData)

    if os.path.exists(LOGDIR):
        pass
    else:
        os.mkdir(LOGDIR)

    # 测试结果
    resu = ''

    # LOG文件名
    logName = datetime.now().strftime('%Y%m%d%H%M%S')

    # 保存路径
    savePath = LOGDIR + '\\' + logName

    # 指定logger输出格式
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')

    # DEBUG输出保存测试LOG
    file_handler = logging.FileHandler('test.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    if not config.hide:
        # 录像开始
        Save = get_video.Job()
        Save.start()

    try:
        # 设置等待时间
        wait = WebDriverWait(driver, 10)
        # 显示1920*1080
        # driver.set_window_size(1366, 768)

        # 最大化
        driver.maximize_window()

        # 获取登录页面
        logging.info('Go to ' + config.URL)
        driver.get(config.URL)

        # 登录
        logging.info('登录账户：' + user['NAME'])
        login(user, wait)

        # 个人资料
        logging.info('个人中心-我的资料')
        userInfo(user, wait, driver)

        # 产品管理
        logging.info('产品管理')
        productManager(user, wait, driver)

        # 产品管理-产品列表
        logging.info('产品管理-产品列表')
        proList(user, wait, driver)

        # 订单管理
        logging.info('订单管理')
        orderManager(user, wait, driver)

        # 订单管理-创建订单
        logging.info('订单管理-创建订单')
        newOrder(wait, user, driver)

        # 订单管理-订单列表
        logging.info('订单管理-订单列表')
        orderList(user, wait, driver)

        # 测试结果PASS
        resu = 'pass'

    except Exception as E:
        logging.info(E)

        # 测试结果FAIL
        resu = 'fail'

    finally:

        if not config.hide:
            # 屏幕截图
            save_screen = driver.save_screenshot(savePath + '-' + resu +
                                                 '.png')
            if save_screen:
                logging.info('测试结果截图：' + savePath + '-' + resu + '.png')
            else:
                logging.info('测试结果截图失败')

            # 录像结束
            Save.stop()
            sleep(1)

            # 保存录像到指定路径
            shutil.move('test.avi', savePath + '-' + resu + '.avi')

        # 浏览器退出
        driver.quit()

        # 测试时间
        allTime = datetime.now() - startTime
        logging.info(resu.upper() + ' 测试时间：' + str(allTime))

        # 保存测试LOG
        logger.removeHandler(file_handler)
        file_handler.close()
        shutil.move('test.log', savePath + '-' + resu + '.log')

        if resu == 'pass':
            return True
        else:
            return False


if __name__ == '__main__':
    # 测试测试
    j = 1
    # pass计数
    i = 0
    while j:
        opt = webdriver.ChromeOptions()
        if config.hide:
            opt.set_headless()
        driver = webdriver.Chrome(options=opt)
        # driver = webdriver.Ie()
        OK = main(driver)
        j = j - 1
        if OK:
            i += 1
            print(i)
