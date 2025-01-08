import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="movie_production.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_person TEXT,
                    email TEXT,
                    phone TEXT,
                    billing_address TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    model TEXT,
                    description TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    project_name TEXT NOT NULL,
                    description TEXT,
                    start_date DATE,
                    end_date DATE,
                    location TEXT,
                    budget REAL,
                    notes TEXT,
                    status TEXT DEFAULT 'Pending',
                    services TEXT,
                    equipment TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating tables: {e}")

    # Generic CRUD operations (can be expanded as needed)
    def fetch_all(self, table):
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data from {table}: {e}")
            return []

    def fetch_one(self, table, record_id):
        try:
            self.cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data from {table}: {e}")
            return None

    def insert(self, table, data):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error inserting data into {table}: {e}")
            return None

    def update(self, table, record_id, data):
        try:
            set_values = ', '.join([f"{key} = ?" for key in data.keys()])
            self.cursor.execute(f"UPDATE {table} SET {set_values} WHERE id = ?", (*data.values(), record_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating data in {table}: {e}")
            return False

    def delete(self, table, record_id):
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting data from {table}: {e}")
            return False

class OrderForm(tk.Toplevel):
    def __init__(self, parent, db_manager, order_id=None):
        super().__init__(parent)
        self.title("Order Form")
        self.db_manager = db_manager
        self.order_id = order_id
        self.client_var = tk.StringVar()
        self.selected_services = []
        self.selected_equipment = []
        self.services_vars = {}
        self.equipment_vars = {}

        self.create_widgets()
        if self.order_id:
            self.load_order_data()

    def create_widgets(self):
        # Client Details Section
        ttk.Label(self, text="Client:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.client_combo = ttk.Combobox(self, textvariable=self.client_var)
        self.populate_client_combo()
        self.client_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="New Client Details:").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Label(self, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Contact Person:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.contact_entry = ttk.Entry(self)
        self.contact_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Phone:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Billing Address:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # Project Details Section
        ttk.Label(self, text="Project Details:").grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky="w")
        ttk.Label(self, text="Project Name:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.project_name_entry = ttk.Entry(self)
        self.project_name_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Description:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.description_text = tk.Text(self, height=3)
        self.description_text.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Shooting Start Date (YYYY-MM-DD):").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Shooting End Date (YYYY-MM-DD):").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.end_date_entry = ttk.Entry(self)
        self.end_date_entry.grid(row=11, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Location Preferences:").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.location_text = tk.Text(self, height=2)
        self.location_text.grid(row=12, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Budget Estimate:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.budget_entry = ttk.Entry(self)
        self.budget_entry.grid(row=13, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Notes:").grid(row=14, column=0, padx=5, pady=5, sticky="w")
        self.notes_text = tk.Text(self, height=2)
        self.notes_text.grid(row=14, column=1, padx=5, pady=5, sticky="ew")

        # Services Section
        ttk.Label(self, text="Services:").grid(row=15, column=0, padx=5, pady=10, sticky="w")
        self.create_services_checkboxes()

        # Equipment Section
        ttk.Label(self, text="Equipment:").grid(row=16, column=0, padx=5, pady=10, sticky="w")
        self.create_equipment_checkboxes()

        # Submit Button
        ttk.Button(self, text="Submit", command=self.submit_order).grid(row=17, column=0, columnspan=2, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def populate_client_combo(self):
        clients = self.db_manager.fetch_all("clients")
        client_names = [f"{client[1]} (ID: {client[0]})" for client in clients]
        self.client_combo['values'] = client_names

    def create_services_checkboxes(self):
        services = self.db_manager.fetch_all("services")
        self.services_vars = {}
        for i, service in enumerate(services):
            var = tk.BooleanVar()
            self.services_vars[service[0]] = var
            ttk.Checkbutton(self, text=service[1], variable=var).grid(row=15 + i + 1, column=1, padx=5, pady=2, sticky="w")

    def create_equipment_checkboxes(self):
        equipment = self.db_manager.fetch_all("equipment")
        self.equipment_vars = {}
        for i, item in enumerate(equipment):
            var = tk.BooleanVar()
            self.equipment_vars[item[0]] = var
            ttk.Checkbutton(self, text=item[1], variable=var).grid(row=16 + i + 1, column=1, padx=5, pady=2, sticky="w")

    def load_order_data(self):
        order = self.db_manager.fetch_one("orders", self.order_id)
        if order:
            # Load client
            client = self.db_manager.fetch_one("clients", order[1])
            if client:
                self.client_var.set(f"{client[1]} (ID: {client[0]})")

            # Load project details
            self.project_name_entry.insert(0, order[2])
            self.description_text.insert(tk.END, order[3])
            self.start_date_entry.insert(0, order[4])
            self.end_date_entry.insert(0, order[5])
            self.location_text.insert(tk.END, order[6])
            self.budget_entry.insert(0, order[7])
            self.notes_text.insert(tk.END, order[8])

            # Load selected services
            if order[10]:
                selected_services = [int(sid) for sid in order[10].split(',')]
                for service_id, var in self.services_vars.items():
                    if service_id in selected_services:
                        var.set(True)

            # Load selected equipment
            if order[11]:
                selected_equipment = [int(eid) for eid in order[11].split(',')]
                for equip_id, var in self.equipment_vars.items():
                    if equip_id in selected_equipment:
                        var.set(True)

    def submit_order(self):
        project_name = self.project_name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not project_name or not start_date or not end_date:
            messagebox.showerror("Validation Error", "Please fill in Project Name, Start Date, and End Date.")
            return

        client_id = None
        selected_client = self.client_var.get()
        if selected_client:
            try:
                client_id = int(selected_client.split('(ID: ')[1][:-1])
            except:
                messagebox.showerror("Error", "Invalid client selection.")
                return
        else:
            # Save new client details
            new_client_data = {
                "name": self.name_entry.get(),
                "contact_person": self.contact_entry.get(),
                "email": self.email_entry.get(),
                "phone": self.phone_entry.get(),
                "billing_address": self.address_entry.get()
            }
            if any(new_client_data.values()):
                client_id = self.db_manager.insert("clients", new_client_data)
                if not client_id:
                    return
            else:
                messagebox.showerror("Validation Error", "Please select an existing client or provide new client details.")
                return

        selected_services = [sid for sid, var in self.services_vars.items() if var.get()]
        selected_equipment = [eid for eid, var in self.equipment_vars.items() if var.get()]

        order_data = {
            "client_id": client_id,
            "project_name": project_name,
            "description": self.description_text.get("1.0", tk.END).strip(),
            "start_date": start_date,
            "end_date": end_date,
            "location": self.location_text.get("1.0", tk.END).strip(),
            "budget": self.budget_entry.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "services": ",".join(map(str, selected_services)),
            "equipment": ",".join(map(str, selected_equipment))
        }

        if self.order_id:
            if self.db_manager.update("orders", self.order_id, order_data):
                messagebox.showinfo("Success", "Order updated successfully.")
                self.master.refresh_orders()  # Refresh the order list in the main window
                self.destroy()
        else:
            if self.db_manager.insert("orders", order_data):
                messagebox.showinfo("Success", "Order created successfully.")
                self.master.refresh_orders()  # Refresh the order list in the main window
                self.destroy()

class ClientManagementWindow(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.title("Client Management")
        self.db_manager = db_manager
        self.selected_client_id = None
        self.create_widgets()
        self.populate_client_table()

    def create_widgets(self):
        # Add Client Section
        ttk.Label(self, text="Add New Client").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_name_entry = ttk.Entry(self)
        self.add_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Contact Person:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_contact_entry = ttk.Entry(self)
        self.add_contact_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.add_email_entry = ttk.Entry(self)
        self.add_email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Phone:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.add_phone_entry = ttk.Entry(self)
        self.add_phone_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Billing Address:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.add_address_entry = ttk.Entry(self)
        self.add_address_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Add Client", command=self.add_client).grid(row=6, column=0, columnspan=2, pady=10)

        # Client Table Section
        ttk.Label(self, text="Existing Clients").grid(row=7, column=0, columnspan=3, pady=10)
        self.client_table = ttk.Treeview(self, columns=("ID", "Name", "Contact", "Email", "Phone", "Address"), show="headings")
        for col in ("ID", "Name", "Contact", "Email", "Phone", "Address"):
            self.client_table.heading(col, text=col)
        self.client_table.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.client_table.bind("<ButtonRelease-1>", self.select_client)

        ttk.Button(self, text="Edit Client", command=self.edit_selected_client).grid(row=9, column=0, padx=5, pady=10)
        ttk.Button(self, text="Delete Client", command=self.delete_selected_client).grid(row=9, column=1, padx=5, pady=10)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(8, weight=1)

    def populate_client_table(self):
        for item in self.client_table.get_children():
            self.client_table.delete(item)
        clients = self.db_manager.fetch_all("clients")
        for client in clients:
            self.client_table.insert("", "end", values=client)

    def add_client(self):
        name = self.add_name_entry.get()
        if name:
            data = {
                "name": name,
                "contact_person": self.add_contact_entry.get(),
                "email": self.add_email_entry.get(),
                "phone": self.add_phone_entry.get(),
                "billing_address": self.add_address_entry.get()
            }
            if self.db_manager.insert("clients", data):
                messagebox.showinfo("Success", "Client added successfully.")
                self.populate_client_table()
                # Clear input fields
                for entry in [self.add_name_entry, self.add_contact_entry, self.add_email_entry, self.add_phone_entry, self.add_address_entry]:
                    entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Client name is required.")

    def select_client(self, event):
        selected_item = self.client_table.focus()
        if selected_item:
            self.selected_client_id = self.client_table.item(selected_item)['values'][0]

    def edit_selected_client(self):
        if self.selected_client_id:
            client_data = self.db_manager.fetch_one("clients", self.selected_client_id)
            if client_data:
                EditClientWindow(self, self.db_manager, client_data)
        else:
            messagebox.showerror("Error", "Please select a client to edit.")

    def delete_selected_client(self):
        if self.selected_client_id:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this client?"):
                if self.db_manager.delete("clients", self.selected_client_id):
                    messagebox.showinfo("Success", "Client deleted successfully.")
                    self.populate_client_table()
                    self.selected_client_id = None
        else:
            messagebox.showerror("Error", "Please select a client to delete.")

class EditClientWindow(tk.Toplevel):
    def __init__(self, parent, db_manager, client_data):
        super().__init__(parent)
        self.title("Edit Client")
        self.db_manager = db_manager
        self.client_id = client_data[0]

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, client_data[1])
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Contact Person:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.contact_entry = ttk.Entry(self)
        self.contact_entry.insert(0, client_data[2])
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self)
        self.email_entry.insert(0, client_data[3])
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.insert(0, client_data[4])
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Billing Address:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = ttk.Entry(self)
        self.address_entry.insert(0, client_data[5])
        self.address_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Update Client", command=self.update_client).grid(row=5, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(1, weight=1)

    def update_client(self):
        data = {
            "name": self.name_entry.get(),
            "contact_person": self.contact_entry.get(),
            "email": self.email_entry.get(),
            "phone": self.phone_entry.get(),
            "billing_address": self.address_entry.get()
        }
        if self.db_manager.update("clients", self.client_id, data):
            messagebox.showinfo("Success", "Client updated successfully.")
            self.master.populate_client_table()  # Refresh the client table in the management window
            self.destroy()

class EquipmentManagementWindow(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.title("Equipment Management")
        self.db_manager = db_manager
        self.selected_equipment_id = None
        self.create_widgets()
        self.populate_equipment_table()

    def create_widgets(self):
        # Add Equipment Section
        ttk.Label(self, text="Add New Equipment").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_name_entry = ttk.Entry(self)
        self.add_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Model:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_model_entry = ttk.Entry(self)
        self.add_model_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.add_description_entry = ttk.Entry(self)
        self.add_description_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Add Equipment", command=self.add_equipment).grid(row=4, column=0, columnspan=2, pady=10)

        # Equipment Table Section
        ttk.Label(self, text="Existing Equipment").grid(row=5, column=0, columnspan=3, pady=10)
        self.equipment_table = ttk.Treeview(self, columns=("ID", "Name", "Model", "Description"), show="headings")
        for col in ("ID", "Name", "Model", "Description"):
            self.equipment_table.heading(col, text=col)
        self.equipment_table.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.equipment_table.bind("<ButtonRelease-1>", self.select_equipment)

        ttk.Button(self, text="Edit Equipment", command=self.edit_selected_equipment).grid(row=7, column=0, padx=5, pady=10)
        ttk.Button(self, text="Delete Equipment", command=self.delete_selected_equipment).grid(row=7, column=1, padx=5, pady=10)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def populate_equipment_table(self):
        for item in self.equipment_table.get_children():
            self.equipment_table.delete(item)
        equipment = self.db_manager.fetch_all("equipment")
        for item in equipment:
            self.equipment_table.insert("", "end", values=item)

    def add_equipment(self):
        name = self.add_name_entry.get()
        if name:
            data = {
                "name": name,
                "model": self.add_model_entry.get(),
                "description": self.add_description_entry.get()
            }
            if self.db_manager.insert("equipment", data):
                messagebox.showinfo("Success", "Equipment added successfully.")
                self.populate_equipment_table()
                # Clear input fields
                for entry in [self.add_name_entry, self.add_model_entry, self.add_description_entry]:
                    entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Equipment name is required.")

    def select_equipment(self, event):
        selected_item = self.equipment_table.focus()
        if selected_item:
            self.selected_equipment_id = self.equipment_table.item(selected_item)['values'][0]

    def edit_selected_equipment(self):
        if self.selected_equipment_id:
            equipment_data = self.db_manager.fetch_one("equipment", self.selected_equipment_id)
            if equipment_data:
                EditEquipmentWindow(self, self.db_manager, equipment_data)
        else:
            messagebox.showerror("Error", "Please select equipment to edit.")

    def delete_selected_equipment(self):
        if self.selected_equipment_id:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this equipment?"):
                if self.db_manager.delete("equipment", self.selected_equipment_id):
                    messagebox.showinfo("Success", "Equipment deleted successfully.")
                    self.populate_equipment_table()
                    self.selected_equipment_id = None
        else:
            messagebox.showerror("Error", "Please select equipment to delete.")

class EditEquipmentWindow(tk.Toplevel):
    def __init__(self, parent, db_manager, equipment_data):
        super().__init__(parent)
        self.title("Edit Equipment")
        self.db_manager = db_manager
        self.equipment_id = equipment_data[0]

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, equipment_data[1])
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Model:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.model_entry = ttk.Entry(self)
        self.model_entry.insert(0, equipment_data[2])
        self.model_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self)
        self.description_entry.insert(0, equipment_data[3])
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Update Equipment", command=self.update_equipment).grid(row=3, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(1, weight=1)

    def update_equipment(self):
        data = {
            "name": self.name_entry.get(),
            "model": self.model_entry.get(),
            "description": self.description_entry.get()
        }
        if self.db_manager.update("equipment", self.equipment_id, data):
            messagebox.showinfo("Success", "Equipment updated successfully.")
            self.master.populate_equipment_table()  # Refresh the equipment table in the management window
            self.destroy()

class ServiceManagementWindow(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.title("Service Management")
        self.db_manager = db_manager
        self.selected_service_id = None
        self.create_widgets()
        self.populate_service_table()

    def create_widgets(self):
        # Add Service Section
        ttk.Label(self, text="Add New Service").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_name_entry = ttk.Entry(self)
        self.add_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_description_entry = ttk.Entry(self)
        self.add_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Add Service", command=self.add_service).grid(row=3, column=0, columnspan=2, pady=10)

        # Service Table Section
        ttk.Label(self, text="Existing Services").grid(row=4, column=0, columnspan=3, pady=10)
        self.service_table = ttk.Treeview(self, columns=("ID", "Name", "Description"), show="headings")
        for col in ("ID", "Name", "Description"):
            self.service_table.heading(col, text=col)
        self.service_table.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.service_table.bind("<ButtonRelease-1>", self.select_service)

        ttk.Button(self, text="Edit Service", command=self.edit_selected_service).grid(row=6, column=0, padx=5, pady=10)
        ttk.Button(self, text="Delete Service", command=self.delete_selected_service).grid(row=6, column=1, padx=5, pady=10)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)

    def populate_service_table(self):
        for item in self.service_table.get_children():
            self.service_table.delete(item)
        services = self.db_manager.fetch_all("services")
        for service in services:
            self.service_table.insert("", "end", values=service)

    def add_service(self):
        name = self.add_name_entry.get()
        if name:
            data = {
                "name": name,
                "description": self.add_description_entry.get()
            }
            if self.db_manager.insert("services", data):
                messagebox.showinfo("Success", "Service added successfully.")
                self.populate_service_table()
                # Clear input fields
                self.add_name_entry.delete(0, tk.END)
                self.add_description_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Service name is required.")

    def select_service(self, event):
        selected_item = self.service_table.focus()
        if selected_item:
            self.selected_service_id = self.service_table.item(selected_item)['values'][0]

    def edit_selected_service(self):
        if self.selected_service_id:
            service_data = self.db_manager.fetch_one("services", self.selected_service_id)
            if service_data:
                EditServiceWindow(self, self.db_manager, service_data)
        else:
            messagebox.showerror("Error", "Please select a service to edit.")

    def delete_selected_service(self):
        if self.selected_service_id:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this service?"):
                if self.db_manager.delete("services", self.selected_service_id):
                    messagebox.showinfo("Success", "Service deleted successfully.")
                    self.populate_service_table()
                    self.selected_service_id = None
        else:
            messagebox.showerror("Error", "Please select a service to delete.")

class EditServiceWindow(tk.Toplevel):
    def __init__(self, parent, db_manager, service_data):
        super().__init__(parent)
        self.title("Edit Service")
        self.db_manager = db_manager
        self.service_id = service_data[0]

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, service_data[1])
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self)
        self.description_entry.insert(0, service_data[2])
        self.description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self, text="Update Service", command=self.update_service).grid(row=2, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(1, weight=1)

    def update_service(self):
        data = {
            "name": self.name_entry.get(),
            "description": self.description_entry.get()
        }
        if self.db_manager.update("services", self.service_id, data):
            messagebox.showinfo("Success", "Service updated successfully.")
            self.master.populate_service_table()  # Refresh the service table in the management window
            self.destroy()

class OrderManagementWindow(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.title("Order Management")
        self.db_manager = db_manager
        self.selected_order_id = None
        self.create_widgets()
        self.refresh_orders()

    def create_widgets(self):
        # View Orders Section
        ttk.Label(self, text="Orders").grid(row=0, column=0, columnspan=4, pady=10)
        self.order_table = ttk.Treeview(self, columns=("ID", "Client", "Project", "Start Date", "End Date", "Status"), show="headings")
        for col in ("ID", "Client", "Project", "Start Date", "End Date", "Status"):
            self.order_table.heading(col, text=col)
        self.order_table.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.order_table.bind("<ButtonRelease-1>", self.select_order)

        # Filter/Search (Basic - can be expanded)
        ttk.Label(self, text="Filter:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.filter_entry = ttk.Entry(self)
        self.filter_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self, text="Search", command=self.search_orders).grid(row=2, column=2, padx=5, pady=5)

        # Add/Edit/Delete Buttons
        ttk.Button(self, text="Add Order", command=self.add_order).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(self, text="Edit Order", command=self.edit_selected_order).grid(row=3, column=1, padx=5, pady=10)
        ttk.Button(self, text="Delete Order", command=self.delete_selected_order).grid(row=3, column=2, padx=5, pady=10)

        # Update Order Status
        ttk.Label(self, text="Update Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(self, textvariable=self.status_var, values=["Pending", "In Progress", "Completed"])
        self.status_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self, text="Update", command=self.update_order_status).grid(row=4, column=2, padx=5, pady=5)

        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def refresh_orders(self):
        for item in self.order_table.get_children():
            self.order_table.delete(item)
        orders = self.db_manager.fetch_all("orders")
        for order in orders:
            client = self.db_manager.fetch_one("clients", order[1])
            client_name = client[1] if client else "Unknown"
            self.order_table.insert("", "end", values=(order[0], client_name, order[2], order[4], order[5], order[9]))

    def search_orders(self):
        filter_text = self.filter_entry.get().lower()
        for item in self.order_table.get_children():
            self.order_table.delete(item)
        orders = self.db_manager.fetch_all("orders")
        for order in orders:
            client = self.db_manager.fetch_one("clients", order[1])
            client_name = client[1] if client else "Unknown"
            if filter_text in client_name.lower() or filter_text in order[2].lower():
                self.order_table.insert("", "end", values=(order[0], client_name, order[2], order[4], order[5], order[9]))

    def add_order(self):
        OrderForm(self, self.db_manager)

    def select_order(self, event):
        selected_item = self.order_table.focus()
        if selected_item:
            self.selected_order_id = self.order_table.item(selected_item)['values'][0]

    def edit_selected_order(self):
        if self.selected_order_id:
            OrderForm(self, self.db_manager, self.selected_order_id)
        else:
            messagebox.showerror("Error", "Please select an order to edit.")

    def delete_selected_order(self):
        if self.selected_order_id:
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this order?"):
                if self.db_manager.delete("orders", self.selected_order_id):
                    messagebox.showinfo("Success", "Order deleted successfully.")
                    self.refresh_orders()
                    self.selected_order_id = None
        else:
            messagebox.showerror("Error", "Please select an order to delete.")

    def update_order_status(self):
        if self.selected_order_id:
            status = self.status_var.get()
            if status:
                if self.db_manager.update("orders", self.selected_order_id, {"status": status}):
                    messagebox.showinfo("Success", "Order status updated successfully.")
                    self.refresh_orders()
            else:
                messagebox.showerror("Error", "Please select a status.")
        else:
            messagebox.showerror("Error", "Please select an order to update status.")

# import tkinter as tk
# from tkinter import ttk  # For themed widgets (optional, but often better looking)

# Assuming you have these classes defined elsewhere
# from your original code
# class DatabaseManager:
#     pass
# class ClientManagementWindow(tk.Toplevel):
#     pass
# class EquipmentManagementWindow(tk.Toplevel):
#     pass
# class ServiceManagementWindow(tk.Toplevel):
#     pass
# class OrderManagementWindow(tk.Toplevel):
#     pass
# class OrderForm(tk.Toplevel):
#     pass

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Production Management")
        self.db_manager = DatabaseManager()  # Initialize here
        self.create_dashboard()

    def create_dashboard(self):
        # Set a solid background color for the main window
        self.configure(bg="#f0f8ff")  # Light blue color (Alice Blue)

        # Configure grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a main frame to hold dashboard elements
        dashboard_frame = ttk.Frame(self, padding=20, style="Dashboard.TFrame")
        dashboard_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid layout for the dashboard frame
        dashboard_frame.columnconfigure((0, 1), weight=1, uniform='equal')  # Equal width columns
        dashboard_frame.rowconfigure((0, 1), weight=1, uniform='equal')    # Equal height rows

        # Define a frame style for modern look
        style = ttk.Style()
        style.configure("Dashboard.TFrame",
                        background="#00f8ff")  # Match the window's background color

        # Define a button style for modern look
        style.configure("TButton",
                        font=("Helvetica", 12, "bold"),
                        foreground="#000000",
                        background="#000000",  # Teal button color
                        padding=10,
                        relief="raised")
        style.map("TButton",
                  background=[("active", "#000000"), ("disabled", "#ccc")])

        # Client Button
        client_button = ttk.Button(dashboard_frame, text="Manage Clients", command=self.open_client_management, style="TButton")
        client_button.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Equipment Button
        equipment_button = ttk.Button(dashboard_frame, text="Manage Equipment", command=self.open_equipment_management, style="TButton")
        equipment_button.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Services Button
        services_button = ttk.Button(dashboard_frame, text="Manage Services", command=self.open_service_management, style="TButton")
        services_button.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Orders Button
        orders_button = ttk.Button(dashboard_frame, text="Manage Orders", command=self.open_order_management, style="TButton")
        orders_button.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create New Order Button (can be placed differently if needed)
        new_order_button = ttk.Button(dashboard_frame, text="Create New Order", command=self.open_order_form, style="TButton")
        new_order_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

    def open_client_management(self):
        ClientManagementWindow(self, self.db_manager)

    def open_equipment_management(self):
        EquipmentManagementWindow(self, self.db_manager)

    def open_service_management(self):
        ServiceManagementWindow(self, self.db_manager)

    def open_order_management(self):
        OrderManagementWindow(self, self.db_manager)

    def open_order_form(self):
        OrderForm(self, self.db_manager)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
