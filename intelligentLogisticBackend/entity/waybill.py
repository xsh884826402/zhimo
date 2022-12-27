class Waybill:
    '''
    运单信息
    '''
    def __init__(self, bill_id, warehouse_name, destination, number, weight, volume, direct_trans_cost):
        self.bill_id = bill_id
        self.warehouse_name = warehouse_name
        self.destination = destination
        self.number = number
        self.weight = weight
        self.volume = volume         
        self.direct_trans_cost = direct_trans_cost

    
    def __str__(self):
        return f'bill_id: {self.bill_id}, warehouse_name: {self.warehouse_name}, destination: {self.destination}, \
            number: {self.number} weight: {self.weight} volume: {self.volume} direct_trans_cost: {self.direct_trans_cost}'