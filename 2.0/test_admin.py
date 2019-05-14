import config
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import logging
from datetime import datetime

# DEBUG LOG
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if config.debug:
    logging.disable(logging.DEBUG)

# 睡眠时间
time = config.timeout

# 测试TEAM
testTeam = config.testTeam

# TEAM成员
teamUsers = config.teamUsers

# 测试产品-型号
proMod = config.proMod

# currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 测试文件
software = config.software


# 将滚动条移动到页面的顶部
def goTop(driver):
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    sleep(time)


# 获取team列表信息，row行1开始，colunm列1开始
def getTeamInfo(wait, row, column):
    teamItem = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'tbody tr:nth-of-type(%d) td:nth-of-type(%d)' % (row, column))),
        message='获取team列表信息失败')

    return teamItem.text


# 登录
def login(user, wait):
    # 点击密码登录
    loginTabView = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          '.way li:nth-of-type(2)')),
        message='找不到 密码登陆TAB')
    logging.debug('登录-Tab项(密码登录)：' + loginTabView.text)
    loginTabView.click()

    # 输入email
    inputEmail = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .mail .el-input__inner')),
        message='找不到 EMALI输入栏')
    inputEmail.send_keys(user['EMAIL'])

    # 输入password
    inputPsw = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.password-login .password .el-input__inner')),
        message='找不到 密码输入栏')
    inputPsw.send_keys(user['LOGIN'])

    # 点击登录
    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.password-login .login')),
        message='找不到 登陆按键')
    logging.debug('登录-按钮(登录/注册)：' + loginBtn.text)
    loginBtn.click()

    # 获取登录状态
    online = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.online')),
        message='找不到 登录-状态(在线)')

    username = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.username')),
        message='找不到 登录-用户')

    sleep(config.timeout)

    logging.info('登录成功：' + username.text + ' ' + online.text)


# 添加成员
def addUserToTeam(wait, driver):
    # 点击用户下拉栏
    userListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-input__inner')),
        message='找不到 用户列表下拉按键')

    userListBtn.click()
    sleep(time)

    # 获取所有user，users
    users = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-scrollbar__wrap li')),
        message='找不到 用户列表')

    # 添加按钮
    sureAddUserBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.sure-add')))

    # 添加用户
    for teamUser in teamUsers:
        logging.debug('TEAM添加用户：' + teamUser)

        # 第一个用户不用点击下拉列表
        if teamUser != teamUsers[0]:
            # 清空下拉栏，否则被选中的下一项会提示不可见，不能操作的BUG
            test = userListBtn.get_attribute('value')
            if test != '':
                ActionChains(driver).move_to_element(userListBtn).perform()
                clearUserBtn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                '.el-select__caret')),
                    message='找不到 清除用户按键')
                clearUserBtn.click()
                sleep(time)

            # 点击下拉列表按键
            userListBtn.click()
            sleep(time)
        for user in users:
            userName = user.get_attribute('innerText')
            # logging.info('用户：' + userName)
            # logging.info('用户：' + user.get_attribute('innerHTML'))
            if userName == teamUser:
                user.click()
                sleep(time)
                sureAddUserBtn.click()
                logging.debug('TEAM添加用户：' + sureAddUserBtn.text + ' ' +
                              userName)

                # 等待用户列表刷新
                sleep(time)
                break

            if user == users[len(users) - 1]:
                raise Exception('找不到用户：' + teamUser)


# 创建TEAM
def createTeam(wait, driver):
    # BUG 当列表为空是，可能获取元素出错
    # 获取team列表
    teams = wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '.el-table__row td:nth-of-type(2) .cell')),
        message='找不到 TEAM列表')

    # 用来标记是否存在'Test team'，False:不存在，True:存在
    isTestTeam = False
    # a到位TEAM
    a = 1
    for i in range(len(teams)):
        if teams[i].text == 'TestTeam':
            isTestTeam = True
            a = a + i
            break

        if i == len(teams) - 1:
            a = a + len(teams)

    if isTestTeam is False:
        # 创建team:'testTeam'
        # 点击创建team 按钮
        createTeambtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.create-team:nth-of-type(3)')),
            message='找不到 创建TEAM按键')
        logging.debug('team管理-创建team：' + createTeambtn.text)
        createTeambtn.click()

        # 输入team name
        teamName = wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '.el-dialog__body .el-form-item:nth-of-type(1) .el-input__inner'
            )),
            message='找不到 TEAM名字输入栏')
        teamName.send_keys(testTeam['NAME'])

        # 输入team描述·
        teamDes = wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '.el-dialog__body .el-form-item:nth-of-type(2) .el-input__inner'
            )),
            message='找不到 TEAM描述输入栏')
        teamDes.send_keys(testTeam['DES'])

        # 点击确定创建
        checkCreateTeamBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '.dialog-footer:nth-of-type(1) .el-button:nth-of-type(2)')),
            message='找不到 确定创建按键')
        logging.debug('创建team-创建：' + checkCreateTeamBtn.text)
        checkCreateTeamBtn.click()

        # 需要延迟，防止页面挡住，刷新列表
        sleep(time)

    # 点击查看
    teamViewBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'tr:nth-of-type(%i) button:nth-of-type(2)' % (a))),
        message='找不到 TEAM 查看按键')
    logging.debug('team管理-查看：' + teamViewBtn.text)
    teamViewBtn.click()

    # 刷新用户列表
    sleep(time)


def adminManager(wait):
    # 点击管理员管理
    adminManagerBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.left-side>ul:nth-child(1) li:nth-child(1) span')),
        message='找不到 管理员管理按键')
    logging.info('管理员管理：' + adminManagerBtn.text)
    adminManagerBtn.click()


# 管理员管理-team管理
def teamManage(user, wait, driver):
    # TEAM 管理测 teamEable:0 不测试，1 测试
    if user['teamEable']:
        # 点击team管理
        teamManageBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.left-side .el-menu-vertical-demo:nth-of-type(1) .el-submenu:nth-of-type(1) .el-menu-item:nth-of-type(2)'
            )),
            message='找不到 team管理按键')
        logging.debug('管理员管理-team管理：' + teamManageBtn.text)
        teamManageBtn.click()

        # 等待所有team列表，否则team列表可能获取为空
        sleep(time)

        # 创建TEAM:
        logging.info('创建TEAM：TestTeam')
        createTeam(wait, driver)
        logging.info('创建TEAM：TestTeam 成功')

        # 添加TEAM成员
        logging.info('添加TEAM成员')
        addUserToTeam(wait, driver)
        logging.info('添加TEAM成员成功')


# 新增产品
def addNewPro(wait, proName, proDes):
    # 点击新增产品按钮
    addNewProBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-newproduct')),
        message='找不到 新增产品按键')
    logging.debug('新增产品-新增产品：' + addNewProBtn.text)
    addNewProBtn.click()

    # 输入产品名称
    inputProName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .new-product:nth-of-type(1) .el-input__inner')),
        message='找不到 产品名输入栏')
    inputProName.send_keys(proName)

    # 输入产品描述
    inputProDes = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .new-product:nth-of-type(2) .el-input__inner')),
        message='找不到 产品描述输入栏')
    inputProDes.send_keys(proDes)

    # 确定添加按钮
    checkAddProBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-dialog__footer .el-button:nth-of-type(2)')),
        message='找不到 确定添加按键')
    logging.debug('新增产品-确定：' + checkAddProBtn.text)
    checkAddProBtn.click()

    # 延时，防止页面被挡住
    sleep(time)


# 添加产品
def addProduct(wait, proName, proDes):
    # 打开添加产品项
    newProductBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(2) li:first-child')),
        message='找不到 添加产品按键')
    logging.debug('产品管理-新增产品：' + newProductBtn.text)
    newProductBtn.click()
    sleep(time)

    # isPro：TestProduct 是否存在,True:存在,False:不存在
    isPro = False

    # 产品列表下拉按钮
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(1) .el-input__inner')),
        message='找不到 产品列表下拉按键')
    proLisBtn.click()
    sleep(time)

    isExistPro = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[x-placement]')),
        message='找不到 产品列表')

    if '无数据' not in isExistPro.get_attribute('innerHTML'):
        # 获取产品列表，并判断是否存在产品名：TestProduct
        proLis = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 '[x-placement] li')),
            message='找不到 产品列表')
        for pro in proLis:
            namePro = pro.get_attribute('innerText')
            # logging.info(namePro)
            if namePro == proName:
                logging.debug('新增产品-选择产品：' + namePro)
                pro.click()
                sleep(time)
                isPro = True
                break

    # TestProduct不存在，需要新增
    if isPro is False:
        addNewPro(wait, proName, proDes)
        proLisBtn.click()
        sleep(time)

        proLis = wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, '.el-select-dropdown__list li')),
            message='找不到 产品列表')

        for pro in proLis:
            namePro = pro.get_attribute('innerText')
            if namePro == proName:
                logging.debug('新增产品-选择产品：' + namePro)
                pro.click()
                break


'''
# 添加产品型号
def addProMod(wait):
    # 输入产品类型名称
    inputModuleName = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(2) .el-input__inner')))
    inputModuleName.send_keys('TestModule')

    # 输入产品类型描述
    inputModuleDes = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'textarea.el-textarea__inner')))
    inputModuleDes.send_keys('TestModule only for test')

    # 点击创建按钮
    createModBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '.el-form-item:nth-of-type(4) .el-button:nth-of-type(1)')))
    logging.info('新增产品-立即创建：' + createModBtn.text)
    createModBtn.click()

    # 前往添加成员页面
    gotoAddBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.el-message-box .el-button:nth-of-type(2)')))
    logging.info('新增产品-立即前往：' + gotoAddBtn.text)
    gotoAddBtn.click()
'''


# 判断类型是否存在
def isExistMod(wait, modName):
    pros = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')),
        message='找不到 类型列表')
    if modName in pros.get_attribute('innerHTML'):
        return True
    else:
        return False


# 添加型号
def newModule(wait, proName, modName, modDes):
    # 打开产品列表项
    productListBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(2) li:last-child')),
        message='找不到 添加产品列表项')
    logging.debug('产品管理-产品列表：' + productListBtn.text)
    productListBtn.click()

    # 等待产品列表加载完成
    sleep(time)

    # 获取产品列表产品名
    proNames = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'tbody tr td:nth-of-type(2)')),
        message='找不到 产品列表中的产品名称')

    # 打开产品 查看功能
    for i in range(len(proNames)):
        if proNames[i].text == proName:
            viewBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%i) button:nth-of-type(2)' %
                     (i + 1))),
                message='找不到 查看按键')
            logging.debug('产品管理-产品列表：' + viewBtn.text)
            viewBtn.click()
            break

    # 等待列表加载
    sleep(time)

    # 判断是否已存在这个类型
    if isExistMod(wait, modName) is False:
        # 输入类型名称
        inputModName = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '.add-module-name input')),
            message='找不到 产品类型名称输入栏')
        inputModName.send_keys(modName)

        # 输入类型描述
        inputModDes = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '.add-mudule-des input')),
            message='找不到 产品类型描述输入栏')
        inputModDes.send_keys(modDes)

        # 添加
        addProModBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.add')),
            message='找不到 添加产品类型按键')
        logging.debug('产品列表-查看：' + addProModBtn.text)
        addProModBtn.click()

        sleep(config.timeout)


# 添加产品角色
def addProRole(wait, driver, proName):
    # 打开产品列表项
    productListBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(2) li:last-child')),
        message='找不到 产品列表按键')
    logging.debug('产品管理-产品列表：' + productListBtn.text)
    productListBtn.click()

    # 等待产品列表加载完成
    sleep(time)

    # 获取产品列表产品名
    proNames = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'tbody tr td:nth-of-type(2)')),
        message='找不到 产品列表中的产品名称')

    # 打开产品 查看功能
    for i in range(len(proNames)):
        if proNames[i].text == proName:
            viewBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%i) button:nth-of-type(2)' %
                     (i + 1))),
                message='找不到 查看按键')
            logging.debug('产品管理-产品列表：' + viewBtn.text)
            viewBtn.click()
            break

    # 等待列表加载
    sleep(time)

    # 添加角色
    addRole(wait, driver, '产品-')


# 添加型号角色
def addModRole(wait, driver, proName):
    # 打开产品列表项
    productListBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'ul:nth-child(1)>li:nth-child(2) li:last-child')),
        message='找不到 产品列表按键')
    logging.debug('产品管理-产品列表：' + productListBtn.text)
    productListBtn.click()

    # 等待产品列表加载完成
    sleep(time)

    # 获取产品列表产品名
    proNames = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR,
                                               'tbody tr td:nth-of-type(2)')),
        message='找不到 产品列表中的产品名称')

    # 打开产品 查看功能
    for i in range(len(proNames)):
        if proNames[i].text == proName:
            viewBtn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'tbody tr:nth-of-type(%i) button:nth-of-type(2)' %
                     (i + 1))),
                message='找不到 查看按键')
            logging.debug('产品管理-产品列表：' + viewBtn.text)
            viewBtn.click()
            break

    # 等待列表加载
    sleep(time)

    # 获取所有型号
    mods = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'tbody tr')),
        message='找不到 型号列表')
    for i in range(len(mods)):
        modViewBtn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'tbody tr:nth-of-type(%i) button:nth-of-type(2)' % (i + 1))),
            message='找不到 型号查看按键')
        logging.debug('产品列表-查看：' + modViewBtn.text)
        modViewBtn.click()
        sleep(time)

        # 添加角色
        addRole(wait, driver, '项目-')

        # 返回上一级
        backBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button .el-icon-arrow-left')),
            message='找不到 返回上一级按键')
        logging.debug('产品列表-查看：' + backBtn.text)
        backBtn.click()

        # 等待列表刷新
        sleep(time)


# 新增角色-用户
def addRole(wait, driver, str):
    if str == '产品-':
        # 点击用户列表按钮
        userListBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#tab-1')),
            message='找不到 产品成员按钮')
        logging.debug('产品型号-产品成员：' + userListBtn.text)
        userListBtn.click()

    # 添加角色按钮
    addRoleBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-role-btn')),
        message='不知道 添加角色按钮')
    logging.debug('用户列表-添加角色：' + addRoleBtn.text)

    # 角色列表下拉框
    roleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-rolelist .el-input__inner')),
        message='找不到 角色列表下拉按钮')
    roleListBtn.click()
    sleep(time)

    # 是否还有角色需要添加
    isExsitRole = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '.el-popper[x-placement]')),
        message='找不到 角色下来列表')

    if '暂无任何可添加的角色' not in isExsitRole.get_attribute('innerHTML'):
        # 获取所有角色
        roleList = wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, '.el-popper[x-placement] li')),
            message='找不到 角色列表')

        # 添加角色
        for i in range(len(roleList)):
            if i:
                roleListBtn.click()
                sleep(time)

            role = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.el-popper[x-placement] li')),
                message='找不到 角色列表')
            logging.debug('用户列表-添加角色：' + role.get_attribute('innerText'))
            if role:
                role.click()
                sleep(time)

                addRoleBtn.click()
                sleep(time)
    else:
        roleListBtn.click()
        sleep(time)

    # 已添加角色列表按钮
    roleAddListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-role .el-input__inner')),
        message='找不到 已添加角色列表按钮')
    roleAddListBtn.click()
    sleep(time)

    # 获取所有添加的角色
    roleAddList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-popper[x-placement] li')),
        message='找不到 已添加角色列表')

    # 用户列表下拉按钮
    userRoleListBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.add-user .el-input__inner')),
        message='找不到 用户列表下拉按钮')
    userRoleListBtn.click()
    sleep(time)

    # 获取所有用户
    userRoleList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               '.el-popper[x-placement] li')),
        message='找不到 用户列表')

    # 添加用户按钮
    addUserBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-user-btn')),
        message='找不到 添加用户按钮')

    for i in range(len(roleAddList)):
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
            # 添加用户
            if roleName in userName and str in userName:
                logging.debug('用户列表-添加用户：' + addUserBtn.text + ' ' + userName)
                user.click()
                sleep(time)
                addUserBtn.click()

                # 刷新列表
                sleep(time + 1)
                break


# 添加产品成员
def addUserRole(wait, driver, proName):
    # 添加产品角色
    addProRole(wait, driver, proName)

    # 添加型号角色
    addModRole(wait, driver, proName)


# 产品管理
def productManager(wait):
    # 点击选择产品管理项
    proManagerBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(2) .el-submenu__title'
        )),
        message='找不到产品管理按键')
    logging.debug('产品管理：' + proManagerBtn.text)
    proManagerBtn.click()
    sleep(time)


# 新增产品
def newProduct(wait, driver, user):
    # addProEable:0 不测试，1 测试
    if user['addProEable']:
        # 新增产品：TestProduct_1
        logging.info('新增产品：' + proMod['PRONAME_1'])
        addProduct(wait, proMod['PRONAME_1'], proMod['PRODES_1'])
        logging.info('新增产品：' + proMod['PRONAME_1'] + ' 成功')

        # 新增产品：TestProduct_2
        logging.info('新增产品：' + proMod['PRONAME_2'])
        addProduct(wait, proMod['PRONAME_2'], proMod['PRODES_2'])
        logging.info('新增产品：' + proMod['PRONAME_2'] + ' 成功')


# 产品列表
def productList(wait, driver, user):
    if user['proListEnable']:
        # TestProduct_1 添加型号：TestModule_1 TestModule_2
        logging.info(proMod['PRONAME_1'] + '添加型号：' + proMod['MODNAME_1'])
        newModule(wait, proMod['PRONAME_1'], proMod['MODNAME_1'],
                  proMod['MODDES_1'])
        logging.info(proMod['PRONAME_1'] + '添加型号：' + proMod['MODNAME_1'] +
                     ' 成功')

        logging.info(proMod['PRONAME_1'] + '添加型号：' + proMod['MODNAME_2'])
        newModule(wait, proMod['PRONAME_1'], proMod['MODNAME_2'],
                  proMod['MODDES_2'])
        logging.info(proMod['PRONAME_1'] + '添加型号：' + proMod['MODNAME_2'] +
                     ' 成功')

        # TestProduct_2 添加型号：TestModule_1 TestModule_2
        logging.info(proMod['PRONAME_2'] + '添加型号：' + proMod['MODNAME_1'])
        newModule(wait, proMod['PRONAME_2'], proMod['MODNAME_1'],
                  proMod['MODDES_1'])
        logging.info(proMod['PRONAME_2'] + '添加型号：' + proMod['MODNAME_1'] +
                     ' 成功')

        logging.info(proMod['PRONAME_2'] + '添加型号：' + proMod['MODNAME_2'])
        newModule(wait, proMod['PRONAME_2'], proMod['MODNAME_2'],
                  proMod['MODDES_2'])
        logging.info(proMod['PRONAME_2'] + '添加型号：' + proMod['MODNAME_2'] +
                     ' 成功')

        # TestProduct_1 添加用户角色
        logging.info(proMod['PRONAME_1'] + '添加用户角色')
        addUserRole(wait, driver, proMod['PRONAME_1'])
        logging.info(proMod['PRONAME_1'] + '添加用户角色成功')

        # TestProduct_2 添加用户角色
        logging.info(proMod['PRONAME_2'] + '添加用户角色')
        addUserRole(wait, driver, proMod['PRONAME_2'])
        logging.info(proMod['PRONAME_2'] + '添加用户角色成功')


# 软件管理
def softManager(wait):
    # 点击软件管理
    sofManagerBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(3) .el-submenu__title'
        )),
        message='找不到 软件管理')
    logging.debug('软件管理：' + sofManagerBtn.text)
    sofManagerBtn.click()


# 软件管理-上传软件
def addSoftware(wait, user):
    if user['upSoftEnable']:
        logging.info('上传软件')
        # upSoftware(wait, user, proMod['PRONAME_1'], proMod['MODNAME_1'])
        # upSoftware(wait, user, proMod['PRONAME_1'], proMod['MODNAME_2'])
        # upSoftware(wait, user, proMod['PRONAME_2'], proMod['MODNAME_1'])
        # upSoftware(wait, user, proMod['PRONAME_2'], proMod['MODNAME_2'])
        upSoftware(wait, user, proMod['PRONAME_1'], None)
        logging.info('上传软件成功')


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
    if product:
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
    if module:
        modLisBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'div.item:nth-of-type(2) .el-input')))
        modLisBtn.click()
        sleep(time)

        modList = wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'div[x-placement="bottom-start"] li')))
        for mod in modList:
            modName = mod.get_attribute('innerText')
            if modName == module:
                logging.debug('上传软件-选择型号：' + modName)
                mod.click()
                sleep(time)
                break
            if mod == modList[len(modList) - 1]:
                raise Exception(module + ' 不存在')

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
    # 软件列表
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


# 订单管理
def orderManager(wait):
    # 点击软件管理
    orderManagerBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(4) .el-submenu__title'
        )),
        message='找不到 订单管理')
    logging.debug('订单管理' + orderManagerBtn.text)
    orderManagerBtn.click()


# 订单管理-创建订单
def newOrder(wait, user):
    if user['createOrderEnable']:
        # 创建订单
        logging.info('创建订单')
        createOrder(wait, proMod['PRONAME_2'], proMod['MODNAME_2'],
                    config.ORDER_8, config.USER_PRO_PE['NAME'])
        createOrder(wait, proMod['PRONAME_2'], proMod['MODNAME_2'],
                    config.ORDER_7, config.USER_MOD_PE['NAME'])
        createOrder(wait, proMod['PRONAME_2'], proMod['MODNAME_1'],
                    config.ORDER_6, config.USER_PRO_PE['NAME'])
        createOrder(wait, proMod['PRONAME_2'], proMod['MODNAME_1'],
                    config.ORDER_5, config.USER_MOD_PE['NAME'])
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_2'],
                    config.ORDER_4, config.USER_PRO_PE['NAME'])
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_2'],
                    config.ORDER_3, config.USER_MOD_PE['NAME'])
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_1'],
                    config.ORDER_2, config.USER_PRO_PE['NAME'])
        createOrder(wait, proMod['PRONAME_1'], proMod['MODNAME_1'],
                    config.ORDER_1, config.USER_MOD_PE['NAME'])
        logging.info('创建订单成功')


# 创建订单
def createOrder(wait, product, module, order, pe):
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
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-menu:nth-of-type(1) .el-submenu:nth-of-type(4) .el-menu-item:nth-of-type(1)'
        )),
        message='找不到 创建订单项')
    logging.debug('订单管理-创建订单：' + createOrderBtn.text)
    createOrderBtn.click()
    sleep(time)

    # 选择产品
    proLisBtn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.order-item:nth-of-type(1) .el-input__inner')),
        message='找不到 产品列表下拉按键')
    proLisBtn.click()
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
    modLisBtn.click()
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
    factoryName.click()
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
    applicantListBtn.click()
    sleep(time)

    applicantList = wait.until(
        EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                               'div[x-placement] li')),
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
    createBtn.click()
    sleep(time)

    upOK = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.page-finish'),
                                         '成功创建'),
        message='创建订单失败')

    if upOK is False:
        raise Exception('创建订单失败')

    sleep(time)


# 关联软件
def relatedMptool(wait):
    # 添加关联
    addSoftBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.addsoft')),
        message='找不到 增加关联按键')
    logging.debug('关联量产工具：' + addSoftBtn.text)
    addSoftBtn.click()
    sleep(time)

    # 软件类型
    inputSoftMod = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '.el-dialog__body .relate-item:nth-of-type(1) input')),
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
             '.el-dialog__body .relate-item:nth-of-type(2) input')),
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
            raise Exception('softFile.txt(1.00) 不存在')

    # 确定
    confirmBtn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '.el-dialog__body .relate-item:nth-of-type(3) button:nth-of-type(2)'
        )),
        message='找不到 确定关联按键')
    logging.debug('关联量产工具-关联软件：' + confirmBtn.text)
    confirmBtn.click()
    sleep(time)

    # 确定关联是否成功
    if getTeamInfo(wait, 1, 1) != software['version']:
        raise Exception('量产工具版本错误')
    if getTeamInfo(wait, 1, 2) != software['name']:
        raise Exception('量产工具软件名错误')
    if getTeamInfo(wait, 1, 3) != software['type']:
        raise Exception('量产工具软件类型错误')
    if getTeamInfo(wait, 1, 4) != software['des']:
        raise Exception('量产工具介绍错误')

    sleep(time)


# 订单关联量产工具
def addOrderTool(user, wait, driver):
    # 关联前两个订单
    for i in range(2):
        relatedBtn = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'tbody .el-table__row:nth-of-type(%s) td:nth-of-type(8) span:nth-child(3)'
                % (i + 1))),
            message='找不到 关联软件按键')
        logging.debug('订单管理-量产工具：' + relatedBtn.text)
        relatedBtn.click()
        sleep(time)

        # 关联软件
        relatedMptool(wait)

        # 返回上一级
        backBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.back')),
            message='找不到 返回上一级按键')
        logging.debug('关联量产工具：' + backBtn.text)
        goTop(driver)
        backBtn.click()
        sleep(time)


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
        addOrderTool(user, wait, driver)
        logging.info('订单关联量产工具成功')


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
    sleep(time)


# 添加样品
def addSampe(wait, driver, user):
    if user['createSampleEnable']:
        # 添加样品
        newSampe(wait, user, config.SAMPLE)
        # 添加记录
        newRecord(wait)


# 添加不良品样品
def addNgSampe(wait, driver, user):
    if user['createSampleEnable']:
        # 添加样品
        newNgSampe(wait, user, config.SAMPLE)
        # 添加记录
        newRecord(wait)


# 新增样品
def newSampe(wait, user, sample):
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

    addSampleInfo(wait, user, sample)


# 新增不良品样品
def newNgSampe(wait, user, sample):
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

    addSampleInfo(wait, user, sample)


# 添加样品信息
def addSampleInfo(wait, user, sample):
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
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(4) input')),
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

    # 不良描述
    ngInput = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(19) input')),
        message='找不到 不良描述输入栏')
    ngInput.send_keys(sample['NG'])

    # 备注
    noteInput = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.add-info-form>div:nth-child(20) input')),
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

    # 不良描述
    ngInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(11) input')),
        message='找不到 不良描述输入栏')
    ngInput.send_keys('不良描述')

    # 结论
    inconInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(12) input')),
        message='找不到 结论述输入栏')
    inconInput.send_keys('结论')

    # 结论
    inconInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(12) input')),
        message='找不到 结论述输入栏')
    inconInput.send_keys('结论')

    # 备注
    noteInput = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'div:nth-child(13) input')),
        message='找不到 备注述输入栏')
    noteInput.send_keys('备注')

    # 添加
    addBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.add')),
        message='找不到 添加按键')
    addBtn.click()
    sleep(time)


def main(driver, user=config.USER_ADMIN):
    # user :USER_ADMIN
    try:
        startTime = datetime.now()
        # 全屏
        # driver.set_window_size(1920, 1080)
        driver.maximize_window()
        driver.get(config.URL)
        # 等待时间
        wait = WebDriverWait(driver, 10)

        logging.info('管理员功能测试')

        logging.info('用户登陆')
        login(user, wait)

        logging.info('管理员管理-team管理')
        teamManage(user, wait, driver)

        logging.debug('管理员管理')
        adminManager(wait)

        logging.info('产品线和项目管理')
        productManager(wait)

        logging.info('产品线和项目管理-新增产品')
        newProduct(wait, driver, user)

        logging.info('产品线和项目管理-产品列表')
        productList(wait, driver, user)

        logging.debug('产品线和项目管理')
        productManager(wait)

        logging.info('软件管理')
        softManager(wait)

        logging.info('软件管理-上传软件')
        addSoftware(wait, user)

        logging.debug('软件管理')
        softManager(wait)

        logging.info('订单管理')
        orderManager(wait)

        logging.info('订单管理-创建订单')
        newOrder(wait, user)

        # 订单管理-关联量产工具
        logging.info('订单管理-关联量产工具')
        orderTools(user, wait, driver)

        logging.debug('订单管理')
        orderManager(wait)

        logging.info('样品管理')
        sampleManage(wait)

        logging.info('样品管理-添加样品')
        addSampe(wait, driver, user)

        logging.info('样品管理-添加不良品样品')
        addNgSampe(wait, driver, user)

        logging.debug('样品管理')
        sampleManage(wait)

        # 测试时间
        allTime = datetime.now() - startTime
        logging.info('PASS ' + '测试时间：' + str(allTime))

        driver.quit()

        return True

    except Exception as E:
        logging.info(E)

        # 测试时间
        allTime = datetime.now() - startTime
        logging.info('FAIL ' + '测试时间：' + str(allTime))

        driver.quit()
        return False


if __name__ == '__main__':
    driver = webdriver.Chrome()
    # driver = webdriver.Ie()
    # driver = webdriver.Firefox()
    main(driver)
