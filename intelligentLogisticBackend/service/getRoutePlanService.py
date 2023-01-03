import time
import numpy as np
import pandas as pd
import requests
from math import radians
from math import isnan
from sklearn.metrics.pairwise import haversine_distances
from entity.demand import Demand
from entity.warehouse import Warehouse
from entity.waybill import Waybill
from entity.vehicle import Vehicle
from entity.available_vehicles import AvailableVehicleInfo

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def getDisTime(start_gis, end_gis):
    '''
    高德地图获取两个经纬度的dis，time
    '''
    try:
        url = 'https://restapi.amap.com/v3/direction/driving?'
        # 参数放入字典,经纬度小数点后不超过6位
        params = {'key': 'e7020b585662064e6ee9f34d40a583fc',
                  'origin': f'{start_gis[0]},{start_gis[1]}',
                  'destination': f'{end_gis[0]},{end_gis[1]}',
                  'extensions': 'base',
                  'strategy': 0,  # 速度优先
                  }
        res = requests.get(url, params).json()
        dis = res['route']['paths'][0]['distance']
        tm = res['route']['paths'][0]['duration']

    except:
        dis, tm = -1, -1

    return int(dis), int(tm)


def getDisTime2(start_gis, end_gis, vehicle_spd):
    '''
    计算点与仓库的球面距离、时间
    p1,p2均是list: [longitude, latitude]
    return: dis单位metre, tm单位second
    '''
    # 使用flipud反转np.array是因为haversine_distances方法需要纬度在前。
    # 根据供应链服务处统计，球面距离*1.17约为实际距离。
    dis = haversine_distances([[radians(_) for _ in np.flipud(start_gis)],
                               [radians(_) for _ in np.flipud(end_gis)]])[0][1] * 6371393 / 1000 * 1.17

    return int(dis * 1000), int(dis / vehicle_spd * 3600)


def getBaseData(inputFile):
    demandDF = pd.read_excel(inputFile, sheet_name='客户信息')
    warehouseDF = pd.read_excel(inputFile, sheet_name='仓库信息')
    vehicleDF = pd.read_excel(inputFile, sheet_name='运输工具')
    available_vehicle_infos_df = pd.read_excel(inputFile, sheet_name='可用运输工具')
    waybillDF = pd.read_excel(inputFile, sheet_name='运单')
    timewindowDF = pd.read_excel(inputFile, sheet_name='工作时间')

    # 获取demand信息
    demandDF2 = pd.merge(demandDF, waybillDF[['目的地', '数量', '重量', '体积']], how='left',
                         left_on='名称', right_on='目的地')
    demandDF3 = pd.merge(demandDF2, timewindowDF, how='left', left_on='名称', right_on='站点')

    demand_points = []
    for index, row in demandDF3.iterrows():
        demand_point = Demand(row['CustomerID'], row['名称'], row['地址'], row['经度'], row['纬度'],
                              row['数量'], row['重量'], row['体积'],
                              row['星期一上班时间'], row['星期一下班时间'])
        demand_points.append(demand_point)

    # 获取warehouse信息
    warehouseDF2 = pd.merge(warehouseDF, timewindowDF, how='left', left_on='名称', right_on='站点')

    warehouse_points = []
    for index, row in warehouseDF2.iterrows():
        warehouse_point = Warehouse(row['SiteID'], row['名称'], row['州/省'], row['城市'], row['地址'],
                                    row['经度'], row['纬度'],
                                    row['星期一上班时间'], row['星期一下班时间'])
        warehouse_points.append(warehouse_point)

    # 获取vehicle信息
    vehicles = []
    for index, row in vehicleDF.iterrows():
        vehicle = Vehicle(row['TransportationAssetID'], row['名称'], row['数量'],
                          row['整车最大装载数量'], row['整车最大装载重量'], row['整车最大装载体积'],
                          row['每班最长工作时间'], row['两班间休息时间'])
        vehicles.append(vehicle)

    available_vehicle_infos = []
    for index, row in available_vehicle_infos_df.iterrows():
        available_vehicle_info = AvailableVehicleInfo(row['ID'], row['站点'], row['运输工具'],
                                                      row['可用数量'], row['干线始发地'], row['干线目的地'], row['状态'])
        available_vehicle_infos.append(available_vehicle_info)

    # 获取waybill信息
    waybills = []
    for index, row in waybillDF.iterrows():
        waybill = Waybill(row['ID'], row['来源地'], row['目的地'], row['数量'], row['重量'], row['体积'], row['直接运输成本'])
        waybills.append(waybill)

    # 首先获取所有warehouse与demand的经纬度并存成字典
    coord_dict = {}
    for index, row in warehouseDF.iterrows():
        coord_dict[row['名称']] = [row['经度'], row['纬度']]
    for index, row in demandDF.iterrows():
        coord_dict[row['名称']] = [row['经度'], row['纬度']]

    # 根据'来源地'拆分waybill为多个子运单，为每个子运单创建一组names列表
    waybillgroup_list = []
    for name, subdf in waybillDF[['来源地', '目的地']].groupby('来源地'):
        subwaybill_names = np.append(np.unique(subdf['来源地'].values),
                                     np.unique(subdf['目的地'].values))
        waybillgroup_list.append(subwaybill_names)

    # 后续优化需要遍历waybillgroup_list,这次由于模拟数据只有一组subwaybill，所有直接取第一个
    # 构建这组subwaybill的dis_matrix, time_matrix.
    subwaybill = waybillgroup_list[0]
    dis_matrix = np.zeros((subwaybill.size, subwaybill.size))
    time_matrix = np.zeros((subwaybill.size, subwaybill.size))

    for frm_idx in range(subwaybill.size):
        for to_idx in range(subwaybill.size):
            if frm_idx != to_idx:
                frm_coord = coord_dict[subwaybill[frm_idx]]
                to_coord = coord_dict[subwaybill[to_idx]]
                dis, tm = getDisTime(frm_coord, to_coord)
                dis_matrix[frm_idx, to_idx] = dis
                time_matrix[frm_idx, to_idx] = tm

    # dis_matrix = {}
    # time_matrix = {}

    # for origin in subwaybill:
    #     for dest in subwaybill:
    #         if origin != dest:
    #             frm_coord = coord_dict[origin]
    #             to_coord = coord_dict[dest]
    #             dis, tm = getDisTime2(frm_coord, to_coord)
    #             dis_matrix[f'{origin}_{dest}'] = dis
    #             time_matrix[f'{origin}_{dest}'] = tm
    #         else:
    #             dis_matrix[f'{origin}_{dest}'] = 0.0
    #             time_matrix[f'{origin}_{dest}'] = 0.0

    return demand_points, warehouse_points, vehicles, available_vehicle_infos, waybills, dis_matrix, time_matrix


def create_data_model(warehouse, available_vehicles, related_waybills, dist_matrix, time_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = dist_matrix
    data['time_matrix'] = time_matrix
    data['demands_in_number'] = [0]
    data['demands_in_weight'] = [0]
    data['demands_in_volume'] = [0]
    for waybill in related_waybills:
        data['demands_in_number'].append(0 if isnan(waybill.number) else waybill.number)
        data['demands_in_weight'].append(0 if isnan(waybill.weight) else waybill.weight)
        data['demands_in_volume'].append(0 if isnan(waybill.volume) else waybill.volume)

    data['vehicle_capacities_in_number'] = []
    data['vehicle_capacities_in_weight'] = []
    data['vehicle_capacities_in_volume'] = []

    # self.max_working_time_per_shift = max_working_time_per_shift
    # self.resting_time_between_shifts = resting_time_between_shifts
    # TODO

    for available_vehicle in available_vehicles:
        data['vehicle_capacities_in_number'].append(
            0 if isnan(available_vehicle.max_loading_number) else available_vehicle.max_loading_number)
        data['vehicle_capacities_in_weight'].append(
            0 if isnan(available_vehicle.max_loading_weight) else available_vehicle.max_loading_weight)
        data['vehicle_capacities_in_volume'].append(
            0 if isnan(available_vehicle.max_loading_volume) else available_vehicle.max_loading_volume)

    data['num_vehicles'] = len(available_vehicles)
    data['available_vehicles'] = available_vehicles

    data['depot'] = 0
    data['warehouse'] = warehouse
    data['related_waybills'] = related_waybills

    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    res = []
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(data['available_vehicles'][vehicle_id].id)
        locations = []
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands_in_weight'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(
                data['warehouse'].name if (node_index == 0) else data['related_waybills'][node_index - 1].destination,
                route_load)
            locations.append(data['warehouse'] if (node_index == 0) else data['related_waybills'][node_index - 1])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)

        if (len(locations) > 1):
            res.append({'vehicle': data['available_vehicles'][vehicle_id], 'locations': locations})
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

    return res


def routine_algorithm(warehouse, available_vehicles, related_waybills, dist_matrix, time_matrix, time_limit):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(warehouse, available_vehicles, related_waybills, dist_matrix, time_matrix)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity in number constraint.
    def demand_in_number_callback(from_index):
        """Returns the demand number of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands_in_number'][from_node]

    demand_in_number_callback_index = routing.RegisterUnaryTransitCallback(
        demand_in_number_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_in_number_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities_in_number'],  # vehicle maximum capacities
        False,  # start cumul to zero
        'Capacity_number')

    # Add Capacity in weight constraint.
    def demand_in_weight_callback(from_index):
        """Returns the demand weight of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands_in_weight'][from_node]

    demand_in_weight_callback_index = routing.RegisterUnaryTransitCallback(
        demand_in_weight_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_in_weight_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities_in_weight'],  # vehicle maximum capacities
        False,  # start cumul to zero
        'Capacity_weight')

    # Add Capacity in volume constraint.
    def demand_in_volume_callback(from_index):
        """Returns the demand volume of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands_in_volume'][from_node]

    demand_in_volume_callback_index = routing.RegisterUnaryTransitCallback(
        demand_in_volume_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_in_volume_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities_in_volume'],  # vehicle maximum capacities
        False,  # start cumul to zero
        'Capacity_volume')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(time_limit)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution)


def routine_problem_case_with_input(warehouse, available_vehicles, related_waybills, dist_matrix, time_matrix,
                                    time_limit):
    return routine_algorithm(warehouse, available_vehicles, related_waybills, dist_matrix, time_matrix, time_limit)


def run_routine_algorithm(inputFile, time_limit):
    demand_points, warehouse_points, vehicles, available_vehicle_infos, waybills, dist_matrix, time_matrix = getBaseData(
        inputFile)

    print('demand_points')
    for demand_point in demand_points:
        print(demand_point)
    print('warehouse_points')
    for warehouse_point in warehouse_points:
        print(warehouse_point)
    print('vehicles')
    vehicle_dict = dict()
    for vehicle in vehicles:
        vehicle_dict[vehicle.name] = vehicle
        print(vehicle)
    print('available_vehicle_infos')
    for available_vehicle_info in available_vehicle_infos:
        print(available_vehicle_info)
    print('waybills')
    for waybill in waybills:
        print(waybill)
    print('dist_matrix')
    print(dist_matrix)
    print('time_matrix')
    print(time_matrix)

    res = []

    for warehouse_point in warehouse_points:
        available_vehicles = []
        for available_vehicle_info in available_vehicle_infos:
            if (available_vehicle_info.warehouse_name == warehouse_point.name):
                vehicle_template = vehicle_dict[available_vehicle_info.vehicle_name]
                for i in range(available_vehicle_info.available_number):
                    vehicle = Vehicle(str(vehicle_template.id) + '_' + str(i), vehicle_template.name, 1,
                                      vehicle_template.max_loading_number, vehicle_template.max_loading_weight,
                                      vehicle_template.max_loading_volume, vehicle_template.max_working_time_per_shift,
                                      vehicle_template.resting_time_between_shifts)
                    available_vehicles.append(vehicle)

        related_waybills = []
        for waybill in waybills:
            if (waybill.warehouse_name == warehouse_point.name):
                related_waybills.append(waybill)

        solution = routine_problem_case_with_input(warehouse_point, available_vehicles, related_waybills, dist_matrix,
                                                   time_matrix, time_limit)
        res.append({'warehouse': warehouse_point, 'solution': solution})

    print(res)

    return res

def getRoutePlanService(input_path):
    '''

    :param stores_path: 选定仓库地址
    :param points_path: 需求点地址
    :param time_cost_path: 时限成本地址
    :return: message_dict 和 新的stores文件
    '''

    message_dict = dict()
    message_dict['status'] = 'success'
    message_dict['message'] = ''

    # # 根据经纬度获取所属地市
    # try:
    #
    # except Exception as e:
    #     message_dict['status'] = 'fail'
    #     message_dict['message'] = repr(e)
    #     return message_dict, None
    print('here')
    # res = run_routine_algorithm(input_path, 5)
    res = {
        '济南仓': [
            [
                {'name': '济南仓', 'geoCoord': [117.2187, 36.65717]},
                {'name': 'BB60', 'geoCoord': [116.9677, 36.64082]},
                {'name': 'BB8A', 'geoCoord': [116.455335, 36.288724]},
                {'name': 'BB8B', 'geoCoord': [116.447678, 36.273443]},
                {'name': 'BB04', 'geoCoord': [117.0742, 36.64804]},
                {'name': 'BB43', 'geoCoord': [117.095027, 36.669696]},
                {'name': '济南仓', 'geoCoord': [117.2187, 36.65717]}
            ]
        ]
    }
    print('there')



    message_dict['routeplan'] = res
    return message_dict


if __name__ == '__main__':
    message_dict = getRoutePlanService('../data/routeplan_inputTemplate.xlsx')

