import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv

class EnergyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Energy Cost Calculator")
        self.root.geometry("720x520")
        self.root.config(background="#2f373e")
        self.root.resizable(False, False)

        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0,background="#ADC2D1")
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_command(label="Delete Selected", command=self.delete_selected)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit,background="#ADC2D1")
        menubar.add_cascade(label="File", menu=file_menu,background="#ADC2D1")

        help_menu = tk.Menu(menubar, tearoff=0,background="#ADC2D1")
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Energy Cost Calculator\nVersion 1.0"))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        tk.Label(root, text="ENERGY COST CALCULATOR", font=("Arial", 16, "bold"),background="#2f373e",foreground='#72C24C').pack(pady=10)

        input_frame = tk.Frame(root,background="#2f373e")
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Appliance Name:",background="#2f373e",foreground='#72C24C').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Power (Watts):",background="#2f373e",foreground='#72C24C').grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Hours/Day:",background="#2f373e",foreground='#72C24C').grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Rate (₱/kWh):",background="#2f373e",foreground='#72C24C').grid(row=3, column=0, padx=5, pady=5)

        self.entry_name = tk.Entry(input_frame, width=25,background="#ADC2D1")
        self.entry_watts = tk.Entry(input_frame,background="#ADC2D1")
        self.entry_hours = tk.Entry(input_frame,background="#ADC2D1")
        self.entry_rate = tk.Entry(input_frame,background="#ADC2D1")

        self.entry_name.grid(row=0, column=1)
        self.entry_watts.grid(row=1, column=1)
        self.entry_hours.grid(row=2, column=1)
        self.entry_rate.grid(row=3, column=1)

        tk.Button(input_frame, text="Add Appliance", command=self.add_appliance,background="#ADC2D1",foreground="#356D1B").grid(row=4, column=0, columnspan=2, pady=10)

        Table = ttk.Style()
        Table.theme_use("clam")
        Table.configure('Treeview', background="#ADC2D1", fieldbackground="#ADC2D1")
        Table.configure('Treeview.Heading', background="#7B97AC",foreground='#FCDEFF')
        
        self.tree = ttk.Treeview(root, columns=("name","watts","hours","rate","daily","monthly"), show="headings", height=8)
        self.tree.pack(pady=5)

        self.tree.heading("name", text="Appliance Name", command=lambda: self.sort_by("name", False))
        self.tree.heading("watts", text="Watts", command=lambda: self.sort_by("watts", False))
        self.tree.heading("hours", text="Hours/Day", command=lambda: self.sort_by("hours", False))
        self.tree.heading("rate", text="Rate (₱/kWh)", command=lambda: self.sort_by("rate", False))
        self.tree.heading("daily", text="Daily Cost (₱)", command=lambda: self.sort_by("daily", False))
        self.tree.heading("monthly", text="Monthly Cost (₱)", command=lambda: self.sort_by("monthly", False))

        self.tree.column("name", width=180)
        self.tree.column("watts", width=80)
        self.tree.column("hours", width=80)
        self.tree.column("rate", width=90)
        self.tree.column("daily", width=110)
        self.tree.column("monthly", width=120)

        tk.Button(root, text="Delete Selected", command=self.delete_selected,background="#ADC2D1",foreground="#356D1B").pack(pady=6)

        self.total_daily_label = ttk.Label(root, text="Total Daily Cost: ₱0.00", font=("Arial", 11, "bold"),background="#2f373e",foreground='#FCDEFF')
        self.total_monthly_label = ttk.Label(root, text="Total Monthly Cost: ₱0.00", font=("Arial", 11, "bold"),background="#2f373e",foreground='#5FCCFA')

        self.total_daily_label.pack()
        self.total_monthly_label.pack()

    def add_appliance(self):
        try:
            name = self.entry_name.get()
            watts = float(self.entry_watts.get())
            hours = float(self.entry_hours.get())
            rate = float(self.entry_rate.get())

            if name.strip() == "":
                name = "Appliance"

            kwh_per_day = (watts / 1000) * hours
            daily_cost = kwh_per_day * rate
            monthly_cost = daily_cost * 30

            self.tree.insert("", tk.END, values=(name, watts, hours, rate, f"{daily_cost:.2f}", f"{monthly_cost:.2f}"))

            self.update_totals()

            self.entry_name.delete(0, tk.END)
            self.entry_watts.delete(0, tk.END)
            self.entry_hours.delete(0, tk.END)
            self.entry_rate.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def update_totals(self):
        total_daily = 0
        total_monthly = 0

        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            total_daily += float(values[4])
            total_monthly += float(values[5])

        self.total_daily_label.config(text=f"Total Daily Cost: ₱{total_daily:.2f}")
        self.total_monthly_label.config(text=f"Total Monthly Cost: ₱{total_monthly:.2f}")

    def sort_by(self, col, descending):
        """Sort tree contents by given column."""
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=descending)
        except Exception:
            data.sort(key=lambda t: t[0].lower(), reverse=descending)
        for i, (val, k) in enumerate(data):
            self.tree.move(k, '', i)
        self.tree.heading(col, command=lambda: self.sort_by(col, not descending))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        rows = []
        for item in self.tree.get_children():
            rows.append(self.tree.item(item, 'values'))
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Appliance","Watts","Hours/Day","Rate(₱/kWh)","Daily(₱)","Monthly(₱)"])
                writer.writerows(rows)
            messagebox.showinfo("Exported", f"Exported {len(rows)} rows to CSV")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def clear_all(self):
        if not messagebox.askyesno("Confirm", "Clear all appliances?"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_totals()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an appliance to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete selected appliance(s)?"):
            return
        for item in sel:
            self.tree.delete(item)
        self.update_totals()


root = tk.Tk()
icon = PhotoImage(file='logo.png')
root.iconphoto(True,icon)
EnergyCalculator(root)
root.mainloop()
