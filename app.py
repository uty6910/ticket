import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

class Store:
    def __init__(self, name):
        self.name = name
        self.lotte = ''
        self.ssg = ''
        self.hy = ''

def fetch_data(url, selectors):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding  # 자동으로 인코딩 감지
    soup = BeautifulSoup(response.content, 'html5lib')
    return [soup.select_one(selector).text for selector in selectors]

# Store instances
stores = {
    '엑스이': Store('엑스이'),
    '미래': Store('미래'),
    '우천': Store('우천'),
    '우현': Store('우현'),
    '최고': Store('최고')
}

# Define URLs and selectors for each store
store_info = {
    '엑스이': ('http://xegift.co.kr/', [
        '#tab1 > div > div.tbl_wrap > table > tbody > tr:nth-child(2) > td.blue',  # 롯데
        '#tab1 > div > div.tbl_wrap > table > tbody > tr:nth-child(5) > td.blue',  # 신세계
        '#tab1 > div > div.tbl_wrap > table > tbody > tr:nth-child(7) > td.blue'   # 현대
    ]),
    '미래': ('http://www.meee.co.kr/bbs/board.php?bo_table=0401', [
        '#container > div > div.subPage.indexConWrap > div.tableWrap > div.table.table1 > table > tbody > tr.sct_li.sct_clear > td:nth-child(2) > span',  # 롯데
        '#container > div > div.subPage.indexConWrap > div.tableWrap > div.table.table1 > table > tbody > tr:nth-child(3) > td:nth-child(2) > span',  # 신세계
        '#container > div > div.subPage.indexConWrap > div.tableWrap > div.table.table1 > table > tbody > tr:nth-child(4) > td:nth-child(2) > span'   # 현대
    ]),
    '우현': ('https://wooh.co.kr/', [
        '#idx_hit > div.tbl_head05.tbl_wrap2 > table > tbody > tr:nth-child(2) > td:nth-child(2)',  # 롯데
        '#idx_hit > div.tbl_head05.tbl_wrap2 > table > tbody > tr:nth-child(11) > td:nth-child(2)',  # 신세계
        '#idx_hit > div.tbl_head05.tbl_wrap2 > table > tbody > tr:nth-child(16) > td:nth-child(2)'   # 현대
    ]),
    '최고': ('https://www.choigoticket.com/', [
        '#main1 > div > div.tbl_wrap > table > tbody > tr:nth-child(2) > td.blue',  # 롯데
        '#main1 > div > div.tbl_wrap > table > tbody > tr:nth-child(5) > td.blue',  # 신세계
        '#main1 > div > div.tbl_wrap > table > tbody > tr:nth-child(8) > td.blue'   # 현대
    ]),
}

# Fetch data for each store except 우천
for name, (url, selectors) in store_info.items():
    if name != '우천':
        lotte, ssg, hy = fetch_data(url, selectors)
        store = stores[name]
        store.lotte, store.ssg, store.hy = lotte, ssg, hy

data = requests.get('http://www.wooticket.com/', headers=headers)
data.encoding='utf-8'
soup = BeautifulSoup(data.text, 'html5lib')
lotte=soup.select_one('body > table > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(4) > td:nth-child(2)')
ssg=soup.select_one('body > table > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(12) > td:nth-child(2)')
hy=soup.select_one('body > table > tbody > tr > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td > div > table > tbody > tr:nth-child(17) > td:nth-child(2)')
stores['우천'].lotte, stores['우천'].ssg, stores['우천'].hy = lotte.text, ssg.text, hy.text

# Create DataFrame for display
data_frame = pd.DataFrame({
    '': ['롯데', '신세계', '현대'],
    **{store.name: [store.lotte, store.ssg, store.hy] for store in stores.values()}
})

# Display the data using Streamlit
st.title('상품권 시세 차트')
st.table(data_frame)
