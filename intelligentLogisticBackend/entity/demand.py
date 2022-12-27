class Demand:
    '''
    需求点信息
    '''

    def __init__(self, points_id, name, address, longitude, latitude,
                 demand_num, demand_weight, demand_volume,
                 start_time, end_time):
        self.points_id = points_id
        self.name = name
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.demand_num = demand_num  # 需求数量
        self.demand_weight = demand_weight  # 需求重量
        self.demand_volume = demand_volume  # 需求体积
        self.start_time = start_time  # 时间窗起始时间
        self.end_time = end_time  # 时间窗结束时间

    def __str__(self):
        return f'points_id: {self.points_id}, name: {self.name}, address: {self.address}, longitude: {self.longitude}, latitude: {self.latitude}, \
            demand_num: {self.demand_num}, demand_weight: {self.demand_weight}, demand_volume: {self.demand_volume}, start_time: {self.start_time}, \
            end_time: {self.end_time}'
