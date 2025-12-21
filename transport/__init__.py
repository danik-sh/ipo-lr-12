import uuid


class Client:
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip


class Vehicle:
    def __init__(self, capacity: float, vehicle_id: str = None, current_load: float = 0):
        self.vehicle_id = vehicle_id if vehicle_id else str(uuid.uuid4())
        self.capacity = capacity
        self.current_load = current_load
        self.clients_list = []

    def load_cargo(self, client: Client) -> bool:
        if not isinstance(client, Client):
            return False
        
        new_load = self.current_load + client.cargo_weight
        
        if new_load > self.capacity:
            print('Вес превышает максимальную грузоподъемность')
            return False

        self.current_load = new_load
        
        self.clients_list.append(client)
        return True
    
    def __str__(self) -> str:
        return f"Транспорт ID: {self.vehicle_id}, Грузоподъемность: {self.capacity} т, Текущая загрузка: {self.current_load} т"

class Train(Vehicle):
    def __init__(self, capacity: float, number_of_cars: int):
        super().__init__(capacity)
        self.numbers_of_cars = number_of_cars

class Airplane(Vehicle):
    def __init__(self, capacity: float, max_altitude: float):
        super().__init__(capacity)
        self.max_altitude = max_altitude

class TransportCompany:
    def __init__(self, name: str):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print(f"Добавлено ТС: {vehicle.vehicle_id}")
    
    def list_vehicles(self):
        return self.vehicles
    
    def add_client(self, client):
        self.clients.append(client)
        print(f"Добавлен клиент: {client.name}")
    
    def list_clients(self):
        return self.clients
    
    def optimize_cargo_distribution(self):
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        sorted_vehicles = sorted(self.vehicles, 
                               key=lambda v: v.capacity, 
                               reverse=True)
        
        for client in vip_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            
            if not loaded:
                print(f"Не удалось загрузить VIP клиента {client.name}")
        
        for client in regular_clients:
            loaded = False
            for vehicle in sorted_vehicles:
                if vehicle.load_cargo(client):
                    loaded = True
                    break
            
            if not loaded:
                print(f"Не удалось загрузить клиента {client.name}")
        
        used_vehicles = [v for v in self.vehicles if v.current_load > 0]
        print(f"Использовано транспорта: {len(used_vehicles)} из {len(self.vehicles)}")
        return used_vehicles