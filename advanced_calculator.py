import tkinter as tk
from tkinter import ttk, font
import math
import re

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Custom fonts
        self.display_font = font.Font(family="Consolas", size=18)
        self.button_font = font.Font(family="Arial", size=12)
        self.small_button_font = font.Font(family="Arial", size=10)
        
        # Expression variables
        self.expression = ""
        self.result = ""
        self.memory = 0
        self.history = []
        self.angle_mode = "DEG"  # DEG, RAD, GRAD
        self.use_degrees = True
        
        # Color scheme
        self.colors = {
            "display_bg": "#1e1e1e",
            "display_fg": "#ffffff",
            "button_bg": "#2d2d2d",
            "button_fg": "#ffffff",
            "operator_bg": "#ff9500",
            "operator_fg": "#ffffff",
            "scientific_bg": "#404040",
            "scientific_fg": "#ffffff",
            "memory_bg": "#0055aa",
            "memory_fg": "#ffffff",
            "clear_bg": "#aa0000",
            "clear_fg": "#ffffff",
            "equals_bg": "#00aa00",
            "equals_fg": "#ffffff",
            "history_bg": "#2a2a2a",
            "history_fg": "#cccccc"
        }
        
        self.setup_ui()
        self.bind_keys()
    
    def setup_ui(self):
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for calculator
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=3)
        
        # Right panel for history and formulas
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=1)
        
        # Setup left panel
        self.setup_left_panel(left_panel)
        
        # Setup right panel
        self.setup_right_panel(right_panel)
    
    def setup_left_panel(self, parent):
        # Display frame
        display_frame = tk.Frame(parent, bg=self.colors["display_bg"], height=80)
        display_frame.pack(fill=tk.X, padx=5, pady=5)
        display_frame.pack_propagate(False)
        
        # Expression display
        self.expression_display = tk.Label(
            display_frame,
            text="",
            font=self.display_font,
            bg=self.colors["display_bg"],
            fg="#888888",
            anchor="e",
            padx=10
        )
        self.expression_display.pack(fill=tk.X, expand=True)
        
        # Result display
        self.result_display = tk.Label(
            display_frame,
            text="0",
            font=self.display_font,
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"],
            anchor="e",
            padx=10
        )
        self.result_display.pack(fill=tk.X, expand=True)
        
        # Mode display
        self.mode_display = tk.Label(
            display_frame,
            text=f"Mode: {self.angle_mode} | M: {self.memory}",
            font=self.small_button_font,
            bg=self.colors["display_bg"],
            fg="#888888",
            anchor="w",
            padx=10
        )
        self.mode_display.pack(fill=tk.X, expand=True)
        
        # Button frame with tabs
        button_notebook = ttk.Notebook(parent)
        button_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic calculator tab
        basic_frame = ttk.Frame(button_notebook)
        button_notebook.add(basic_frame, text="Basic")
        self.setup_basic_buttons(basic_frame)
        
        # Scientific calculator tab
        scientific_frame = ttk.Frame(button_notebook)
        button_notebook.add(scientific_frame, text="Scientific")
        self.setup_scientific_buttons(scientific_frame)
        
        # Statistics tab
        stats_frame = ttk.Frame(button_notebook)
        button_notebook.add(stats_frame, text="Statistics")
        self.setup_statistics_buttons(stats_frame)
        
        # Formulas tab
        formulas_frame = ttk.Frame(button_notebook)
        button_notebook.add(formulas_frame, text="Formulas")
        self.setup_formulas_buttons(formulas_frame)
    
    def setup_right_panel(self, parent):
        # History section
        history_label = tk.Label(
            parent,
            text="History",
            font=self.button_font,
            bg=self.colors["history_bg"],
            fg=self.colors["history_fg"]
        )
        history_label.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        # History listbox
        self.history_listbox = tk.Listbox(
            parent,
            font=self.small_button_font,
            bg=self.colors["history_bg"],
            fg=self.colors["history_fg"],
            height=15
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        
        # Memory buttons frame
        memory_frame = tk.Frame(parent)
        memory_frame.pack(fill=tk.X, padx=5, pady=5)
        
        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store)
        ]
        
        for text, command in memory_buttons:
            btn = tk.Button(
                memory_frame,
                text=text,
                font=self.small_button_font,
                bg=self.colors["memory_bg"],
                fg=self.colors["memory_fg"],
                command=command
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # Angle mode selector
        mode_frame = tk.Frame(parent)
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(mode_frame, text="Angle Mode:").pack(side=tk.LEFT)
        
        self.angle_var = tk.StringVar(value=self.angle_mode)
        for mode in ["DEG", "RAD", "GRAD"]:
            rb = tk.Radiobutton(
                mode_frame,
                text=mode,
                variable=self.angle_var,
                value=mode,
                command=self.change_angle_mode
            )
            rb.pack(side=tk.LEFT, padx=5)
    
    def setup_basic_buttons(self, parent):
        # Basic calculator buttons
        basic_layout = [
            ('C', 0, 0, 1, 1, self.colors["clear_bg"]),
            ('⌫', 0, 1, 1, 1, self.colors["clear_bg"]),
            ('%', 0, 2, 1, 1, self.colors["operator_bg"]),
            ('÷', 0, 3, 1, 1, self.colors["operator_bg"]),
            ('7', 1, 0, 1, 1, self.colors["button_bg"]),
            ('8', 1, 1, 1, 1, self.colors["button_bg"]),
            ('9', 1, 2, 1, 1, self.colors["button_bg"]),
            ('×', 1, 3, 1, 1, self.colors["operator_bg"]),
            ('4', 2, 0, 1, 1, self.colors["button_bg"]),
            ('5', 2, 1, 1, 1, self.colors["button_bg"]),
            ('6', 2, 2, 1, 1, self.colors["button_bg"]),
            ('-', 2, 3, 1, 1, self.colors["operator_bg"]),
            ('1', 3, 0, 1, 1, self.colors["button_bg"]),
            ('2', 3, 1, 1, 1, self.colors["button_bg"]),
            ('3', 3, 2, 1, 1, self.colors["button_bg"]),
            ('+', 3, 3, 1, 1, self.colors["operator_bg"]),
            ('±', 4, 0, 1, 1, self.colors["button_bg"]),
            ('0', 4, 1, 1, 1, self.colors["button_bg"]),
            ('.', 4, 2, 1, 1, self.colors["button_bg"]),
            ('=', 4, 3, 1, 1, self.colors["equals_bg"])
        ]
        
        self.create_buttons_grid(parent, basic_layout)
    
    def setup_scientific_buttons(self, parent):
        # Scientific calculator buttons (3 columns)
        scientific_layout = [
            # Row 0
            ('sin', 0, 0, 1, 1, self.colors["scientific_bg"]),
            ('cos', 0, 1, 1, 1, self.colors["scientific_bg"]),
            ('tan', 0, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 1
            ('asin', 1, 0, 1, 1, self.colors["scientific_bg"]),
            ('acos', 1, 1, 1, 1, self.colors["scientific_bg"]),
            ('atan', 1, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 2
            ('sinh', 2, 0, 1, 1, self.colors["scientific_bg"]),
            ('cosh', 2, 1, 1, 1, self.colors["scientific_bg"]),
            ('tanh', 2, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 3
            ('log₁₀', 3, 0, 1, 1, self.colors["scientific_bg"]),
            ('logₑ', 3, 1, 1, 1, self.colors["scientific_bg"]),
            ('log₂', 3, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 4
            ('x²', 4, 0, 1, 1, self.colors["scientific_bg"]),
            ('x³', 4, 1, 1, 1, self.colors["scientific_bg"]),
            ('xʸ', 4, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 5
            ('√', 5, 0, 1, 1, self.colors["scientific_bg"]),
            ('∛', 5, 1, 1, 1, self.colors["scientific_bg"]),
            ('y√x', 5, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 6
            ('π', 6, 0, 1, 1, self.colors["scientific_bg"]),
            ('e', 6, 1, 1, 1, self.colors["scientific_bg"]),
            ('10ˣ', 6, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 7
            ('n!', 7, 0, 1, 1, self.colors["scientific_bg"]),
            ('1/x', 7, 1, 1, 1, self.colors["scientific_bg"]),
            ('|x|', 7, 2, 1, 1, self.colors["scientific_bg"]),
            # Row 8
            ('(', 8, 0, 1, 1, self.colors["operator_bg"]),
            (')', 8, 1, 1, 1, self.colors["operator_bg"]),
            ('=', 8, 2, 1, 1, self.colors["equals_bg"])
        ]
        
        self.create_buttons_grid(parent, scientific_layout, columns=3)
    
    def setup_statistics_buttons(self, parent):
        # Statistics buttons
        stats_layout = [
            ('∑x', 0, 0, 1, 1, self.colors["scientific_bg"]),
            ('∑x²', 0, 1, 1, 1, self.colors["scientific_bg"]),
            ('Mean', 0, 2, 1, 1, self.colors["scientific_bg"]),
            ('Median', 1, 0, 1, 1, self.colors["scientific_bg"]),
            ('Std Dev', 1, 1, 1, 1, self.colors["scientific_bg"]),
            ('Variance', 1, 2, 1, 1, self.colors["scientific_bg"]),
            ('Add Data', 2, 0, 1, 2, self.colors["scientific_bg"]),
            ('Clear Data', 2, 2, 1, 1, self.colors["clear_bg"]),
            ('Enter', 3, 0, 1, 3, self.colors["equals_bg"])
        ]
        
        self.data_points = []
        self.data_label = tk.Label(
            parent,
            text="Data: []",
            font=self.small_button_font,
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"]
        )
        self.data_label.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)
        
        self.create_buttons_grid(parent, stats_layout, columns=3)
    
    def setup_formulas_buttons(self, parent):
        # Formula buttons
        formulas = [
            ("Quadratic Eq", "ax²+bx+c=0"),
            ("Area Circle", "πr²"),
            ("Area Triangle", "½bh"),
            ("Pythagorean", "a²+b²=c²"),
            ("Cosine Law", "c²=a²+b²-2ab·cos(C)"),
            ("Sine Law", "a/sin(A)=b/sin(B)"),
            ("Volume Sphere", "4/3πr³"),
            ("Compound Interest", "P(1+r/n)ⁿᵗ"),
            ("Distance 2D", "√((x₂-x₁)²+(y₂-y₁)²)"),
            ("Slope", "(y₂-y₁)/(x₂-x₁)"),
            ("BMI", "weight/height²"),
            ("Kinetic Energy", "½mv²")
        ]
        
        for i, (name, formula) in enumerate(formulas):
            row = i // 2
            col = (i % 2) * 2
            
            btn = tk.Button(
                parent,
                text=name,
                font=self.small_button_font,
                bg=self.colors["scientific_bg"],
                fg=self.colors["scientific_fg"],
                command=lambda f=formula: self.insert_formula(f),
                height=2,
                wraplength=150
            )
            btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=2)
            
            # Add formula label
            formula_label = tk.Label(
                parent,
                text=formula,
                font=self.small_button_font,
                fg="#888888"
            )
            formula_label.grid(row=row, column=col+2, sticky="w", padx=5, pady=2)
        
        # Configure grid
        for i in range(6):  # 6 rows
            parent.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4 columns
            parent.grid_columnconfigure(i, weight=1)
    
    def create_buttons_grid(self, parent, layout, columns=4):
        for text, row, col, rowspan, colspan, bg_color in layout:
            fg_color = self.colors["button_fg"]
            if bg_color == self.colors["operator_bg"]:
                fg_color = self.colors["operator_fg"]
            elif bg_color == self.colors["equals_bg"]:
                fg_color = self.colors["equals_fg"]
            elif bg_color == self.colors["clear_bg"]:
                fg_color = self.colors["clear_fg"]
            
            button = tk.Button(
                parent,
                text=text,
                font=self.button_font if columns == 4 else self.small_button_font,
                bg=bg_color,
                fg=fg_color,
                borderwidth=1,
                relief="ridge",
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(
                row=row,
                column=col,
                rowspan=rowspan,
                columnspan=colspan,
                sticky="nsew",
                padx=2,
                pady=2
            )
        
        # Configure grid weights
        max_row = max([r + rs for _, r, _, rs, _, _ in layout])
        for i in range(max_row):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(columns):
            parent.grid_columnconfigure(i, weight=1)
    
    def bind_keys(self):
        # Bind keyboard keys
        keys = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '×', '/': '÷',
            '.': '.', '(': '(', ')': ')',
            '^': 'xʸ', '!': 'n!',
            'p': 'π', 'e': 'e'
        }
        
        for key, value in keys.items():
            self.root.bind(f'<KeyPress-{key}>', lambda e, v=value: self.on_button_click(v))
        
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<Delete>', lambda e: self.clear_entry())
        
        # Focus on root window
        self.root.focus_set()
    
    def on_button_click(self, value):
        """Handle button clicks"""
        # Basic operations
        if value.isdigit() or value in ['+', '-', '×', '÷', '(', ')', '.']:
            self.expression += value
        
        # Scientific functions
        elif value in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                      'sinh', 'cosh', 'tanh', 'log₁₀', 'logₑ', 'log₂']:
            self.expression += f"{value}("
        
        # Power and roots
        elif value == 'x²':
            self.expression += '²'
        elif value == 'x³':
            self.expression += '³'
        elif value == 'xʸ':
            self.expression += '^'
        elif value == '√':
            self.expression += 'sqrt('
        elif value == '∛':
            self.expression += 'cbrt('
        elif value == 'y√x':
            self.expression += 'root('
        
        # Constants
        elif value == 'π':
            self.expression += 'pi'
        elif value == 'e':
            self.expression += 'e'
        elif value == '10ˣ':
            self.expression += '10^'
        
        # Other functions
        elif value == 'n!':
            self.expression += '!'
        elif value == '1/x':
            self.expression = f"1/({self.expression})" if self.expression else "1/"
        elif value == '|x|':
            self.expression = f"abs({self.expression})"
        
        # Clear and delete
        elif value == 'C':
            self.clear_all()
            return
        elif value == '⌫':
            self.backspace()
            return
        
        # Percentage
        elif value == '%':
            self.expression += '/100'
        
        # Sign change
        elif value == '±':
            if self.expression and self.expression[0] == '-':
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
        
        # Statistics functions
        elif value in ['∑x', '∑x²', 'Mean', 'Median', 'Std Dev', 'Variance']:
            self.perform_statistical_operation(value)
            return
        
        elif value == 'Add Data':
            self.add_data_point()
            return
        elif value == 'Clear Data':
            self.clear_data()
            return
        
        # Calculate
        elif value == '=':
            self.calculate()
            return
        
        self.update_display()
    
    def insert_formula(self, formula):
        """Insert a formula into the expression"""
        self.expression = formula
        self.update_display()
    
    def perform_statistical_operation(self, operation):
        """Perform statistical operations on data points"""
        if not self.data_points:
            self.result_display.config(text="No data")
            return
        
        data = self.data_points
        
        if operation == '∑x':
            result = sum(data)
        elif operation == '∑x²':
            result = sum(x**2 for x in data)
        elif operation == 'Mean':
            result = sum(data) / len(data)
        elif operation == 'Median':
            sorted_data = sorted(data)
            n = len(sorted_data)
            if n % 2 == 0:
                result = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                result = sorted_data[n//2]
        elif operation == 'Std Dev':
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            result = math.sqrt(variance)
        elif operation == 'Variance':
            mean = sum(data) / len(data)
            result = sum((x - mean) ** 2 for x in data) / len(data)
        
        self.result = str(round(result, 10))
        self.result_display.config(text=self.result)
        
        # Add to history
        self.add_to_history(f"{operation}: {self.result}")
    
    def add_data_point(self):
        """Add current result as data point"""
        try:
            value = float(self.result if self.result else 0)
            self.data_points.append(value)
            self.data_label.config(text=f"Data: {self.data_points}")
        except ValueError:
            pass
    
    def clear_data(self):
        """Clear all data points"""
        self.data_points = []
        self.data_label.config(text="Data: []")
    
    def update_display(self):
        """Update the display with current expression"""
        self.expression_display.config(text=self.expression)
        
        # Try to evaluate and show result
        try:
            if self.expression:
                result = self.evaluate_expression(self.expression)
                if result is not None:
                    self.result_display.config(text=str(result)[:20])
        except:
            pass
    
    def evaluate_expression(self, expr):
        """Evaluate mathematical expression safely"""
        try:
            # Replace symbols with Python equivalents
            expr = expr.replace('×', '*').replace('÷', '/')
            expr = expr.replace('²', '**2').replace('³', '**3')
            expr = expr.replace('^', '**')
            expr = expr.replace('pi', str(math.pi))
            expr = expr.replace('e', str(math.e))
            
            # Handle factorials
            while '!' in expr:
                idx = expr.find('!')
                # Find the number before !
                num_str = ''
                i = idx - 1
                while i >= 0 and (expr[i].isdigit() or expr[i] == '.' or expr[i] == '-'):
                    num_str = expr[i] + num_str
                    i -= 1
                
                if num_str:
                    num = float(num_str) if '.' in num_str else int(num_str)
                    factorial = math.factorial(int(num))
                    expr = expr[:i+1] + str(factorial) + expr[idx+1:]
                else:
                    break
            
            # Handle functions with angle conversion
            functions = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'log₁₀': math.log10,
                'logₑ': math.log,
                'log₂': lambda x: math.log(x, 2),
                'sqrt': math.sqrt,
                'cbrt': lambda x: x ** (1/3),
                'root': lambda x, y: y ** (1/x) if x != 0 else None,
                'abs': abs
            }
            
            # Replace function calls
            for func_name, func in functions.items():
                while func_name in expr:
                    idx = expr.find(func_name)
                    if idx != -1:
                        # Find the matching parentheses
                        paren_count = 0
                        j = idx + len(func_name)
                        while j < len(expr) and (expr[j].isspace() or expr[j] == '('):
                            j += 1
                        
                        start = j
                        while j < len(expr):
                            if expr[j] == '(':
                                paren_count += 1
                            elif expr[j] == ')':
                                paren_count -= 1
                                if paren_count == 0:
                                    break
                            j += 1
                        
                        if j < len(expr):
                            arg_str = expr[start:j]
                            try:
                                # Handle multiple arguments for root function
                                if func_name == 'root':
                                    args = arg_str.split(',')
                                    if len(args) == 2:
                                        x = float(args[0].strip())
                                        y = float(args[1].strip())
                                        result = func(x, y)
                                    else:
                                        result = None
                                else:
                                    arg = float(eval(arg_str))
                                    # Convert angle if needed
                                    if func_name in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                                        if self.angle_mode == "DEG":
                                            if func_name.startswith('a'):  # Inverse functions
                                                result = math.degrees(func(arg))
                                            else:
                                                result = func(math.radians(arg))
                                        elif self.angle_mode == "GRAD":
                                            if func_name.startswith('a'):
                                                result = func(arg) * 200 / math.pi
                                            else:
                                                result = func(arg * math.pi / 200)
                                        else:  # RAD
                                            result = func(arg)
                                    else:
                                        result = func(arg)
                                
                                if result is not None:
                                    expr = expr[:idx] + str(result) + expr[j+1:]
                            except:
                                break
                        else:
                            break
            
            # Evaluate the remaining expression
            result = eval(expr)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limit decimal places
                    result = round(result, 10)
                    if abs(result) < 1e-10:
                        result = 0
            
            return result
            
        except Exception as e:
            return None
    
    def calculate(self):
        """Perform calculation"""
        if not self.expression:
            return
        
        try:
            result = self.evaluate_expression(self.expression)
            if result is not None:
                self.result = str(result)
                self.result_display.config(text=self.result)
                
                # Add to history
                history_entry = f"{self.expression} = {self.result}"
                self.add_to_history(history_entry)
                
                # Clear expression for next calculation
                self.expression = ""
                self.expression_display.config(text="")
            else:
                self.result_display.config(text="Error")
        except Exception as e:
            self.result_display.config(text="Error")
    
    def add_to_history(self, entry):
        """Add entry to history"""
        self.history.append(entry)
        self.history_listbox.insert(0, entry)
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop()
            self.history_listbox.delete(50)
    
    def on_history_select(self, event):
        """Handle history selection"""
        selection = self.history_listbox.curselection()
        if selection:
            entry = self.history_listbox.get(selection[0])
            # Extract expression from history entry
            if ' = ' in entry:
                expr = entry.split(' = ')[0]
                self.expression = expr
                self.update_display()
    
    def change_angle_mode(self):
        """Change angle mode"""
        self.angle_mode = self.angle_var.get()
        self.mode_display.config(text=f"Mode: {self.angle_mode} | M: {self.memory}")
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.mode_display.config(text=f"Mode: {self.angle_mode} | M: {self.memory}")
    
    def memory_recall(self):
        """Recall from memory"""
        self.expression += str(self.memory)
        self.update_display()
    
    def memory_store(self):
        """Store to memory"""
        try:
            self.memory = float(self.result if self.result else 0)
            self.mode_display.config(text=f"Mode: {self.angle_mode} | M: {self.memory}")
        except ValueError:
            pass
    
    def memory_add(self):
        """Add to memory"""
        try:
            value = float(self.result if self.result else 0)
            self.memory += value
            self.mode_display.config(text=f"Mode: {self.angle_mode} | M: {self.memory}")
        except ValueError:
            pass
    
    def memory_subtract(self):
        """Subtract from memory"""
        try:
            value = float(self.result if self.result else 0)
            self.memory -= value
            self.mode_display.config(text=f"Mode: {self.angle_mode} | M: {self.memory}")
        except ValueError:
            pass
    
    def clear_all(self):
        """Clear everything"""
        self.expression = ""
        self.result = ""
        self.expression_display.config(text="")
        self.result_display.config(text="0")
    
    def clear_entry(self):
        """Clear current entry"""
        self.expression = ""
        self.expression_display.config(text="")
    
    def backspace(self):
        """Remove last character"""
        if self.expression:
            self.expression = self.expression[:-1]
            self.update_display()

def main():
    root = tk.Tk()
    app = AdvancedCalculator(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()