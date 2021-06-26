from time import sleep

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_cookies():
    """获取cookies"""
    option = Options()
    option.debugger_address = "localhost:9222"
    driver = webdriver.Chrome(options=option)
    driver.get("https://work.weixin.qq.com/wework_admin/frame")
    expect = expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="menu_index"]/span'))
    WebDriverWait(driver, 30).until(expect)   # 手动扫码登录，获取cookies
    cookies = driver.get_cookies()
    # 将cookies写入文件
    with open("./data/cookies.yaml", "w", encoding="utf-8") as f:
        yaml.dump(cookies, f)


def get_name():
    """获取被测数据姓名"""
    with open("./data/test_data.yaml", encoding="utf-8") as f:
        username = yaml.safe_load(f)
    return username


def init_data():
    """初始化通讯录列表"""
    username = get_name()
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://work.weixin.qq.com/wework_admin/frame")  # 进入登录页
    with open("data/cookies.yaml", encoding="utf-8") as f:  # 获取cookies
        cookies = yaml.safe_load(f)
    for cookie in cookies:  # 添加cookies
        driver.add_cookie(cookie)
    driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")  # 进入通讯录页
    #  获取通讯录姓名元素
    elements = driver.find_elements_by_xpath('//*[@id="member_list"]//td[2]/span')
    sleep(1)
    # 判断用例要添加的姓名是否存在，如果存在就删除
    for name in username:
        for element in elements:
            if name in element.text:
                element.click()
                sleep(1)
                driver.find_element_by_link_text("删除").click()
                sleep(1)
                driver.find_element_by_xpath('//*[@id="__dialog__MNDialog__"]/div/div[3]/a[1]').click()
    driver.quit()


if __name__ == '__main__':
    get_cookies()
    # get_name()
