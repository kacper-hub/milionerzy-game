import tkinter as tk
from tkinter import font
import json
import random
from itertools import cycle
from PIL import Image, ImageTk  # Zaimportowanie bibliotek do obsługi obrazków

# Kolorystyka
COLORS = {
    "background": "#2c3e50",
    "question": "#ecf0f1",
    "button": "#3498db",
    "correct": "#2ecc71",
    "wrong": "#e74c3c",
    "text": "#2c3e50",
    "highlight": "#f1c40f",
    "timer": "#e67e22",
    "menu_button": "#9b59b6"
}

# Lista nagród
nagrody = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000,
           64000, 125000, 250000, 500000, 1000000]

class MainMenu(tk.Frame):
    def __init__(self, master, start_callback):
        super().__init__(master, bg=COLORS["background"])
        self.master = master

        # Wczytanie zdjęcia tła
        self.bg_image = Image.open("pliczek.jpg")  # Wczytanie pliku 'pliczek.jpg' (upewnij się, że jest w tym samym folderze)
        self.bg_image = self.bg_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))  # Dopasowanie do rozmiaru ekranu
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Ustawienie tła
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Wypełnia całe okno
        
        # Główny napis
        self.title_label = tk.Label(self, text="VETTER", font=("Arial", 128, "bold"),  # Większy napis 
                                  fg=COLORS["highlight"], bg=COLORS["background"])
        self.title_label.pack(pady=150)
        
        # Przycisk startowy
        self.start_button = tk.Button(self, text="ROZPOCZNIJ GRĘ", font=("Arial", 32, "bold"),
                                    bg=COLORS["menu_button"], fg=COLORS["text"], relief="ridge",
                                    borderwidth=5, command=start_callback)
        self.start_button.pack(pady=50, ipadx=20, ipady=10)
        
        # Stopka z autorami
        self.credits_label = tk.Label(self, text="by Dominik Kwiatkowski, Kacper Kurlak",
                                    font=("Arial", 10), bg=COLORS["background"], fg=COLORS["question"])
        self.credits_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

class MilionerzyGame(tk.Frame):
    def __init__(self, master, return_to_menu_callback):
        super().__init__(master, bg=COLORS["background"])
        self.master = master
        self.return_to_menu = return_to_menu_callback
        
        # Wczytaj pytania
        sets = ["physics_set1.json", "physics_set2.json", "physics_set3.json", "physics_set4.json", "physics_set5.json", "physics_set6.json", "physics_set7.json", "physics_set8.json", "physics_set9.json"]
        chosen_set = random.choice(sets)
        with open(chosen_set, 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
        self.questions = random.sample(all_questions, min(15, len(all_questions)))
        
        self.current_question_index = 0
        self.score = 0
        self.buttons_blocked = False
        self.time_left = 30
        self.lifelines = {"50:50": True, "public": True}

        # Panel czasowy
        self.timer_frame = tk.Frame(self, bg=COLORS["background"])
        self.timer_frame.pack(pady=10)
        
        self.timer_label = tk.Label(self.timer_frame, text="Czas: 30", bg=COLORS["background"], 
                                  fg=COLORS["timer"], font=("Arial", 16, "bold"))
        self.timer_label.pack(side=tk.LEFT)
        
        self.progress_bar = tk.Canvas(self.timer_frame, width=200, height=20, bg=COLORS["background"], 
                                    highlightthickness=0)
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.progress = self.progress_bar.create_rectangle(0, 0, 200, 20, fill=COLORS["timer"])
        
        # Koła ratunkowe
        self.lifeline_frame = tk.Frame(self, bg=COLORS["background"])
        self.lifeline_frame.pack(pady=10)
        
        self.lifeline_buttons = {
            "50:50": tk.Button(self.lifeline_frame, text="50:50", width=8,
                             font=("Arial", 12, "bold"), bg=COLORS["button"],
                             fg=COLORS["text"], relief="ridge", borderwidth=3,
                             command=self.use_fifty_fifty),
            "public": tk.Button(self.lifeline_frame, text="Publiczność", width=12,
                              font=("Arial", 12, "bold"), bg=COLORS["button"],
                              fg=COLORS["text"], relief="ridge", borderwidth=3,
                              command=self.use_audience_poll)
        }
        
        for btn in self.lifeline_buttons.values():
            btn.pack(side=tk.LEFT, padx=5, ipady=5)

        # Główny kontener
        self.container = tk.Frame(self, bg=COLORS["background"])
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Etykieta z komunikatem
        self.feedback_label = tk.Label(self.container, text="", bg=COLORS["background"], 
                                     fg=COLORS["question"], font=("Arial", 16, "bold"))
        self.feedback_label.pack(pady=10)

        # Panel z pytaniem
        self.question_label = tk.Label(self.container, text="", wraplength=1500, 
                                     bg=COLORS["background"], fg=COLORS["question"],
                                     font=("Arial", 48, "bold"))
        self.question_label.pack(pady=20)

        # Przyciski z odpowiedziami
        self.buttons_frame = tk.Frame(self.container, bg=COLORS["background"])
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        self.buttons = []
        self.button_colors = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", width=70,
                          font=("Arial", 24, "bold"), bg=COLORS["button"],
                          fg=COLORS["text"], relief="ridge", borderwidth=3,
                          command=lambda i=i: self.check_answer(i))
            btn.pack(pady=8, ipady=8)
            self.buttons.append(btn)
            self.button_colors.append(cycle([COLORS["button"], "#2980b9", "#3498db", "#2980b9"]))

        # Panel boczny z drabinką nagród
        self.drabinka_frame = tk.Frame(self, bg=COLORS["background"], padx=10)
        self.drabinka_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.drabinka_labels = []
        for i, kwota in enumerate(reversed(nagrody)):
            lbl = tk.Label(self.drabinka_frame, text=f"{kwota} zł", 
                         bg=COLORS["background"], fg=COLORS["question"],
                         font=("Arial", 12, "bold" if i == 0 else ""))
            lbl.pack(pady=3, padx=10, ipadx=10)
            self.drabinka_labels.append(lbl)
        
        self.update_drabinka()
        self.next_question()
        self.start_pulsing()
        self.start_timer()

    def update_drabinka(self):
        idx = len(nagrody) - self.current_question_index - 1
        for i, lbl in enumerate(self.drabinka_labels):
            lbl.config(
                bg=COLORS["highlight"] if i == idx else COLORS["background"],
                fg=COLORS["text"] if i == idx else COLORS["question"],
                font=("Arial", 14, "bold") if i == idx else ("Arial", 12)
            )

    def start_pulsing(self):
        for i, btn in enumerate(self.buttons):
            if btn["state"] == tk.NORMAL:
                btn.config(bg=next(self.button_colors[i]))
        self.master.after(500, self.start_pulsing)

    def start_timer(self):
        if self.time_left > 0 and not self.buttons_blocked:
            self.time_left -= 1
            self.timer_label.config(text=f"Czas: {self.time_left}")
            self.progress_bar.coords(self.progress, 0, 0, 200 * (self.time_left/30), 20)
            self.master.after(1000, self.start_timer)
        elif self.time_left <= 0:
            self.timeout()

    def reset_timer(self):
        self.time_left = 30
        self.timer_label.config(text="Czas: 30")
        self.progress_bar.coords(self.progress, 0, 0, 200, 20)

    def timeout(self):
        self.show_feedback("Czas upłynął! ⏳", COLORS["wrong"])
        self.block_buttons()
        self.master.after(2000, self.show_final_score)

    def use_fifty_fifty(self):
        if self.lifelines["50:50"] and not self.buttons_blocked:
            self.lifelines["50:50"] = False
            self.lifeline_buttons["50:50"].config(state=tk.DISABLED)
            q = self.questions[self.current_question_index]
            wrong_answers = [i for i, (oi, _) in enumerate(self.current_answers) if oi != q["poprawna"]]
            for i in random.sample(wrong_answers, 2):
                self.buttons[i].config(text="", state=tk.DISABLED)

    def use_audience_poll(self):
        if self.lifelines["public"] and not self.buttons_blocked:
            self.lifelines["public"] = False
            self.lifeline_buttons["public"].config(state=tk.DISABLED)
            q = self.questions[self.current_question_index]
            correct_index = next(i for i, (oi, _) in enumerate(self.current_answers) if oi == q["poprawna"])
            percentages = [random.randint(5, 20) for _ in range(4)]
            percentages[correct_index] += random.randint(30, 60)
            total = sum(percentages)
            for i, btn in enumerate(self.buttons):
                btn.config(text=f"{btn['text']} ({int(percentages[i]/total*100)}%)")

    def next_question(self):
        self.reset_timer()
        if self.current_question_index < len(self.questions):
            q = self.questions[self.current_question_index]
            self.question_label.config(text=q["pytanie"])
            self.current_answers = list(enumerate(q["odpowiedzi"]))
            random.shuffle(self.current_answers)
            for i, (orig_index, answer) in enumerate(self.current_answers):
                self.buttons[i].config(text=answer, state=tk.NORMAL)
            self.feedback_label.config(text="")
            self.buttons_blocked = False
            self.update_drabinka()
            self.start_timer()
        else:
            self.show_final_score()

    def show_feedback(self, message, color):
        self.feedback_label.config(text=message, fg=color)

    def block_buttons(self):
        self.buttons_blocked = True
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def check_answer(self, chosen_index):
        if self.buttons_blocked:
            return
            
        self.block_buttons()
        q = self.questions[self.current_question_index]
        orig_index = self.current_answers[chosen_index][0]
        
        # Podświetl odpowiedzi
        for i, (oi, ans) in enumerate(self.current_answers):
            if oi == q["poprawna"]:
                self.buttons[i].config(bg=COLORS["correct"])
            elif i == chosen_index:
                self.buttons[i].config(bg=COLORS["wrong"])

        if orig_index == q["poprawna"]:
            self.score += 1
            self.show_feedback("Poprawna odpowiedź! ✔️", COLORS["correct"])
            self.master.after(2000, self.move_to_next_question)
        else:
            self.show_feedback("Niepoprawna odpowiedź! ❌", COLORS["wrong"])
            self.master.after(2000, self.show_final_score)

    def move_to_next_question(self):
        self.current_question_index += 1
        self.next_question()

    def show_final_score(self):
        for btn in self.buttons:
            btn.pack_forget()
        
        if self.score == 14:
            final_text = (f"BRAWO WYGRALES MILION!!!")
        elif self.score > 0:
            final_text = (f"KONIEC GRY! Zdobyta kwota: {nagrody[self.score-1]} zł")
        else:
            final_text = (f"KONIEC GRY!")

        self.question_label.config(text=final_text)
        self.feedback_label.config(text="Dziękujemy za grę!")
        self.reset_timer()
        self.master.after(3000, self.return_to_menu)

class GameController:
    def __init__(self, root):
        self.root = root
        self.root.title("VETTER - Milionerzy")
        screen_width = self.root.winfo_screenwidth()  # Pobranie szerokości ekranu
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")  # Ustawienie szerokości na pełną szerokość ekranu, wysokość 700px
        self.show_menu()

    def show_menu(self):
        if hasattr(self, 'game'):
            self.game.destroy()
        self.menu = MainMenu(self.root, self.start_game)
        self.menu.pack(fill=tk.BOTH, expand=True)

    def start_game(self):
        self.menu.pack_forget()
        self.game = MilionerzyGame(self.root, self.show_menu)
        self.game.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameController(root)
    root.mainloop()