from utils.AddressToCoordinate import *


def getJingweiduByAddress(datapath, mapType='高德', sheet_name='需求点'):
    message_dict = {'status': 'success', 'message': ""}
    keys_dict = {'高德': 'f9c26925b7e4303e22a4ac67dc993ba7', '腾讯': 'BCIBZ-7FOWQ-QP75R-G2RKP-ZXDBK-IPBRI'}
    try:
        atc = AddressToCoordinate(mapType)
        atc.key = keys_dict[mapType]
        message = atc.getBatchCoordinate(datapath, sheet_name)
        return message
    except Exception as e:
        message_dict['status'] = 'fail'
        message_dict['message'] = str(e)
        return message_dict