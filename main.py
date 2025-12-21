import sys
from transport import TransportCompany, Client, Vehicle, Train, Airplane


def create_sample_data():
    """Создание тестовых данных"""
    company = TransportCompany("Быстрая доставка")
    
    # Добавляем транспорт
    company.add_vehicle(Vehicle(capacity=5000))
    company.add_vehicle(Train(capacity=20000, number_of_cars=10))
    company.add_vehicle(Airplane(capacity=10000, max_altitude=11000))
    company.add_vehicle(Vehicle(capacity=3000))
    
    # Добавляем клиентов
    company.add_client(Client("VIP Иванов", 1500, is_vip=True))
    company.add_client(Client("Петров", 800))
    company.add_client(Client("VIP Сидоров", 2500, is_vip=True))
    company.add_client(Client("Смирнов", 600))
    company.add_client(Client("Кузнецов", 1200))
    
    return company


def print_menu():
    """Вывод меню"""
    print("\n" + "="*50)
    print("ТРАНСПОРТНАЯ КОМПАНИЯ - УПРАВЛЕНИЕ")
    print("="*50)
    print("1. Вывести все транспортные средства")
    print("2. Вывести всех клиентов")
    print("3. Добавить транспортное средство")
    print("4. Добавить клиента")
    print("5. Оптимизировать распределение грузов")
    print("6. Показать результат распределения")
    print("7. Загрузить груз клиента в транспорт")
    print("0. Выйти из программы")
    print("="*50)


def main():
    """Основная функция"""
    # Создаем или загружаем компанию
    company = create_sample_data()
    
    while True:
        print_menu()
        
        try:
            choice = int(input("Выберите пункт меню: "))
        except ValueError:
            print("Ошибка: введите число от 0 до 9")
            continue
        
        if choice == 0:
            print("Выход из программы...")
            sys.exit(0)
        
        elif choice == 1:
            # Вывести все транспортные средства
            print("\n--- ТРАНСПОРТНЫЕ СРЕДСТВА ---")
            if company.vehicles:
                for i, vehicle in enumerate(company.vehicles, 1):
                    print(f"{i}. {vehicle}")
                    if hasattr(vehicle, 'number_of_cars'):
                        print(f"   Вагонов: {vehicle.number_of_cars}")
                    if hasattr(vehicle, 'max_altitude'):
                        print(f"   Макс. высота: {vehicle.max_altitude} м")
                    print(f"   Клиентов загружено: {len(vehicle.clients_list)}")
            else:
                print("Транспортных средств нет")
        
        elif choice == 2:
            # Вывести всех клиентов
            print("\n--- КЛИЕНТЫ ---")
            if company.clients:
                for i, client in enumerate(company.clients, 1):
                    vip = "VIP" if client.is_vip else "Обычный"
                    print(f"{i}. {client.name} | Груз: {client.cargo_weight} кг | Статус: {vip}")
            else:
                print("Клиентов нет")
        
        elif choice == 3:
            # Добавить транспортное средство
            print("\n--- ДОБАВЛЕНИЕ ТРАНСПОРТА ---")
            print("1. Обычный транспорт")
            print("2. Поезд")
            print("3. Самолет")
            
            try:
                transport_type = int(input("Выберите тип: "))
                capacity = float(input("Грузоподъемность (кг): "))
                
                if transport_type == 1:
                    vehicle = Vehicle(capacity=capacity)
                    company.add_vehicle(vehicle)
                    print(f"Добавлен транспорт с ID: {vehicle.vehicle_id}")
                
                elif transport_type == 2:
                    cars = int(input("Количество вагонов: "))
                    vehicle = Train(capacity=capacity, number_of_cars=cars)
                    company.add_vehicle(vehicle)
                    print(f"Добавлен поезд с ID: {vehicle.vehicle_id}")
                
                elif transport_type == 3:
                    altitude = float(input("Максимальная высота полета (м): "))
                    vehicle = Airplane(capacity=capacity, max_altitude=altitude)
                    company.add_vehicle(vehicle)
                    print(f"Добавлен самолет с ID: {vehicle.vehicle_id}")
                
                else:
                    print("Неверный тип транспорта")
            
            except ValueError:
                print("Ошибка ввода данных")
        
        elif choice == 4:
            # Добавить клиента
            print("\n--- ДОБАВЛЕНИЕ КЛИЕНТА ---")
            name = input("Имя клиента: ")
            weight = float(input("Вес груза (кг): "))
            
            vip_input = input("VIP клиент? (да/нет): ").lower()
            is_vip = vip_input in ['да', 'yes', 'y', 'д']
            
            client = Client(name=name, cargo_weight=weight, is_vip=is_vip)
            company.add_client(client)
            print(f"Добавлен клиент: {name}")
        
        elif choice == 5:
            # Оптимизировать распределение грузов
            print("\n--- ОПТИМИЗАЦИЯ РАСПРЕДЕЛЕНИЯ ---")
            
            # Сбрасываем загрузку транспорта
            for vehicle in company.vehicles:
                vehicle.current_load = 0
                vehicle.clients_list = []
            
            # Запускаем оптимизацию
            used_vehicles = company.optimize_cargo_distribution()
            print(f"\nРаспределение завершено!")
            print(f"Использовано транспорта: {len(used_vehicles)} из {len(company.vehicles)}")
        
        elif choice == 6:
            # Показать результат распределения
            print("\n--- РЕЗУЛЬТАТ РАСПРЕДЕЛЕНИЯ ---")
            total_loaded = 0
            total_capacity = 0
            
            for i, vehicle in enumerate(company.vehicles, 1):
                if vehicle.current_load > 0:
                    print(f"\nТранспорт {i} ({vehicle.vehicle_id}):")
                    print(f"  Загружено: {vehicle.current_load} / {vehicle.capacity} кг")
                    print(f"  Клиенты ({len(vehicle.clients_list)}):")
                    
                    for client in vehicle.clients_list:
                        vip = "VIP" if client.is_vip else ""
                        print(f"    - {client.name} {client.cargo_weight} кг {vip}")
                    
                    total_loaded += vehicle.current_load
                total_capacity += vehicle.capacity
            
            print(f"\nИтого: загружено {total_loaded} из {total_capacity} кг")
        
        elif choice == 7:
            # Загрузить груз клиента в транспорт вручную
            print("\n--- РУЧНАЯ ЗАГРУЗКА ---")
            
            if not company.clients:
                print("Нет клиентов")
                continue
            
            if not company.vehicles:
                print("Нет транспорта")
                continue
            
            # Выбор клиента
            print("\nДоступные клиенты:")
            for i, client in enumerate(company.clients, 1):
                vip = "VIP" if client.is_vip else ""
                print(f"{i}. {client.name} ({client.cargo_weight} кг) {vip}")
            
            try:
                client_idx = int(input("Выберите клиента: ")) - 1
                if 0 <= client_idx < len(company.clients):
                    client = company.clients[client_idx]
                    
                    # Выбор транспорта
                    print("\nДоступный транспорт:")
                    for i, vehicle in enumerate(company.vehicles, 1):
                        free = vehicle.capacity - vehicle.current_load
                        print(f"{i}. {vehicle.vehicle_id} (свободно: {free} кг)")
                    
                    vehicle_idx = int(input("Выберите транспорт: ")) - 1
                    if 0 <= vehicle_idx < len(company.vehicles):
                        vehicle = company.vehicles[vehicle_idx]
                        
                        if vehicle.load_cargo(client):
                            print(f"Груз клиента {client.name} загружен в {vehicle.vehicle_id}")
                        else:
                            print("Не удалось загрузить груз")
                    else:
                        print("Неверный номер транспорта")
                else:
                    print("Неверный номер клиента")
            
            except ValueError:
                print("Ошибка ввода")
        
        else:
            print("Неверный пункт меню. Выберите от 0 до 9")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()