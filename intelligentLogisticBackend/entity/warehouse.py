class Warehouse:
    '''
    仓库信息
    '''
    def __init__(self, store_id, name, province, city, address, 
                 longitude, latitude, start_time, end_time):
        self.store_id = store_id
        self.name = name
        self.province = province
        self.city = city
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.start_time = start_time   #时间窗开始时间
        self.end_time = end_time       #时间窗结束时间
        self.available_vehicles = []

    def __str__(self):
        return f'store_id: {self.store_id}, name: {self.name}, province: {self.province}, city: {self.city}, address: {self.address}, \
            longitude: {self.longitude}, latitude: {self.latitude}, start_time: {self.start_time}, end_time: {self.end_time}'