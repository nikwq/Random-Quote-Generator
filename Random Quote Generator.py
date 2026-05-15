import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

DATA_FILE = "quotes.json"

# ========== ЗАГРУЗКА ДАННЫХ ==========
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            return d.get("quotes", []), d.get("history", [])
    # Начальные цитаты
    quotes = [
        {"text": "Будь изменением, которое хочешь видеть в мире", "author": "Ганди", "theme": "Мотивация"},
        {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы", "author": "Леннон", "theme": "Жизнь"},
        {"text": "Воображение важнее знания", "author": "Эйнштейн", "theme": "Знание"},
        {"text": "Единственный способ делать великую работу — любить её", "author": "Джобс", "theme": "Работа"}
    ]
    return quotes, []

def save_data(quotes, history):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"quotes": quotes, "history": history}, f, indent=4, ensure_ascii=False)

# ========== ГЕНЕРАЦИЯ ==========
def generate():
    quotes, history = load_data()
    if not quotes:
        messagebox.showwarning("Ошибка", "Нет цитат!")
        return
    
    quote = random.choice(quotes)
    history.append(quote)
    save_data(quotes, history)
    
    # Показываем
    label_text.config(text=f"«{quote['text']}»")
    label_author.config(text=f"— {quote['author']} —")
    
    # Обновляем историю
    for item in tree.get_children():
        tree.delete(item)
    
    # Фильтры
    f_author = filter_author.get()
    f_theme = filter_theme.get()
    
    for q in history:
        if f_author and q['author'] != f_author:
            continue
        if f_theme and q['theme'] != f_theme:
            continue
        tree.insert("", tk.END, values=(q['text'], q['author'], q['theme']))

# ========== ДОБАВЛЕНИЕ ==========
def add():
    text = entry_text.get().strip()
    author = entry_author.get().strip()
    theme = combo_theme.get()
    
    if not text or not author:
        messagebox.showerror("Ошибка", "Заполните текст и автора!")
        return
    
    quotes, history = load_data()
    quotes.append({"text": text, "author": author, "theme": theme})
    save_data(quotes, history)
    
    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    messagebox.showinfo("Успех", "Цитата добавлена!")
    
    # Обновляем фильтры
    authors = sorted(set(q['author'] for q in quotes))
    filter_author['values'] = [""] + authors
    themes = sorted(set(q['theme'] for q in quotes))
    filter_theme['values'] = [""] + themes

# ========== ПРИМЕНЕНИЕ ФИЛЬТРА ==========
def filter_history(event=None):
    generate()  # Просто обновляем

# ========== СОЗДАНИЕ ОКНА ==========
root = tk.Tk()
root.title("Генератор цитат")
root.geometry("700x550")

# ---------- Текущая цитата ----------
frame1 = tk.LabelFrame(root, text="Случайная цитата", padx=10, pady=10)
frame1.pack(fill="x", padx=10, pady=5)

label_text = tk.Label(frame1, text="Нажмите кнопку", font=("Arial", 12, "italic"), wraplength=600)
label_text.pack(pady=10)
label_author = tk.Label(frame1, text="", font=("Arial", 10), fg="gray")
label_author.pack()

tk.Button(frame1, text="🎲 Сгенерировать", command=generate, bg="lightblue", font=("Arial", 10)).pack(pady=10)

# ---------- Добавление ----------
frame2 = tk.LabelFrame(root, text="Добавить цитату", padx=10, pady=10)
frame2.pack(fill="x", padx=10, pady=5)

tk.Label(frame2, text="Текст:").grid(row=0, column=0, padx=5)
entry_text = tk.Entry(frame2, width=50)
entry_text.grid(row=0, column=1, padx=5)

tk.Label(frame2, text="Автор:").grid(row=1, column=0, padx=5)
entry_author = tk.Entry(frame2, width=20)
entry_author.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frame2, text="Тема:").grid(row=1, column=2, padx=5)
combo_theme = ttk.Combobox(frame2, values=["Мотивация", "Жизнь", "Знание", "Работа"], width=12)
combo_theme.set("Мотивация")
combo_theme.grid(row=1, column=3, padx=5)

tk.Button(frame2, text="➕ Добавить", command=add, bg="lightgreen").grid(row=2, column=0, columnspan=4, pady=5)

# ---------- Фильтры ----------
frame3 = tk.LabelFrame(root, text="Фильтр истории", padx=10, pady=10)
frame3.pack(fill="x", padx=10, pady=5)

tk.Label(frame3, text="Автор:").grid(row=0, column=0, padx=5)
filter_author = ttk.Combobox(frame3, width=20, state="readonly")
filter_author.grid(row=0, column=1, padx=5)
filter_author.bind("<<ComboboxSelected>>", filter_history)

tk.Label(frame3, text="Тема:").grid(row=0, column=2, padx=5)
filter_theme = ttk.Combobox(frame3, width=15, state="readonly")
filter_theme.grid(row=0, column=3, padx=5)
filter_theme.bind("<<ComboboxSelected>>", filter_history)

# ---------- История ----------
frame4 = tk.LabelFrame(root, text="История", padx=10, pady=10)
frame4.pack(fill="both", expand=True, padx=10, pady=5)

tree = ttk.Treeview(frame4, columns=("Текст", "Автор", "Тема"), show="headings", height=10)
tree.heading("Текст", text="Цитата")
tree.heading("Автор", text="Автор")
tree.heading("Тема", text="Тема")
tree.column("Текст", width=350)
tree.column("Автор", width=120)
tree.column("Тема", width=100)

scroll = ttk.Scrollbar(frame4, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# ========== ЗАПУСК ==========
if not os.path.exists(DATA_FILE):
    q, h = load_data()
    save_data(q, h)

# Обновляем фильтры
quotes, _ = load_data()
filter_author['values'] = [""] + sorted(set(q['author'] for q in quotes))
filter_theme['values'] = [""] + sorted(set(q['theme'] for q in quotes))

root.mainloop()
