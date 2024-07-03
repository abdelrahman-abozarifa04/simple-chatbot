import tkinter as tk
from tkinter import scrolledtext, messagebox, CENTER
from main import load_knowledge_base, find_best_match, get_answer_for_question, save_knowledge_base

class ChatBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Bot")
        self.knowledge_base = load_knowledge_base('knowledge_base.json')

        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        # Set font and colors
        font = ("Arial", 12)
        background_color = "#f0f0f0"
        button_color = "#3071B7"
        button_text_color = "white"

        # User input label and entry
        self.label_user_input = tk.Label(self, text="You:", font=font, bg=background_color)
        self.label_user_input.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.entry_user_input = tk.Entry(self, width=50, font=font)
        self.entry_user_input.grid(row=0, column=1, padx=10, pady=10)

        # Chat conversation display
        self.conversation_display = scrolledtext.ScrolledText(self, width=60, height=20, font=font)
        self.conversation_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message, bg=button_color, fg=button_text_color, font=font)
        self.send_button.grid(row=0, column=2, padx=10, pady=10)

        # Clear button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_conversation, bg=button_color, fg=button_text_color, font=font)
        self.clear_button.grid(row=1, column=2, padx=10, pady=10)

        # Bind Enter key to send_message function
        self.entry_user_input.bind('<Return>', lambda event: self.send_message())

    def center_window(self):
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate window position
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2

        # Set window position
        self.geometry(f"+{x}+{y}")

    def send_message(self):
        user_input = self.entry_user_input.get()
        if user_input.lower() == 'quit':
            self.quit()
        best_match = find_best_match(user_input, [q["question"] for q in self.knowledge_base["questions"]])
        if best_match:
            answer = get_answer_for_question(best_match, self.knowledge_base)
            self.update_conversation(f"You: {user_input}\nBot: {answer}\n")
        else:
            self.handle_unknown_question(user_input)

    def handle_unknown_question(self, user_input):
        new_answer = messagebox.askquestion("New Answer", "I don't know the answer. Do you want to provide an answer?")
        if new_answer == 'yes':
            answer_dialog = tk.Toplevel(self)
            answer_dialog.title("New Answer")
            answer_dialog.geometry("+%d+%d" % (self.winfo_x() + 50, self.winfo_y() + 50))

            label = tk.Label(answer_dialog, text="Type the answer:", font=("Arial", 12))
            label.pack()

            entry = tk.Entry(answer_dialog, font=("Arial", 12))
            entry.pack()

            def save_answer():
                new_answer_text = entry.get()
                if new_answer_text:
                    self.knowledge_base["questions"].append({"question": user_input, "answer": new_answer_text})
                    save_knowledge_base("knowledge_base.json", self.knowledge_base)
                    self.update_conversation(f"You: {user_input}\nBot: Thank you! I have learned a new response.\n")
                    answer_dialog.destroy()

            save_button = tk.Button(answer_dialog, text="Save", command=save_answer, bg="#4CAF50", fg="white", font=("Arial", 12))
            save_button.pack()

    def clear_conversation(self):
        self.conversation_display.delete('1.0', tk.END)

    def update_conversation(self, message):
        self.conversation_display.insert(tk.END, message)
        self.conversation_display.see(tk.END)
        self.entry_user_input.delete(0, tk.END)

def main():
    app = ChatBotApp()
    app.mainloop()

if __name__ == "__main__":
    main()
