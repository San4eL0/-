import json
import random
import tkinter as tk
from tkinter import messagebox, ttk

# Предопределённые задачи
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть вебинар", "type": "учёба"},
    {"text": "Пробежка 20 минут", "type": "спорт"},
    {"text": "Обновить документацию", "type": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.tasks = self.load_tasks()
        self.history = []

        # Интерфейс
        self.create_widgets()
        self.update_filtered_list()

    def create_widgets(self):
        # Рамка для генерации
        frame_gen = tk.Frame(self.root)
        frame_gen.pack(pady=10)

        self.task_label = tk.Label(frame_gen, text="Нажмите кнопку", font=("Arial", 14), wraplength=500)
        self.task_label.pack(pady=5)

        self.gen_button = tk.Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task, bg="#4CAF50", fg="white")
        self.gen_button.pack(pady=5)

        # Рамка добавления новой задачи
        frame_add = tk.LabelFrame(self.root, text="Добавить новую задачу")
        frame_add.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_add, text="Текст задачи:").grid(row=0, column=0, padx=5, pady=5)
        self.new_task_entry = tk.Entry(frame_add, width=40)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="учёба")
        type_menu = ttk.Combobox(frame_add, textvariable=self.type_var, values=["учёба", "спорт", "работа"], state="readonly")
        type_menu.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(frame_add, text="Добавить", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Рамка фильтрации истории
        frame_filter = tk.LabelFrame(self.root, text="Фильтр по типу")
        frame_filter.pack(pady=10, padx=10, fill="x")

        self.filter_var = tk.StringVar(value="все")
        filter_all = tk.Radiobutton(frame_filter, text="Все", variable=self.filter_var, value="все", command=self.on_filter_change)
        filter_study = tk.Radiobutton(frame_filter, text="Учёба", variable=self.filter_var, value="учёба", command=self.on_filter_change)
        filter_sport = tk.Radiobutton(frame_filter, text="Спорт", variable=self.filter_var, value="спорт", command=self.on_filter_change)
        filter_work = tk.Radiobutton(frame_filter, text="Работа", variable=self.filter_var, value="работа", command=self.on_filter_change)

        filter_all.pack(side="left", padx=10)
        filter_study.pack(side="left", padx=10)
        filter_sport.pack(side="left", padx=10)
        filter_work.pack(side="left", padx=10)

        # Список истории
        frame_history = tk.LabelFrame(self.root, text="История задач")
        frame_history.pack(pady=10, padx=10, fill="both", expand=True)

        self.history_listbox = tk.Listbox(frame_history, height=12)
        self.history_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_history)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

    def load_tasks(self):
        """Загрузка задач из JSON, если файл существует"""
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return DEFAULT_TASKS.copy()

    def save_tasks(self):
        """Сохранение текущего списка задач в JSON"""
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self):
        """Валидация и добавление новой задачи"""
        text = self.new_task_entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка ввода", "Текст задачи не может быть пустым!")
            return
        task_type = self.type_var.get()
        self.tasks.append({"text": text, "type": task_type})
        self.save_tasks()
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{text}' добавлена!")

    def generate_task(self):
        """Генерация случайной задачи и сохранение в истории"""
        if not self.tasks:
            messagebox.showwarning("Нет задач", "Список задач пуст! Добавьте хотя бы одну.")
            return

        task = random.choice(self.tasks)
        self.history.append(task)
        self.save_history()
        self.task_label.config(text=f"✨ {task['text']} [{task['type']}] ✨")
        self.update_filtered_list()

    def save_history(self):
        """Сохранение истории в JSON"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Загрузка истории из JSON при старте"""
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []

    def on_filter_change(self):
        """Обработчик изменения фильтра"""
        self.update_filtered_list()

    def update_filtered_list(self):
        """Обновление списка истории с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()

        for task in self.history:
            if filter_type == "все" or task["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{task['text']} ({task['type']})")

    def run(self):
        self.load_history()
        self.update_filtered_list()
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    app.run()"""
Random Task Generator - GUI приложение для генерации случайных задач
Автор: Александр Шило
Версия: 1.0.0 (Функциональная версия)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================

# Цветовая схема
COLORS = {
    "primary": "#4CAF50",
    "secondary": "#2196F3",
    "danger": "#f44336",
    "warning": "#FF9800",
    "dark": "#333333",
    "light": "#f5f5f5"
}

# Предопределённые задачи
DEFAULT_TASKS = [
    {"name": "Прочитать статью по Python", "type": "учёба"},
    {"name": "Сделать зарядку 15 минут", "type": "спорт"},
    {"name": "Закончить отчёт по работе", "type": "работа"},
    {"name": "Выучить 10 новых английских слов", "type": "учёба"},
    {"name": "Пробежка 2 км", "type": "спорт"},
    {"name": "Провести встречу с клиентом", "type": "работа"},
    {"name": "Посмотреть лекцию по машинному обучению", "type": "учёба"},
    {"name": "Йога и медитация 20 минут", "type": "спорт"},
    {"name": "Сделать код-ревью коллегам", "type": "работа"},
    {"name": "Решить 3 задачи на LeetCode", "type": "учёба"},
    {"name": "Отжимания 50 раз", "type": "спорт"},
    {"name": "Составить план на неделю", "type": "работа"}
]

# Глобальные переменные состояния
tasks = DEFAULT_TASKS.copy()
history = []
current_filter = "все"
data_file = "task_history.json"

# Ссылки на виджеты (будут установлены при создании UI)
generate_btn = None
current_task_label = None
filter_var = None
filter_menu = None
task_name_entry = None
task_type_var = None
history_listbox = None
stats_label = None
root_window = None


# ==================== ФУНКЦИИ РАБОТЫ С ДАННЫМИ ====================

def save_data():
    """Сохранение данных в JSON"""
    global history, tasks
    try:
        data = {
            "history": history,
            "custom_tasks": [task for task in tasks if task not in DEFAULT_TASKS],
            "last_saved": datetime.now().isoformat(),
            "total_tasks_generated": len(history)
        }
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")


def load_data():
    """Загрузка данных из JSON"""
    global history, tasks
    if not os.path.exists(data_file):
        return
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        history = data.get("history", [])
        custom_tasks = data.get("custom_tasks", [])
        tasks = DEFAULT_TASKS.copy() + custom_tasks
        
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        history = []


# ==================== ФУНКЦИИ ВАЛИДАЦИИ ====================

def is_valid_task_name(name):
    """Проверка валидности названия задачи"""
    name = name.strip()
    if not name:
        return False, "Название задачи не может быть пустым!"
    if len(name) < 3:
        return False, f"Название слишком короткое! Минимум 3 символа (сейчас {len(name)})"
    if len(name) > 100:
        return False, f"Название слишком длинное! Максимум 100 символов (сейчас {len(name)})"
    return True, ""


def is_duplicate(name):
    """Проверка на дубликат"""
    name_lower = name.strip().lower()
    for task in tasks:
        if task["name"].lower() == name_lower:
            return True, f"Задача '{name}' уже существует!"
    return False, ""


# ==================== ФУНКЦИИ РАБОТЫ С ЗАДАЧАМИ ====================

def get_available_tasks():
    """Получение задач с учётом фильтра"""
    global tasks, current_filter
    if current_filter == "все":
        return tasks
    return [task for task in tasks if task["type"] == current_filter]


def generate_task():
    """Генерация случайной задачи"""
    global history, generate_btn, current_task_label, root_window
    
    available_tasks = get_available_tasks()
    
    if not available_tasks:
        messagebox.showwarning("⚠️ Нет задач", 
                              "Нет доступных задач для выбранного фильтра!\n\n"
                              "Пожалуйста:\n"
                              "• Добавьте новую задачу\n"
                              "• Или измените фильтр")
        return
    
    selected_task = random.choice(available_tasks)
    
    # Эмодзи для типов задач
    type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
    emoji = type_emoji.get(selected_task["type"], "✨")
    
    # Отображение текущей задачи
    current_task_label.config(
        text=f"{emoji}  {selected_task['name']}  {emoji}",
        fg=COLORS["primary"],
        font=("Arial", 15, "bold")
    )
    
    # Добавление в историю с временной меткой
    history_entry = {
        "name": selected_task["name"],
        "type": selected_task["type"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(history_entry)
    save_data()
    refresh_history()
    update_stats()
    flash_button()


def add_task():
    """Добавление новой задачи с валидацией"""
    global tasks, task_name_entry, task_type_var
    
    task_name = task_name_entry.get().strip()
    task_type = task_type_var.get()
    
    # Валидация
    is_valid, error_msg = is_valid_task_name(task_name)
    if not is_valid:
        messagebox.showwarning("❌ Ошибка валидации", error_msg)
        return
    
    is_dup, dup_msg = is_duplicate(task_name)
    if is_dup:
        messagebox.showwarning("❌ Ошибка валидации", dup_msg)
        return
    
    # Добавление задачи
    new_task = {"name": task_name, "type": task_type}
    tasks.append(new_task)
    
    # Очистка поля ввода
    task_name_entry.delete(0, tk.END)
    
    # Успешное добавление
    type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
    emoji = type_emoji.get(task_type, "✅")
    
    messagebox.showinfo("✅ Успех", 
                       f"{emoji} Задача успешно добавлена!\n\n"
                       f"Название: {task_name}\n"
                       f"Тип: {task_type}")
    
    refresh_history()


# ==================== ФУНКЦИИ ОБНОВЛЕНИЯ ИНТЕРФЕЙСА ====================

def refresh_history():
    """Обновление отображения истории"""
    global history_listbox, history, current_filter
    
    history_listbox.delete(0, tk.END)
    
    # Фильтрация истории
    filtered_history = history
    if current_filter != "все":
        filtered_history = [h for h in history if h["type"] == current_filter]
    
    if not filtered_history:
        history_listbox.insert(tk.END, "📭 Нет задач в истории")
        history_listbox.insert(tk.END, "👉 Сгенерируйте задачу, чтобы начать!")
        return
    
    # Эмодзи для типов
    type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
    
    # Отображение историй (новые сверху)
    for i, entry in enumerate(filtered_history[::-1], 1):
        emoji = type_emoji.get(entry["type"], "📌")
        display_text = f"{i:3d}. {entry['timestamp']}  {emoji} [{entry['type']}]  {entry['name']}"
        history_listbox.insert(tk.END, display_text)


def update_stats():
    """Обновление статистики"""
    global stats_label, history
    
    total = len(history)
    
    if total == 0:
        stats_label.config(text="📊 Статистика: нет выполненных задач")
        return
    
    # Подсчёт по типам
    type_counts = {"учёба": 0, "спорт": 0, "работа": 0}
    for entry in history:
        if entry["type"] in type_counts:
            type_counts[entry["type"]] += 1
    
    # Расчёт процентов
    study_percent = (type_counts["учёба"] / total * 100) if total > 0 else 0
    sport_percent = (type_counts["спорт"] / total * 100) if total > 0 else 0
    work_percent = (type_counts["работа"] / total * 100) if total > 0 else 0
    
    stats_text = (
        f"📊 Статистика | Всего: {total} задач | "
        f"📚 Учёба: {type_counts['учёба']} ({study_percent:.0f}%) | "
        f"🏃‍♂️ Спорт: {type_counts['спорт']} ({sport_percent:.0f}%) | "
        f"💼 Работа: {type_counts['работа']} ({work_percent:.0f}%)"
    )
    
    stats_label.config(text=stats_text)


def on_filter_change(event=None):
    """Обработка изменения фильтра"""
    global current_filter, filter_var
    current_filter = filter_var.get()
    refresh_history()


def clear_history():
    """Очистка истории"""
    global history, current_task_label
    
    if messagebox.askyesno("⚠️ Подтверждение", 
                          "Вы уверены, что хотите очистить всю историю?\n\n"
                          "Это действие нельзя отменить!",
                          icon='warning'):
        history = []
        save_data()
        refresh_history()
        update_stats()
        current_task_label.config(
            text="✨ История очищена. Сгенерируйте новую задачу! ✨",
            fg=COLORS["secondary"],
            font=("Arial", 14)
        )
        messagebox.showinfo("✅ Очистка", "История успешно очищена!")


def flash_button():
    """Эффект мигания кнопки"""
    global generate_btn, root_window
    
    original_bg = generate_btn.cget("bg")
    original_text = generate_btn.cget("text")
    
    generate_btn.config(bg=COLORS["warning"], text="🎲 ГЕНЕРАЦИЯ... 🎲")
    root_window.after(200, lambda: generate_btn.config(bg=original_bg, text=original_text))


# ==================== ФУНКЦИИ СОЗДАНИЯ ИНТЕРФЕЙСА ====================

def setup_ui(root):
    """Настройка пользовательского интерфейса"""
    global generate_btn, current_task_label, filter_var, filter_menu
    global task_name_entry, task_type_var, history_listbox, stats_label, root_window
    
    root_window = root
    root.title("Random Task Generator")
    root.geometry("750x650")
    root.resizable(True, True)
    
    # Основной контейнер
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Заголовок
    title_label = tk.Label(main_frame, text="🎲 RANDOM TASK GENERATOR 🎲", 
                           font=("Arial", 20, "bold"),
                           fg=COLORS["primary"])
    title_label.pack(pady=10)
    
    subtitle_label = tk.Label(main_frame, text="Генератор случайных задач для продуктивного дня",
                             font=("Arial", 10),
                             fg=COLORS["dark"])
    subtitle_label.pack(pady=(0, 15))
    
    # Фрейм для генерации
    generate_frame = tk.LabelFrame(main_frame, text="🎯 Генерация задачи", 
                                   font=("Arial", 12, "bold"),
                                   bg=COLORS["light"])
    generate_frame.pack(fill="x", pady=10)
    
    generate_btn = tk.Button(generate_frame, 
                            text="✨ Сгенерировать случайную задачу ✨", 
                            command=generate_task,
                            bg=COLORS["primary"], 
                            fg="white",
                            font=("Arial", 13, "bold"),
                            padx=30, 
                            pady=12,
                            cursor="hand2",
                            relief="raised",
                            bd=2)
    generate_btn.pack(pady=15)
    
    # Фрейм текущей задачи
    current_frame = tk.LabelFrame(main_frame, text="📌 Текущая задача", 
                                  font=("Arial", 12, "bold"),
                                  bg=COLORS["light"])
    current_frame.pack(fill="x", pady=10)
    
    current_task_label = tk.Label(current_frame, 
                                 text="🌟 Нажмите кнопку, чтобы получить задачу 🌟",
                                 font=("Arial", 14),
                                 fg=COLORS["secondary"],
                                 bg=COLORS["light"],
                                 wraplength=650,
                                 justify="center",
                                 pady=20)
    current_task_label.pack()
    
    # Фрейм фильтрации
    filter_frame = tk.LabelFrame(main_frame, text="🔍 Фильтрация истории", 
                                 font=("Arial", 12, "bold"),
                                 bg=COLORS["light"])
    filter_frame.pack(fill="x", pady=10)
    
    filter_inner = tk.Frame(filter_frame, bg=COLORS["light"])
    filter_inner.pack(pady=10)
    
    filter_label = tk.Label(filter_inner, text="Тип задачи:", 
                           font=("Arial", 11),
                           bg=COLORS["light"])
    filter_label.pack(side="left", padx=5)
    
    filter_var = tk.StringVar(value="все")
    filter_types = ["все", "учёба", "спорт", "работа"]
    filter_menu = ttk.Combobox(filter_inner, 
                              textvariable=filter_var,
                              values=filter_types,
                              width=15,
                              state="readonly",
                              font=("Arial", 11))
    filter_menu.pack(side="left", padx=5)
    filter_menu.bind("<<ComboboxSelected>>", on_filter_change)
    
    # Фрейм добавления задачи
    add_frame = tk.LabelFrame(main_frame, text="➕ Добавить новую задачу", 
                              font=("Arial", 12, "bold"),
                              bg=COLORS["light"])
    add_frame.pack(fill="x", pady=10)
    
    add_inner = tk.Frame(add_frame, bg=COLORS["light"])
    add_inner.pack(pady=10, padx=10)
    
    # Поле названия
    name_label = tk.Label(add_inner, text="Название:", 
                         font=("Arial", 11),
                         bg=COLORS["light"])
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    task_name_entry = tk.Entry(add_inner, width=40, 
                              font=("Arial", 11),
                              relief="solid",
                              bd=1)
    task_name_entry.grid(row=0, column=1, padx=5, pady=5)
    task_name_entry.bind('<Return>', lambda e: add_task())
    
    # Поле типа
    type_label = tk.Label(add_inner, text="Тип:", 
                         font=("Arial", 11),
                         bg=COLORS["light"])
    type_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    task_type_var = tk.StringVar(value="учёба")
    type_menu = ttk.Combobox(add_inner, 
                            textvariable=task_type_var,
                            values=["учёба", "спорт", "работа"],
                            width=12,
                            state="readonly",
                            font=("Arial", 11))
    type_menu.grid(row=0, column=3, padx=5, pady=5)
    
    add_button = tk.Button(add_inner, 
                          text="➕ Добавить задачу",
                          command=add_task,
                          bg=COLORS["secondary"],
                          fg="white",
                          font=("Arial", 11, "bold"),
                          padx=15,
                          pady=5,
                          cursor="hand2",
                          relief="raised")
    add_button.grid(row=0, column=4, padx=15, pady=5)
    
    # Фрейм истории
    history_frame = tk.LabelFrame(main_frame, text="📜 История задач", 
                                  font=("Arial", 12, "bold"),
                                  bg=COLORS["light"])
    history_frame.pack(fill="both", expand=True, pady=10)
    
    # Контейнер для списка
    list_container = tk.Frame(history_frame, bg=COLORS["light"])
    list_container.pack(fill="both", expand=True, padx=5, pady=5)
    
    scrollbar = tk.Scrollbar(list_container)
    scrollbar.pack(side="right", fill="y")
    
    history_listbox = tk.Listbox(list_container, 
                                yscrollcommand=scrollbar.set,
                                font=("Consolas", 10),
                                selectmode=tk.SINGLE,
                                height=12,
                                relief="solid",
                                bd=1,
                                bg="white",
                                fg=COLORS["dark"])
    history_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=history_listbox.yview)
    
    # Информационная панель
    info_frame = tk.Frame(main_frame, bg=COLORS["light"])
    info_frame.pack(fill="x", pady=5)
    
    stats_label = tk.Label(info_frame, text="", 
                          font=("Arial", 10),
                          bg=COLORS["light"],
                          fg=COLORS["dark"])
    stats_label.pack(side="left")
    
    clear_button = tk.Button(info_frame, 
                            text="🗑️ Очистить историю",
                            command=clear_history,
                            bg=COLORS["danger"],
                            fg="white",
                            font=("Arial", 10, "bold"),
                            padx=15,
                            pady=5,
                            cursor="hand2",
                            relief="raised")
    clear_button.pack(side="right")
    
    # Подсказка
    hint_label = tk.Label(main_frame, 
                         text="💡 Подсказка: нажмите Enter после ввода названия задачи | История автоматически сохраняется в JSON файл",
                         font=("Arial", 9),
                         fg="gray",
                         bg=COLORS["light"])
    hint_label.pack(pady=5)


def center_window(root):
    """Центрирование окна на экране"""
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    """Запуск приложения"""
    global root_window
    
    # Загрузка сохранённых данных
    load_data()
    
    # Создание окна
    root = tk.Tk()
    root_window = root
    
    # Настройка интерфейса
    setup_ui(root)
    
    # Обновление отображения
    refresh_history()
    update_stats()
    
    # Центрирование окна
    center_window(root)
    
    # Запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()
