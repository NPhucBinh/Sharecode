import random
import pandas as pd
import requests
import json
import re
from bs4 import BeautifulSoup



'''
Hàm cuối lấy dữ liệu là hàm:
```
   get_data_vnindex('số trang')
```
Vấn đề gặp phải là dữ liệu khi requests và trả về khi check trên trình duyệt là kiểu 'plain'.
Vậy nên mình dùng số trang để điều hướng vì mỗi trang chỉ trả về dữ liệu của 20 ngày.
Mình để file .html mà dữ liệu trả về cùng thư mục các bạn xem thử nhé.
Hiện mình muốn cải thiện đoạn code này để khi load data chỉ cần nhập ngày bắt đầu và kết thúc mà,
không cần sử dụng số trang để điều hướng.
Mọi người có ý tưởng thì giúp mình nhé. Mình cảm ơn mọi người.
'''











url='https://s.cafef.vn/Lich-su-giao-dich-VNINDEX-1.chn'

def cooki(): #hàm lấy giả trị cookie, __VIEWSTATE và __VIEWSTATEGENERATOR
    head={'Accept': '*/*',
          'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,vi-VN;q=0.7,fr-FR;q=0.6,fr;q=0.5',
          'Connection': 'keep-alive',
          'DNT': '1',
          'Origin': 'https://dstock.vndirect.com.vn',
          'Referer': 'https://dstock.vndirect.com.vn/',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
          'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',}
    r=requests.post(url, headers=head)
    soup=BeautifulSoup(r.content)
    a=soup.find_all('input')
    vSTT=str(a[2])
    vSTT=vSTT.replace('<input id="__VIEWSTATE" name="__VIEWSTATE" type="hidden" value="','')
    vSTT=vSTT.replace('"/>','')
    vsttG=str(a[-1])
    vsttG=vsttG.replace('<input id="__VIEWSTATEGENERATOR" name="__VIEWSTATEGENERATOR" type="hidden" value="','')
    vsttG=vsttG.replace('"/>','')
    cookie=r.cookies.get_dict()
    asp_cookie=cookie['ASP.NET_SessionId']
    #cookie=list(cookie)
    #asp_cookie=str(cookie[1])
    #asp_cookie=asp_cookie.replace('<Cookie ASP.NET_SessionId=','')
    #asp_cookie=asp_cookie.replace('for s.cafef.vn/>','')
    #asp_cookie=asp_cookie.replace(' ','')
    return vSTT,vsttG,asp_cookie

def headers(asp_cookie): #hàm tạo header
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,vi-VN;q=0.7,fr-FR;q=0.6,fr;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://dstock.vndirect.com.vn',
        'Referer': 'https://dstock.vndirect.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': 'cafef.IsMobile=IsMobile=NO; ASP.NET_SessionId={}'.format(asp_cookie)}
    return header


def data_vnindex(number_page,fdate,tdate): #hàm xử lý data load về
    number=int(number_page+1)
    list_payload=[]
    for num in range(1,number):
        vSTT,vsttG,row=cooki()
        header=headers(row)
        payload={'ctl00$ContentPlaceHolder1$scriptmanager':'ctl00$ContentPlaceHolder1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager2',
                  'ctl00$ContentPlaceHolder1$ctl03$txtKeyword': 'VNINDEX',
                  'tl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker':fdate,
                  'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker':tdate,
                  '__VIEWSTATE':vSTT, '__VIEWSTATEGENERATOR':vsttG,'__EVENTTARGET':'ctl00$ContentPlaceHolder1$ctl03$pager2',
                  '__EVENTARGUMENT':num,
                  '__ASYNCPOST': 'true',}
        list_payload.append(payload)
    list_df=[]
    for pay in list_payload:
        chaythu=requests.post(url, headers=header,data=pay)
        soup=BeautifulSoup(chaythu.content,'html.parser')
        bangls=pd.read_html(chaythu.text,header=1)
        list_df.append(bangls[0])
        df=pd.concat(list_df)
        df.drop(['Thay đổi (+/-%).1'],axis=1,inplace=True)
        df.rename(columns={'KL':'KLGD khớp lệnh','GT':'GTGD khớp lệnh','KL.1':'KLGD thỏa thuận','GT.1':'GTGD thỏa thuận'}, inplace=True)
    return df.reset_index(drop=True)

def get_data_vnindex(number_page): # Hàm load theo page
    date_now=dt.datetime.now()
    fdate=pd.to_datetime(date_now)
    fdate=fdate.strftime('%d-%m-%Y')
    fdate=fdate.replace('-','/')
    tdate=date_now-dt.timedelta(170)
    tdate=pd.to_datetime(tdate)
    tdate=tdate.strftime('%d-%m-%Y')
    tdate=tdate.replace('-','/')
    vSTT,vsttG,asp_cookie=cooki()
    header=headers(asp_cookie)
    df=data_vnindex(number_page,fdate,tdate)
    ngay=len(df)
    df=df.rename_axis((f'{ngay} Ngày'),axis='columns')
    return df

