import customtkinter as ctk
from tkinter import messagebox
import requests
import html

# SETTINGS
API_KEY = "your_api_key_here"  # Replace if using a real API
NUM_QUESTIONS = 5
API_URL = f"https://opentdb.com/api.php?amount={NUM_QUESTIONS}&type=multiple"

# CTk setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def fetch_questions():
    try:
        response = requests.get(API_URL)
        data = response.json()
        questions = []

        for item in data['results']:
            q_text = html.unescape(item['question'])
            correct = html.unescape(item['correct_answer'])
            options = [html.unescape(opt) for opt in item['incorrect_answers']]
            options.append(correct)
            options.sort()  # Shuffle if needed
            questions.append({
                "question": q_text,
                "options": options,
                "correct": correct
            })
        return questions
    except Exception as e:
        print("Error fetching questions:", e)
        return []

class QuizApp(ctk.CTk):
    def __init__(self, questions):
        super().__init__()
        self.title("Quiz App 🔥")
        self.geometry("500x360")
        self.configure(bg="black")

        self.questions = questions
        self.current_question = 0
        self.score = 0
        self.selected_option = None

        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="🧠 Quiz Master", font=("Segoe UI", 22, "bold"), text_color="red")
        self.title_label.pack(pady=(10, 5))

        self.question_label = ctk.CTkLabel(self, text="", wraplength=440, font=("Segoe UI", 16), text_color="white")
        self.question_label.pack(pady=(10, 15))

        self.option_buttons = []
        for _ in range(4):
            btn = ctk.CTkRadioButton(self, text="", command=self.option_selected,
                                     border_color="red", fg_color="red", hover_color="#cc0000")
            btn.pack(anchor="w", padx=40, pady=3)
            self.option_buttons.append(btn)

        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.check_answer,
                                        fg_color="red", hover_color="#cc0000", font=("Segoe UI", 15))
        self.submit_btn.pack(pady=15)

        self.footer = ctk.CTkLabel(self, text="🔎 Powered by Y7X 💗", font=("Segoe UI", 13), text_color="gray")
        self.footer.pack(pady=(5, 0))

    def load_question(self):
        q = self.questions[self.current_question]
        self.question_label.configure(text=f"Q{self.current_question + 1}: {q['question']}")
        self.selected_option = None

        for i, btn in enumerate(self.option_buttons):
            if i < len(q['options']):
                btn.configure(text=q['options'][i])
                btn.deselect()
                btn.pack(anchor="w", padx=40, pady=3)
            else:
                btn.pack_forget()

    def option_selected(self):
        for btn in self.option_buttons:
            if btn.get() == 1:
                self.selected_option = btn.cget("text")

    def check_answer(self):
        if not self.selected_option:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        correct = self.questions[self.current_question]['correct']
        if self.selected_option == correct:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Quiz Over", f"You scored {self.score} out of {len(self.questions)}!")
        self.destroy()

if __name__ == "__main__":
    questions_data = fetch_questions()
    if questions_data:
        app = QuizApp(questions_data)
        app.mainloop()
    else:
        print("❌ Failed to load quiz questions.")