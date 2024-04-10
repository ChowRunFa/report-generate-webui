import requests,re
from lxml import etree


def get_cookie(): # 获取访问的cookie
    params = (
        ('action', ''),
        ('NaviCode', 'A'), # 筛选的类别
        ('ua', '1.21'),
        ('PageName', 'ASP.brief_result_aspx'),
        ('DbPrefix', 'SCPD'),
        ('DbCatalog', '\u4E2D\u56FD\u4E13\u5229\u6570\u636E\u5E93'),
        ('ConfigFile', 'SCPD.xml'),
        ('db_opt', '\u4E2D\u56FD\u4E13\u5229\u6570\u636E\u5E93'),
        ('db_value', '\u4E2D\u56FD\u4E13\u5229\u6570\u636E\u5E93'),
        ('date_gkr_from', '2020-01-24'), # 筛选日期
        ('date_gkr_to', '2020-01-24'), # 筛选日期
        ('his', '0'),
        ('__', 'Fri Oct 16 2020 14:37:38 GMT+0800 (\u4E2D\u56FD\u6807\u51C6\u65F6\u95F4)'),
    )
    session = requests.session()
    session.get('https://epub.cnki.net/kns/request/SearchHandler.ashx', headers=headers, params=params)
    return session

def get_list_info(): # 获取列表页
    params = (
        ('curpage', '1'), # 当前页数
        ('RecordsPerPage', '50'),
        ('QueryID', '20'),
        ('ID', ''),
        ('turnpage', '1'),
        ('tpagemode', 'L'),
        ('dbPrefix', 'SCPD'),
        ('Fields', ''),
        ('DisplayMode', 'listmode'),
        ('SortType', "(公开日, 'DATE')desc"),
        ('PageName', 'ASP.brief_result_aspx'),
    )

    response = session.get('https://epub.cnki.net/kns/brief/brief.aspx', headers=headers, params=params)
    print(response.text)
    selector = etree.HTML(response.text)
    urls_info = re.compile("<a class='fz14' href='/kns/detail/detail.aspx(.*?)'").findall(response.text)
    print(urls_info)
    page_info = selector.xpath('//*[@id="J_ORDER"]/tr[2]/td/table/tr/td[2]/div/span[1]')[0].text
    nums = len(urls_info)
    now_page = int(re.compile('浏览(.*?)/').findall(page_info)[0])
    print("当前获取第{}页数据".format(now_page), "数目", nums)
    return urls_info

def get_detil():# 获取详情页
    for url in urls_info:
        # 旧地址访问速度慢，可更换新地址 https://kns.cnki.net/KCMS/detail/detail.aspx 需修改正则匹配
        detail_url = 'https://dbpub.cnki.net/grid2008/dbpub/detail.aspx' + url # 详情页地址
        print(detail_url)
        response = requests.get(url=detail_url, headers=headers)
        main_info = ''.join(etree.HTML(response.text).xpath('//*[@id="box"]//text()')).replace('\r\n', '').replace(' ','').replace(' ', '')
        # print(main_info)
        title = re.compile('font-weight:bold;text-align:center;">(.*?)</td>').findall(response.text)[0]
        gb_id = re.compile('【公开号】(.*?)【').findall(main_info)[0]
        gb_time = re.compile('【公开日】(.*?)【').findall(main_info)[0]
        sq_id = re.compile('【申请号】(.*?)【').findall(main_info)[0]
        sq_time = re.compile('【申请日】(.*?)【').findall(main_info)[0]
        sq_person = re.compile('【申请人】(.*?)【').findall(main_info)[0]
        addr = re.compile('【地址】(.*?)【').findall(main_info)[0]
        fmr = '#'.join(re.compile('【发明人】(.*?)【').findall(main_info)[0].split(';'))
        int_cl = re.compile('【专利分类号】(.*?)推荐下载').findall(main_info)[0]
        try:
            patent_agency = re.compile('【专利代理机构】(.*?)【').findall(main_info)[0]
            agent = '#'.join(re.compile('【代理人】(.*?)【').findall(main_info)[0].split(';'))
        except Exception:
            patent_agency = agent = ''
        abstract = re.compile('【摘要】(.*?)【').findall(main_info)[0].replace("'", '"')
        print(title, gb_id, gb_time, sq_id, sq_time, sq_person, addr, fmr, int_cl, patent_agency, agent, abstract)
        # break


if __name__ == '__main__':
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        'Referer': 'https://epub.cnki.net/kns/brief/result.aspx?dbprefix=SCPD',
    }

    session = get_cookie()
    print(session)
    urls_info = get_list_info()
    get_detil()