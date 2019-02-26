import unittest
from createUser import createUser
from selenium import webdriver
import config
import test_admin
import test_pro_pm
import test_mod_pm
import test_pro_tl
import test_mod_tl
import test_pro_te
import test_mod_te
import test_pro_pmc
import test_mod_pmc
import test_pro_pe
import test_mod_pe
import test_pro_rd
import test_mod_rd
import test_pro_pj
import test_mod_pj


class testCases(unittest.TestCase):
    # 测试前配置工作
    def setUp(self):
        # 谷歌浏览器
        if config.webBrower == 0:
            self.driver = webdriver.Chrome()

        # 火狐浏览器
        if config.webBrower == 1:
            profile = webdriver.FirefoxProfile()
            # 设置自定义下载路径
            profile.set_preference('browser.download.dir',
                                   '%s' % (config.filePath))
            # 设置Firefox的默认 下载 文件夹。0是桌面；1是“我的下载”；2是自定义
            profile.set_preference('browser.download.folderList', 2)
            # 设置在开始下载时是否显示下载管理器 True ：显示，False：不显示
            profile.set_preference('browser.download.manager.showWhenStarting',
                                   False)
            # 设置不询问的文件类型
            profile.set_preference(
                'browser.helperApps.neverAsk.saveToDisk',
                'application/octet-stream, application/vnd.ms-excel, text/csv, application/zip'
            )
            self.driver = webdriver.Firefox(firefox_profile=profile)

        # IE浏览器
        if config.webBrower == 2:
            self.driver = webdriver.Ie()

    # 创建产品-产品经理
    def test_newUserProPM(self):
        resu = createUser(self.driver, config.USER_PRO_PM)
        self.assertEqual(resu, True)

    # 创建型号-产品经理
    def test_newUserModPM(self):
        resu = createUser(self.driver, config.USER_MOD_PM)
        self.assertEqual(resu, True)

    # 创建产品-研发工程师
    def test_newUserProRD(self):
        resu = createUser(self.driver, config.USER_PRO_RD)
        self.assertEqual(resu, True)

    # 创建型号-研发工程师
    def test_newUserModRD(self):
        resu = createUser(self.driver, config.USER_MOD_RD)
        self.assertEqual(resu, True)

    # 创建产品-测试主管
    def test_newUserProTL(self):
        resu = createUser(self.driver, config.USER_PRO_TL)
        self.assertEqual(resu, True)

    # 创建型号-测试主管
    def test_newUserModTL(self):
        resu = createUser(self.driver, config.USER_MOD_TL)
        self.assertEqual(resu, True)

    # 创建产品-测试工程师
    def test_newUserProTE(self):
        resu = createUser(self.driver, config.USER_PRO_TE)
        self.assertEqual(resu, True)

    # 创建型号-测试工程师
    def test_newUserModTE(self):
        resu = createUser(self.driver, config.USER_MOD_TE)
        self.assertEqual(resu, True)

    # 创建产品-PMC
    def test_newUserProPMC(self):
        resu = createUser(self.driver, config.USER_PRO_PMC)
        self.assertEqual(resu, True)

    # 创建型号-PMC
    def test_newUserModPMC(self):
        resu = createUser(self.driver, config.USER_MOD_PMC)
        self.assertEqual(resu, True)

    # 创建产品-产线工程师
    def test_newUserProPE(self):
        resu = createUser(self.driver, config.USER_PRO_PE)
        self.assertEqual(resu, True)

    # 创建型号-产线工程师
    def test_newUserModPE(self):
        resu = createUser(self.driver, config.USER_MOD_PE)
        self.assertEqual(resu, True)

    # 创建型号-产线工程师
    def test_newUserProPJ(self):
        resu = createUser(self.driver, config.USER_PRO_PJ)
        self.assertEqual(resu, True)

    # 创建型号-产线工程师
    def test_newUserModPJ(self):
        resu = createUser(self.driver, config.USER_MOD_PJ)
        self.assertEqual(resu, True)

    # 管理员配置测试环境成员
    def test_admin(self):
        resu = test_admin.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-产品经理测试
    def test_pro_pm(self):
        resu = test_pro_pm.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-产品经理测试
    def test_mod_pm(self):
        resu = test_mod_pm.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-研发工程师测试
    def test_pro_rd(self):
        resu = test_pro_rd.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-研发工程师测试
    def test_mod_rd(self):
        resu = test_mod_rd.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-测试主管测试
    def test_pro_tl(self):
        resu = test_pro_tl.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-测试主管测试
    def test_mod_tl(self):
        resu = test_mod_tl.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-测试工程师
    def test_pro_te(self):
        resu = test_pro_te.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-测试工程师
    def test_mod_te(self):
        resu = test_mod_te.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-PMC
    def test_pro_pmc(self):
        resu = test_pro_pmc.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-PMC
    def test_mod_pmc(self):
        resu = test_mod_pmc.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-产线工程师
    def test_pro_pe(self):
        resu = test_pro_pe.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-产线工程师
    def test_mod_pe(self):
        resu = test_mod_pe.main(self.driver)
        self.assertEqual(resu, True)

    # 产品-项目工程师
    def test_pro_pj(self):
        resu = test_pro_pj.main(self.driver)
        self.assertEqual(resu, True)

    # 型号-项目工程师
    def test_mod_pj(self):
        resu = test_mod_pj.main(self.driver)
        self.assertEqual(resu, True)


if __name__ == '__main__':
    # 创建用户
    suite = unittest.TestSuite()
    newUsers = [
        testCases('test_newUserProPM'),
        testCases('test_newUserModPM'),
        testCases('test_newUserProRD'),
        testCases('test_newUserModRD'),
        # testCases('test_newUserProTL'),
        # testCases('test_newUserModTL'),
        testCases('test_newUserProTE'),
        testCases('test_newUserModTE'),
        testCases('test_newUserProPMC'),
        testCases('test_newUserModPMC'),
        testCases('test_newUserProPE'),
        testCases('test_newUserModPE'),
        testCases('test_newUserProPJ'),
        testCases('test_newUserModPJ'),
    ]

    suite.addTests(newUsers)
    # suite.addTest(testCases('test_admin'))
    # suite.addTest(testCases('test_pro_pm'))
    # suite.addTest(testCases('test_mod_pm'))
    # suite.addTest(testCases('test_pro_rd'))
    # suite.addTest(testCases('test_mod_rd'))
    # suite.addTest(testCases('test_pro_tl'))
    # suite.addTest(testCases('test_mod_tl'))
    # suite.addTest(testCases('test_pro_te'))
    # suite.addTest(testCases('test_mod_te'))
    # suite.addTest(testCases('test_pro_pmc'))
    # suite.addTest(testCases('test_mod_pmc'))
    # suite.addTest(testCases('test_pro_pe'))
    # suite.addTest(testCases('test_mod_pe'))
    # suite.addTest(testCases('test_pro_pj'))
    # suite.addTest(testCases('test_mod_pj'))
    runer = unittest.TextTestRunner(verbosity=2)
    runer.run(suite)
