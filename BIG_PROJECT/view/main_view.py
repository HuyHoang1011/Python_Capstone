import tkinter as tk
from tkinter import messagebox

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Student Card Processing")
        self.root.geometry("400x300")
        self.result_text = tk.StringVar()

        # GUI Elements
        tk.Label(self.root, text="MSSV Reader", font=("Arial", 16)).pack(pady=10)
        self.process_button = tk.Button(self.root, text="Process Images", command=self.run_process)
        self.process_button.pack(pady=10)

        self.result_label = tk.Label(self.root, textvariable=self.result_text, justify=tk.LEFT)
        self.result_label.pack(pady=10)

    def run_process(self):
        try:
            self.controller.process_images()
            self.result_text.set(self.controller.get_mssv_list())
            messagebox.showinfo("Success", "Processing completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.root.mainloop()
