import uuid
class Client:
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class Vehicle:
    def __init__(self, capasity: float, clients_list: list, vehicle_id: str = None, current_load: float = 0):
        self.vehicle_id = vehicle_id if vehicle_id else str(uuid.uuid4())
        self.capasity = capasity
        self.current_laod = current_load
        self.clients_list = clients_list

    def load_cargo(self, сlient: Client) -> bool:
        new_load = self.current_laod + Client.cargo_weight
        if new_load > self.capasity:
            print('вес привышает максимальную грузоподъемность')
            return False
        
        self.clients_list.append(client)

if __name__ =="__main__":       
    a = Vehicle(
        capasity=1000.0,
        clients_list=[]
    )
    print(a)

