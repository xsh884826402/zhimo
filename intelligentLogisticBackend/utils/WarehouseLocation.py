import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
import math
from math import radians

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
# 打包exe时需导入以下两个包，测试时注释掉
import sklearn.utils._typedefs
import sklearn.neighbors._partition_nodes

from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Bing")


class MultiCenterGravity(object):
    '''
    不指定仓的多重心选址
    '''

    def __init__(self, n_clusters=4, seed=42, max_iter=300, init='kmeans', dis_coef=1.17):
        self.n_clusters = n_clusters
        self.seed = seed
        self.max_iter = max_iter
        self.dis_coef = dis_coef
        self.init = init

        self.X_all = None  # df: 包含输入数据的所有纬度
        self.X = None  # df: 输入数据X,有5个纬度：name,log,lat,W,C
        self.X_p = None  # df: X_p有2维，df,log,lat
        self.longitude = None
        self.latitude = None
        self.prod_output = None
        self.trans_rate = None

        self.stores = None  # np.array: 仓位置，2维： log,lat
        self.label = None

    def _rdInitStores(self):
        '''
        随机初始化仓
        '''
        # 使用样本点的部分来进行初始化
        k = 0
        indices = []
        np.random.seed(self.seed)

        while True:
            index = np.random.randint(self.X_p.shape[0])
            if index not in indices:
                indices.append(index)
                k = k + 1
                if k == self.n_clusters:
                    break
        # 返回的初始化stores是np.array
        return self.X_p.loc[indices].values

    def _kmInitStores(self):
        '''
        使用kmeans的方法初始化仓
        '''
        sts = StandardScaler()
        feature = sts.fit_transform(self.X_p.values)
        model = KMeans(n_clusters=self.n_clusters, random_state=self.seed)
        model.fit(feature)
        init_stores = sts.inverse_transform(model.cluster_centers_)

        return init_stores

    def _ortInitStoresNew(self):
        '''
        使用or-tools的方法初始化仓的第三种方法(进行了时间优化)，不使用kmeans，纯使用or-tools。
        '''
        designatedFacilityLocations = []
        totalFacilityNumber = self.n_clusters
        demandLocations = self.X

        if (len(designatedFacilityLocations) >= totalFacilityNumber):
            return []

        maxDemandLocationNumber = math.ceil(len(demandLocations) / totalFacilityNumber)

        totalDesignatedFacilityLocationNumber = len(designatedFacilityLocations)  # 这个取值是0
        totalDemandLocationNumber = len(demandLocations)
        totalCandidateLocationNumber = totalDesignatedFacilityLocationNumber + totalDemandLocationNumber

        solver0 = pywraplp.Solver.CreateSolver('GLOP')
        x0 = {}
        y0 = {}
        for i in range(totalCandidateLocationNumber):
            y0[i] = solver0.NumVar(0.0, 1.0, 'y')
            for j in range(totalCandidateLocationNumber):
                x0[i, j] = solver0.NumVar(0.0, 1.0, 'x')

        # Each demandLocation is assigned to 1 facilityLocation.
        for i in range(totalDemandLocationNumber):
            solver0.Add(solver0.Sum(x0[i, j] for j in range(totalCandidateLocationNumber)) == 1)

        for i in range(totalDemandLocationNumber):
            for j in range(totalCandidateLocationNumber):
                solver0.Add(x0[i, j] <= y0[j])

        # Each designatedFacilityLocation is assigned to at most maxFacilityNumber demandLocations.
        for j in range(totalCandidateLocationNumber):
            solver0.Add(solver0.Sum([x0[i, j] for i in range(totalDemandLocationNumber)]) <= maxDemandLocationNumber)

        for i in range(totalDemandLocationNumber, totalCandidateLocationNumber):
            solver0.Add(y0[i] == 1)
            solver0.Add(solver0.Sum([x0[i, j] for j in range(totalCandidateLocationNumber)]) == 0)

        solver0.Add(solver0.Sum([y0[i] for i in range(totalCandidateLocationNumber)]) == totalFacilityNumber)

        # Objective
        objective_terms0 = []
        for i in range(totalDemandLocationNumber):
            for j in range(totalDemandLocationNumber):
                objective_terms0.append(
                    self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                          demandLocations.loc[j][[self.longitude, self.latitude]].values)
                    * demandLocations.loc[i][self.prod_output]
                    * demandLocations.loc[i][self.trans_rate] * x0[i, j])
            # 其实这个for循环没跑,因为range(totalDemandLocationNumber, totalCandidateLocationNumber)是个空list。
            for j in range(totalDemandLocationNumber, totalCandidateLocationNumber):
                objective_terms0.append(
                    self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                          designatedFacilityLocations[j - totalDemandLocationNumber])
                    * demandLocations.loc[i][self.prod_output]
                    * demandLocations.loc[i][self.trans_rate] * x0[i, j])

        solver0.Minimize(solver0.Sum(objective_terms0))

        status0 = solver0.Solve()

        y_result = []

        if status0 == pywraplp.Solver.OPTIMAL:
            print(f'Relaxed model total cost = {solver0.Objective().Value()}\n')
            for i in range(totalDemandLocationNumber):
                y_result.append(y0[i].solution_value())
        else:
            print('No solution found111.')

        max_indices = np.argpartition(np.array(y_result), -totalFacilityNumber)[-totalFacilityNumber:]

        model = cp_model.CpModel()
        x = {}
        y = {}
        for i in range(totalCandidateLocationNumber):
            y[i] = model.NewBoolVar(f'y[{i}]')
            for j in range(totalCandidateLocationNumber):
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

        # Each demandLocation is assigned to 1 designatedFacilityLocation.
        for i in range(totalDemandLocationNumber):
            model.Add(sum([x[i, j] for j in range(totalCandidateLocationNumber)]) == 1)

        for i in range(totalDemandLocationNumber):
            for j in range(totalCandidateLocationNumber):
                model.Add(x[i, j] <= y[j])

        # Each designatedFacilityLocation is assigned to at most maxFacilityNumber demandLocations.
        for j in range(totalCandidateLocationNumber):
            model.Add(sum([x[i, j] for i in range(totalDemandLocationNumber)]) <= maxDemandLocationNumber)

        for i in range(totalDemandLocationNumber, totalCandidateLocationNumber):
            model.Add(y[i] == 1)
            model.Add(sum([x[i, j] for j in range(totalCandidateLocationNumber)]) == 0)

        for max_index in max_indices:
            model.Add(y[max_index] == 1)

        model.Add(sum([y[i] for i in range(totalCandidateLocationNumber)]) == totalFacilityNumber)

        # Objective
        objective_terms = []
        for i in range(totalDemandLocationNumber):
            for j in range(totalDemandLocationNumber):
                objective_terms.append(
                    int(self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                              demandLocations.loc[j][[self.longitude, self.latitude]].values)
                        * demandLocations.loc[i][self.prod_output]
                        * demandLocations.loc[i][self.trans_rate] * 1000) * x[i, j])
            # 这个循环其实没跑，因为range(totalDemandLocationNumber, totalCandidateLocationNumber)是空list。
            for j in range(totalDemandLocationNumber, totalCandidateLocationNumber):
                objective_terms.append(
                    int(self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                              designatedFacilityLocations[j - totalDemandLocationNumber])
                        * demandLocations.loc[i][self.prod_output]
                        * demandLocations.loc[i][self.trans_rate] * 1000) * x[i, j])
        model.Minimize(sum(objective_terms))

        # Solve
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        initNewFacilityLocations = []
        # Print solution.
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f'Total cost = {solver.ObjectiveValue()}\n')
            for i in range(totalDemandLocationNumber):
                if solver.BooleanValue(y[i]):
                    facilityLocation = demandLocations.loc[i][[self.longitude, self.latitude]].values
                    initNewFacilityLocations.append(facilityLocation)
        else:
            print('No solution found.')

        ort_init = np.array(initNewFacilityLocations)

        return ort_init

    def _initStores(self):
        '''
        初始化仓：根据init参数选择使用的初始化仓方法
        '''
        init_stores = None
        if self.init == 'random':
            init_stores = self._rdInitStores()
        elif self.init == 'kmeans':
            init_stores = self._kmInitStores()
        elif self.init == 'or-tools':
            init_stores = self._ortInitStoresNew()
        else:
            init_stores = None

        return init_stores

    def _getDistanceBall(self, p1, p2):
        '''
        计算点与仓库的球面距离
        p1,p2均是list: [longitude, latitude]
        '''
        # 使用flipud反转np.array是因为haversine_distances方法需要纬度在前。
        dis = haversine_distances([[radians(_) for _ in np.flipud(p1)],
                                   [radians(_) for _ in np.flipud(p2)]])[0][
                  1] * 6371393 / 1000  # multiply by Earth radius to get kilometers

        return dis * self.dis_coef

    def _getDistanceEul(self, p1, p2):
        '''
        计算点与仓库的欧式距离
        p1,p2均是list: [longitude, latitude]
        '''
        dis = math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

        return dis

    def _classifyPoint(self):
        '''
        为每个点选择最近的仓当作它的仓
        '''
        label = np.zeros(self.X_p.shape[0], dtype=np.int32)
        for i, p in enumerate(self.X_p.values):
            # 计算每一个data到所有store的距离，然后选择最近的store
            distances = np.array([self._getDistanceBall(p, s) for s in self.stores])
            label[i] = distances.argmin()
        #             label[i] = self.stores[distances.argmin()]

        return label

    def _gravtityMethodDist(self, data):
        '''
        重心法，重心法的输入是dataframe
        '''
        WC = np.array(data[self.prod_output]) * np.array(data[self.trans_rate])
        lon = np.array(data[self.longitude])
        lat = np.array(data[self.latitude])
        data_p = np.array(data[[self.longitude, self.latitude]])
        # 计算初始重心,初始距离,初始总费用
        x_i = (lon * WC).sum() / WC.sum()
        y_i = (lat * WC).sum() / WC.sum()
        s_i = np.array([x_i, y_i])
        # di的后面加0.0001的目的是防止di=0后无法作为分母
        # 但这样有一个问题，就是当单点被分为一类的时候，该点会单独成为一个仓。
        di = np.array([self._getDistanceEul(p, s_i) for p in data_p]) + 0.000001
        s_list = [np.array([0, 0])]
        s_list.append(s_i)
        n = 1
        # 开始循环迭代，满足最后一次选址比上次距离小于10km
        while self._getDistanceEul(s_list[-1], s_list[-2]) >= 0.000001:
            x_i = ((lon * WC) / di).sum() / (WC / di).sum()
            y_i = ((lat * WC) / di).sum() / (WC / di).sum()
            s_i = np.array([x_i, y_i])
            di = np.array([self._getDistanceEul(p, s_i) for p in data_p]) + 0.000001
            s_list.append(s_i)
            n = n + 1
        #             print('重心法：第{}次'.format(n))

        return s_list[-1]

    def _gravtityMethodCost(self, data):
        '''
        重心法，重心法的输入是dataframe
        '''
        WC = np.array(data[self.prod_output]) * np.array(data[self.trans_rate])
        lon = np.array(data[self.longitude])
        lat = np.array(data[self.latitude])
        data_p = np.array(data[[self.longitude, self.latitude]])
        # 计算初始重心,初始距离,初始总费用
        x_i = (lon * WC).sum() / WC.sum()
        y_i = (lat * WC).sum() / WC.sum()
        s_i = np.array([x_i, y_i])
        # 但这样有一个问题，就是当单点被分为一类的时候，该点会单独成为一个仓。
        di = np.array([self._getDistanceBall(p, s_i) for p in data_p]) + 0.000001
        Ti = (WC * di).sum()
        T_list = [float('inf')]
        T_list.append(Ti)
        n = 1
        # 开始循环迭代，满足最后一次选址比上次距离小于10km
        while (T_list[-2] - T_list[-1]) / (T_list[-1]) >= 0.000001:
            x_i = ((lon * WC) / di).sum() / (WC / di).sum()
            y_i = ((lat * WC) / di).sum() / (WC / di).sum()
            s_i = np.array([x_i, y_i])
            di = np.array([self._getDistanceBall(p, s_i) for p in data_p]) + 0.000001
            Ti = (WC * di).sum()
            T_list.append(Ti)
            n = n + 1
        #             print('重心法：第{}次'.format(n))

        return s_i

    def _updateStores(self, label):
        '''
        为每一类点，使用重心法优化仓的位置
        '''
        # 先按照label把数据分成对应的cluster
        clusters = [pd.DataFrame() for i in range(self.n_clusters)]
        for i, x in enumerate(label):
            #             clusters[x].append(self.X[i])
            clusters[x] = clusters[x].append(self.X.loc[i])
            # 为每一个cluster使用重心法计算store
        #         center = [np.mean(cluster) for cluster in clusters if cluster.size > 0]
        stores = np.array([self._gravtityMethodCost(cluster) for cluster in clusters if cluster.size > 0])

        return stores

    def _clusterStop(self, label, newLabel, iteration):
        '''
        判断聚类是否收敛
        '''
        if iteration > self.max_iter:
            return True
        return np.array_equal(label, newLabel)

    def fit(self, X, name, longitude, latitude, prod_output, trans_rate):
        '''
        主函数，循环迭代，直到每个仓到它自己点的花费都最优
        '''
        self.longitude = longitude
        self.latitude = latitude
        self.prod_output = prod_output
        self.trans_rate = trans_rate
        self.X_all = X
        self.X = X[[name, longitude, latitude, prod_output, trans_rate]]  # 输入数据X,有5个纬度：name,log,lat,W,C
        self.X_p = X[[longitude, latitude]]  # X的2维，log,lat

        iteration = 0
        oldlabel = np.zeros(self.X_p.shape[0], dtype=np.int32)  # 定义老的label全0
        #         self.stores = self._rdInitStores()    #随机初始化仓
        #         self.stores = self._kmInitStores()    #kmeans初始化仓
        self.stores = self._initStores()
        newlabel = self._classifyPoint()  # 为每个点选择它的仓，即标记label
        while not self._clusterStop(oldlabel, newlabel, iteration):
            oldlabel = np.copy(newlabel)
            iteration = iteration + 1
            self.stores = self._updateStores(newlabel)
            newlabel = self._classifyPoint()
        #             print('聚类，第{}次'.format(iteration))

        self.label = newlabel

    def _getAddress(self, lon, lat):
        '''
        predict辅助函数：根据经纬度获取地址，此部分需联网才能使用。
        '''
        address = geolocator.reverse(str(lat) + "," + str(lon)).address

        return address

    def _geneDistance(self, label, stores, lon, lat):
        '''
        predict辅助函数：需求点列表中添加仓、距离。
        '''
        store_coordinate = [float(stores[label][1]), float(stores[label][2])]
        point_coordinate = [lon, lat]
        distance = self._getDistanceBall(store_coordinate, point_coordinate)

        return distance

    def predict(self):
        '''
        函数给出3个结果：
        df_stores: 仓库列表
        df_points: 需求点列表
        dict_result: 给出需求点与仓的关系字典,用于画图
        '''
        # 创建结果字典，用来存储仓与点对应关系
        print('生成需求点与仓库的关系字典……')
        stores = []  # 仓库列表
        dict_result = {}  # 仓库与点对应关系字典
        for i, s in enumerate(self.stores):
            stores.append(tuple(['新建仓{}'.format(i + 1)] + list(s)))
            dict_result[tuple(['新建仓{}'.format(i + 1)] + list(s))] = []

        for l, p in zip(self.label, self.X.values[:, :3]):
            dict_result[stores[l]].append(tuple(p))

        print('生成仓库列表……')
        # 计算仓库列表：df_stores
        df_stores = pd.DataFrame(stores, columns=['仓库', '经度', '纬度'])
        print('联网获取仓库列表详细地址……')
        try:
            df_stores['地址'] = df_stores.apply(lambda row: self._getAddress(row['经度'], row['纬度']), axis=1)
        except:
            print('地址未获取成功！')
            df_stores['地址'] = None

        print('生成需求点列表……')
        # 计算需求点列表：df_points
        df_points = self.X_all.copy()
        df_points['label'] = self.label
        df_points['仓库'] = df_points['label'].apply(lambda x: stores[x][0])
        df_points['距离'] = df_points.apply(lambda row: self._geneDistance(row['label'],
                                                                         stores, row['经度'], row['纬度']), axis=1)
        df_points = df_points.drop('label', axis=1)
        df_points['总成本'] = df_points[self.prod_output] * df_points[self.trans_rate] * df_points['距离']

        return df_stores, df_points, dict_result


class MultiCenterGravityDefineStores(object):
    '''
    可以指定仓的多重心选址
    '''

    def __init__(self, n_clusters=2, seed=42, max_iter=300, init='kmeans', dis_coef=1.17):
        self.n_clusters = n_clusters
        self.seed = seed
        self.max_iter = max_iter
        self.dis_coef = dis_coef
        self.init = init

        self.X_all = None  # df: 包含输入数据的所有纬度
        self.X = None  # df: 输入数据X,有5个纬度：name,log,lat,W,C
        self.X_p = None  # df: X_p有2维，df,log,lat
        self.longitude = None
        self.latitude = None
        self.prod_output = None
        self.trans_rate = None

        self.define_stores = None  # np.array: 指定仓,3维： name,log,lat
        self.stores = None  # np.array: 仓位置,2维： log,lat
        self.label = None

    def setDefineStores(self, data, name, longitude, latitude):
        '''
        配置指定仓库
        '''
        self.define_stores = data[[name, longitude, latitude]].values  # 指定仓库3维，name,log,lat

    def _rdInitStores(self):
        '''
        随机初始化仓
        '''
        # 使用样本点的部分来进行初始化
        k = 0
        indices = []
        np.random.seed(self.seed)

        while True:
            index = np.random.randint(self.X_p.shape[0])
            if index not in indices:
                indices.append(index)
                k = k + 1
                if k == self.n_clusters:
                    break
        # 返回的初始化stores是np.array: 指定stores+随机点
        random_init = np.vstack((self.define_stores[:, 1:], self.X_p.loc[indices].values))

        return random_init

    def _delCenters(self, centers):
        '''
        配合kmeans初始化仓使用，在初始化的n+m个质心中依次删除离指定仓最近的n个质心
        '''
        # 距离矩阵，row为质心，col为指定仓
        dis_matrix = np.array([[self._getDistanceBall(c, s) for s in self.define_stores[:, 1:]]
                               for c in centers])
        del_centers_index = []
        for i in range(self.define_stores.shape[0]):
            row, col = np.unravel_index(dis_matrix.argmin(), dis_matrix.shape)
            del_centers_index.append(row)
            dis_matrix[row, :], dis_matrix[:, col] = np.inf, np.inf

        return np.delete(centers, del_centers_index, axis=0)

    def _kmInitStores(self):
        '''
        使用kmeans的方法初始化仓
        '''
        # 先用kmeans挑选n+m个中心点，其中n为指定仓个数，m为新建仓个数
        sts = StandardScaler()
        feature = sts.fit_transform(self.X_p.values)
        model = KMeans(n_clusters=self.define_stores.shape[0] + self.n_clusters, random_state=self.seed)
        model.fit(feature)
        kmeans_centers = sts.inverse_transform(model.cluster_centers_)
        # 删除距离指定仓最近的n个中心后剩余的中心
        remain_centers = self._delCenters(kmeans_centers)
        # 返回的初始化stores是np.array: 指定stores+kmeans剩余中心
        kmeans_init = np.vstack((self.define_stores[:, 1:], remain_centers))

        return kmeans_init

    def _calcUnAssignedDemandLocationArrays(self):
        '''
        or-tools的聚类方法，使用运筹优化算法，计算出未被分配到仓的需求点。
        '''
        demandLocations = self.X_p.values
        designatedFacilityLocations = self.define_stores[:, 1:]

        totalFacilityNumber = self.define_stores.shape[0] + self.n_clusters
        maxFacilityNumber = math.ceil(self.X_p.shape[0] / totalFacilityNumber)

        totalDesignatedFacilityLocationNumber = self.define_stores.shape[0]
        totalDemandLocationNumber = self.X_p.shape[0]

        # solver = pywraplp.Solver.CreateSolver('SCIP')
        model = cp_model.CpModel()
        # if demandLocation i is assigned to designatedFacilityLocation j.
        x = {}
        for i in range(totalDemandLocationNumber):
            for j in range(totalDesignatedFacilityLocationNumber):
                # x[i, j] = solver.IntVar(0, 1, '')
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

        # Each demandLocation is assigned to at most 1 designatedFacilityLocation.
        for i in range(totalDemandLocationNumber):
            # solver.Add(solver.Sum([x[i, j] for j in range(totalDesignatedFacilityLocationNumber)]) <= 1)
            model.Add(sum(x[i, j] for j in range(totalDesignatedFacilityLocationNumber)) <= 1)

        # Each designatedFacilityLocation is assigned to exactly maxFacilityNumber demandLocations.
        for j in range(totalDesignatedFacilityLocationNumber):
            # solver.Add(solver.Sum([x[i, j] for i in range(totalDemandLocationNumber)]) == maxFacilityNumber)
            model.Add(sum([x[i, j] for i in range(totalDemandLocationNumber)]) == maxFacilityNumber)

        # Objective
        objective_terms = []
        for i in range(totalDemandLocationNumber):
            for j in range(totalDesignatedFacilityLocationNumber):
                objective_terms.append(self._getDistanceBall(demandLocations[i],
                                                             designatedFacilityLocations[j]) * x[i, j])
        # solver.Minimize(solver.Sum(objective_terms))
        model.Minimize(sum(objective_terms))

        # Solve
        # status = solver.Solve()

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 120
        status = solver.Solve(model)

        unAssignedDemandLocationArray = []
        # Print solution.
        # if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # print(f'Total cost = {solver.Objective().Value()}\n')
            # print(f'Total cost = {solver.ObjectiveValue()}\n')
            for i in range(totalDemandLocationNumber):
                isDemandLocationAssigned = False
                for j in range(totalDesignatedFacilityLocationNumber):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    # if (x[i, j].solution_value() > 0.5):
                    if solver.BooleanValue(x[i, j]):
                        isDemandLocationAssigned = True

                if (not isDemandLocationAssigned):
                    unAssignedDemandLocationArray.append(demandLocations[i])
        else:
            print('No solution found.')

        return unAssignedDemandLocationArray

    def _kmInitStoresOr(self):
        '''
        使用or-tools的方法初始化仓
        '''
        # 先根据指定仓计算指定仓周围的可分配需求点、未分配需求点
        unAssignedDemandLocationArray = self._calcUnAssignedDemandLocationArrays()
        # 使用kmeans的方法对未分配需求点进行仓选址
        if (len(unAssignedDemandLocationArray) != 0):
            scaler = StandardScaler()
            X = scaler.fit_transform(np.array(unAssignedDemandLocationArray))
            kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.seed).fit(X)
            clusterCenters = scaler.inverse_transform(kmeans.cluster_centers_)
            # X = np.array(unAssignedDemandLocationArray)
            # kmeans = KMeans(n_clusters = self.n_clusters, random_state=self.seed).fit(X)
        # 综合返回所有的stores：指定stores+未分配点的仓
        kmort_init = np.vstack((self.define_stores[:, 1:], clusterCenters))

        return kmort_init

    def _ortInitStoresNew(self):
        '''
        使用or-tools的方法初始化仓的第二种方法，不使用kmeans，纯使用or-tools。
        '''
        designatedFacilityLocations = self.define_stores[:, 1:]
        totalFacilityNumber = self.define_stores.shape[0] + self.n_clusters
        demandLocations = self.X

        if (len(designatedFacilityLocations) >= totalFacilityNumber):
            return []

        maxDemandLocationNumber = math.ceil(len(demandLocations) / totalFacilityNumber)

        totalDesignatedFacilityLocationNumber = len(designatedFacilityLocations)
        totalDemandLocationNumber = len(demandLocations)
        totalCandidateLocationNumber = totalDesignatedFacilityLocationNumber + totalDemandLocationNumber

        solver0 = pywraplp.Solver.CreateSolver('GLOP')
        x0 = {}
        y0 = {}
        for i in range(totalCandidateLocationNumber):
            y0[i] = solver0.NumVar(0.0, 1.0, 'y')
            for j in range(totalCandidateLocationNumber):
                x0[i, j] = solver0.NumVar(0.0, 1.0, 'x')

        # Each demandLocation is assigned to 1 facilityLocation.
        for i in range(totalDemandLocationNumber):
            solver0.Add(solver0.Sum(x0[i, j] for j in range(totalCandidateLocationNumber)) == 1)

        for i in range(totalDemandLocationNumber):
            for j in range(totalCandidateLocationNumber):
                solver0.Add(x0[i, j] <= y0[j])

        # Each designatedFacilityLocation is assigned to at most maxFacilityNumber demandLocations.
        for j in range(totalCandidateLocationNumber):
            solver0.Add(solver0.Sum([x0[i, j] for i in range(totalDemandLocationNumber)]) <= maxDemandLocationNumber)

        for i in range(totalDemandLocationNumber, totalCandidateLocationNumber):
            solver0.Add(y0[i] == 1)
            solver0.Add(solver0.Sum([x0[i, j] for j in range(totalCandidateLocationNumber)]) == 0)

        solver0.Add(solver0.Sum([y0[i] for i in range(totalCandidateLocationNumber)]) == totalFacilityNumber)

        # Objective
        objective_terms0 = []
        for i in range(totalDemandLocationNumber):
            for j in range(totalDemandLocationNumber):
                objective_terms0.append(
                    self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                          demandLocations.loc[j][[self.longitude, self.latitude]].values)
                    * demandLocations.loc[i][self.prod_output]
                    * demandLocations.loc[i][self.trans_rate] * x0[i, j])
            for j in range(totalDemandLocationNumber, totalCandidateLocationNumber):
                objective_terms0.append(
                    self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                          designatedFacilityLocations[j - totalDemandLocationNumber])
                    * demandLocations.loc[i][self.prod_output]
                    * demandLocations.loc[i][self.trans_rate] * x0[i, j])
        solver0.Minimize(solver0.Sum(objective_terms0))

        status0 = solver0.Solve()

        y_result = []

        if status0 == pywraplp.Solver.OPTIMAL:
            print(f'Relaxed model total cost = {solver0.Objective().Value()}\n')
            for i in range(totalCandidateLocationNumber):
                y_result.append(y0[i].solution_value())
        else:
            print('No solution found111.')

        max_indices = np.argpartition(np.array(y_result), -totalFacilityNumber)[-totalFacilityNumber:]

        model = cp_model.CpModel()
        x = {}
        y = {}
        for i in range(totalCandidateLocationNumber):
            y[i] = model.NewBoolVar(f'y[{i}]')
            for j in range(totalCandidateLocationNumber):
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

        # Each demandLocation is assigned to 1 designatedFacilityLocation.
        for i in range(totalDemandLocationNumber):
            model.Add(sum([x[i, j] for j in range(totalCandidateLocationNumber)]) == 1)

        for i in range(totalDemandLocationNumber):
            for j in range(totalCandidateLocationNumber):
                model.Add(x[i, j] <= y[j])

        # Each designatedFacilityLocation is assigned to at most maxFacilityNumber demandLocations.
        for j in range(totalCandidateLocationNumber):
            model.Add(sum([x[i, j] for i in range(totalDemandLocationNumber)]) <= maxDemandLocationNumber)

        for i in range(totalDemandLocationNumber, totalCandidateLocationNumber):
            model.Add(y[i] == 1)
            model.Add(sum([x[i, j] for j in range(totalCandidateLocationNumber)]) == 0)

        for max_index in max_indices:
            model.Add(y[max_index] == 1)

        model.Add(sum([y[i] for i in range(totalCandidateLocationNumber)]) == totalFacilityNumber)

        # Objective
        objective_terms = []
        for i in range(totalDemandLocationNumber):
            for j in range(totalDemandLocationNumber):
                objective_terms.append(
                    int(self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                              demandLocations.loc[j][[self.longitude, self.latitude]].values)
                        * demandLocations.loc[i][self.prod_output]
                        * demandLocations.loc[i][self.trans_rate] * 1000) * x[i, j])
            for j in range(totalDemandLocationNumber, totalCandidateLocationNumber):
                objective_terms.append(
                    int(self._getDistanceBall(demandLocations.loc[i][[self.longitude, self.latitude]].values,
                                              designatedFacilityLocations[j - totalDemandLocationNumber])
                        * demandLocations.loc[i][self.prod_output]
                        * demandLocations.loc[i][self.trans_rate] * 1000) * x[i, j])
        model.Minimize(sum(objective_terms))

        # Solve
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        initNewFacilityLocations = []
        # Print solution.
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f'Total cost = {solver.ObjectiveValue()}\n')
            for i in range(totalDemandLocationNumber):
                if solver.BooleanValue(y[i]):
                    facilityLocation = demandLocations.loc[i][[self.longitude, self.latitude]].values
                    initNewFacilityLocations.append(facilityLocation)
        else:
            print('No solution found.')

        ort_init = np.vstack((self.define_stores[:, 1:], np.array(initNewFacilityLocations)))

        return ort_init

    def _initStores(self):
        '''
        初始化仓：根据init参数选择使用的初始化仓方法
        '''
        init_stores = None
        if self.init == 'random':
            init_stores = self._rdInitStores()
        elif self.init == 'kmeans':
            init_stores = self._kmInitStores()
        elif self.init == 'or-tools':
            init_stores = self._ortInitStoresNew()
        else:
            init_stores = None

        return init_stores

    def _getDistanceBall(self, p1, p2):
        '''
        计算点与仓库的球面距离
        p1,p2均是list: [longitude, latitude]
        '''
        # 使用flipud反转np.array是因为haversine_distances方法需要纬度在前。
        dis = haversine_distances([[radians(_) for _ in np.flipud(p1)],
                                   [radians(_) for _ in np.flipud(p2)]])[0][
                  1] * 6371393 / 1000  # multiply by Earth radius to get kilometers

        return dis * self.dis_coef

    def _getDistanceEul(self, p1, p2):
        '''
        计算点与仓库的欧式距离
        p1,p2均是list: [longitude, latitude]
        '''
        dis = math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))

        return dis

    def _classifyPoint(self):
        '''
        为每个点选择最近的仓当作它的仓
        '''
        label = np.zeros(self.X_p.shape[0], dtype=np.int32)
        for i, p in enumerate(self.X_p.values):
            # 计算每一个data到所有store的距离，然后选择最近的store
            distances = np.array([self._getDistanceBall(p, s) for s in self.stores])
            label[i] = distances.argmin()
        #             label[i] = self.stores[distances.argmin()]

        return label

    def _gravityMethodDist(self, data):
        '''
        重心法，重心法的输入是dataframe
        '''
        WC = np.array(data[self.prod_output]) * np.array(data[self.trans_rate])
        lon = np.array(data[self.longitude])
        lat = np.array(data[self.latitude])
        data_p = np.array(data[[self.longitude, self.latitude]])
        # 计算初始重心,初始距离,初始总费用
        x_i = (lon * WC).sum() / WC.sum()
        y_i = (lat * WC).sum() / WC.sum()
        s_i = np.array([x_i, y_i])
        # di的后面加0.0001的目的是防止di=0后无法作为分母
        # 但这样有一个问题，就是当单点被分为一类的时候，该点会单独成为一个仓。
        di = np.array([self._getDistanceEul(p, s_i) for p in data_p]) + 0.000001
        s_list = [np.array([0, 0])]
        s_list.append(s_i)
        n = 1
        # 开始循环迭代，满足最后一次选址比上次距离小于10km
        while self._getDistanceEul(s_list[-1], s_list[-2]) >= 0.000001:
            x_i = ((lon * WC) / di).sum() / (WC / di).sum()
            y_i = ((lat * WC) / di).sum() / (WC / di).sum()
            s_i = np.array([x_i, y_i])
            di = np.array([self._getDistanceEul(p, s_i) for p in data_p]) + 0.000001
            s_list.append(s_i)
            n = n + 1
        #             print('重心法：第{}次'.format(n))

        return s_list[-1]

    def _gravityMethodCost(self, data):
        '''
        重心法，重心法的输入是dataframe
        '''
        WC = np.array(data[self.prod_output]) * np.array(data[self.trans_rate])
        lon = np.array(data[self.longitude])
        lat = np.array(data[self.latitude])
        data_p = np.array(data[[self.longitude, self.latitude]])
        # 计算初始重心,初始距离,初始总费用
        x_i = (lon * WC).sum() / WC.sum()
        y_i = (lat * WC).sum() / WC.sum()
        s_i = np.array([x_i, y_i])
        # 但这样有一个问题，就是当单点被分为一类的时候，该点会单独成为一个仓。
        di = np.array([self._getDistanceBall(p, s_i) for p in data_p]) + 0.000001
        Ti = (WC * di).sum()
        T_list = [float('inf')]
        T_list.append(Ti)
        n = 1
        # 开始循环迭代，满足最后一次选址比上次距离小于10km
        while (T_list[-2] - T_list[-1]) / (T_list[-1]) >= 0.000001:
            x_i = ((lon * WC) / di).sum() / (WC / di).sum()
            y_i = ((lat * WC) / di).sum() / (WC / di).sum()
            s_i = np.array([x_i, y_i])
            di = np.array([self._getDistanceBall(p, s_i) for p in data_p]) + 0.000001
            Ti = (WC * di).sum()
            T_list.append(Ti)
            n = n + 1
        #             print('重心法：第{}次'.format(n))

        return s_i

    def _updateStores(self, label):
        '''
        为每一类点，使用重心法优化仓的位置
        '''
        # 先按照label把数据分成对应的cluster，clusters: [df,df,df]
        clusters = [pd.DataFrame() for i in range(self.define_stores.shape[0] + self.n_clusters)]
        for i, x in enumerate(label):
            # cluster[0]代表label是0的
            clusters[x] = clusters[x].append(self.X.loc[i])
            # 挑出参与迭代的df,cluser[0] -> label=0 -> distances.argmin()=0 -> X[i]到第0个stores距离近，
        # stores的前n个为define_stores，所以不参与迭代。
        cal_center_clusters = clusters[self.define_stores.shape[0]:]
        # 为每一个需要更新重心的cluster使用重心法计算store
        cal_stores = np.array([self._gravityMethodCost(cluster) for cluster in cal_center_clusters
                               if cluster.size > 0])
        update_stores = np.vstack((self.define_stores[:, 1:], cal_stores))

        return update_stores

    def _clusterStop(self, label, newLabel, iteration):
        '''
        判断聚类是否收敛
        '''
        if iteration > self.max_iter:
            return True
        return np.array_equal(label, newLabel)

    def fit(self, X, name, longitude, latitude, prod_output, trans_rate):
        '''
        主函数，循环迭代，直到每个仓到它自己点的花费都最优
        '''
        self.longitude = longitude
        self.latitude = latitude
        self.prod_output = prod_output
        self.trans_rate = trans_rate
        self.X_all = X
        self.X = X[[name, longitude, latitude, prod_output, trans_rate]]  # 输入数据X,有5个纬度：name,log,lat,W,C
        self.X_p = X[[longitude, latitude]]  # X的2维，log,lat

        # 第一种情况：只指定仓不新建仓
        if self.n_clusters == 0:
            self.stores = self.define_stores[:, 1:]
            self.label = self._classifyPoint()
        else:  # 第二种情况：指定仓+新建仓
            iteration = 0
            oldlabel = np.zeros(self.X_p.shape[0], dtype=np.int32)  # 定义老的label全0
            self.stores = self._initStores()
            newlabel = self._classifyPoint()
            while not self._clusterStop(oldlabel, newlabel, iteration):
                oldlabel = np.copy(newlabel)
                iteration = iteration + 1
                self.stores = self._updateStores(newlabel)
                newlabel = self._classifyPoint()
            self.label = newlabel

    def _getAddress(self, lon, lat):
        '''
        predict辅助函数：根据经纬度获取地址，此部分需联网才能使用。
        '''
        address = geolocator.reverse(str(lat) + "," + str(lon)).address

        return address

    def _geneDistance(self, label, stores, lon, lat):
        '''
        predict辅助函数：需求点列表中添加仓、距离。
        '''
        store_coordinate = [float(stores[label][1]), float(stores[label][2])]
        point_coordinate = [lon, lat]
        distance = self._getDistanceBall(store_coordinate, point_coordinate)

        return distance

    def predict(self):
        '''
        函数给出3个结果：
        df_stores: 仓库列表
        df_points: 需求点列表
        dict_result: 给出需求点与仓的关系字典,用于画图
        '''
        stores = []  # 仓库列表
        dict_result = {}  # 仓库与需求点对应关系字典
        print('生成需求点与仓库的关系字典……')
        # 只指定仓不新建仓
        if self.n_clusters == 0:
            for s in self.define_stores:
                stores.append(tuple(s))
                dict_result[tuple(s)] = []
            for l, p in zip(self.label, self.X.values[:, :3]):
                dict_result[stores[l]].append(tuple(p))
        else:  # 指定仓+新建仓
            stores_list = np.vstack((self.define_stores,
                                     [tuple(['新建仓{}'.format(i + 1)] + list(s))
                                      for i, s in enumerate(self.stores[self.define_stores.shape[0]:])]))
            for s in stores_list:
                stores.append(tuple(s))
                dict_result[tuple(s)] = []
            for l, p in zip(self.label, self.X.values[:, :3]):
                dict_result[stores[l]].append(tuple(p))

        print('生成仓库列表……')
        # 计算仓库列表：df_stores
        df_stores = pd.DataFrame(stores, columns=['仓库', '经度', '纬度'])
        print('联网获取仓库列表详细地址……')
        try:
            df_stores['地址'] = df_stores.apply(lambda row: self._getAddress(row['经度'], row['纬度']), axis=1)
        except:
            print('地址未获取成功！')
            df_stores['地址'] = None

        print('生成需求点列表……')
        # 计算需求点列表：df_points
        df_points = self.X_all.copy()
        df_points['label'] = self.label
        df_points['仓库'] = df_points['label'].apply(lambda x: stores[x][0])
        df_points['距离'] = df_points.apply(lambda row: self._geneDistance(row['label'],
                                                                         stores, row['经度'], row['纬度']), axis=1)
        df_points = df_points.drop('label', axis=1)
        df_points['总成本'] = df_points[self.prod_output] * df_points[self.trans_rate] * df_points['距离']

        return df_stores, df_points, dict_result


if __name__ == '__main__':
    data = pd.read_excel('./模拟数据.xlsx', sheet_name='需求点')

    # 不指定仓
    mcg = MultiCenterGravity(n_clusters=4, seed=42, init='kmeans')
    mcg.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
    df_stores, df_points, dict_result = mcg.predict()

    # 指定仓
    stores = pd.read_excel('./模拟数据.xlsx', sheet_name='指定仓')
    mcgds = MultiCenterGravityDefineStores(n_clusters=2, seed=42, init='or-tools')
    # 指定仓sheet只有3个字段：仓库名、经度、纬度
    mcgds.setDefineStores(stores, '详细地址', '经度', '纬度')
    mcgds.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
    df_stores, df_points, dict_result = mcgds.predict()