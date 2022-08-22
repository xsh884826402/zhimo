import requests

if __name__ == '__main__':
    data={'filepath':'D:\Project\intelligentlogisticsexe\中邮信科测试数据3.xlsx'}
    res = requests.post(url="http://127.0.0.1:5000/write", data=data)
    print(res)