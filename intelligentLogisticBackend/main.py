import os
import sys
from flask import Flask, render_template, request, Response, send_file, send_from_directory, make_response
from flask_cors import CORS
import pandas as pd
import json
from service.getWarehouseLocationControllerService import getWarehouseLocationControllerService
from service.getJingweiduByAddress import getJingweiduByAddress
from utils.check import *
from service.getTimeLimitService import getTimeLimitService


# 获取资源路径
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = Flask(__name__, static_url_path="", static_folder=resource_path('./resource'),
            template_folder=resource_path("./resource"))

# 允许全局跨域配置
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/write', methods=['post', 'get'])
def write_excel():
    print(request.args.get('filepath'))
    df = pd.read_excel(request.args.get('filepath'))
    print(df.head())
    df.to_excel(request.args.get('filepath') + '_modify.xlsx')
    return "success"


@app.route('/test', methods=['post', 'get'])
def test_flask():
    print(request)
    message = {'status': 'success'}
    print(message)
    return Response(json.dumps(message), mimetype='application/json')


@app.route('/upload/warehouseData', methods=['post'])
def uploadWarehouseData():
    print(request.files)
    file = request.files.get('file')
    file.save(input_file_path)
    message = {'status': 'success'}
    return Response(json.dumps(message), mimetype='application/json')




@app.route('/getWarehouseLocation', methods=['post'])
def getWarehouseLocationController():
    # to do 校验逻辑
    # 检查新建仓数量;检查需求点；如果指定仓，检查指定仓z
    # 获取经纬度
    message = {'status': 'success'}
    form_dict = request.get_json()

    # 检查输入文件的合法性
    # 检查需求点
    check_file = checkFile()
    data_demand_points = pd.read_excel(input_file_path, sheet_name='需求点')
    check_result = check_file.check(data_demand_points, file_type='需求点')
    # print(check_result, check_result['status'], type(check_result))
    if check_result['status'] != 'success':
        message = check_result
        return Response(json.dumps(message), mimetype='application/json')
    # 检查指定仓文件
    if form_dict['specWarehouse'] == '指定仓':
        data_spec_warehouse = pd.read_excel(input_file_path, sheet_name='指定仓')
        check_result = check_file.check(data_spec_warehouse, file_type='指定仓')
        if check_result['status'] != 'success':
            message = check_result
            return Response(json.dumps(message), mimetype='application/json')
    # 检查完毕

    # 获取经纬度
    get_result = getJingweiduByAddress(input_file_path, sheet_name='需求点')
    print(get_result)
    if get_result['status'] != 'success':
        return Response(json.dumps(get_result), mimetype='application/json')
    # 获取指定仓的经纬度，可选
    if form_dict['specWarehouse'] == '指定仓':
        get_result = getJingweiduByAddress(input_file_path, sheet_name='指定仓')
        if get_result['status'] != 'success':
            return Response(json.dumps(get_result), mimetype='application/json')

    if form_dict['specWarehouse'] == '指定仓':
        map_json = getWarehouseLocationControllerService(data=pd.read_excel(input_file_path, sheet_name='需求点'),
                                                         spec_warehouses_data=pd.read_excel(input_file_path,
                                                                                            sheet_name='指定仓'),
                                                         n_clusters=int(form_dict['warehouseLocationNumber']),
                                                         bool_spec_warehouse=True,
                                                         result_dir=base_dir)
    else:
        map_json = getWarehouseLocationControllerService(data=pd.read_excel(input_file_path, sheet_name='需求点'),
                                                         n_clusters=int(form_dict['warehouseLocationNumber']),
                                                         bool_spec_warehouse=False,
                                                         result_dir=base_dir)

    print('map_json', map_json)
    message = {'status': 'success'}
    message['message'] = 'success'
    message['map_json'] = map_json
    return Response(json.dumps(message), mimetype='application/json')


@app.route('/getTimeLimit', methods=['get', 'post'])
def getTimeLimitController():
    # to do 校验逻辑
    # 检查新建仓数量;检查需求点；如果指定仓，检查指定仓z
    # 获取经纬度
    message = {'status': 'success', 'message': '', 'filename': ""}
    # form_dict = request.get_json()
    print(request)
    message_dict, add_time_limit_path = getTimeLimitService(stores_path, points_path, time_cost_path, add_time_points_path)
    if message_dict['status'] == 'success':
        message_dict['filename'] = os.path.basename(add_time_points_path)
        response = make_response(send_file(add_time_points_path, as_attachment=True))
    else:
        print('在getTimeLimitController中', message_dict['message'])
        response = make_response()
    response.headers['message_dict'] = json.dumps(message_dict)
    response.headers['Access-Control-Expose-Headers'] = 'message_dict'
    return response




if __name__ == '__main__':
    base_dir = os.path.join(os.getcwd(), 'data')
    print('base dir', base_dir)
    # input_file_path = 'input.xlsx'
    input_file_path = os.path.join(base_dir, 'input.xlsx')
    stores_path = os.path.join(base_dir, 'stores.xlsx')
    points_path = os.path.join(base_dir, 'points.xlsx')
    time_cost_path = os.path.join(base_dir, 'line_time_cost')
    add_time_points_path = os.path.join(base_dir, 'add_time_points.xlsx')
    app.run(debug=True)
