def laisuat(fromdate,todate):
    fromdate=pd.to_datetime(fromdate)
    todate=pd.to_datetime(todate)
    tungay=str(fromdate.strftime('%Y-%m-%d'))
    denngay=str(todate.strftime('%Y-%m-%d'))
    urltoken='https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-xuat.htm#'
    head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
    loadlan1=requests.get(urltoken,headers=head)
    soup=BeautifulSoup(loadlan1.content,'html.parser')
    stoken=soup.body.input
    stoken=str(stoken)
    listtoken=stoken.split()
    xre=[]
    for i in listtoken[1:]:
        i=i.replace('=',':')
        i=i.replace('"','')
        xre.append(i)
    token=str(xre[2])
    token=token.replace('value:','')
    token=token.replace('/>','')
    dic=dict(loadlan1.cookies.get_dict())
    revtoken=dic['__RequestVerificationToken']
    revasp=dic['ASP.NET_SessionId']
    url='https://finance.vietstock.vn/data/reportdatatopbynormtype'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
           'Cookie': 'language=vi-VN; ASP.NET_SessionId={}; __RequestVerificationToken={}; Theme=Light; _ga=GA1.2.521754408.1675222361; _gid=GA1.2.2063415792.1675222361; AnonymousNotification='.format(revasp,revtoken)
           }
    payload={'type':'1','fromYear':'2022','toYear':'2023','from':'2022-01-01','to':'2023-02-01','normTypeID':'66',
        '__RequestVerificationToken': '{}'.format(token)
        }
    ls=requests.post(url,headers=header,data=payload)
    cov1=dict(ls.json())
    bangls=pd.DataFrame(cov1['data'])
    bangls.drop(['ReportDataID','TermID','TermYear','TernDay','NormID','GroupName','CssStyle','NormTypeID','NormGroupID'], axis=1, inplace=True)
    return bangls