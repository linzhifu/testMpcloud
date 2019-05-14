# 超级管理员
# mpsystem@longsys.com
# 2A12vx5O
import datetime
# 测试用浏览器设置 0：谷歌 ，1：火狐 ，2：IE
webBrower = 1

# 测试网站
URL = 'https://mpstest.longsys.com'
# URL = 'https://mps.longsys.com'

# 测试文件下载路径
filePath = r'C:\Users\Administrator\Downloads'

# 操作等待时间
timeout = 0.5

# 是否隐藏浏览器界面 1:隐藏 ，0：显示
hide = 0

# 是否隐藏DEBUG日志 1:隐藏 ，0：显示
debug = 1

# 订单授权剩余天数
authTime = str((datetime.datetime(2019, 11, 1) - datetime.datetime.now()).days)

# 测试产品-型号
proMod = {
    # 产品
    'PRONAME_1': 'TestProduct_1',
    'PRODES_1': 'TestProduct_1 only for test',
    'PRONAME_2': 'TestProduct_2',
    'PRODES_2': 'TestProduct_2 only for test',
    # 型号
    'MODNAME_1': 'TestModule_1',
    'MODDES_1': 'TestModule_1 only for test',
    'MODNAME_2': 'TestModule_2',
    'MODDES_2': 'TestModule_2 only for test',
}
# 测试软件
software = {
    'type': 'mptool',
    'name': 'softFile.zip',
    'version': 'V0.0.01',
    'testFile': r'C:\software\softFile.zip',
    'testReport': r'C:\software\testFile.txt',
    'des': 'The sofeware exists only for test',
    'soft': 'softFile.zip(V0.0.01)',
}

# 测试TEAM
testTeam = {
    'NAME': 'TestTeam',
    'DES': 'Only for auto test',
}

# 测试订单1
ORDER_1 = {
    'NUM': '20180001',
    'OFFLINE': '2000',
    'ONLINE': '1000',
    'FACTORY': 'DLT',
    'TIME': '20191101',
    'DES': 'only for test1',
}
# 测试订单2
ORDER_2 = {
    'NUM': '20180002',
    'OFFLINE': '1000',
    'ONLINE': '2000',
    'FACTORY': 'OSE',
    'TIME': '20191101',
    'DES': 'only for test2',
}

# 测试订单3
ORDER_3 = {
    'NUM': '20180003',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'Walton',
    'TIME': '20191101',
    'DES': 'only for test3',
}

# 测试订单4
ORDER_4 = {
    'NUM': '20180004',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'ZKT',
    'TIME': '20191101',
    'DES': 'only for test4',
}

# 测试订单5
ORDER_5 = {
    'NUM': '20180005',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'DLT',
    'TIME': '20191101',
    'DES': 'only for test5',
}

# 测试订单4
ORDER_6 = {
    'NUM': '20180006',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'OSE',
    'TIME': '20191101',
    'DES': 'only for test6',
}

# 测试订单7
ORDER_7 = {
    'NUM': '20180007',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'Walton',
    'TIME': '20191101',
    'DES': 'only for test7',
}

# 测试订单8
ORDER_8 = {
    'NUM': '20180008',
    'OFFLINE': '3000',
    'ONLINE': '3000',
    'FACTORY': 'ZKT',
    'TIME': '20191101',
    'DES': 'only for test8',
}

# 测试样品
SAMPLE = {
    'PRO': proMod['PRONAME_1'],
    'MOD': proMod['MODNAME_1'],
    'NUM': '20181116',
    # 'DETAIL': 'C:\\software\\sample_detail.json',
    # 'BRIEF': 'C:\\software\\sample_brief.json',
    'TYPE': 'LPDDR3',
    'ORDER': ORDER_1['NUM'],
    'CLIENT': 'TESTER',
    'FACTORY': ORDER_1['FACTORY'],
    'CODE': '12345678',
    'RES': 'Micron Z11M',
    'WAFER': '2P',
    'PARTNO': 'TEST123',
    'SIZE': '8Gb',
    'BITWID': '4bit',
    'DIE': 'x4',
    'PACKAGE': 'FBGA200',
    'SUB': '1120009721',
    'AREA': '10*10',
    'PROCESS': 'TEST',
    'TIME': '20191224',
    'NG': 'UNKNOWN',
    'NOTE': 'ONLY FOR TEST',
}

# 管理员
USER_ADMIN = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'NAME': 'Administrator',
    'EMAIL': 'linzhifu221@163.com',
    'LOGIN': 'Lin5535960',

    # TEAM 管理测 teamEable:0 不测试，1 测试
    'teamEable': 0,

    # 新增产品 addProEable:0 不测试，1 测试
    'addProEable': 0,

    # 产品列表(添加型号、角色) proListEable:0 不测试，1 测试
    'proListEnable': 0,

    # 上传软件 upSoftEnable:0 不测试，1 测试
    'upSoftEnable': 1,

    # 创建订单 createOrderEnable:0 不测试，1 测试
    'createOrderEnable': 0,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable': 0,
}

# 产品-产品经理
USER_PRO_PM = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': '18129832245@163.com',
    'PSW': 'Lin5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-产品经理',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-产品经理', proMod['PRONAME_2'] + '-产品经理'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-产品经理',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试添加产品型号 addModEnable:0 不测试，1测试
    'addModEnable': 1,
    'modName': 'TempModule',
    'modDes': 'TempModule only for test',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 1,
    'tempMod': 'TempTestMod',
    'tempModDes': 'TempTestMod test',
    'modifyPro': 'modifyTestPro',
    'modifyProDes': 'modifyTestPro test',
    'modifyMod': 'modifyTestMod',
    'modifyModDes': 'modifyTestMod test',

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 1
}

# 型号-产品经理
USER_MOD_PM = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu220@163.com',
    'PSW':
    'Lin5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-产品经理',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-产品经理',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-产品经理',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-产品经理',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-产品经理',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-产品型号经理',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,
    'modifyMod':
    'modifyTestMod',
    'modifyModDes':
    'modifyTestMod test',

    # 关联量产工具 orderToolEnable:0 不测试，1测试
    'orderToolEnable':
    1,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,
}

# 产品-研发工程师
USER_PRO_RD = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': 'linzhifu225@163.com',
    'PSW': 'Lin5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-研发工程师',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-研发工程师', proMod['PRONAME_2'] + '-研发工程师'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 0,
    'userName': 'TestProduct-研发工程师',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 0,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 0,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable': 1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable': 0,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 0,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable': 0,
}

# 型号-研发工程师
USER_MOD_RD = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu226@163.com',
    'PSW':
    'Lin5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-研发工程师',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-研发工程师',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-研发工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-研发工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-研发工程师',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-研发工程师',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable':
    1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable':
    0,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable':
    1,
}

# 产品-测试主管
USER_PRO_TL = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': '17388730192@163.com',
    'PSW': 'Lin241507',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-测试主管',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-测试主管', proMod['PRONAME_2'] + '-测试主管'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-测试主管',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 1,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable': 1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable': 1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable': 1,
}

# 型号-测试主管
USER_MOD_TL = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu221@163.com',
    'PSW':
    'Lin5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-测试主管',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-测试主管',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-测试主管',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-测试主管',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-测试主管',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-产品型号测试主管',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable':
    1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable':
    1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable':
    1,
}

# 产品-测试工程师
USER_PRO_TE = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': 'linzhifu222@163.com',
    'PSW': 'Lin5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-测试工程师',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-测试工程师', proMod['PRONAME_2'] + '-测试工程师'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-产品测试工程师',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 1,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable': 1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable': 0,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable': 1,
}

# 型号-测试工程师
USER_MOD_TE = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu120@163.com',
    'PSW':
    '5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-测试工程师',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-测试工程师',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-测试工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-测试工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-测试工程师',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-测试工程师',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,

    # 测试上传软件 upSoftEnable:0 不测试，1测试
    'upSoftEnable':
    1,

    # 测试软件列表 softListEnable:0 不测试，1测试
    'softListEnable':
    0,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable':
    1,
}

# 产品-PMC
USER_PRO_PMC = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': 'linzhifu223@163.com',
    'PSW': 'Lin5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-pmc',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-pmc', proMod['PRONAME_2'] + '-pmc'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-产品PMC',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 1,

    # 创建订单 createOrderEnable:0 不测试，1测试
    'createOrderEnable': 1,
    'tempOrder': {
        'NUM': '20181111',
        'OFFLINE': '1000',
        'ONLINE': '2000',
        'FACTORY': 'OSE',
        'TIME': '20191001',
        'DES': 'only for test temOrder',
    },

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 1,
}

# 型号-PMC
USER_MOD_PMC = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu121@163.com',
    'PSW':
    '5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-pmc',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-pmc',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-pmc',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-pmc',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-pmc',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-PMC',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,

    # 创建订单 createOrderEnable:0 不测试，1测试
    'createOrderEnable':
    1,
    'tempOrder': {
        'NUM': '20181111',
        'OFFLINE': '1000',
        'ONLINE': '2000',
        'FACTORY': 'DLT',
        'TIME': '20191101',
        'DES': 'only for test temOrder',
    },

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,
}

# 产品-产线工程师
USER_PRO_PE = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': 'linzhifu122@163.com',
    'PSW': '5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-产线工程师',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-产线工程师', proMod['PRONAME_2'] + '-产线工程师'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-产线工程师',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 1,
}

# 型号-产线工程师
USER_MOD_PE = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu224@163.com',
    'PSW':
    'Lin5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-产线工程师',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-产线工程师',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-产线工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-产线工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-产线工程师',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-产线工程师',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,
}

# 产品-项目工程师
USER_PRO_PJ = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL': 'linzhifu227@163.com',
    'PSW': 'Lin5535960',
    'SERVER': 'pop.163.com',
    'NAME': 'TEST 产品-项目工程师',
    'LOGIN': '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [proMod['PRONAME_1'] + '-项目工程师', proMod['PRONAME_2'] + '-项目工程师'],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable': 1,
    'userName': 'TestProduct-项目工程师',
    'qq': '254082684',
    'im': 'Test',
    'phone': '18129832245',
    'passWord': '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable': 1,
    'teamName': 'Temp test team',
    'teamDes': 'Temp test add team',
    'modifyTeamName': 'Temp Team',
    'modifyTeamDes': 'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable': 1,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable': 1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable': 1,
}
# 型号-项目工程师
USER_MOD_PJ = {
    # 基础默认设置(用于第一次测试创建用户,一般不做修改)
    'EMAIL':
    'linzhifu228@163.com',
    'PSW':
    'Lin5535960',
    'SERVER':
    'pop.163.com',
    'NAME':
    'TEST 型号-项目工程师',
    'LOGIN':
    '123',
    'TEAM': [testTeam['NAME']],
    'ROLE': [
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_1'] + '-项目工程师',
        proMod['PRONAME_1'] + '-' + proMod['MODNAME_2'] + '-项目工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_1'] + '-项目工程师',
        proMod['PRONAME_2'] + '-' + proMod['MODNAME_2'] + '-项目工程师',
    ],

    # 测试修改资料，包括个人资料和密码 updateUserInfoEnable:0 不测试，1 测试
    'updateUserInfoEnable':
    1,
    'userName':
    'TestProduct-项目工程师',
    'qq':
    '254082684',
    'im':
    'Test',
    'phone':
    '18129832245',
    'passWord':
    '123456',

    # 测试team功能 teamEnable:0 不测试，1测试
    'teamEnable':
    1,
    'teamName':
    'Temp test team',
    'teamDes':
    'Temp test add team',
    'modifyTeamName':
    'Temp Team',
    'modifyTeamDes':
    'Temp test modify team',

    # 测试产品列表功能 proLisEnable:0 不测试，1测试
    'proLisEnable':
    1,

    # 订单列表 orderListEnable:0 不测试，1测试
    'orderListEnable':
    1,

    # 添加样品 createSampleEnable:0 不测试，1 测试
    'createSampleEnable':
    1
}

# 测试成员
teamUsers = (
    USER_ADMIN['NAME'],
    USER_PRO_PM['NAME'],
    USER_PRO_RD['NAME'],
    USER_MOD_RD['NAME'],
    USER_MOD_PM['NAME'],
    # USER_PRO_TL['NAME'],
    # USER_MOD_TL['NAME'],
    USER_PRO_TE['NAME'],
    USER_MOD_TE['NAME'],
    USER_PRO_PMC['NAME'],
    USER_MOD_PMC['NAME'],
    USER_PRO_PE['NAME'],
    USER_MOD_PE['NAME'],
    USER_PRO_PJ['NAME'],
    USER_MOD_PJ['NAME'],
)
