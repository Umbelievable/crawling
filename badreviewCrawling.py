import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('/Users/10000say/Downloads/dzbz/chromedriver')
url="https://cr.shopping.naver.com/adcr.nhn?x=bwv2eObe%2FGf0%2BqVCaifW%2B%2F%2F%2F%2Fw%3D%3DsAyaZAQnvBfEDZUVe%2Bj61H1HMamM%2BT4MYek63f5L3MXHF6tTtHw1jIJXpgNFNZp3Les4wSU6q%2BwkmiwQ19Xt3aFVd6Z%2BmZ5fvTALbBBPmfKLR71%2BG1mg7pxhejX%2BnHQgTyY9LCEu%2BcAiMgGbzTxXXAGFJkOslDxD4Q3jMAfhdLTvYiaRmIm9S7iqRGcRn2%2Fbpfdx90CtIdY7jMsoj9CXM4M2qpJUNTIl9hFyLyRI0%2Fw8g%2BQQ9u%2FasamhYnfBDlgj%2FSgIJ3f8X1Wwe%2Bp93gITdmlb63pR1LaPyDKznswT74hTDpmNu2Rs3tEPrV0ZTODsbWqyaFa2xLbpwGCJChqMDqgbw%2BYYY9%2B4n4DsJGbGo5m58i8%2Bb52W6RWB4adaKIleJrzEEp4pMe2EzhjL%2BIPFd0jrisELbxFUg27BHIDkwdcOJXQ8r0Q3shsAj3iTjuRenmqIuUBNpPLlMvYCM3n8A8Zte7poKKZ0rXPNcJnW31v%2BGsEKwUVeEPZmxFMSbmKTzAOc%2BsAP%2F8T1JlRje3PIDATKnE%2BLQHxIk96dCEE9Yfp6sSPft5LY8ZEjd%2BEl213NiTQ%2FwcJ65jMqYvzffpxBTBj91i%2FbriIPgSxsgNIoCeZE6m%2FNKEqQ8Pl9ljdd4cCsNRP82l%2F23qHmwF7n7lFl4EeR79U%2F6Az3gE9mQ%2Flgn57E%3D&nvMid=82067464483&catId=50003245"
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

filename = 'training/living0-badreview.csv'
data.to_csv(filename, encoding='utf-8-sig', index = True)
#다하고 첫 항에 review_no 열 이름 추가, 쉼표 스페이스바로 바꾸기

driver.close()

