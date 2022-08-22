from utils.WarehouseLocation import *
import os


def getWarehouseLocationControllerService(data, spec_warehouses_data='df', algorithm_type='综合最优', bool_spec_warehouse=False, n_clusters=4, result_dir = './data'):

    message_dict = dict()
    message_dict['status'] = True
    message_dict['message'] = ''
    algorithm_map = {'运算最快': 'random', '综合最优': 'kmeans', '效果最优': 'or-tools'}

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
    map_json_list = []
    for k in dict_result.keys():
        for v in dict_result[k]:
            map_json_list.append({'coords': [[k[1], k[2]], [v[1], v[2]]]})
    return map_json_list


