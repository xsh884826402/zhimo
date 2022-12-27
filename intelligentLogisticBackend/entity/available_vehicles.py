class AvailableVehicleInfo:
    '''
    仓库信息
    '''
    def __init__(self, id, warehouse_name, vehicle_name, available_number, origin, 
                 destination, state):
        self.id = id
        self.warehouse_name = warehouse_name
        self.vehicle_name = vehicle_name
        self.available_number = available_number
        self.origin = origin
        self.destination = destination
        self.state = state


    def __str__(self):
        return f'id: {self.id}, warehouse_name: {self.warehouse_name}, vehicle_name: {self.vehicle_name}, available_number: {self.available_number}, \
            origin: {self.origin}, destination: {self.destination}, state: {self.state}'