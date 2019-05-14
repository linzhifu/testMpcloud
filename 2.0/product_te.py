# 产品-测试工程师测试脚本
import logging
import os
import shutil
import get_video
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import config
import mpcloud


# 主程序
def main(driver, user=config.USER_PRO_TE):
    # user :USER_PRO_PM
    startTime = datetime.now()

    # 测试目录
    logData = datetime.now().strftime('%Y-%m-%d')
    LOGDIR = logData + '/' + user['NAME']

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
    result = {'errcode': 0, 'errmsg': 'ok'}

    # LOG文件名
    logName = datetime.now().strftime('%Y%m%d%H%M%S')

    # 保存路径
    savePath = LOGDIR + '/' + logName

    # 指定logger输出格式
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')

    # DEBUG输出保存测试LOG
    file_handler = logging.FileHandler('test.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    # 录像开始
    Save = get_video.Job()
    Save.start()

    try:
        # 设置等待时间
        wait = WebDriverWait(driver, 10)

        # 最大化
        driver.maximize_window()

        # 前往测试前端网站
        logging.info('Go to ' + config.URL)
        driver.get(config.URL)

        # 登录
        logging.info('登录账户：' + user['NAME'])
        mpcloud.login(wait, email=user['EMAIL'], password=user['LOGIN'])

        # 个人资料
        logging.info('个人中心-我的资料')
        mpcloud.userInfo(driver, wait, user)

        # 产品管理
        logging.info('产品线和项目管理')
        mpcloud.productManager(driver, wait, user)

        # 产品管理-产品线列表
        logging.info('产品管理-产品线列表')
        mpcloud.proList(driver, wait, user)

        # 软件管理，请安排人工测试

        # # 订单管理
        logging.info('订单管理')
        mpcloud.orderManager(driver, wait, user)

        # 订单管理-订单列表
        logging.info('订单管理-订单列表')
        mpcloud.orderList(driver, wait, user)

        # 样品管理
        logging.info('样品管理')
        mpcloud.sampleManage(driver, wait, user)

        # 样品管理-添加样品
        logging.info('样品管理-添加样品')
        mpcloud.addSampe(driver, wait, user)

        # 样品管理-添加不良品样品
        logging.info('样品管理-添加不良品样品')
        mpcloud.addNgSampe(driver, wait, user)

        # 测试结果PASS
        resu = 'pass'

    except Exception as E:
        logging.info(E)

        # 测试结果FAIL
        resu = 'fail'
        result['errcode'] = 1
        result['errmsg'] = str(E)

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

        return result


if __name__ == '__main__':
    main(driver=webdriver.Chrome(), user=config.USER_PRO_TE)
