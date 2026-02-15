import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Configuration
# Make sure this matches your compiled file name! (e.g. "simulation.c -o simulation -lm")
C_PROGRAM_NAME = "./simulation" 

class BilliardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billiard Simulator Control")
        self.root.geometry("400x350")
        
        # Title
        tk.Label(root, text="Physics Simulator", font=("Arial", 16, "bold")).pack(pady=10)

        # Input Fields Container
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Mode Selection
        tk.Label(self.frame, text="Simulation Mode:").grid(row=0, column=0, sticky="e", pady=5)
        self.mode_var = tk.IntVar(value=1)
        tk.Radiobutton(self.frame, text="Circular", variable=self.mode_var, value=1).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self.frame, text="Semi-Circular", variable=self.mode_var, value=2).grid(row=1, column=1, sticky="w")

        # X Coordinate
        tk.Label(self.frame, text="Initial X:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_x = tk.Entry(self.frame)
        self.entry_x.insert(0, "2.0") # Default value
        self.entry_x.grid(row=2, column=1)

        # Y Coordinate
        tk.Label(self.frame, text="Initial Y:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_y = tk.Entry(self.frame)
        self.entry_y.insert(0, "1.0") 
        self.entry_y.grid(row=3, column=1)

        # Angle
        tk.Label(self.frame, text="Angle (rad):").grid(row=4, column=0, sticky="e", pady=5)
        self.entry_angle = tk.Entry(self.frame)
        self.entry_angle.insert(0, "0.5")
        self.entry_angle.grid(row=4, column=1)

        # Run Button
        self.btn_run = tk.Button(root, text="Run Simulation", command=self.run_simulation, 
                                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.btn_run.pack(pady=20, fill="x", padx=50)

    def run_simulation(self):
        # 1. Get Inputs & Validate Types
        try:
            mode = self.mode_var.get()
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            angle = float(self.entry_angle.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return

        # 2. Validate Constraints (The Restriction Logic)
        RADIUS = 7.5
        dist_sq = x*x + y*y
        
        # Check A: Is it inside the circle?
        if dist_sq >= RADIUS*RADIUS:
            current_dist = dist_sq**0.5
            messagebox.showerror("Physics Error", 
                f"Position ({x}, {y}) is OUTSIDE the table!\n"
                f"Distance from center: {current_dist:.2f}\n"
                f"Max allowed radius: {RADIUS}")
            return

        # Check B: Is it valid for Semi-Circle?
        if mode == 2 and y < 0:
            messagebox.showerror("Physics Error", 
                "In Semi-Circular mode, Y cannot be negative.\n"
                "Please enter a value >= 0.")
            return

        # 3. Check if C program exists
        # Handle Windows vs Linux path
        program_path = C_PROGRAM_NAME
        if not os.path.exists(program_path):
             program_path = "simulation.exe" # Try Windows name
        
        if not os.path.exists(program_path):
            messagebox.showerror("Error", f"Could not find executable '{C_PROGRAM_NAME}'.\nDid you compile the C code?")
            return

        # 4. Prepare Input String 
        # The C program expects: Mode -> X -> Y -> Angle
        # We add newlines (\n) to simulate pressing Enter key
        input_data = f"{mode}\n{x}\n{y}\n{angle}\n"

        # 5. Run the C Program
        try:
            # Popen allows us to send input to stdin securely
            process = subprocess.Popen(
                [program_path], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True # Treat input/output as text, not bytes
            )
            
            # Send our input and get output
            stdout, stderr = process.communicate(input=input_data)
            
            if process.returncode != 0:
                 # If C program crashed, show why
                 messagebox.showerror("Simulation Error", f"The C program returned an error:\n{stderr}")
            else:
                 print("Simulation finished successfully.")
                 # The C program automatically launches the plot window, so we are done!

        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to run subprocess:\n{str(e)}")

# Main Loop
if __name__ == "__main__":
    root = tk.Tk()
    app = BilliardApp(root)
    root.mainloop()
