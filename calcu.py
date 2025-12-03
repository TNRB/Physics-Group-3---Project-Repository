import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv
import os

class EnergyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Cost Calculator")

        # Set a reasonable fixed size for all content
        self.root.geometry("1300x785") # Reduced width, adjusted height
        self.root.config(background="#2f373e")
        self.root.resizable(False, False)

        self.image_cache = {}
        self.selected_image_path = None

        # Menu Bar setup remains the same
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0, background="#ADC2D1")
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_command(label="Delete Selected", command=self.delete_selected)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0, background="#ADC2D1")
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Energy Cost Calculator v1.0"))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Title
        tk.Label(root, text="ENERGY COST CALCULATOR", font=("Arial", 16, "bold"),
                 background="#2f373e", foreground='#72C24C').pack(pady=10)

        # --- Top Section: Input Frame ---
        input_frame = tk.Frame(root, background="#2f373e")
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Appliance Name:", background="#2f373e", foreground='#72C24C').grid(row=0, column=0, pady=5, sticky='e')
        ttk.Label(input_frame, text="Power (Watts):", background="#2f373e", foreground='#72C24C').grid(row=1, column=0, pady=5, sticky='e')
        ttk.Label(input_frame, text="Hours/Day:", background="#2f373e", foreground='#72C24C').grid(row=2, column=0, pady=5, sticky='e')
        ttk.Label(input_frame, text="Rate (₱/kWh):", background="#2f373e", foreground='#72C24C').grid(row=3, column=0, pady=5, sticky='e')

        self.entry_name = tk.Entry(input_frame, width=25, background="#ADC2D1")
        self.entry_watts = tk.Entry(input_frame, background="#ADC2D1")
        self.entry_hours = tk.Entry(input_frame, background="#ADC2D1")
        self.entry_rate = tk.Entry(input_frame, background="#ADC2D1")

        self.entry_name.grid(row=0, column=1)
        self.entry_watts.grid(row=1, column=1)
        self.entry_hours.grid(row=2, column=1)
        self.entry_rate.grid(row=3, column=1)

        tk.Button(input_frame, text="Choose Image (PNG)", command=self.choose_image,
                  background="#ADC2D1", foreground="#356D1B").grid(row=4, column=0, columnspan=2, pady=8)

        tk.Button(input_frame, text="Add Appliance", command=self.add_appliance,
                  background="#ADC2D1", foreground="#356D1B").grid(row=5, column=0, columnspan=2, pady=10)

        # Treeview Style setup remains the same
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ADC2D1", fieldbackground="#ADC2D1",
                        foreground="#000000", rowheight=70)
        style.configure("Treeview.Heading", background="#7B97AC", foreground="#FCDEFF")

        # --- Middle Section: Table ---
        main_table_container = tk.Frame(root, background="#2f373e")
        main_table_container.pack(pady=(10, 5), fill='x')

        table_frame = tk.Frame(main_table_container, background="#2f373e")
        table_frame.pack(anchor="center")

        # Treeview - Height fixed at 5 rows to ensure it fits and allows bottom elements to show
        # Original height was 10 which was too tall for the default window
        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "watts", "hours", "rate", "daily", "monthly"),
            show="tree headings",
            height=5 
        )
        self.tree.pack()

        # Image column
        self.tree.heading("#0", text="Image")
        self.tree.column("#0", width=90, anchor="center")

        # Data columns
        self.tree.heading("name", text="Appliance")
        self.tree.heading("watts", text="Watts")
        self.tree.heading("hours", text="Hours/Day")
        self.tree.heading("rate", text="Rate (₱/kWh)")
        self.tree.heading("daily", text="Daily Cost (₱)")
        self.tree.heading("monthly", text="Monthly Cost (₱)")

        self.tree.column("name", width=220)
        self.tree.column("watts", width=80)
        self.tree.column("hours", width=80)
        self.tree.column("rate", width=120)
        self.tree.column("daily", width=140)
        self.tree.column("monthly", width=140)
        
        # --- Bottom Section: Button and Totals ---
        
        # New frame to ensure the bottom elements are grouped and placed at the bottom
        # This structure is necessary when using .pack() on the root window
        bottom_frame = tk.Frame(root, background="#2f373e")
        bottom_frame.pack(side="bottom", fill="x", pady=(5, 15)) 
        
        # Delete Button - Centered in the bottom frame
        tk.Button(bottom_frame, text="Delete Selected", command=self.delete_selected,
                  background="#ADC2D1", foreground="#356D1B").pack(pady=6)

        # Totals - Centered below the button
        self.total_daily_label = ttk.Label(bottom_frame, text="Total Daily Cost: ₱0.00",
                                           font=("Arial", 11, "bold"),
                                           background="#2f373e", foreground='#FCDEFF')
        self.total_monthly_label = ttk.Label(bottom_frame, text="Total Monthly Cost: ₱0.00",
                                             font=("Arial", 11, "bold"),
                                             background="#2f373e", foreground='#5FCCFA')

        self.total_daily_label.pack()
        self.total_monthly_label.pack()


    # Choose Image
    def choose_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if path:
            self.selected_image_path = path
            messagebox.showinfo("Image Selected", f"Selected: {os.path.basename(path)}")

    # Add Appliance
    def add_appliance(self):
        try:
            name = self.entry_name.get() or "Appliance"
            watts = float(self.entry_watts.get())
            hours = float(self.entry_hours.get())
            rate = float(self.entry_rate.get())

            if not self.selected_image_path:
                messagebox.showwarning("No Image", "Please choose a PNG image first.")
                return

            photo = PhotoImage(file=self.selected_image_path)

            scale = max(1, int(max(photo.width(), photo.height()) / 60))
            photo = photo.subsample(scale, scale)

            self.image_cache[id(photo)] = photo

            daily_cost = (watts / 1000) * hours * rate
            monthly_cost = daily_cost * 30

            self.tree.insert(
                "",
                END,
                text="",
                image=photo,
                values=(name, watts, hours, rate, f"{daily_cost:.2f}", f"{monthly_cost:.2f}")
            )

            self.update_totals()

            self.entry_name.delete(0, END)
            self.entry_watts.delete(0, END)
            self.entry_hours.delete(0, END)
            self.entry_rate.delete(0, END)
            self.selected_image_path = None

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def update_totals(self):
        total_daily = 0
        total_monthly = 0

        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            try:
                # vals[4] and vals[5] are strings formatted as 'X.XX'
                total_daily += float(vals[4])
                total_monthly += float(vals[5])
            except ValueError:
                pass

        self.total_daily_label.config(text=f"Total Daily Cost: ₱{total_daily:.2f}")
        self.total_monthly_label.config(text=f"Total Monthly Cost: ₱{total_monthly:.2f}")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an appliance to delete.")
            return
        for item in sel:
            self.tree.delete(item)
        self.update_totals()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        rows = [self.tree.item(item, "values") for item in self.tree.get_children()]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Appliance", "Watts", "Hours/Day", "Rate", "Daily", "Monthly"])
            writer.writerows(rows)

        messagebox.showinfo("Exported", "CSV Export Successful!")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all appliances?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.update_totals()


root = tk.Tk()
EnergyCalculator(root)
root.mainloop()
