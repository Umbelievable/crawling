import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('/Users/10000say/Downloads/dzbz/chromedriver')
url="https://cr.shopping.naver.com/adcr.nhn?x=jt6jaB%2BMjwOAxRwDk7C4OP%2F%2F%2Fw%3D%3Ds77KkzJiYB0AORMNBqpHJMMpeZRtc7nBw%2FiHJsfCONRnlwyos%2F4%2FzaQi%2BfdOPz6FL1aUrYQHKjqO36Lo37p713lVd6Z%2BmZ5fvTALbBBPmfKLR71%2BG1mg7pxhejX%2BnHQgT0q24CRHbS4hHKL4hMaFYGTi6E9Rl40qHdmY%2FDvMQxYCegbXs50ssX5z59A0RDbypfdx90CtIdY7jMsoj9CXM4M2qpJUNTIl9hFyLyRI0%2Fw8LnNmhUU%2B1aSJziYEnyOQY14Lu0j%2BeUrtKMqx1CRLRazIXaK478a%2F9iyg3qF0NUeNVXemfpmeX70wC2wQT5nyi5pxiwDZPU40LYzhHX%2FcRv2AC4TbvGOWeLNBGBTZi%2Fqtw%2B5SDScJrKSE0dgkIPwdlB6EtWSBecTXTcuoLDN%2Byjoy1TgZpajRSJ9IRaQg5SdIQd0YSbnEMzGlvFWTJ4YWg9uaqiu1NoMMpXe8CcDP2OGCeGSIRsr2GIBc%2BArTxgLkiu11Gy3HrtmLukSi6nGBwhQOlYutcYTflCET5J3M%2BH0excisAXD%2BqI9tRaUZW5xq3rDFgRrr8VoBHibSER9Gy06Z9raciyCLMaHRRpaen3svHHLMqLPXjGqp8Xaf48MIZ5IvZ%2Fp19Vy2Oxw3i6MXVV3OdHgSE8LoEjTx9zpNPbFaRsOtQUnaEEbxBoHxZXOc%3D&nvMid=80460094726&catId=50003215"
driver.get(url)
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.0)  # 인터발 1이상으로 줘야 데이터 취득가능(롤링시 데이터 로딩 시간 때문)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height
html_source = driver.page_source
soup = BeautifulSoup(html_source, "lxml")

result = []

bedbtn=driver.find_element_by_xpath('//*[@id="REVIEW"]/div/div[3]/div/div[1]/div[1]/ul/li[4]/a').send_keys(Keys.ENTER)
print("push")
    # 리뷰 다음페이지 버튼 1번 페이지가 2임  그래서 5번페이지까지 뽑음 만약 없으면 pass
page = 2
while page < 7:
    time.sleep(3)
    if page != 2:
        try:
            bt = driver.find_element_by_xpath(
                        '//*[@id="REVIEW"]/div/div[3]/div/div[2]/a[' + str(page) + ']').send_keys(Keys.ENTER)
        except:
            break
        time.sleep(3)
    page += 1

    html_source1 = driver.page_source
    soup = BeautifulSoup(html_source1, "html.parser")
    driver.implicitly_wait(30)

    stars = []
    ul = soup.find('ul', {'class': '_1iaDS5tcmC'})
    ems = ul.find_all('em')
    for em in ems:
        stars.append(em.text)
    review = soup.select("#REVIEW > div > div.hmdMeuNPAt > div > ul > div > div > div.KHHDezUtRz > div > div._3AZFu4SXct > div > div._2hmOjCcGBh > div.eBQ2qaKgOU > div > span")
    customerId = soup.select("#REVIEW > div > div.hmdMeuNPAt > div > ul > div > div > div.KHHDezUtRz > div > div._3AZFu4SXct > div > div._2hmOjCcGBh > div._3iYCagsFsO > div._301WLm00sr > div._2DSGiSauFJ > strong")
    reviewDate = soup.select("#REVIEW > div > div.hmdMeuNPAt > div > ul > div > div > div.KHHDezUtRz > div > div._3AZFu4SXct > div > div._2hmOjCcGBh > div._3iYCagsFsO > div._301WLm00sr > div._2DSGiSauFJ > span")

    for k in range(len(stars)):
        s = stars[k]
        r = review[k].text
        c = customerId[k].text
        rD = reviewDate[k].text

        result.append([s, r, c, rD])
    print(len(review))
    if len(review) < 20:
        break

print(result)
data = pd.DataFrame(result)
data.columns = ['star', 'review', 'customerId', 'reviewDate']

filename = 'training/bed0-bedreview.csv'
data.to_csv(filename, encoding='utf-8-sig', index = True)
#다하고 첫 항에 review_no 열 이름 추가, 쉼표 스페이스바로 바꾸기

driver.close()

