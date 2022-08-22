import requests
import json


class CoordinateToAddress(object):
    '''
    给定地址，获取经纬度
    '''

    def __init__(self, channel):
        self.channel = channel
        self.key = None

    def _gaudurMap(self, lon, lat):
        '''
        高德地图
        '''
        url = 'https://restapi.amap.com/v3/geocode/regeo'
        # 参数放入字典
        params = {'key': self.key,
                  'location': str(lon) + ',' + str(lat)}
        res = requests.get(url, params)
        json_text = json.loads(res.text)
        if json_text['regeocode']['addressComponent']['province'] in ('北京市', '上海市', '天津市', '重庆市'):
            return json_text['regeocode']['addressComponent']['province'], json_text['regeocode']['formatted_address']
        else:
            return json_text['regeocode']['addressComponent']['city'], json_text['regeocode']['formatted_address']

    def _baiduMap(self, lon, lat):
        '''
        百度地图
        '''
        url = 'https://api.map.baidu.com/reverse_geocoding/v3'
        # 参数放入字典
        params = {'ak': self.key,
                  'location': str(lat) + ',' + str(lon),
                  'output': 'json'}
        res = requests.get(url, params)
        json_text = json.loads(res.text)

        return json_text['result']['addressComponent']['city'], json_text['result']['formatted_address']

    def _tencentMap(self, lon, lat):
        '''
        腾讯地图
        '''
        url = 'https://apis.map.qq.com/ws/geocoder/v1/'
        # 参数放入字典
        params = {
            "qt": "geoc",
            "location": str(lat) + ',' + str(lon),  # 传入地址参数
            "output": "json",
            "key": self.key,  # 即腾讯地图API的key
            "pf": "jsapi",
            "ref": "jsapi"}
        res = requests.get(url, params)
        json_text = json.loads(res.text)

        return json_text['result']['address_component']['city'], json_text['result']['address']

    def _freeNominatimMap(self, lon, lat):
        '''
        免费的Nominatim，速度很慢
        '''
        result = geolocator.reverse([lat, lon])
        address = result.address
        pattern = re.compile(r'(.*?市)', re.S)
        city = None
        for s in address.split(','):
            p = pattern.findall(s)
            if p and p[0] == s:
                city = s.strip()

        return city, address

    def _freeArcgisMap(self, lon, lat):
        '''
        免费的Arcgis，速度很慢
        '''
        result = geocoder.arcgis([lat, lon], method='reverse')
        address = result.address
        pattern = re.compile(r'.*省(.*?市).*?', re.S)
        p = pattern.findall(address)
        if p:
            city = p[0].strip()
        else:
            city = None

        return city, address

    def _chooseMap(self):
        '''
        根据界面选择，使用对应的厂商地图
        '''
        if self.channel == '高德':
            map_provider = self._gaudurMap
        elif self.channel == '百度':
            map_provider = self._baiduMap
        elif self.channel == '腾讯':
            map_provider = self._tencentMap
        elif self.channel == 'Arcgis':
            map_provider = self._freeArcgisMap
        elif self.channel == 'Nominatim':
            map_provider = self._freeNominatimMap
        else:
            map_provider = None

        return map_provider

    def getSingleAddress(self, lon, lat):
        '''
        获取单个经纬度的城市和地址
        '''
        map_provider = self._chooseMap()
        city, address = map_provider(lon, lat)

        return city, address

    def getStoresCity(self, stores):

        '''
        获取每个仓库所在的城市推荐建仓城市
        '''
        message = 'success'
        flag = True
        for i in range(stores.shape[0]):
            lon = float(stores.loc[i, '经度'])
            lat = float(stores.loc[i, '纬度'])
            city_name, address = self.getSingleAddress(lon, lat)
            print(lon, lat, city_name, address)
            if not city_name:
                flag = False
                stores.loc[i, '补充地址'] = address
                stores.loc[i, '推荐建仓城市'] = None
            else:
                stores.loc[i, '补充地址'] = address
                stores.loc[i, '推荐建仓城市'] = city_name
        if flag:
            message = 'success'
        else:
            message = '部分仓获取推荐建仓城市失败,建议更换地图或者手动输入'
        return stores, message