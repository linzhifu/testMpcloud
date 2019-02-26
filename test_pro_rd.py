from selenium import webdriver
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import config
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import os
import get_video
import shutil
import filecmp

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
    loginBtn.click()

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
    setInfoBtn.click()


# 还原用户名，方便后续测试
def resUserName(user, wait, driver):
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
    setInfoBtn.click()


# 核对用户资料
def checkUserInfo(user, wait):
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
    setPswBtn.click()

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
    checkBtn.click()

    isNewPsw = not isNewPsw


# 刷新页面
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


# 添加Team
def addTeam(user, wait):
    # 创建Team按键
    createTeamBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.create-team')),
        message='找不到 创建Team按键')
    logging.debug('个人资料-查看我的team：' + createTeamBtn.text)
    createTeamBtn.click()

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
    createBtn.click()
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


def checkTeamInfo(user, wait):
    # 核对TestTeam
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
    modifyTeamBtn.click()

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
    confirmBtn.click()
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
    deleteTeamBtn.click()

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '[aria-label=提示] button.el-button:nth-of-type(2)')))
    logging.debug('查看我的team-删除：' + confirmBtn.text)
    confirmBtn.click()
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
    teamUserBtn_TestTeam.click()
    sleep(time)

    # 等待页面刷新
    pageFinish(driver)

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
    backBtn.click()
    sleep(time)

    # 等待页面刷新
    pageFinish(driver)


# 测试TempTeam查看功能
def test_TempTeam(user, wait, driver):
    # 查看
    teamUserBtn_TestTeam = getTeamFunction(wait, 2, 2)
    teamUserBtn_TestTeam.click()
    sleep(time)

    # 等待页面刷新
    pageFinish(driver)

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

    confirmDelBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定删除用户按键')
    logging.debug('查看我的team-查看：' + confirmDelBtn.text)
    confirmDelBtn.click()
    sleep(time)

    # 添加测试主管
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
    backBtn.click()
    sleep(time)

    # 等待页面刷新
    pageFinish(driver)


# 添加成员
def addUserToTeam(wait, driver):
    # 添加用户
    # logging.info('添加：' + username)
    # 点击用户下拉栏
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-input__inner')),
        message='找不到 用户列表下拉栏')

    userListBtn.click()

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
            userListBtn.click()
            sleep(time)
        userName = user.get_attribute('innerText')
        if userName in teamUsers:
            logging.debug('team查看-添加用户：' + sureAddUserBtn.text + ' ' +
                          userName)
            goToElement(user, driver)
            user.click()
            sleep(time)

            goTop(driver)
            sureAddUserBtn.click()
            sleep(time)

        else:
            raise Exception('team以外的用户存在team列表中')


# 测试team查看用户等功能
def testTeamUser(user, wait, driver):
    # 测试TestTeam
    test_TestTeam(wait, driver)

    # 测试TempTeam
    test_TempTeam(user, wait, driver)


def testTeamFunction(user, wait, driver):
    # 测试修改team信息
    testModifyTeam(user, wait)
    # 测试team用户功能
    testTeamUser(user, wait, driver)
    # 测试删除team
    deleteTeam(wait)


def goTop(driver):
    # 将滚动条移动到页面的顶部
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)


# 拖动到可见的元素去
def goToElement(element, driver):
    js = 'arguments[0].scrollIntoView();'
    driver.execute_script(js, element)
    sleep(time)


# 添加产品类型
def addMod(user, wait, driver):
    # 产品列表下拉按钮
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(1) .el-input__inner')),
        message='不知道 产品列表下拉按键')
    proLisBtn.click()
    sleep(time)

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
    createModBtn.click()

    # 前往添加成员页面
    gotoAddBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box .el-button:nth-of-type(2)')),
        message='找不到 前往添加成员页面按键')
    logging.debug('新增产品-立即前往：' + gotoAddBtn.text)
    gotoAddBtn.click()
    sleep(time)

    # 获取产品-型号名称，确定是否创建成功
    isCreateName = wait.until(
        EC.text_to_be_present_in_element(
            ((By.CSS_SELECTOR, '.container .title')),
            proMod['PRONAME_1'] + '-' + user['modName']),
        message='找不到 产品-型号名称')
    if not isCreateName:
        raise Exception('型号创建失败 ' + proMod['PRONAME_1'] + '-' +
                        user['modName'])

    # 获取产品-型号创建人，确定是否创建成功
    isCreateUser = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                         '创建人：' + user['NAME']),
        message='找不到 产品-型号创建人')
    if not isCreateUser:
        raise Exception('型号创建失败 ' + '创建人：' + user['NAME'])

    # 获取产品-型号描述，确定是否创建成功
    isCreateDes = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.product-des')),
                                         ' 项目描述：' + user['modDes']),
        message='找不到 产品-型号描述')
    if not isCreateDes:
        raise Exception('型号创建失败 ' + ' 项目描述：' + user['modDes'])


# 添加角色
def addProRole(user, wait, driver):
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    userListBtn.click()

    # 用户列表下拉按钮
    userRoleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-user .el-input__inner')),
        message='找不到 用户列表下拉按键')
    userRoleListBtn.click()
    sleep(time)

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

    sleep(time)
    # 已添加角色列表按钮
    roleAddListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-role .el-input__inner')),
        message='找不到 已添加角色下拉列表按键')
    roleAddListBtn.click()
    sleep(time)

    # 获取所有添加的角色
    roleAddList = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 已添加角色')

    if len(roleAddList) != 5:
        raise Exception('已添加角色总数有误(5)：' + str(len(roleAddList)))

    for i in range(len(roleAddList)):
        logging.debug('已添加角色总数：' + str(len(roleAddList)))
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

        role = roleAddList[i]
        roleName = role.text

        # 添加测试主管
        if roleName != '测试主管':
            break

        logging.debug('赋予角色：' + roleName)
        role.click()

        # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
        test = userRoleListBtn.get_attribute('value')
        # logging.info(test)
        if test != '':
            ActionChains(driver).move_to_element(userRoleListBtn).perform()
            clearUserBtn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.add-user .el-select__caret')))
            clearUserBtn.click()

        userRoleListBtn.click()
        sleep(time)

        for j in range(len(userRoleList)):
            user_ = userRoleList[j]
            userName = user_.get_attribute('innerText')
            logging.debug(str(j) + ':' + userName)

            if userName not in teamUsers:
                raise Exception('用户异常-用户：' + userName + ' 不在team里面')

            # 添加所有角色用户
            if userName == user['NAME']:
                logging.debug('用户列表-添加用户：' + addUserBtn.text + ' ' + userName)
                user_.click()
                sleep(time)

                addUserBtn.click()

                # 刷新用户列表
                sleep(time + 3)
                isFinish = wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.user-finish'), '已加载'),
                    message='用户刷新加载失败')

                if not isFinish:
                    raise Exception('用户刷新加载失败')

                sleep(time)

                break
        break

    # 删除新添加的测试主管
    for i in range(1, 7):
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
            message='获取用户列表信息失败').text
        if user_ == user['NAME'] and role == '测试主管':
            deleteBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%d) td:nth-of-type(5) button' %
                     (i))),
                message='找不到 删除按键')
            deleteBtn.click()

            # 确定删除按键
            confirmDelBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '[aria-label=提示] .el-message-box__btns button:nth-of-type(2)'
                )),
                message='找不到 确定删除按键')
            logging.debug('添加用户-删除：' + confirmDelBtn.text)
            confirmDelBtn.click()
            break

        if i == 6:
            raise ('新添加：' + user['NAME'] + ' 测试主管 不存在')

    # 刷新用户列表
    sleep(time)


# 添加角色
def addRole(user, wait, driver):
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    userListBtn.click()

    # 添加角色按钮
    addRoleBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-role-btn')),
        message='找不到 添加角色按键')
    logging.debug('用户列表-添加角色：' + addRoleBtn.text)

    # 角色列表下拉框
    roleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-rolelist .el-input__inner')),
        message='找不到 角色列表下拉按键')
    roleListBtn.click()
    sleep(time)

    # 获取所有角色
    roleList = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 下拉列表角色')

    # 添加角色
    if len(roleList) != 5:
        raise Exception('添加角色总数有误(5)：' + str(len(roleList)))
    for i in range(len(roleList)):
        logging.debug('添加角色总数：' + str(len(roleList)))
        if i:
            roleListBtn.click()
            sleep(time)

        role = roleList[i]
        logging.debug('用户列表-添加角色：' + role.get_attribute('innerText'))
        if role:
            role.click()
            sleep(time)

            addRoleBtn.click()
            sleep(time)

    # 用户列表下拉按钮
    userRoleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-user .el-input__inner')),
        message='找不到 用户列表下拉按键')
    userRoleListBtn.click()
    sleep(time)

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

    sleep(time)
    # 已添加角色列表按钮
    roleAddListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-role .el-input__inner')),
        message='找不到 已添加角色下拉列表按键')
    roleAddListBtn.click()
    sleep(time)

    # 获取所有添加的角色
    roleAddList = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 已添加角色')

    if len(roleAddList) != 5:
        raise Exception('已添加角色总数有误(5)：' + str(len(roleAddList)))

    # 列表行，获取显示用户角色
    row = 0

    for i in range(len(roleAddList)):
        logging.debug('已添加角色总数：' + str(len(roleAddList)))
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
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.add-user .el-select__caret')))
            clearUserBtn.click()

        userRoleListBtn.click()
        sleep(time)

        for j in range(len(userRoleList)):
            user = userRoleList[j]
            userName = user.get_attribute('innerText')
            logging.debug(str(j) + ':' + userName)

            if userName not in teamUsers:
                raise Exception('用户异常-用户：' + userName + ' 不在team里面')

            # 添加所有角色用户
            if roleName in userName:
                logging.debug('用户列表-添加用户：' + addUserBtn.text + ' ' + userName)
                user.click()
                sleep(time)

                addUserBtn.click()
                sleep(time + 1)

                row += 1
                # 获取列表显示是否正确
                if getTeamInfo(wait, row, 2) != userName and getTeamInfo(
                        wait, row, 4) != roleName:
                    raise Exception('用户角色显示异常')

                if getTeamInfo(wait, row, 4) == '产品经理' or getTeamInfo(
                        wait, row, 4) == '测试主管':
                    deleteBtn = wait.until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR,
                            'tbody tr:nth-of-type(%d) td:nth-of-type(5) button'
                            % (row))),
                        message='找不到 删除按键')
                    deleteBtn.click()

                    # 确定删除按键
                    confirmDelBtn = wait.until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR,
                            '[aria-label=提示] .el-message-box__btns button:nth-of-type(2)'
                        )),
                        message='找不到 确定删除按键')
                    logging.debug('添加用户-删除：' + confirmDelBtn.text)
                    confirmDelBtn.click()
                    row -= 1
                    sleep(time)
                break


# 修改产品信息
def modifyProInfo(user, wait):
    global isModifyPro
    # 产品名称输入栏
    inputProName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper .el-form-item:nth-of-type(1) input')),
        message='找不到 产品名称输入栏')
    if isModifyPro:
        inputProName.send_keys(proMod['PRONAME_1'])
    else:
        inputProName.send_keys(user['modifyPro'])

    # 产品描述输入栏
    inputProDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__wrapper .el-form-item:nth-of-type(2) input')),
        message='找不到 产品描述输入栏')
    if isModifyPro:
        inputProDes.send_keys(proMod['PRODES_1'])
    else:
        inputProDes.send_keys(user['modifyProDes'])

    # 确定修改
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-dialog__wrapper button:nth-of-type(2)')),
        message='找不到 确定修改按键')
    logging.debug('产品列表-修改：' + confirmBtn.text)
    confirmBtn.click()
    sleep(time)


def searchPro(user, wait, driver):
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

    # 等待订单加载
    sleep(time)
    orderFinish = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.order-finish'),
                                         '订单已加载'),
        message='订单加载失败')

    if orderFinish is False:
        raise Exception('订单加载失败')

    # 检查订单显示
    # ORDER1
    if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + ' 订单号显示错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 3) != config.ORDER_1['ONLINE']:
        raise Exception(config.ORDER_1['ONLINE'] + ' 在线数量显示错误：' +
                        getTeamInfo(wait, 1, 3))
    if getTeamInfo(wait, 1, 4) != config.ORDER_1['OFFLINE']:
        raise Exception(config.ORDER_1['OFFLINE'] + ' 离线数量显示错误：' +
                        getTeamInfo(wait, 1, 4))
    if getTeamInfo(wait, 1, 5) != config.ORDER_1['FACTORY']:
        raise Exception(config.ORDER_1['FACTORY'] + ' 工厂显示错误：' +
                        getTeamInfo(wait, 1, 5))
    if getTeamInfo(wait, 1, 6) != config.authTime:
        raise Exception(config.authTime + ' 有效时间显示错误：' +
                        getTeamInfo(wait, 1, 6))
    # if getTeamInfo(wait, 1, 7) != config.USER_PRO_PE['NAME']:
    #     raise Exception(config.USER_PRO_PE['NAME'] + ' 创建人显示错误：' +
    #                     getTeamInfo(wait, 1, 7))

    # ORDER2
    if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
        raise Exception(config.ORDER_2['NUM'] + ' 订单号显示错误：' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 3) != config.ORDER_2['ONLINE']:
        raise Exception(config.ORDER_2['ONLINE'] + ' 在线数量显示错误：' +
                        getTeamInfo(wait, 2, 3))
    if getTeamInfo(wait, 2, 4) != config.ORDER_2['OFFLINE']:
        raise Exception(config.ORDER_2['OFFLINE'] + ' 离线数量显示错误：' +
                        getTeamInfo(wait, 2, 4))
    if getTeamInfo(wait, 2, 5) != config.ORDER_2['FACTORY']:
        raise Exception(config.ORDER_2['FACTORY'] + ' 工厂显示错误：' +
                        getTeamInfo(wait, 2, 5))
    if getTeamInfo(wait, 2, 6) != config.authTime:
        raise Exception(config.authTime + '有效时间显示错误：' +
                        getTeamInfo(wait, 2, 6))
    # if getTeamInfo(wait, 2, 7) != config.USER_MOD_PE['NAME']:
    #     raise Exception(config.USER_MOD_PE['NAME'] + ' 创建人显示错误：' +
    #                     getTeamInfo(wait, 2, 7))

    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    userListBtn.click()
    sleep(time)

    # 查看产品成员是否为空
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    userListBtn.click()
    sleep(time)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回上一级按键')
    logging.debug('产品列表-查看：' + backBtn.text)
    goTop(driver)
    backBtn.click()
    sleep(time)
    pageFinish(driver)

    # 查看产品成员是否为空
    # 点击用户列表按钮
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
        message='找不到 用户列表tab按键')
    logging.debug('产品型号-用户列表：' + userListBtn.text)
    userListBtn.click()
    sleep(time)


# 添加产品类型
def test_addProMod(user, wait):
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
    addProModBtn.click()
    sleep(time)


# 修改产品类型
def modifyMod(user, wait):
    # 输入产品类型名称
    inputProModName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'div.el-dialog__wrapper .el-form-item:nth-of-type(1) input')),
        message='找不到 产品类型名称输入栏')
    inputProModName.send_keys(user['modifyMod'])

    # 输入产品类型描述
    inputProModDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'div.el-dialog__wrapper .el-form-item:nth-of-type(2) input')),
        message='找不到 产品类型描述输入栏')
    inputProModDes.send_keys(user['modifyModDes'])

    # 确认修改
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'div.el-dialog__wrapper .el-dialog__footer button:nth-of-type(2)'
             )),
        message='找不到 确认修改产品类型按键')
    logging.debug('产品列表-查看：' + confirmBtn.text)
    confirmBtn.click()
    sleep(time)


# 测试修改
def test_modifyProMod(user, wait, driver):
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

        if proModName == user['modName'] and proModDes == user[
                'modDes'] and proModUser == user['NAME']:
            #  修改产品类型按键
            modifyModBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(3)'
                    % (i + 1))),
                message='找不到 修改产品类型按键')
            logging.debug('产品列表-查看：' + modifyModBtn.text)
            modifyModBtn.click()

            # 修改产品类型
            modifyMod(user, wait)

        if proModName == user['tempMod'] and proModDes == user[
                'tempModDes'] and proModUser == user['NAME']:
            #  修改产品类型按键
            modifyModBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(3)'
                    % (i + 1))),
                message='找不到 修改产品类型按键')
            logging.debug('产品列表-查看：' + modifyModBtn.text)
            modifyModBtn.click()

            # 修改产品类型
            modifyMod(user, wait)

            #  查看产品类型按键
            addRoleModBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(2)'
                    % (i + 1))),
                message='找不到 查看产品类型按键')
            logging.debug('产品列表-查看：' + addRoleModBtn.text)
            addRoleModBtn.click()

            # 测试添加用户角色
            test_addRole(user, wait, driver)

            # 返回上一级
            backBtn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
                message='找不到 返回上一级按键')
            logging.debug('产品列表-查看：' + backBtn.text)
            goTop(driver)
            backBtn.click()
            sleep(time)
            pageFinish(driver)


# 测试删除
def test_deleteProMod(user, wait):
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

            #  删除产品类型按键
            deleteModBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody tr:nth-of-type(%d) td:nth-of-type(6) button:nth-of-type(1)'
                    % (row))),
                message='找不到 删除产品类型按键')
            logging.debug('产品列表-查看：' + deleteModBtn.text)
            deleteModBtn.click()

            # 确定删除
            confirmBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '[aria-label="提示"] .el-message-box__btns button:nth-of-type(2)'
                )),
                message='找不到 删除产品类型按键')
            logging.debug('产品列表-查看：' + confirmBtn.text)
            confirmBtn.click()
            sleep(time)
            row -= 1
        row += 1

    # 判断是否删除成功
    # 获取所有产品类型
    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-table__row')),
        message='找不到 产品类型列表')

    for i in range(len(modules)):
        # 产品型号名称
        proModName = getTeamInfo(wait, i + 1, 2)

        if proModName != proMod['MODNAME_1'] and proModName != proMod[
                'MODNAME_2']:
            raise Exception('产品类型删除失败')


# 测试查看-添加角色
def test_addRole(user, wait, driver):
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

    # 获取产品-型号创建人，确定是否加载成功
    isCreateUser = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.creator')),
                                         '创建人：' + user['NAME']),
        message='找不到 产品-型号创建人')
    if not isCreateUser:
        raise Exception('型号创建失败 创建人:' + user['NAME'])

    # 获取产品-型号描述，确定是否加载成功
    isCreateDes = wait.until(
        EC.text_to_be_present_in_element(((By.CSS_SELECTOR, '.product-des')),
                                         '项目描述：' + user['modifyModDes']),
        message='找不到 产品-型号描述')
    if not isCreateDes:
        raise Exception('型号创建失败 项目描述：' + user['modifyModDes'])

    # 添加角色
    addRole(user, wait, driver)


def test_proModFuc(user, wait, driver):
    # 测试添加产品类型
    test_addProMod(user, wait)

    # 测试修改
    test_modifyProMod(user, wait, driver)

    # 测试删除
    test_deleteProMod(user, wait)

    # 测试产品添加删除角色(未完成)
    addProRole(user, wait, driver)


# 关联软件
def relatedMptool(wait):
    # 软件类型
    inputSoftMod = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .el-form-item:nth-of-type(1) input')),
        message='找不到 软件类型输入栏')
    inputSoftMod.click()
    sleep(time)

    softMods = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')))
    for i in range(len(softMods)):
        softMod = softMods[i].get_attribute('innerText')
        if softMod == software['type']:
            softMods[i].click()
            sleep(time)
            break

        if i == len(softMods) - 1:
            raise Exception('Test software 不存在')

    # 软件
    inputSoft = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .el-form-item:nth-of-type(2) input')),
        message='找不到 软件输入栏')
    inputSoft.click()
    sleep(time)

    softs = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')))
    for i in range(len(softs)):
        soft = softs[i].get_attribute('innerText')
        if soft == software['soft']:
            softs[i].click()
            sleep(time)
            break

        if i == len(softs) - 1:
            raise Exception(software['name'] + '(1.00) 不存在')

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-dialog__footer button:nth-of-type(2)')),
        message='找不到 确定关联按键')
    logging.debug('关联量产工具-关联软件：' + confirmBtn.text)
    confirmBtn.click()
    sleep(time)


# 取消关联
def cancleRelated(wait):
    cancleBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box__btns button:nth-of-type(2)')),
        message='找不到 确定取消关联按键')
    logging.debug('关联量产工具-关联软件：' + cancleBtn.text)
    cancleBtn.click()
    sleep(time)


# 订单关联量产工具
def addOrderTool(user, wait):
    # 选择产品
    selectProBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.search-module .order-info-input:nth-of-type(1)')),
        message='找不到 选择产品下拉按键')
    selectProBtn.click()
    sleep(time)

    products = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品列表')

    for i in range(len(products)):
        proName = products[i].get_attribute('innerText')
        if proName == proMod['PRONAME_1']:
            products[i].click()
            sleep(time)
            break

        if i == len(products) - 1:
            raise Exception(proMod['PRONAME_1'] + ' 产品不存在')

    # 选择类型
    selectModBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.search-module .order-info-input:nth-of-type(2)')),
        message='找不到 选择产品类型下拉按键')
    selectModBtn.click()
    sleep(time)

    modules = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '[x-placement] li')),
        message='找不到 产品类型列表')

    for i in range(len(modules)):
        modName = modules[i].get_attribute('innerText')
        if modName == proMod['MODNAME_1']:
            modules[i].click()
            sleep(time)
            break

        if i == len(modules) - 1:
            raise Exception(proMod['MODNAME_1'] + ' 产品不存在')

    # 确定
    confirmSelectBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.sure')),
        message='找不到 确定选择按键')
    logging.debug('订单管理-量产工具：' + confirmSelectBtn.text)
    confirmSelectBtn.click()
    sleep(time)

    # 检查列表显示是否正确
    if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + ' 订单号错误：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 4) != config.ORDER_1['FACTORY']:
        raise Exception(config.ORDER_1['FACTORY'] + ' 工厂错误：' +
                        getTeamInfo(wait, 1, 4))
    if getTeamInfo(wait, 1, 6) != config.authTime:
        raise Exception(config.authTime + ' 有效时间错误：' +
                        getTeamInfo(wait, 1, 6))

    if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
        raise Exception(config.ORDER_2['NUM'] + ' 订单号错误：' +
                        getTeamInfo(wait, 2, 2))
    if getTeamInfo(wait, 2, 4) != config.ORDER_2['FACTORY']:
        raise Exception(config.ORDER_2['FACTORY'] + ' 工厂错误：' +
                        getTeamInfo(wait, 2, 4))
    if getTeamInfo(wait, 2, 6) != config.ORDER_2['TIME']:
        raise Exception(config.ORDER_2['TIME'] + ' 有效时间错误：' +
                        getTeamInfo(wait, 2, 6))

    # 订单列表量产工具项
    proMptools = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'tbody td:nth-of-type(7)')),
        message='找不到 订单列表量产工具项')

    for i in range(len(proMptools)):
        proMptool = proMptools[i].get_attribute('innerText')
        if proMptool == '暂未关联':
            # 关联软件
            relatedBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody .el-table__row:nth-of-type(%d) td:nth-of-type(8) button:nth-of-type(2)'
                    % (i + 1))),
                message='找不到 关联软件按键')
            logging.debug('订单管理-量产工具：' + relatedBtn.text)
            relatedBtn.click()
            sleep(time)

            # 关联软件
            relatedMptool(wait)

            # 确定关联是否成功
            proMptools = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'tbody td:nth-of-type(7)')),
                message='找不到 订单列表量产工具项')

            proMptool = proMptools[i].get_attribute('innerText')
            if proMptool == '暂未关联':
                raise Exception('关联软件失败')

        else:
            # 取消关联
            cancleBtn = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'tbody .el-table__row:nth-of-type(%d) td:nth-of-type(8) button:nth-of-type(1)'
                    % (i + 1))),
                message='找不到 取消关联软件按键')
            logging.debug('订单管理-量产工具：' + cancleBtn.text)
            cancleBtn.click()
            sleep(time)

            # 取消关联
            cancleRelated(wait)

            # 确定关联是否取消成功
            proMptools = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'tbody td:nth-of-type(7)')),
                message='找不到 订单列表量产工具项')
            proMptool = proMptools[i].get_attribute('innerText')
            if proMptool != '暂未关联':
                raise Exception('取消关联软件失败')


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
    ordNumSearchBtn.click()
    sleep(time)

    # 检查查询结果
    if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + ' 订单号不对：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 1, 5) != config.ORDER_1['FACTORY']:
        raise Exception(config.ORDER_1['FACTORY'] + ' 工厂不对：' +
                        getTeamInfo(wait, 1, 5))
    if getTeamInfo(wait, 1, 6) != config.authTime:
        raise Exception(config.authTime + ' 有效时间不对：' +
                        getTeamInfo(wait, 1, 6))


# 按产品类型查询
def searchByProMod(wait):
    # 选择产品
    prolistBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.el-select:nth-of-type(1) input')),
        message='找不到 产品列表下拉按键')
    prolistBtn.click()
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
    proModSearchBtn.click()
    sleep(time)

    # 检查查询结果
    if getTeamInfo(wait, 1, 2) != config.ORDER_1['NUM']:
        raise Exception(config.ORDER_1['NUM'] + '订单号不对：' +
                        getTeamInfo(wait, 1, 2))
    if getTeamInfo(wait, 2, 2) != config.ORDER_2['NUM']:
        raise Exception(config.ORDER_2['NUM'] + '订单号不对：' +
                        getTeamInfo(wait, 2, 2))


# 查询所有订单
def searchAllOrder(wait):
    allOrderBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-all')),
        message='找不到 查询所有订单按键')
    logging.debug('订单列表-查询：' + allOrderBtn.text)
    allOrderBtn.click()
    sleep(time)

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
def searchOrder(user, wait):
    # 按订单号查询
    searchByOrderNum(wait)

    # 按产品型号查询
    searchByProMod(wait)

    # 查询所有订单
    searchAllOrder(wait)


# 用户资料
def userInfo(user, wait, driver):
    if user['updateUserInfoEnable']:
        # 修改个人资料
        logging.info('修改用户资料')
        updateUserInfo(user, wait)
        checkUserInfo(user, wait)
        logging.info('修改资料PASS')

        # 将滚动条移动到页面的顶部
        goTop(driver)

        # 修改密码
        logging.info('修改密码')
        updatePassword(user, wait)
        driver.get(config.URL)
        login(user, wait)
        checkUserInfo(user, wait)
        updatePassword(user, wait)
        logging.info('修改密码PASS')

        # 还原用户名，方便后续测试
        resUserName(user, wait, driver)

        # 将滚动条移动到页面的顶部
        goTop(driver)

    if user['teamEnable']:
        # team功能
        myTeamBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.watch-myteam')),
            message='找不到 查看我的群组按键')
        logging.debug('个人中心-我的资料：' + myTeamBtn.text)
        myTeamBtn.click()
        sleep(time)

        # 等待team列表刷新
        pageFinish(driver)

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

        # raise Exception('Test stop!')


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


# 新增产品
def addProduct(user, wait, driver):
    if user['addModEnable']:
        # 打开添加产品项
        addNewProModBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(2) .el-menu-item-group li:nth-of-type(1)'
            )),
            message='找不到 新增产品')
        logging.debug('产品管理-新增产品：' + addNewProModBtn.text)
        addNewProModBtn.click()

        logging.info('添加产品型号')
        addMod(user, wait, driver)
        logging.info('添加产品型号成功')

        logging.info('添加产品型号角色')
        addRole(user, wait, driver)
        logging.info('添加产品型号角色成功')

    # raise Exception('Test stop!')


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
        pageFinish(driver)

        # 查询功能
        logging.info('查询产品列表')
        searchPro(user, wait, driver)
        logging.info('查询产品列表成功')


# 订单管理
def orderManager(user, wait, driver):
    # 点击选择产品管理项
    orderManagerBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'li.el-submenu:nth-of-type(4) div.el-submenu__title')),
        message='找不到 软件管理')
    logging.debug('订单管理：' + orderManagerBtn.text)
    orderManagerBtn.click()


# 关联量产工具
def orderTools(user, wait, driver):
    if user['orderToolEnable']:
        # 关联量产工具按键
        orderToolsBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'li.el-submenu:nth-of-type(4) li.el-menu-item:nth-of-type(2)'
                 )),
            message='找不到 关联量产工具按键')
        logging.debug('订单管理-量产工具：' + orderToolsBtn.text)
        orderToolsBtn.click()

        logging.info('订单关联量产工具')
        addOrderTool(user, wait)
        logging.info('订单关联量产工具成功')


# 上传软件
def upSoftware(wait, user, product, module):
    # 点击软件管理-上传软件
    upSoftBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(3) .el-menu-item:nth-of-type(1)'
        )),
        message='找不到 上传软件选项')
    logging.debug('软件管理-上传软件：' + upSoftBtn.text)
    upSoftBtn.click()

    # 选择产品
    proLisBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'div.item:nth-of-type(1) .el-input')),
        message='找不到 选择产品按键')
    proLisBtn.click()
    sleep(time)

    proList = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')),
        message='找不到 产品列表')
    for pro in proList:
        proName = pro.get_attribute('innerText')
        if proName == product:
            logging.debug('上传软件-选择产品：' + proName)
            pro.click()
            sleep(time)
            break
        if pro == proList[len(proList) - 1]:
            raise Exception(product + ' 不存在')

    # 选择型号
    # modLisBtn = wait.until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR,
    #                                 'div.item:nth-of-type(2) .el-input')))
    # modLisBtn.click()
    # sleep(time)

    # modList = wait.until(
    #     EC.visibility_of_any_elements_located(
    #         (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')))
    # for mod in modList:
    #     modName = mod.get_attribute('innerText')
    #     if modName == module:
    #         logging.debug('上传软件-选择型号：' + modName)
    #         mod.click()
    #         sleep(time)
    #         break
    #     if mod == modList[len(modList) - 1]:
    #         raise Exception(module + ' 不存在')

    # 软件类型
    inputSoftType = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.item:nth-of-type(3) .el-input__inner')),
        message='找不到 软件类型输入栏')
    inputSoftType.click()
    sleep(time)

    softTypes = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li')),
        message='找不到 软件类型列表')
    inputSoftType.send_keys(software['type'])
    for type in softTypes:
        type_name = type.text
        if type_name == software['type']:
            type.click()
            sleep(time)
            break

        if type == softTypes[len(softTypes) - 1]:
            raise Exception('找不到 软件类型 ' + software['type'])
    logging.debug('上传软件-软件类型：' + software['type'])

    # 选择文件
    inputFile = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.item:nth-of-type(4) input[type=file]')),
        message='找不到 文件输入栏')
    inputFile.send_keys(software['testFile'])

    # 测试报告
    inputTest = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.item:nth-of-type(5) input')),
        message='找不到 测试报告输入栏')
    inputTest.send_keys(software['testReport'])

    # 版本号
    inputSoftVer = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.item:nth-of-type(6) .el-input__inner')),
        message='找不到 版本号输入栏')
    inputSoftVer.send_keys(Keys.CONTROL + 'a')
    inputSoftVer.send_keys(software['version'])
    logging.debug('上传软件-软件版本：' + software['version'])

    # 软件介绍
    inputSoftDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.item:nth-of-type(7) .el-textarea__inner')),
        message='找不到 软件介绍输入栏')
    inputSoftDes.send_keys(Keys.CONTROL + 'a')
    inputSoftDes.send_keys(software['des'])
    logging.debug('上传软件-软件介绍：' + software['des'])

    sleep(time)

    # 上传
    submitBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit')),
        message='找不到 上传按键')
    logging.debug('上传软件：' + submitBtn.text)
    submitBtn.click()
    sleep(0.5)

    upOK = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.page-finish'),
                                         '成功上传'),
        message='上传软件失败')

    if upOK is False:
        raise Exception('上传软件失败')


# 核对软件列表
def check_softList(user, wait, driver):
    pass
    # if getTeamInfo(wait, 1, 1) != software['version']:
    #     raise Exception(software['version'] + ' 软件版本错误' +
    #                     getTeamInfo(wait, 1, 1))
    # if getTeamInfo(wait, 1, 2) != software['name']:
    #     raise Exception(software['name'] + ' 软件名错误' + getTeamInfo(wait, 1, 2))
    # if getTeamInfo(wait, 1, 3) != software['type']:
    #     raise Exception(software['type'] + ' 软件类型错误' + getTeamInfo(wait, 1, 3))
    # if getTeamInfo(wait, 1, 4) != proMod['MODNAME_1']:
    #     raise Exception(proMod['MODNAME_1'] + ' 产品型号错误' +
    #                     getTeamInfo(wait, 1, 4))
    # if getTeamInfo(wait, 1, 5) != software['des']:
    #     raise Exception(software['des'] + ' 软件描述错误' + getTeamInfo(wait, 1, 5))

    # if getTeamInfo(wait, 2, 1) != software['version']:
    #     raise Exception(software['version'] + ' 软件版本错误' +
    #                     getTeamInfo(wait, 2, 1))
    # if getTeamInfo(wait, 2, 2) != software['name']:
    #     raise Exception(software['name'] + ' 软件名错误' + getTeamInfo(wait, 2, 2))
    # if getTeamInfo(wait, 2, 3) != software['type']:
    #     raise Exception(software['type'] + ' 软件类型错误' + getTeamInfo(wait, 2, 3))
    # if getTeamInfo(wait, 2, 4) != proMod['MODNAME_2']:
    #     raise Exception(proMod['MODNAME_1'] + ' 产品型号错误' +
    #                     getTeamInfo(wait, 2, 4))
    # if getTeamInfo(wait, 2, 5) != software['des']:
    #     raise Exception(software['des'] + ' 软件描述错误' + getTeamInfo(wait, 2, 5))

    # if getTeamInfo(wait, 3, 1) != software['version']:
    #     raise Exception(software['version'] + ' 软件版本错误' +
    #                     getTeamInfo(wait, 3, 1))
    # if getTeamInfo(wait, 3, 2) != software['name']:
    #     raise Exception(software['name'] + ' 软件名错误' + getTeamInfo(wait, 3, 2))
    # if getTeamInfo(wait, 3, 3) != software['type']:
    #     raise Exception(software['type'] + ' 软件类型错误' + getTeamInfo(wait, 3, 3))
    # if getTeamInfo(wait, 3, 4) != proMod['MODNAME_1']:
    #     raise Exception(proMod['MODNAME_1'] + ' 产品型号错误' +
    #                     getTeamInfo(wait, 3, 4))
    # if getTeamInfo(wait, 3, 5) != software['des']:
    #     raise Exception(software['des'] + ' 软件描述错误' + getTeamInfo(wait, 3, 5))

    # if getTeamInfo(wait, 4, 1) != software['version']:
    #     raise Exception(software['version'] + ' 软件版本错误' +
    #                     getTeamInfo(wait, 4, 1))
    # if getTeamInfo(wait, 4, 2) != software['name']:
    #     raise Exception(software['name'] + ' 软件名错误' + getTeamInfo(wait, 4, 2))
    # if getTeamInfo(wait, 4, 3) != software['type']:
    #     raise Exception(software['type'] + ' 软件类型错误' + getTeamInfo(wait, 4, 3))
    # if getTeamInfo(wait, 4, 4) != proMod['MODNAME_2']:
    #     raise Exception(proMod['MODNAME_1'] + ' 产品型号错误' +
    #                     getTeamInfo(wait, 4, 4))
    # if getTeamInfo(wait, 4, 5) != software['des']:
    #     raise Exception(software['des'] + ' 软件描述错误' + getTeamInfo(wait, 4, 5))


# 软件列表查询
def test_searchSoft(user, wait, driver):
    # 软件列表显示是否正确
    check_softList(user, wait, driver)
    # 查询按键
    searchBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-btn')),
        message='找不到 查询按键')
    logging.debug('软件管理-软件列表：' + searchBtn.text)

    # 所有按键
    allBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-all')),
        message='找不到 查询所有按键')
    logging.debug('软件管理-软件列表：' + allBtn.text)

    # 按软件类型查询
    bySoftType = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-softtype-input input')),
        message='找不到 按软件类型查询输入栏')

    bySoftType.send_keys(software['type'])
    searchBtn.click()
    sleep(time)

    # 软件列表显示是否正确
    check_softList(user, wait, driver)

    # 按软件名查询
    bySoftName = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.search-input input')),
        message='找不到 按软件名查询输入栏')
    bySoftName.send_keys(software['name'])
    bySoftType.send_keys(Keys.CONTROL + 'a')
    bySoftType.send_keys(Keys.DELETE)
    searchBtn.click()
    sleep(time)

    # 软件列表显示是否正确
    check_softList(user, wait, driver)

    # 查询全部
    allBtn.click()
    sleep(time)

    # 软件列表显示是否正确
    check_softList(user, wait, driver)


# 下载软件功能
def dowmload_softFuc(user, wait, driver):
    # 下载软件
    downloadSoftBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.download-url')),
        message='找不到 下载软件按键')
    logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    downloadSoftBtn.click()
    sleep(time)

    downloadSoftBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.download-url')),
        message='找不到 下载软件按键')
    logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    downloadSoftBtn.click()
    sleep(time+2)

    # 核对下载的软件是否正确
    myfile = filePath + '\\' + software['name']
    if os.path.exists(myfile):
        # 删除文件
        os.remove(myfile)

    else:
        raise Exception('下载软件失败')

    if os.path.exists(myfile):
        raise Exception('删除下载软件失败')


# 软件列表功能
def test_softFuc(user, wait, driver):
    # 设置为无效状态
    if getTeamInfo(wait, 1, 7) == '有效状态':
        # 获取设置禁止状态按键
        vaildBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'tbody tr:nth-of-type(1) a.download-url')),
            message='找不到 设置禁止状态按键')
        logging.debug('软件管理-软件列表：' + vaildBtn.text)
        vaildBtn.click()
        sleep(time)
    else:
        raise Exception('禁止状态显示错误：' + getTeamInfo(wait, 1, 7))

    if getTeamInfo(wait, 1, 7) == '禁止状态':
        # 获取设置有效状态按键
        vaildBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'tbody tr:nth-of-type(1) a.download-url')),
            message='找不到 设置有效状态按键')
        logging.debug('软件管理-软件列表：' + vaildBtn.text)
        vaildBtn.click()
        sleep(time)

        if getTeamInfo(wait, 1, 7) != '有效状态':
            raise Exception('设置有效状态失败')
    else:
        raise Exception('设置禁止状态失败')

    # 下载软件
    downloadSoftBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(1) span.download-url:nth-of-type(1)')),
        message='找不到 下载软件按键')
    logging.debug('软件管理-软件列表：' + downloadSoftBtn.text)
    downloadSoftBtn.click()
    sleep(time + 2)

    # 核对下载的软件是否正确
    myfile = filePath + '\\' + software['name']
    if os.path.exists(myfile):
        res = filecmp.cmp(myfile, software['testFile'])
        if not res:
            raise Exception('软件下载错误')

        # 删除文件
        os.remove(myfile)

    else:
        raise Exception('下载软件失败')

    if os.path.exists(myfile):
        raise Exception('删除下载软件失败')

    # 下载报告
    downloadRepoBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(1) span.download-url:nth-of-type(2)')),
        message='找不到 下载软件按键')
    logging.debug('软件管理-软件列表：' + downloadRepoBtn.text)
    downloadRepoBtn.click()
    sleep(time + 2)

    # 核对下载的报告是否正确
    myfile = filePath + '\\' + 'testFile.txt'
    if os.path.exists(myfile):
        res = filecmp.cmp(myfile, software['testReport'])
        if not res:
            raise Exception('软件下载错误')

        # 删除文件
        os.remove(myfile)

    else:
        raise Exception('下载报告失败')

    if os.path.exists(myfile):
        raise Exception('删除下载报告失败')


# 订单列表
def orderList(user, wait, driver):
    if user['orderListEnable']:
        # 订单列表按键
        orderListsBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'li.el-submenu:nth-of-type(4) li.el-menu-item:nth-of-type(2)'
                 )),
            message='找不到 订单列表按键')
        logging.debug('订单管理-量产工具：' + orderListsBtn.text)
        orderListsBtn.click()

        logging.info('查询订单')
        searchOrder(user, wait)
        logging.info('查询订单成功')

        # 测试下载功能
        logging.info('测试下载功能')
        dowmload_softFuc(user, wait, driver)
        logging.info('测试下载功能成功')


# 软件管理
def softwareManager(user, wait, driver):
    # 点击选择软件管理项
    orderManagerBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'li.el-submenu:nth-of-type(3) div.el-submenu__title')),
        message='找不到 订单管理')
    logging.debug('订单管理：' + orderManagerBtn.text)
    orderManagerBtn.click()
    sleep(time)


# 软件管理-上传软件
def upSoftWare(user, wait, driver):
    if user['upSoftEnable']:
        # 点击软件管理-上传软件
        upSoftBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(3) .el-menu-item:nth-of-type(1)'
            )))
        logging.debug('软件管理-上传软件：' + upSoftBtn.text)
        upSoftBtn.click()
        sleep(time)

        # 上传软件
        logging.info('上传软件')
        upSoftware(wait, user, proMod['PRONAME_1'], proMod['MODNAME_1'])
        logging.info('上传软件成功')


# 软件列表
def softList(user, wait, driver):
    if user['softListEnable']:
        softListBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(3) .el-menu-item:nth-of-type(2)'
            )),
            message='找不到 软件列表选项')
        logging.debug('软件管理-上传软件：' + softListBtn.text)
        softListBtn.click()
        # 等待列表加载完成
        sleep(time)
        pageFinish(driver)

        # 测试查询功能
        logging.info('测试查询功能')
        test_searchSoft(user, wait, driver)
        logging.info('测试查询功能成功')

        # 测试下载功能
        logging.info('测试下载功能')
        test_softFuc(user, wait, driver)
        logging.info('测试下载功能成功')


# 样品管理
def sampleManage(wait):
    sampleManage = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(5) .el-submenu__title'
        )),
        message='找不到 样品管理')
    logging.debug('样品管理：' + sampleManage.text)
    sampleManage.click()


# 添加样品
def addSampe(wait, driver, user):
    if user['createSampleEnable']:
        # 添加样品
        newSampe(wait, user, config.SAMPLE, driver)
        # 添加记录
        newRecord(wait)


# 添加不良品样品
def addNgSampe(wait, driver, user):
    if user['createSampleEnable']:
        # 添加样品
        newNgSampe(wait, user, config.SAMPLE, driver)
        # 添加记录
        newRecord(wait)


# 新增样品
def newSampe(wait, user, sample, driver):
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
    sleep(time)

    # 获取产品线列表
    pros = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 产品线列表')
    sleep(time)

    # 选择产品线
    for i in range(len(pros)):
        if pros[i].text == sample['PRO']:
            pros[i].click()
            break

        if i == (len(pros) - 1):
            raise Exception('找不到：' + sample['PRO'])
    sleep(time)

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
    sleep(time)

    addSampleInfo(wait, user, sample, driver)


# 新增不良品样品
def newNgSampe(wait, user, sample, driver):
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
    sleep(time)

    # 获取产品线列表
    pros = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 产品线列表')
    sleep(time)

    # 选择产品线
    for i in range(len(pros)):
        if pros[i].text == sample['PRO']:
            pros[i].click()
            break

        if i == (len(pros) - 1):
            raise Exception('找不到：' + sample['PRO'])
    sleep(time)

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
    sleep(time)

    addSampleInfo(wait, user, sample, driver)


# 添加样品信息
def addSampleInfo(wait, user, sample, driver):
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
    sleep(time)

    types = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 型号列表')

    for i in range(len(types)):
        if sample['TYPE'] == types[i].text:
            types[i].click()
            sleep(time)
            break

        if i == len(types) - 1:
            raise Exception('型号不存在：' + sample['TYPE'])

    # 项目
    modInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(3) input')),
        message='找不到 项目输入栏')
    modInput.click()
    sleep(time)

    mods = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 项目列表')

    for i in range(len(mods)):
        if sample['MOD'] == mods[i].text:
            mods[i].click()
            sleep(time)
            break

        if i == len(mods) - 1:
            raise Exception('项目不存在：' + sample['MOD'])

    # 订单
    orderInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(4) div input')),
        message='找不到 订单输入栏')
    orderInput.click()
    sleep(time)

    orders = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 订单列表')

    for i in range(len(orders)):
        if sample['ORDER'] == orders[i].text:
            orders[i].click()
            sleep(time)
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
    sleep(time)

    factorys = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 工厂列表')

    for i in range(len(factorys)):
        if sample['FACTORY'] == factorys[i].text:
            factorys[i].click()
            sleep(time)
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
    sleep(time)

    res = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 资源列表')

    for i in range(len(res)):
        if sample['RES'] == res[i].text:
            res[i].click()
            sleep(time)
            break

        if i == len(res) - 1:
            raise Exception('资源不存在：' + sample['RES'])

    # wafer
    waferInput = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-info-form>div:nth-child(9) input')),
        message='找不到 容量输入栏')

    waferInput.click()
    sleep(time)
    wafers = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 容量列表')

    for i in range(len(wafers)):
        if sample['WAFER'] == wafers[i].text:
            wafers[i].click()
            sleep(time)
            break

        if i == len(wafers) - 1:
            raise Exception('容量不存在：' + sample['WAFER'])

    # 料号
    sizeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(10) input')),
        message='找不到 容量输入栏')
    sizeInput.send_keys(sample['PARTNO'])
    sleep(time)

    # DIE
    DIEInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(11) input')),
        message='找不到 DIE输入栏')
    DIEInput.click()
    sleep(time)

    DIEs = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 DIE列表')

    for i in range(len(DIEs)):
        if sample['DIE'] == DIEs[i].text:
            DIEs[i].click()
            sleep(time)
            break

        if i == len(DIEs) - 1:
            raise Exception('DIE不存在：' + sample['DIE'])

    # 容量
    sizeInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(12) input')),
        message='找不到 容量输入栏')
    sizeInput.click()
    sleep(time)

    sizes = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 容量列表')

    for i in range(len(sizes)):
        if sample['SIZE'] == sizes[i].text:
            sizes[i].click()
            sleep(time)
            break

        if i == len(sizes) - 1:
            raise Exception('容量不存在：' + sample['SIZE'])

    # 位宽
    bitInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(13) input')),
        message='找不到 位宽输入栏')
    bitInput.click()
    sleep(time)

    bits = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 位宽列表')

    for i in range(len(bits)):
        if sample['BITWID'] == bits[i].text:
            bits[i].click()
            sleep(time)
            break

        if i == len(bits) - 1:
            raise Exception('位宽不存在：' + sample['BITWID'])

    # 封装
    packageInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(14) input')),
        message='找不到 封装输入栏')
    packageInput.click()
    sleep(time)

    packages = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li span')),
        message='找不到 封装列表')

    for i in range(len(packages)):
        if sample['PACKAGE'] == packages[i].text:
            packages[i].click()
            sleep(time)
            break

        if i == len(packages) - 1:
            raise Exception('封装不存在：' + sample['PACKAGE'])

    # 基板
    subInput = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(15) input')),
        message='找不到 基板输入栏')
    subInput.send_keys(sample['SUB']),
    sleep(time)

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
    sleep(time)

    # 返回上一级
    backBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
        message='找不到 返回按键')
    goTop(driver)
    backBtn.click()
    sleep(time)


def newRecord(wait):
    # 添加样品记录
    addRecordBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'tbody button:nth-child(2) span')),
        message='找不到 添加记录按键')
    logging.info('样品列表：' + addRecordBtn.text)
    addRecordBtn.click()
    sleep(time)

    # platform = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'input')),
    #     message='找不到 平台输入栏')
    # platform.send_keys('TEST')

    testTime = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.el-date-editor--datetime input')),
        message='找不到 测试时间')
    testTime.click()
    sleep(time)

    now = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'div[x-placement] .el-picker-panel__footer button:nth-child(1)')),
        message='找不到 此刻')
    now.click()
    sleep(time)

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
    sleep(time)


def main(driver, user=config.USER_PRO_RD):
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

    # 录像开始
    if not config.hide:
        Save = get_video.Job()
        Save.start()

    try:
        # 设置等待时间
        wait = WebDriverWait(driver, 10)
        # 显示1920*1080
        # driver.set_window_size(1366, 768)

        # 最大化
        if not config.hide:
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

        # 软件管理
        logging.info('软件管理')
        softwareManager(user, wait, driver)

        # 软件管理-上传软件
        logging.info('软件管理-上传软件')
        upSoftWare(user, wait, driver)

        # 软件管理-软件列表
        logging.info('软件管理-软件列表')
        softList(user, wait, driver)

        # 订单管理
        logging.info('订单管理')
        orderManager(user, wait, driver)

        # 订单管理-订单列表
        logging.info('订单管理-订单列表')
        orderList(user, wait, driver)

        logging.info('样品管理')
        sampleManage(wait)

        logging.info('样品管理-添加样品')
        addSampe(wait, driver, user)

        logging.info('样品管理-添加不良品样品')
        addNgSampe(wait, driver, user)

        logging.debug('样品管理')
        sampleManage(wait)

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
            opt.add_argument("--headless")
            # 谷歌文档提到需要加上这个属性来规避bug
            opt.add_argument('--disable-gpu')
            # 指定浏览器分辨率
            opt.add_argument('window-size=1920x3000')
            # 无痕模式
            opt.add_argument('--incognito')
        driver = webdriver.Chrome(options=opt)
        OK = main(driver)
        # 只测试J次
        # j = j - 1
        if OK:
            # 必须J次pass
            j = j - 1
            i += 1
            print(i)
