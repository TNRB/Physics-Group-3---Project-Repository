import tkinter as tk
from tkinter import ttk, messagebox

class EnergyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Energy Cost Calculator")
        self.root.geometry("550x370")
        self.root.resizable(False, False)

        ttk.Label(root, text="ENERGY COST CALCULATOR", font=("Arial", 16, "bold")).pack(pady=10)

        input_frame = ttk.Frame(root)
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Appliance Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Power (Watts):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Hours/Day:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Rate (₱/kWh):").grid(row=3, column=0, padx=5, pady=5)

        self.entry_name = ttk.Entry(input_frame, width=25)
        self.entry_watts = ttk.Entry(input_frame)
        self.entry_hours = ttk.Entry(input_frame)
        self.entry_rate = ttk.Entry(input_frame)

        self.entry_name.grid(row=0, column=1)
        self.entry_watts.grid(row=1, column=1)
        self.entry_hours.grid(row=2, column=1)
        self.entry_rate.grid(row=3, column=1)

        ttk.Button(input_frame, text="Add Appliance", command=self.add_appliance).grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(root, columns=("watts","hours","rate","daily","monthly"), show="headings", height=8)
        self.tree.pack(pady=5)

        self.tree.heading("watts", text="Watts")
        self.tree.heading("hours", text="Hours/Day")
        self.tree.heading("rate", text="Rate (₱/kWh)")
        self.tree.heading("daily", text="Daily Cost (₱)")
        self.tree.heading("monthly", text="Monthly Cost (₱)")

        self.tree.column("watts", width=80)
        self.tree.column("hours", width=80)
        self.tree.column("rate", width=90)
        self.tree.column("daily", width=110)
        self.tree.column("monthly", width=120)

        self.total_daily_label = ttk.Label(root, text="Total Daily Cost: ₱0.00", font=("Arial", 11, "bold"))
        self.total_monthly_label = ttk.Label(root, text="Total Monthly Cost: ₱0.00", font=("Arial", 11, "bold"))

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

            self.tree.insert("", tk.END, values=(watts, hours, rate, f"{daily_cost:.2f}", f"{monthly_cost:.2f}"))

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
            total_daily += float(values[3])
            total_monthly += float(values[4])

        self.total_daily_label.config(text=f"Total Daily Cost: ₱{total_daily:.2f}")
        self.total_monthly_label.config(text=f"Total Monthly Cost: ₱{total_monthly:.2f}")


root = tk.Tk()
EnergyCalculator(root)
root.mainloop()