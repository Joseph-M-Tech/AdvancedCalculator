import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Custom font
        self.display_font = font.Font(family="Arial", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=14)
        
        # Variables
        self.current_input = ""
        self.result = ""
        self.operation = ""
        self.waiting_for_operand = False
        
        # Color scheme
        self.colors = {
            "display_bg": "#2d2d2d",
            "display_fg": "#ffffff",
            "button_bg": "#f0f0f0",
            "button_fg": "#000000",
            "operator_bg": "#ff9500",
            "operator_fg": "#ffffff",
            "clear_bg": "#a6a6a6",
            "clear_fg": "#000000",
            "equals_bg": "#ff9500",
            "equals_fg": "#ffffff"
        }
        
        self.setup_ui()
        self.bind_keys()
    
    def setup_ui(self):
        # Create display frame
        display_frame = tk.Frame(self.root, height=100)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Display widget
        self.display = tk.Entry(
            display_frame,
            font=self.display_font,
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"],
            borderwidth=0,
            justify="right",
            readonlybackground=self.colors["display_bg"]
        )
        self.display.pack(fill=tk.BOTH, expand=True, ipady=15)
        self.display.config(state='readonly')
        self.update_display()
        
        # Create button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
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
        
        # Create buttons
        for text, row, col, rowspan, colspan, bg_color in buttons:
            fg_color = self.colors["operator_fg"] if bg_color == self.colors["operator_bg"] else self.colors["button_fg"]
            if text == '=':
                fg_color = self.colors["equals_fg"]
            elif text in ['C', '⌫']:
                fg_color = self.colors["clear_fg"]
            
            button = tk.Button(
                button_frame,
                text=text,
                font=self.button_font,
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
            
            # Make button expand
            button_frame.grid_rowconfigure(row, weight=1)
            button_frame.grid_columnconfigure(col, weight=1)
    
    def bind_keys(self):
        # Bind keyboard keys
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<Delete>', lambda e: self.clear_entry())
        
        # Focus on root window to capture key events
        self.root.focus_set()
    
    def update_display(self):
        """Update the display with current input or result"""
        display_text = self.current_input if self.current_input else "0"
        if len(display_text) > 20:
            display_text = display_text[:20]
        
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, display_text)
        self.display.config(state='readonly')
    
    def on_button_click(self, value):
        """Handle button clicks"""
        if value.isdigit():
            self.input_digit(value)
        elif value == '.':
            self.input_decimal()
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
        elif value in ['+', '-', '×', '÷']:
            self.set_operation(value)
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear_all()
        elif value == '⌫':
            self.backspace()
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit():
            self.input_digit(key)
        elif key in ['+', '-', '*', '/']:
            op_map = {'+': '+', '-': '-', '*': '×', '/': '÷'}
            self.set_operation(op_map[key])
        elif key == '.':
            self.input_decimal()
        elif key in ['=', '\r']:
            self.calculate()
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key == '\x1b':  # Escape
            self.clear_all()
    
    def input_digit(self, digit):
        """Input a digit"""
        if self.waiting_for_operand:
            self.current_input = ""
            self.waiting_for_operand = False
        
        # Prevent leading zeros
        if digit == '0' and (self.current_input == '0' or self.current_input == ''):
            self.current_input = '0'
        elif self.current_input == '0':
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
    
    def input_decimal(self):
        """Input decimal point"""
        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
        elif '.' not in self.current_input:
            if not self.current_input:
                self.current_input = "0."
            else:
                self.current_input += '.'
            self.update_display()
    
    def toggle_sign(self):
        """Toggle positive/negative sign"""
        if self.current_input and self.current_input != '0':
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        """Convert to percentage"""
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                self.current_input = str(value)
                self.update_display()
            except ValueError:
                self.current_input = "Error"
                self.update_display()
    
    def set_operation(self, op):
        """Set the operation to perform"""
        if self.current_input:
            if self.operation and not self.waiting_for_operand:
                self.calculate()
            
            self.result = self.current_input
            self.operation = op
            self.waiting_for_operand = True
    
    def calculate(self):
        """Perform the calculation"""
        if not self.operation or not self.result or not self.current_input:
            return
        
        try:
            num1 = float(self.result)
            num2 = float(self.current_input)
            
            if self.operation == '+':
                result = num1 + num2
            elif self.operation == '-':
                result = num1 - num2
            elif self.operation == '×':
                result = num1 * num2
            elif self.operation == '÷':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2
            else:
                return
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limit decimal places
                    result = round(result, 10)
            
            self.current_input = str(result)
            self.operation = ""
            self.result = ""
            self.waiting_for_operand = True
            
        except (ValueError, ZeroDivisionError):
            self.current_input = "Error"
            self.operation = ""
            self.result = ""
            self.waiting_for_operand = True
        
        self.update_display()
    
    def clear_all(self):
        """Clear everything"""
        self.current_input = ""
        self.result = ""
        self.operation = ""
        self.waiting_for_operand = False
        self.update_display()
    
    def clear_entry(self):
        """Clear current entry"""
        self.current_input = ""
        self.update_display()
    
    def backspace(self):
        """Remove last character"""
        if self.current_input and not self.waiting_for_operand:
            self.current_input = self.current_input[:-1]
            if not self.current_input or self.current_input == '-':
                self.current_input = ""
            self.update_display()

def main():
    root = tk.Tk()
    app = Calculator(root)
    
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