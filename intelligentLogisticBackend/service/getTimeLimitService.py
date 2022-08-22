from utils.CoordinateToAddress import CoordinateToAddress
import pandas as pd
from utils.AddLineTimeCost import AddLineTimeCost


def getTimeLimitService(stores_path, points_path, time_cost_path, add_time_points_path):
    '''

    :param stores_path: 选定仓库地址
    :param points_path: 需求点地址
    :param time_cost_path: 时限成本地址
    :return: message_dict 和 新的stores文件
    '''

    message_dict = dict()
    message_dict['status'] = 'success'
    message_dict['message'] = ''

    # 根据经纬度获取所属地市
    cta = CoordinateToAddress('高德')
    cta.key = 'f9c26925b7e4303e22a4ac67dc993ba7'
    stores, message = cta.getStoresCity(pd.read_excel(stores_path))
    stores.to_excel(stores_path, index=False)
    if message != "success":
       message_dict['status'] = 'fail'
       message_dict['message'] = message
       return message_dict, None

    print('根据经纬度获取城市成功')

    # 加载模型跑出的stores,points表
    stores = pd.read_excel(stores_path)
    points = pd.read_excel(points_path)
    try:
        altc = AddLineTimeCost(time_cost_path)
        results, message = altc.addLineTime(stores, points)
        if message != 'success':
            message_dict['status'] = 'fail'
            message_dict['message'] = message
            return message_dict, None
        results.to_excel(add_time_points_path, index=False)
    except Exception as e:
        print('添加时限过程中出现异常', repr(e))
        message_dict['status'] = 'fail'
        message_dict['message'] = str(e)
        return message_dict, None

    message_dict['message'] = '计算完成！\n增加大网时限后的结果存储在{}文件中！'.format(add_time_points_path)
    return message_dict, add_time_points_path








