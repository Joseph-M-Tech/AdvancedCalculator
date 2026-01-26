import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class FinancialCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Financial Calculator")
        self.geometry("500x450")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Financial Calculator", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        self.create_npv_tab(notebook)
        self.create_irr_tab(notebook)
        self.create_fv_tab(notebook)
        self.create_loan_tab(notebook)

    # ---------- NPV ----------
    def create_npv_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="NPV")

        ttk.Label(frame, text="Discount Rate (e.g. 0.1):").grid(row=0, column=0, sticky="w")
        self.npv_rate = ttk.Entry(frame)
        self.npv_rate.grid(row=0, column=1)

        ttk.Label(frame, text="Cash Flows (comma-separated):").grid(row=1, column=0, sticky="w")
        self.npv_flows = ttk.Entry(frame, width=30)
        self.npv_flows.grid(row=1, column=1)

        ttk.Button(frame, text="Calculate NPV", command=self.calculate_npv).grid(row=2, column=0, columnspan=2, pady=10)

        self.npv_result = ttk.Label(frame, text="")
        self.npv_result.grid(row=3, column=0, columnspan=2)

    def calculate_npv(self):
        try:
            rate = float(self.npv_rate.get())
            cash_flows = list(map(float, self.npv_flows.get().split(",")))
            npv = np.npv(rate, cash_flows)
            self.npv_result.config(text=f"NPV: {npv:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- IRR ----------
    def create_irr_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="IRR")

        ttk.Label(frame, text="Cash Flows (comma-separated):").grid(row=0, column=0, sticky="w")
        self.irr_flows = ttk.Entry(frame, width=30)
        self.irr_flows.grid(row=0, column=1)

        ttk.Button(frame, text="Calculate IRR", command=self.calculate_irr).grid(row=1, column=0, columnspan=2, pady=10)

        self.irr_result = ttk.Label(frame, text="")
        self.irr_result.grid(row=2, column=0, columnspan=2)

    def calculate_irr(self):
        try:
            cash_flows = list(map(float, self.irr_flows.get().split(",")))
            irr = np.irr(cash_flows)
            self.irr_result.config(text=f"IRR: {irr * 100:.2f}%")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Future Value ----------
    def create_fv_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Future Value")

        ttk.Label(frame, text="Present Value:").grid(row=0, column=0, sticky="w")
        self.fv_pv = ttk.Entry(frame)
        self.fv_pv.grid(row=0, column=1)

        ttk.Label(frame, text="Rate (e.g. 0.05):").grid(row=1, column=0, sticky="w")
        self.fv_rate = ttk.Entry(frame)
        self.fv_rate.grid(row=1, column=1)

        ttk.Label(frame, text="Periods:").grid(row=2, column=0, sticky="w")
        self.fv_n = ttk.Entry(frame)
        self.fv_n.grid(row=2, column=1)

        ttk.Button(frame, text="Calculate FV", command=self.calculate_fv).grid(row=3, column=0, columnspan=2, pady=10)

        self.fv_result = ttk.Label(frame, text="")
        self.fv_result.grid(row=4, column=0, columnspan=2)

    def calculate_fv(self):
        try:
            pv = float(self.fv_pv.get())
            rate = float(self.fv_rate.get())
            n = int(self.fv_n.get())
            fv = pv * (1 + rate) ** n
            self.fv_result.config(text=f"Future Value: {fv:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Loan ----------
    def create_loan_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Loan")

        ttk.Label(frame, text="Loan Amount:").grid(row=0, column=0, sticky="w")
        self.loan_amount = ttk.Entry(frame)
        self.loan_amount.grid(row=0, column=1)

        ttk.Label(frame, text="Annual Rate (e.g. 0.08):").grid(row=1, column=0, sticky="w")
        self.loan_rate = ttk.Entry(frame)
        self.loan_rate.grid(row=1, column=1)

        ttk.Label(frame, text="Years:").grid(row=2, column=0, sticky="w")
        self.loan_years = ttk.Entry(frame)
        self.loan_years.grid(row=2, column=1)

        ttk.Button(frame, text="Calculate Payment", command=self.calculate_loan).grid(row=3, column=0, columnspan=2, pady=10)

        self.loan_result = ttk.Label(frame, text="")
        self.loan_result.grid(row=4, column=0, columnspan=2)

    def calculate_loan(self):
        try:
            principal = float(self.loan_amount.get())
            annual_rate = float(self.loan_rate.get())
            years = int(self.loan_years.get())

            monthly_rate = annual_rate / 12
            payments = years * 12

            payment = principal * (monthly_rate * (1 + monthly_rate) ** payments) / ((1 + monthly_rate) ** payments - 1)
            self.loan_result.config(text=f"Monthly Payment: {payment:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = FinancialCalculator()
    app.mainloop()
