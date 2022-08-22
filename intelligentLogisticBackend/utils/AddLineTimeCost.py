import pickle
from sklearn.metrics.pairwise import  haversine_distances
from math import radians
from functools import reduce
import pandas as pd
import numpy as np


class AddLineTimeCost(object):
    '''
    结果中加入特快、快包线路时限
    '''

    def __init__(self, data_path, dis_coef=1.17):
        self.data_path = data_path
        self.city = None
        self.tk_line = None
        self.kb_line = None
        self.dis_coef = dis_coef

    def _loadData(self):
        '''
        加载城市经纬度及线路特快、快包时限
        '''
        with open(self.data_path, 'rb') as file:
            data_dict = pickle.load(file)
        self.city_df = data_dict['coordinate']
        self.tk_line = data_dict['tk']
        self.kb_line = data_dict['kb']

    def _getDistanceBall(self, p1, p2):
        '''
        计算两点球面距离
        p1,p2均是list: [lon, lat]
        '''
        dis = haversine_distances([[radians(_) for _ in np.flipud(p1)],
                                   [radians(_) for _ in np.flipud(p2)]])[0][1] * 6371393 / 1000

        return dis * self.dis_coef

    def _getNearestCity(self, stores):
        '''
        获取每个仓库最近的城市推荐建仓城市
        '''
        for i in range(stores.shape[0]):
            store_coord = [float(stores.loc[i, '经度']),
                           float(stores.loc[i, '纬度'])]
            store_city_dis = np.array([self._getDistanceBall(store_coord,
                                                             [float(self.city_df.loc[j, '经度']),
                                                              float(self.city_df.loc[j, '纬度'])])
                                       for j in range(self.city_df.shape[0])])
            city_indx = store_city_dis.argmin()

            stores.loc[i, '推荐建仓城市'] = self.city_df.loc[city_indx, '城市']

        return stores

    def _standardiseCityName(self, x, citys):
        '''
        修改城市名称，尽量标准化
        '''
        name = x
        for city in citys:
            # 这个地方初期默认x是city的简化，故使用in，后期可使用字符串相似度，或词向量相似度。
            if x in city:
                name = city
        return name

    def addLineTime(self, stores, points):
        '''
        在结果表中加入时限
        '''
        try:
            self._loadData()
            #对stores进行处理，加入最近城市
            if '推荐建仓城市' not in stores.columns:
                stores = self._getNearestCity(stores)
            stores_select = stores[['仓库', '推荐建仓城市']]
            # 对points进行处理，points中名称标准化
            citys = self.city_df['城市'].tolist()
            points['城市'] = points['城市'].apply(lambda x: self._standardiseCityName(x, citys))
            # 合并points与stores，增加线路字段，然后匹配各线路时限。

            results = pd.merge(points, stores_select, how='left', on='仓库')
            results['线路'] = results.apply(lambda row: row['推荐建仓城市'] + '->' + row['城市'], axis=1)
            dfs = [results, self.tk_line, self.kb_line]
            results = reduce(lambda left, right: pd.merge(left, right, how='left', on='线路'), dfs)
            message = 'success'
            return results, message
        except Exception as e:
            message = repr(e)
            return results, repr(e)