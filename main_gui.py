# -*- coding: utf-8 -*-
"""
GUI for Transport Company
"""

import dearpygui.dearpygui as dpg
from transport import TransportCompany, Client, Vehicle, Train, Airplane

# Global variables
current_company = TransportCompany("Fast Delivery")

def create_sample_data():
    """Create sample data"""
    global current_company
    
    # Add vehicles
    current_company.add_vehicle(Vehicle(capacity=5000))
    current_company.add_vehicle(Train(capacity=20000, number_of_cars=10))
    current_company.add_vehicle(Airplane(capacity=10000, max_altitude=11000))
    current_company.add_vehicle(Vehicle(capacity=3000))
    
    # Add clients
    current_company.add_client(Client("VIP Ivanov", 1500, is_vip=True))
    current_company.add_client(Client("Petrov", 800))
    current_company.add_client(Client("VIP Sidorov", 2500, is_vip=True))
    current_company.add_client(Client("Smirnov", 600))
    current_company.add_client(Client("Kuznetsov", 1200))

def show_about():
    """Show about window"""
    with dpg.window(label="About", modal=True, show=True, tag="modal_about"):
        dpg.add_text("Transport Company")
        dpg.add_text("Version 1.0")
        dpg.add_text("Variant 12")
        dpg.add_text("Developer: Student")
        dpg.add_separator()
        dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item("modal_about"))

def show_add_client():
    """Show add client window"""
    with dpg.window(label="Add Client", width=400, height=300, show=True, tag="add_client_win"):
        dpg.add_text("Client Name:")
        dpg.add_input_text(tag="client_name_input", default_value="")
        
        dpg.add_text("Cargo Weight (kg):")
        dpg.add_input_float(tag="client_weight_input", default_value=100.0, min_value=0.1, max_value=10000.0)
        
        dpg.add_checkbox(label="VIP Client", tag="client_vip_input")
        
        dpg.add_spacing(count=2)
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_client)
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("add_client_win"))

def save_client():
    """Save client"""
    global current_company
    
    name = dpg.get_value("client_name_input").strip()
    weight = dpg.get_value("client_weight_input")
    is_vip = dpg.get_value("client_vip_input")
    
    if not name or weight <= 0:
        dpg.set_value("status_text", "Error: invalid data")
        return
    
    client = Client(name, weight, is_vip)
    current_company.add_client(client)
    
    update_clients_table()
    dpg.delete_item("add_client_win")
    dpg.set_value("status_text", f"Client added: {name}")

def show_add_vehicle():
    """Show add vehicle window"""
    with dpg.window(label="Add Vehicle", width=400, height=350, show=True, tag="add_vehicle_win"):
        dpg.add_text("Vehicle Type:")
        dpg.add_combo(items=["Truck", "Train", "Airplane"], 
                     default_value="Truck", tag="vehicle_type_input")
        
        dpg.add_text("Capacity (kg):")
        dpg.add_input_float(tag="vehicle_capacity_input", default_value=1000.0, 
                           min_value=100.0, max_value=100000.0)
        
        with dpg.group(tag="train_group", show=False):
            dpg.add_text("Number of cars:")
            dpg.add_input_int(tag="train_cars_input", default_value=10, min_value=1)
        
        with dpg.group(tag="plane_group", show=False):
            dpg.add_text("Max altitude (m):")
            dpg.add_input_float(tag="plane_altitude_input", default_value=10000.0, min_value=1000.0)
        
        def vehicle_type_changed():
            vtype = dpg.get_value("vehicle_type_input")
            dpg.hide_item("train_group")
            dpg.hide_item("plane_group")
            if vtype == "Train":
                dpg.show_item("train_group")
            elif vtype == "Airplane":
                dpg.show_item("plane_group")
        
        dpg.set_item_callback("vehicle_type_input", vehicle_type_changed)
        
        dpg.add_spacing(count=2)
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save", callback=save_vehicle)
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("add_vehicle_win"))

def save_vehicle():
    """Save vehicle"""
    global current_company
    
    vtype = dpg.get_value("vehicle_type_input")
    capacity = dpg.get_value("vehicle_capacity_input")
    
    if capacity <= 0:
        dpg.set_value("status_text", "Error: capacity must be > 0")
        return
    
    if vtype == "Truck":
        vehicle = Vehicle(capacity=capacity)
    elif vtype == "Train":
        cars = dpg.get_value("train_cars_input")
        # FIX: Используем правильное имя атрибута
        vehicle = Train(capacity=capacity, number_of_cars=cars)
    elif vtype == "Airplane":
        altitude = dpg.get_value("plane_altitude_input")
        vehicle = Airplane(capacity=capacity, max_altitude=altitude)
    
    current_company.add_vehicle(vehicle)
    update_vehicles_table()
    dpg.delete_item("add_vehicle_win")
    dpg.set_value("status_text", f"Vehicle added: {vtype}")

def optimize_distribution():
    """Optimize cargo distribution"""
    global current_company
    
    if not current_company.clients:
        dpg.set_value("status_text", "Error: no clients")
        return
    
    if not current_company.vehicles:
        dpg.set_value("status_text", "Error: no vehicles")
        return
    
    # Reset loading
    for vehicle in current_company.vehicles:
        vehicle.current_load = 0
        vehicle.clients_list = []
    
    # Optimize
    used_vehicles = current_company.optimize_cargo_distribution()
    
    update_clients_table()
    update_vehicles_table()
    show_results(used_vehicles)
    
    dpg.set_value("status_text", f"Distribution complete. Used {len(used_vehicles)} vehicles")

def show_results(used_vehicles):
    """Show distribution results"""
    result_text = "DISTRIBUTION RESULTS:\n\n"
    
    total_loaded = sum(v.current_load for v in used_vehicles)
    total_capacity = sum(v.capacity for v in current_company.vehicles)
    
    result_text += f"Total clients: {len(current_company.clients)}\n"
    result_text += f"VIP clients: {sum(1 for c in current_company.clients if c.is_vip)}\n"
    result_text += f"Used vehicles: {len(used_vehicles)} of {len(current_company.vehicles)}\n"
    result_text += f"Loaded: {total_loaded:.1f} kg of {total_capacity:.1f} kg\n\n"
    
    for i, vehicle in enumerate(used_vehicles, 1):
        result_text += f"{i}. {vehicle}\n"
        if vehicle.clients_list:
            result_text += "   Clients:\n"
            for client in vehicle.clients_list:
                vip = " (VIP)" if client.is_vip else ""
                result_text += f"   - {client.name}: {client.cargo_weight} kg{vip}\n"
        result_text += "\n"
    
    with dpg.window(label="Distribution Results", width=700, height=500, 
                   show=True, tag="results_win"):
        dpg.add_text(result_text, tag="results_text")
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("results_win"))

def update_clients_table():
    """Update clients table"""
    global current_company
    
    dpg.delete_item("clients_table", children_only=True)
    
    for client in current_company.clients:
        with dpg.table_row(parent="clients_table"):
            dpg.add_text(client.name)
            dpg.add_text(f"{client.cargo_weight:.1f}")
            dpg.add_text("Yes" if client.is_vip else "No")

def update_vehicles_table():
    """Update vehicles table"""
    global current_company
    
    dpg.delete_item("vehicles_table", children_only=True)
    
    for vehicle in current_company.vehicles:
        with dpg.table_row(parent="vehicles_table"):
            # Determine vehicle type
            if hasattr(vehicle, 'max_altitude'):
                vtype = "Airplane"
                details = f"Altitude: {vehicle.max_altitude} m"
            elif hasattr(vehicle, 'number_of_cars'):
                vtype = "Train"
                details = f"Cars: {vehicle.number_of_cars}"
            elif hasattr(vehicle, 'cars'):
                vtype = "Train"
                details = f"Cars: {vehicle.cars}"
            else:
                vtype = "Truck"
                details = "-"
            
            dpg.add_text(vtype)
            dpg.add_text(f"{vehicle.capacity:.1f}")
            dpg.add_text(f"{vehicle.current_load:.1f}")
            dpg.add_text(details)

def export_results():
    """Export results"""
    dpg.set_value("status_text", "Export results (in development)")

def clear_all():
    """Clear all data"""
    global current_company
    current_company.clients.clear()
    current_company.vehicles.clear()
    
    update_clients_table()
    update_vehicles_table()
    
    dpg.set_value("status_text", "All data cleared")

def setup_gui():
    """Setup GUI"""
    dpg.create_context()
    
    create_sample_data()
    
    with dpg.window(label="Transport Company", tag="primary_window"):
        
        # Menu
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Export Results", callback=export_results)
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=show_about)
        
        # Control panel
        dpg.add_text("Control Panel:")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add Client", callback=show_add_client)
            dpg.add_button(label="Add Vehicle", callback=show_add_vehicle)
            dpg.add_button(label="Distribute Cargo", callback=optimize_distribution)
            dpg.add_button(label="Clear All", callback=clear_all)
        
        dpg.add_separator()
        
        # Data tables
        with dpg.tab_bar():
            # Clients tab
            with dpg.tab(label="Clients"):
                dpg.add_text(f"Clients: {len(current_company.clients)}")
                with dpg.table(header_row=True, tag="clients_table", 
                              borders_innerH=True, borders_outerH=True, 
                              borders_innerV=True, borders_outerV=True):
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Weight (kg)")
                    dpg.add_table_column(label="VIP")
                
                update_clients_table()
            
            # Vehicles tab
            with dpg.tab(label="Vehicles"):
                dpg.add_text(f"Vehicles: {len(current_company.vehicles)}")
                with dpg.table(header_row=True, tag="vehicles_table",
                              borders_innerH=True, borders_outerH=True,
                              borders_innerV=True, borders_outerV=True):
                    dpg.add_table_column(label="Type")
                    dpg.add_table_column(label="Capacity (kg)")
                    dpg.add_table_column(label="Loaded (kg)")
                    dpg.add_table_column(label="Details")
                
                update_vehicles_table()
        
        dpg.add_separator()
        
        # Status bar
        dpg.add_text("Status:", tag="status_label")
        dpg.add_text("Ready", tag="status_text", color=[0, 200, 0])
    
    # Setup viewport
    dpg.create_viewport(title='Transport Company', width=1000, height=700)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    
    # Start main loop
    dpg.start_dearpygui()
    dpg.destroy_context()

def main():
    """Main function"""
    setup_gui()

if __name__ == "__main__":
    main()