import customtkinter as ctk
from tkinter import messagebox
import requests
import html

API_URL = "https://opentdb.com/api.php?amount=5&type=multiple"

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
            options.sort()
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
        self.title("QuizVerse 🌌")
        self.geometry("520x420")
        self.configure(bg="#1e1e1e")  # Dark but not AMOLED

        self.questions = questions
        self.current_question = 0
        self.score = 0
        self.selected_option = ctk.StringVar()

        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="🌌 QuizVerse", font=("Segoe UI", 22, "bold"), text_color="red")
        self.title_label.pack(pady=(10, 5))

        self.question_label = ctk.CTkLabel(self, text="", wraplength=460, font=("Segoe UI", 16), text_color="white")
        self.question_label.pack(pady=(10, 15))

        self.option_buttons = []
        for _ in range(4):
            btn = ctk.CTkRadioButton(
                self,
                text="",
                variable=self.selected_option,
                border_color="red",
                fg_color="red",
                hover_color="#ff4d4d",
                text_color="white",
                font=("Segoe UI", 14),
                bg_color="#1e1e1e"
            )
            btn.pack(anchor="w", padx=50, pady=5)
            self.option_buttons.append(btn)

        self.submit_btn = ctk.CTkButton(
            self, text="Submit", command=self.check_answer,
            fg_color="red", hover_color="#cc0000", font=("Segoe UI", 15)
        )
        self.submit_btn.pack(pady=15)

        self.footer = ctk.CTkLabel(
            self, text="🔎 Powered by Y7X 💗", font=("Segoe UI", 13), text_color="gray"
        )
        self.footer.pack(pady=(5, 0))

    def load_question(self):
        q = self.questions[self.current_question]
        self.question_label.configure(text=f"Q{self.current_question + 1}: {q['question']}")
        self.selected_option.set("")

        for i, btn in enumerate(self.option_buttons):
            if i < len(q['options']):
                btn.configure(text=q['options'][i])
                btn._value = q['options'][i]
                btn.pack(anchor="w", padx=50, pady=5)
            else:
                btn.pack_forget()

    def check_answer(self):
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        correct = self.questions[self.current_question]['correct']
        if selected == correct:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Quiz Complete", f"You scored {self.score} out of {len(self.questions)}!")
        self.destroy()

if __name__ == "__main__":
    questions_data = fetch_questions()
    if questions_data:
        app = QuizApp(questions_data)
        app.mainloop()
    else:
        print("❌ Failed to load quiz questions.")