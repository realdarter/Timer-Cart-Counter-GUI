import tkinter as tk
import time
import datetime

class TimerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Timer and Counter")
        self.master.attributes("-topmost", True)  # Set the window to stay on top

        self.timer_running = False
        self.start_time = None
        self.elapsed_time = 0

        self.cart_count = 0

        self.dark_mode = False

        self.timer_entry = tk.Entry(self.master, font=("Helvetica", 24), width=7)
        self.timer_entry.insert(tk.END, "00:00:00")
        self.timer_entry.grid(row=0, column=0, columnspan=2, pady=0)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, width=6, height=3)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer, state=tk.DISABLED, width=6, height=3, bg="light gray")
        self.pause_button.grid(row=3, column=0, padx=5, pady=5)

        self.cart_label = tk.Label(self.master, text="Count: 0", font=("Helvetica", 14))
        self.cart_label.grid(row=1, column=0, columnspan=2, pady=0)

        self.add_button = tk.Button(self.master, text="Add", command=self.add_to_cart, width=6, height=3, bg="#4bad6a")
        self.add_button.grid(row=2, column=1, padx=5, pady=5)

        self.sub_button = tk.Button(self.master, text="Sub", command=self.subtract_from_cart, width=6, height=3, bg="#f2575f")
        self.sub_button.grid(row=3, column=1, padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=2, rowspan=4, sticky=tk.N+tk.S)

        self.text_box = tk.Listbox(self.master, yscrollcommand=self.scrollbar.set, width=30)
        self.text_box.grid(row=0, column=3, columnspan=2, rowspan=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar.config(command=self.text_box.yview)
        self.text_box.bind("<Double-Button-1>", self.edit_item)

        self.mode_button = tk.Button(self.master, text="T", command=self.toggle_mode, width=2, height=1)
        self.mode_button.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)

        self.set_light_mode()

    def set_dark_mode(self):
        bg_color = "#282828"
        fg_color = "white"
        button_bg = "#383838"
        button_fg = "white"

        self.master.config(bg=bg_color)

        self.timer_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.start_button.config(bg=button_bg, fg=button_fg)
        self.pause_button.config(bg=button_bg, fg=button_fg)
        self.cart_label.config(bg=bg_color, fg=fg_color)
        self.add_button.config(bg="#4bad6a", fg=button_fg)
        self.sub_button.config(bg="#f2575f", fg=button_fg)
        self.text_box.config(bg=bg_color, fg=fg_color)
        self.scrollbar.config(bg=bg_color)
        self.mode_button.config(bg=button_bg, fg=button_fg)
        
    def set_light_mode(self):
        bg_color = "white"
        fg_color = "black"
        button_bg = "#eaeaea"
        button_fg = "black"

        self.master.config(bg=bg_color)

        self.timer_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.start_button.config(bg=button_bg, fg=button_fg)
        self.pause_button.config(bg=button_bg, fg=button_fg)
        self.cart_label.config(bg=bg_color, fg=fg_color)
        self.add_button.config(bg="#4bad6a", fg=button_fg)
        self.sub_button.config(bg="#f2575f", fg=button_fg)
        self.text_box.config(bg=bg_color, fg=fg_color)
        self.scrollbar.config(bg=bg_color)
        self.mode_button.config(bg=button_bg, fg=button_fg)

    def toggle_mode(self):
        if self.dark_mode:
            self.set_light_mode()
            self.dark_mode = False
        else:
            self.set_dark_mode()
            self.dark_mode = True

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            entered_time = self.timer_entry.get()
            try:
                hours, minutes, seconds = map(int, entered_time.split(":"))
                self.elapsed_time = hours * 3600 + minutes * 60 + seconds
            except ValueError:
                self.timer_entry.delete(0, tk.END)
                self.timer_entry.insert(tk.END, "00:00:00")
                self.elapsed_time = 0

            self.start_time = time.time()
            self.update_timer()
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time += time.time() - self.start_time
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.timer_running:
            elapsed = self.elapsed_time + time.time() - self.start_time
            minutes, seconds = divmod(elapsed, 60)
            hours, minutes = divmod(minutes, 60)
            time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            self.timer_entry.delete(0, tk.END)
            self.timer_entry.insert(tk.END, time_str)
            self.master.after(1000, self.update_timer)

    def add_to_cart(self):
        entered_time = self.timer_entry.get()
        self.cart_count += 1
        self.update_cart_label()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time as a string
        item = self.text_box.size() + 1
        self.text_box.insert(tk.END, f"{entered_time}, {current_time}")  # Add current time to the list item
        self.text_box.itemconfig(item - 1, bg="white")
        self.text_box.bind("<Double-Button-1>", self.edit_item)

    def subtract_from_cart(self):
        if self.cart_count > 0:
            self.cart_count -= 1
            self.update_cart_label()
            if self.text_box.size() > 0:
                self.text_box.delete(tk.END)

    def update_cart_label(self):
        self.cart_label.config(text=f"Count: {self.cart_count}")

    def edit_item(self, event):
        selected_index = self.text_box.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.text_box.itemconfig(selected_index, bg="yellow")
            self.text_box.bind("<Return>", lambda event: self.update_item(event, selected_index))
            self.text_box.bind("<FocusOut>", lambda event: self.update_item(event, selected_index))
            self.text_box.focus_set()
            self.text_box.select_set(selected_index)
            self.text_box.selection_set(tk.END)

    def update_item(self, event, index):
        new_time = self.text_box.get(index)  # Corrected from listbox to text_box
        self.text_box.itemconfig(index, bg="white")
        self.text_box.unbind("<Return>")
        self.text_box.unbind("<FocusOut>")
        self.text_box.bind("<Double-Button-1>", self.edit_item)
        self.text_box.focus_set()
        self.text_box.select_clear(index)
        self.text_box.delete(index)
        self.text_box.insert(index, new_time)


root = tk.Tk()
root.resizable(False, False)
timer_gui = TimerGUI(root)
root.mainloop()
