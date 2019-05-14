import unittest
from selenium import webdriver
import config
import product_pm
import product_pmc
import product_rd
import product_te
import product_pe
import product_pj
import model_pm
import model_pmc
import model_rd
import model_te
import model_pe
import model_pj


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

    # 产品-产品经理测试
    def test_pro_pm(self):
        resu = product_pm.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-产品经理测试
    def test_mod_pm(self):
        resu = model_pm.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 产品-研发工程师测试
    def test_pro_rd(self):
        resu = product_rd.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-研发工程师测试
    def test_mod_rd(self):
        resu = model_rd.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 产品-测试工程师
    def test_pro_te(self):
        resu = product_te.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-测试工程师
    def test_mod_te(self):
        resu = model_te.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 产品-PMC
    def test_pro_pmc(self):
        resu = product_pmc.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-PMC
    def test_mod_pmc(self):
        resu = model_pmc.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 产品-产线工程师
    def test_pro_pe(self):
        resu = product_pe.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-产线工程师
    def test_mod_pe(self):
        resu = model_pe.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 产品-项目工程师
    def test_pro_pj(self):
        resu = product_pj.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')

    # 型号-项目工程师
    def test_mod_pj(self):
        resu = model_pj.main(self.driver)
        self.assertEqual(resu['errmsg'], 'ok')


if __name__ == '__main__':
    # 创建用户
    suite = unittest.TestSuite()
    suite.addTest(testCases('test_pro_pm'))
    suite.addTest(testCases('test_mod_pm'))
    suite.addTest(testCases('test_pro_rd'))
    suite.addTest(testCases('test_mod_rd'))
    suite.addTest(testCases('test_pro_te'))
    suite.addTest(testCases('test_mod_te'))
    suite.addTest(testCases('test_pro_pmc'))
    suite.addTest(testCases('test_mod_pmc'))
    suite.addTest(testCases('test_pro_pe'))
    suite.addTest(testCases('test_mod_pe'))
    suite.addTest(testCases('test_pro_pj'))
    suite.addTest(testCases('test_mod_pj'))
    runer = unittest.TextTestRunner(verbosity=2)
    runer.run(suite)
