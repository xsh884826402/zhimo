class Vehicle:
    def __init__(self, id, name, count, max_loading_number, max_loading_weight, max_loading_volume, max_working_time_per_shift, resting_time_between_shifts):
        self.id = id
        self.name = name
        self.count = count
        self.max_loading_number = max_loading_number
        self.max_loading_weight = max_loading_weight
        self.max_loading_volume = max_loading_volume
        self.max_working_time_per_shift = max_working_time_per_shift
        self.resting_time_between_shifts = resting_time_between_shifts


    def __str__(self):
        return f'vehicle id: {self.id}, name: {self.name}, count: {self.count}, max_loading_number: {self.max_loading_number}, \
            max_loading_weight: {self.max_loading_weight}, max_loading_volume: {self.max_loading_volume}, \
            max_working_time_per_shift: {self.max_working_time_per_shift}, resting_time_between_shifts: {self.resting_time_between_shifts}'
