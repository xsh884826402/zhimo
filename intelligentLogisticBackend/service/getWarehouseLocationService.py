from utils.WarehouseLocation import *
import os


def getWarehouseLocationService(data, spec_warehouses_data='df', algorithm_type='综合最优', bool_spec_warehouse=False, n_clusters=4, result_dir ='./data'):

    message_dict = dict()
    message_dict['status'] = 'success'
    message_dict['message'] = ''
    algorithm_map = {'运算最快': 'random', '综合最优': 'kmeans', '效果最优': 'or-tools'}

    if algorithm_type not in algorithm_map.keys():
        message_dict['status'] = 'fail'
        message_dict['message'] = '选定的算法种类暂不支持'
        return message_dict
    try:
        if bool_spec_warehouse:
                mcgds = MultiCenterGravityDefineStores(n_clusters=n_clusters, seed=42,
                                                                         init=algorithm_map[algorithm_type])
                mcgds.setDefineStores(spec_warehouses_data, '详细地址', '经度', '纬度')
                mcgds.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
                df_stores, df_points, dict_result = mcgds.predict()

        else:
            mcg = MultiCenterGravity(n_clusters=n_clusters, seed=1011, init=algorithm_map[algorithm_type])
            mcg.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
            df_stores, df_points, dict_result = mcg.predict()


        # 保存结果文件
        df_stores_path = os.path.join(result_dir, 'stores.xlsx')
        df_points_path = os.path.join(result_dir, 'points.xlsx')

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        df_stores.to_excel(df_stores_path, index=False)
        df_points.to_excel(df_points_path, index=False)
        # to do 计算地图
        map_list = []
        for k in dict_result.keys():
            for v in dict_result[k]:
                map_list.append({'coords': [[k[1], k[2]], [v[1], v[2]]]})
        message_dict['map_list'] = map_list
        return message_dict
    except Exception as e:
        message_dict['status'] = 'fail'
        message_dict['message'] = repr(e)
        return message_dict

