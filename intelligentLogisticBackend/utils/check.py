class check(object):

    def check(self):
        message_dict = {}
        message_dict['status'] = 'success'
        message_dict['message'] = ''
        return message_dict


class checkFile(check):
    def check(self, data, file_type):
        '''

        :param data: 待检查文件
        :param file_type: 根据检查的文件类型制定对应的逻辑
        :return: message_dict
        '''
        message_dict = {}
        message_dict['status'] = 'success'
        message_dict['message'] = ''
        if file_type == "需求点":

            if data.columns.tolist() != ['客户名称', '省份', '城市', '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）']:
                message_dict['message'] = '仓库详情数据文件不符合模板要求'
                message_dict['status'] = 'fail'
                return message_dict
            elif data['客户名称'].count() != data.shape[0]:
                message_dict['message'] = "客户名称列存在空值！！！"
                message_dict['status'] = 'fail'
                return message_dict
            elif data['客户名称'].nunique() < data.shape[0]:
                message_dict['message'] =  "客户名称列存在重复值！！！"
                message_dict['status'] = 'fail'
                return message_dict
            elif data['详细地址'].count() != data.shape[0]:
                message_dict['message'] =  "详细地址列存在空值！！！"
                message_dict['status'] = 'fail'
                return message_dict
            elif data['详细地址'].nunique() < data.shape[0]:
                message_dict['message'] = "详细地址列存在重复值！！！"
                message_dict['status'] = 'fail'
                return message_dict
            return message_dict

        elif file_type == "指定仓":

            if data.shape[0] == 0:
                message_dict['message'] = "指定仓数据为空"
                message_dict['status'] = 'fail'
                return message_dict
            elif data['详细地址'].count() != data.shape[0]:
                message_dict['message'] = "详细地址列存在空值！！！"
                message_dict['status'] = 'fail'
                return message_dict
            elif data['详细地址'].nunique() < data.shape[0]:
                message_dict['message'] = "详细地址列存在重复值！！！"
                message_dict['status'] = 'fail'
                return message_dict
        return message_dict


class checkParam(check):
    pass