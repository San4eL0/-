"""
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
    main()"""
Random Task Generator - GUI приложение для генерации случайных задач
Автор: Александр Шило
Версия: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Класс для представления задачи"""
    
    def __init__(self, name: str, task_type: str):
        self.name = name.strip()
        self.task_type = task_type
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "type": self.task_type}
    
    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        return Task(data['name'], data['type'])


class TaskHistoryEntry:
    """Класс для записи в истории"""
    
    def __init__(self, task: Task, timestamp: Optional[str] = None):
        self.task = task
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            "name": self.task.name,
            "type": self.task.task_type,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'TaskHistoryEntry':
        task = Task(data['name'], data['type'])
        return TaskHistoryEntry(task, data['timestamp'])


class TaskGeneratorApp:
    """Главное приложение"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        # Цветовая схема
        self.colors = {
            "primary": "#4CAF50",
            "secondary": "#2196F3",
            "danger": "#f44336",
            "warning": "#FF9800",
            "dark": "#333333",
            "light": "#f5f5f5"
        }
        
        # Предопределённые задачи
        self.default_tasks = [
            Task("Прочитать статью по Python", "учёба"),
            Task("Сделать зарядку 15 минут", "спорт"),
            Task("Закончить отчёт по работе", "работа"),
            Task("Выучить 10 новых английских слов", "учёба"),
            Task("Пробежка 2 км", "спорт"),
            Task("Провести встречу с клиентом", "работа"),
            Task("Посмотреть лекцию по машинному обучению", "учёба"),
            Task("Йога и медитация 20 минут", "спорт"),
            Task("Сделать код-ревью коллегам", "работа"),
            Task("Решить 3 задачи на LeetCode", "учёба"),
            Task("Отжимания 50 раз", "спорт"),
            Task("Составить план на неделю", "работа")
        ]
        
        self.tasks: List[Task] = self.default_tasks.copy()
        self.history: List[TaskHistoryEntry] = []
        self.current_filter: str = "все"
        self.data_file: str = "task_history.json"
        
        # Загрузка сохранённых данных
        self.load_data()
        
        # Настройка интерфейса
        self.setup_ui()
        self.update_stats()
        self.refresh_history()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Основной контейнер с отступами
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="🎲 RANDOM TASK GENERATOR 🎲", 
                               font=("Arial", 20, "bold"),
                               fg=self.colors["primary"])
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(main_frame, text="Генератор случайных задач для продуктивного дня",
                                 font=("Arial", 10),
                                 fg=self.colors["dark"])
        subtitle_label.pack(pady=(0, 15))
        
        # Фрейм для генерации
        generate_frame = tk.LabelFrame(main_frame, text="🎯 Генерация задачи", 
                                       font=("Arial", 12, "bold"),
                                       bg=self.colors["light"])
        generate_frame.pack(fill="x", pady=10)
        
        self.generate_btn = tk.Button(generate_frame, 
                                      text="✨ Сгенерировать случайную задачу ✨", 
                                      command=self.generate_task,
                                      bg=self.colors["primary"], 
                                      fg="white",
                                      font=("Arial", 13, "bold"),
                                      padx=30, 
                                      pady=12,
                                      cursor="hand2",
                                      relief="raised",
                                      bd=2)
        self.generate_btn.pack(pady=15)
        
        # Фрейм текущей задачи
        current_frame = tk.LabelFrame(main_frame, text="📌 Текущая задача", 
                                      font=("Arial", 12, "bold"),
                                      bg=self.colors["light"])
        current_frame.pack(fill="x", pady=10)
        
        self.current_task_label = tk.Label(current_frame, 
                                          text="🌟 Нажмите кнопку, чтобы получить задачу 🌟",
                                          font=("Arial", 14),
                                          fg=self.colors["secondary"],
                                          bg=self.colors["light"],
                                          wraplength=650,
                                          justify="center",
                                          pady=20)
        self.current_task_label.pack()
        
        # Фрейм фильтрации
        filter_frame = tk.LabelFrame(main_frame, text="🔍 Фильтрация истории", 
                                     font=("Arial", 12, "bold"),
                                     bg=self.colors["light"])
        filter_frame.pack(fill="x", pady=10)
        
        filter_inner = tk.Frame(filter_frame, bg=self.colors["light"])
        filter_inner.pack(pady=10)
        
        filter_label = tk.Label(filter_inner, text="Тип задачи:", 
                               font=("Arial", 11),
                               bg=self.colors["light"])
        filter_label.pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="все")
        filter_types = ["все", "учёба", "спорт", "работа"]
        self.filter_menu = ttk.Combobox(filter_inner, 
                                       textvariable=self.filter_var,
                                       values=filter_types,
                                       width=15,
                                       state="readonly",
                                       font=("Arial", 11))
        self.filter_menu.pack(side="left", padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Фрейм добавления задачи
        add_frame = tk.LabelFrame(main_frame, text="➕ Добавить новую задачу", 
                                  font=("Arial", 12, "bold"),
                                  bg=self.colors["light"])
        add_frame.pack(fill="x", pady=10)
        
        add_inner = tk.Frame(add_frame, bg=self.colors["light"])
        add_inner.pack(pady=10, padx=10)
        
        # Поле названия
        name_label = tk.Label(add_inner, text="Название:", 
                             font=("Arial", 11),
                             bg=self.colors["light"])
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.task_name_entry = tk.Entry(add_inner, width=40, 
                                       font=("Arial", 11),
                                       relief="solid",
                                       bd=1)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.task_name_entry.bind('<Return>', lambda e: self.add_task())
        
        # Поле типа
        type_label = tk.Label(add_inner, text="Тип:", 
                             font=("Arial", 11),
                             bg=self.colors["light"])
        type_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        self.task_type_var = tk.StringVar(value="учёба")
        type_menu = ttk.Combobox(add_inner, 
                                textvariable=self.task_type_var,
                                values=["учёба", "спорт", "работа"],
                                width=12,
                                state="readonly",
                                font=("Arial", 11))
        type_menu.grid(row=0, column=3, padx=5, pady=5)
        
        add_button = tk.Button(add_inner, 
                              text="➕ Добавить задачу",
                              command=self.add_task,
                              bg=self.colors["secondary"],
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
                                      bg=self.colors["light"])
        history_frame.pack(fill="both", expand=True, pady=10)
        
        # Контейнер для списка и скроллбара
        list_container = tk.Frame(history_frame, bg=self.colors["light"])
        list_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(list_container, 
                                         yscrollcommand=scrollbar.set,
                                         font=("Consolas", 10),
                                         selectmode=tk.SINGLE,
                                         height=12,
                                         relief="solid",
                                         bd=1,
                                         bg="white",
                                         fg=self.colors["dark"])
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Информационная панель
        info_frame = tk.Frame(main_frame, bg=self.colors["light"])
        info_frame.pack(fill="x", pady=5)
        
        self.stats_label = tk.Label(info_frame, text="", 
                                   font=("Arial", 10),
                                   bg=self.colors["light"],
                                   fg=self.colors["dark"])
        self.stats_label.pack(side="left")
        
        clear_button = tk.Button(info_frame, 
                                text="🗑️ Очистить историю",
                                command=self.clear_history,
                                bg=self.colors["danger"],
                                fg="white",
                                font=("Arial", 10, "bold"),
                                padx=15,
                                pady=5,
                                cursor="hand2",
                                relief="raised")
        clear_button.pack(side="right")
        
        # Подсказка
        hint_label = tk.Label(main_frame, 
                             text="💡 Подсказка: нажмите Enter после ввода названия задачи | "
                                  "История автоматически сохраняется в JSON файл",
                             font=("Arial", 9),
                             fg="gray",
                             bg=self.colors["light"])
        hint_label.pack(pady=5)
    
    def generate_task(self):
        """Генерация случайной задачи"""
        available_tasks = self.get_available_tasks()
        
        if not available_tasks:
            messagebox.showwarning("⚠️ Нет задач", 
                                  "Нет доступных задач для выбранного фильтра!\n\n"
                                  "Пожалуйста:\n"
                                  "• Добавьте новую задачу\n"
                                  "• Или измените фильтр",
                                  parent=self.root)
            return
        
        selected_task = random.choice(available_tasks)
        
        # Эмодзи для типов задач
        type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
        emoji = type_emoji.get(selected_task.task_type, "✨")
        
        # Отображение текущей задачи с анимацией
        self.current_task_label.config(
            text=f"{emoji}  {selected_task.name}  {emoji}",
            fg=self.colors["primary"],
            font=("Arial", 15, "bold")
        )
        
        # Добавление в историю
        entry = TaskHistoryEntry(selected_task)
        self.history.append(entry)
        self.save_data()
        self.refresh_history()
        self.update_stats()
        
        # Визуальный эффект
        self.flash_button()
    
    def get_available_tasks(self) -> List[Task]:
        """Получение задач с учётом фильтра"""
        if self.current_filter == "все":
            return self.tasks
        return [task for task in self.tasks if task.task_type == self.current_filter]
    
    def add_task(self):
        """Добавление новой задачи с валидацией"""
        task_name = self.task_name_entry.get().strip()
        task_type = self.task_type_var.get()
        
        # Валидация: пустая строка
        if not task_name:
            messagebox.showwarning("❌ Ошибка валидации", 
                                  "Название задачи не может быть пустым!\n\n"
                                  "Пожалуйста, введите название задачи.",
                                  parent=self.root)
            return
        
        # Валидация: минимальная длина
        if len(task_name) < 3:
            messagebox.showwarning("❌ Ошибка валидации", 
                                  f"Название задачи слишком короткое!\n\n"
                                  f"Минимальная длина: 3 символа\n"
                                  f"Ваша длина: {len(task_name)} символа(ов)",
                                  parent=self.root)
            return
        
        # Валидация: максимальная длина
        if len(task_name) > 100:
            messagebox.showwarning("❌ Ошибка валидации", 
                                  f"Название задачи слишком длинное!\n\n"
                                  f"Максимальная длина: 100 символов\n"
                                  f"Ваша длина: {len(task_name)} символов",
                                  parent=self.root)
            return
        
        # Проверка на дубликат
        for task in self.tasks:
            if task.name.lower() == task_name.lower():
                messagebox.showwarning("❌ Ошибка валидации", 
                                      f"Задача '{task_name}' уже существует!\n\n"
                                      f"Пожалуйста, введите уникальное название.",
                                      parent=self.root)
                return
        
        # Добавление задачи
        new_task = Task(task_name, task_type)
        self.tasks.append(new_task)
        
        # Очистка поля ввода
        self.task_name_entry.delete(0, tk.END)
        
        # Успешное добавление
        type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
        emoji = type_emoji.get(task_type, "✅")
        
        messagebox.showinfo("✅ Успех", 
                           f"{emoji} Задача успешно добавлена!\n\n"
                           f"Название: {task_name}\n"
                           f"Тип: {task_type}",
                           parent=self.root)
        
        # Обновление отображения
        self.refresh_history()
    
    def on_filter_change(self, event=None):
        """Обработка изменения фильтра"""
        self.current_filter = self.filter_var.get()
        self.refresh_history()
    
    def refresh_history(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        
        # Фильтрация истории
        filtered_history = self.history
        if self.current_filter != "все":
            filtered_history = [h for h in self.history 
                              if h.task.task_type == self.current_filter]
        
        if not filtered_history:
            self.history_listbox.insert(tk.END, "📭 Нет задач в истории")
            self.history_listbox.insert(tk.END, "👉 Сгенерируйте задачу, чтобы начать!")
            return
        
        # Эмодзи для типов
        type_emoji = {"учёба": "📚", "спорт": "🏃‍♂️", "работа": "💼"}
        
        # Отображение историй
        for i, entry in enumerate(filtered_history[::-1], 1):  # Обратный порядок (новые сверху)
            emoji = type_emoji.get(entry.task.task_type, "📌")
            display_text = f"{i:3d}. {entry.timestamp}  {emoji} [{entry.task.task_type}]  {entry.task.name}"
            self.history_listbox.insert(tk.END, display_text)
    
    def update_stats(self):
        """Обновление статистики"""
        total = len(self.history)
        
        if total == 0:
            self.stats_label.config(text="📊 Статистика: нет выполненных задач")
            return
        
        # Подсчёт по типам
        type_counts = {"учёба": 0, "спорт": 0, "работа": 0}
        for entry in self.history:
            if entry.task.task_type in type_counts:
                type_counts[entry.task.task_type] += 1
        
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
        
        self.stats_label.config(text=stats_text)
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            data = {
                "history": [entry.to_dict() for entry in self.history],
                "custom_tasks": [task.to_dict() for task in self.tasks 
                               if task not in self.default_tasks],
                "last_saved": datetime.now().isoformat(),
                "total_tasks_generated": len(self.history)
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{str(e)}", parent=self.root)
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загрузка истории
            self.history = [TaskHistoryEntry.from_dict(entry) 
                          for entry in data.get("history", [])]
            
            # Загрузка пользовательских задач
            custom_tasks = [Task.from_dict(task) 
                          for task in data.get("custom_tasks", [])]
            self.tasks = self.default_tasks.copy() + custom_tasks
            
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            self.history = []
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.history = []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("⚠️ Подтверждение", 
                              "Вы уверены, что хотите очистить всю историю?\n\n"
                              "Это действие нельзя отменить!",
                              parent=self.root,
                              icon='warning'):
            self.history = []
            self.save_data()
            self.refresh_history()
            self.update_stats()
            self.current_task_label.config(
                text="✨ История очищена. Сгенерируйте новую задачу! ✨",
                fg=self.colors["secondary"],
                font=("Arial", 14)
            )
            messagebox.showinfo("✅ Очистка", "История успешно очищена!", parent=self.root)
    
    def flash_button(self):
        """Эффект мигания кнопки"""
        original_bg = self.generate_btn.cget("bg")
        original_text = self.generate_btn.cget("text")
        
        self.generate_btn.config(bg=self.colors["warning"], text="🎲 ГЕНЕРАЦИЯ... 🎲")
        self.root.after(200, lambda: self.generate_btn.config(bg=original_bg, text=original_text))


def main():
    """Запуск приложения"""
    root = tk.Tk()
    
    # Установка иконки (опционально, если есть файл)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = TaskGeneratorApp(root)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()"""
Random Task Generator - GUI приложение для генерации случайных задач
Автор: Александр Шило
Версия: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Класс для представления задачи"""
    
    def __init__(self, name: str, task_type: str):
        self.name = name.strip()
        self.task_type = task_type
    
    def to_dict(self) -> Dict:
        return {"name": self.name, "type": self.task_type}
    
    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        return Task(data['name'], data['type'])


class TaskHistoryEntry:
    """Класс для записи в истории"""
    
    def __init__(self, task: Task, timestamp: Optional[str] = None):
        self.task = task
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            "name": self.task.name,
            "type": self.task.task_type,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'TaskHistoryEntry':
        task = Task(data['name'], data['type'])
        return TaskHistoryEntry(task, data['timestamp'])


class TaskGeneratorApp:
    """Главное приложение"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Предопределённые задачи
        self.default_tasks = [
            Task("Прочитать статью по Python", "учёба"),
            Task("Сделать зарядку 15 минут", "спорт"),
            Task("Закончить отчёт по работе", "работа"),
            Task("Выучить 10 новых английских слов", "учёба"),
            Task("Пробежка 2 км", "спорт"),
            Task("Провести встречу с клиентом", "работа"),
            Task("Посмотреть лекцию по машинному обучению", "учёба"),
            Task("Йога и медитация 20 минут", "спорт"),
            Task("Сделать код-ревью коллегам", "работа"),
            Task("Решить 3 задачи на LeetCode", "учёба"),
            Task("Отжимания 50 раз", "спорт"),
            Task("Составить план на неделю", "работа")
        ]
        
        self.tasks: List[Task] = self.default_tasks.copy()
        self.history: List[TaskHistoryEntry] = []
        self.current_filter: str = "все"
        self.data_file: str = "task_history.json"
        
        # Загрузка сохранённых данных
        self.load_data()
        
        # Настройка интерфейса
        self.setup_ui()
        self.update_stats()
        self.refresh_history()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Стили
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        style.configure("Task.TLabel", font=("Arial", 14))
        
        # Заголовок
        title_label = ttk.Label(self.root, text="🎲 Random Task Generator", 
                                style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Фрейм для генерации
        generate_frame = ttk.LabelFrame(self.root, text="Генерация задачи", 
                                       padding=10)
        generate_frame.pack(fill="x", padx=20, pady=10)
        
        self.generate_btn = tk.Button(generate_frame, 
                                      text="🎲 Сгенерировать случайную задачу", 
                                      command=self.generate_task,
                                      bg="#4CAF50", fg="white",
                                      font=("Arial", 12, "bold"),
                                      padx=20, pady=10,
                                      cursor="hand2")
        self.generate_btn.pack()
        
        # Текущая задача
        current_frame = ttk.LabelFrame(self.root, text="Текущая задача", 
                                      padding=10)
        current_frame.pack(fill="x", padx=20, pady=10)
        
        self.current_task_label = tk.Label(current_frame, 
                                          text="✨ Нажмите кнопку, чтобы получить задачу ✨",
                                          font=("Arial", 13),
                                          fg="#2196F3",
                                          wraplength=600,
                                          justify="center")
        self.current_task_label.pack(pady=15)
        
        # Фильтрация
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация истории", 
                                     padding=10)
        filter_frame.pack(fill="x", padx=20, pady=5)
        
        filter_label = ttk.Label(filter_frame, text="Тип задачи:")
        filter_label.pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="все")
        filter_types = ["все", "учёба", "спорт", "работа"]
        self.filter_menu = ttk.Combobox(filter_frame, 
                                       textvariable=self.filter_var,
                                       values=filter_types,
                                       width=15,
                                       state="readonly")
        self.filter_menu.pack(side="left", padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Добавление задачи
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", 
                                  padding=10)
        add_frame.pack(fill="x", padx=20, pady=5)
        
        # Поля ввода
        input_inner_frame = tk.Frame(add_frame)
        input_inner_frame.pack(fill="x")
        
        ttk.Label(input_inner_frame, text="Название:").pack(side="left", padx=5)
        self.task_name_entry = ttk.Entry(input_inner_frame, width=35)
        self.task_name_entry.pack(side="left", padx=5)
        self.task_name_entry.bind('<Return>', lambda e: self.add_task())
        
        ttk.Label(input_inner_frame, text="Тип:").pack(side="left", padx=5)
        self.task_type_var = tk.StringVar(value="учёба")
        type_menu = ttk.Combobox(input_inner_frame, 
                                textvariable=self.task_type_var,
                                values=["учёба", "спорт", "работа"],
                                width=10,
                                state="readonly")
        type_menu.pack(side="left", padx=5)
        
        add_button = tk.Button(input_inner_frame, 
                              text="➕ Добавить задачу",
                              command=self.add_task,
                              bg="#2196F3", fg="white",
                              cursor="hand2")
        add_button.pack(side="left", padx=10)
        
        # История
        history_frame = ttk.LabelFrame(self.root, text="История задач", 
                                      padding=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Скроллбар и список
        list_frame = tk.Frame(history_frame)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(list_frame, 
                                         yscrollcommand=scrollbar.set,
                                         font=("Consolas", 10),
                                         selectmode=tk.SINGLE,
                                         height=12)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Информационная панель
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=20, pady=5)
        
        self.stats_label = ttk.Label(info_frame, text="", font=("Arial", 9))
        self.stats_label.pack(side="left")
        
        clear_button = tk.Button(info_frame, 
                                text="🗑️ Очистить историю",
                                command=self.clear_history,
                                bg="#f44336", fg="white",
                                cursor="hand2")
        clear_button.pack(side="right")
        
        # Подсказка
        hint_label = ttk.Label(self.root, 
                              text="💡 Подсказка: нажмите Enter после ввода названия задачи",
                              font=("Arial", 8),
                              foreground="gray")
        hint_label.pack(pady=5)
    
    def generate_task(self):
        """Генерация случайной задачи"""
        available_tasks = self.get_available_tasks()
        
        if not available_tasks:
            messagebox.showwarning("Нет задач", 
                                  "Нет доступных задач для выбранного фильтра!\n"
                                  "Добавьте новую задачу или измените фильтр.")
            return
        
        selected_task = random.choice(available_tasks)
        
        # Отображение текущей задачи
        type_emoji = {"учёба": "📚", "спорт": "🏃", "работа": "💼"}
        emoji = type_emoji.get(selected_task.task_type, "✨")
        
        self.current_task_label.config(
            text=f"{emoji} {selected_task.name} {emoji}",
            fg="#4CAF50"
        )
        
        # Добавление в историю
        entry = TaskHistoryEntry(selected_task)
        self.history.append(entry)
        self.save_data()
        self.refresh_history()
        self.update_stats()
        
        # Анимация мигания
        self.flash_button()
    
    def get_available_tasks(self) -> List[Task]:
        """Получение задач с учётом фильтра"""
        if self.current_filter == "все":
            return self.tasks
        return [task for task in self.tasks if task.task_type == self.current_filter]
    
    def add_task(self):
        """Добавление новой задачи с валидацией"""
        task_name = self.task_name_entry.get().strip()
        task_type = self.task_type_var.get()
        
        # Валидация: пустая строка
        if not task_name:
            messagebox.showwarning("Ошибка валидации", 
                                  "❌ Название задачи не может быть пустым!")
            return
        
        # Валидация: минимальная длина
        if len(task_name) < 3:
            messagebox.showwarning("Ошибка валидации", 
                                  "❌ Название задачи должно содержать минимум 3 символа!")
            return
        
        # Валидация: максимальная длина
        if len(task_name) > 100:
            messagebox.showwarning("Ошибка валидации", 
                                  "❌ Название задачи не может превышать 100 символов!")
            return
        
        # Проверка на дубликат
        for task in self.tasks:
            if task.name.lower() == task_name.lower():
                messagebox.showwarning("Ошибка валидации", 
                                      f"❌ Задача '{task_name}' уже существует!")
                return
        
        # Добавление задачи
        new_task = Task(task_name, task_type)
        self.tasks.append(new_task)
        
        # Очистка поля ввода
        self.task_name_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", 
                           f"✅ Задача '{task_name}' успешно добавлена!\n"
                           f"Тип: {task_type}")
        
        # Обновление отображения
        self.refresh_history()
    
    def on_filter_change(self, event=None):
        """Обработка изменения фильтра"""
        self.current_filter = self.filter_var.get()
        self.refresh_history()
    
    def refresh_history(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        
        # Фильтрация истории
        filtered_history = self.history
        if self.current_filter != "все":
            filtered_history = [h for h in self.history 
                              if h.task.task_type == self.current_filter]
        
        if not filtered_history:
            self.history_listbox.insert(tk.END, "📭 Нет задач в истории")
            return
        
        # Отображение историй
        type_emoji = {"учёба": "📚", "спорт": "🏃", "работа": "💼"}
        
        for i, entry in enumerate(filtered_history, 1):
            emoji = type_emoji.get(entry.task.task_type, "📌")
            display_text = (f"{i:3d}. {entry.timestamp}  "
                          f"{emoji} [{entry.task.task_type}]  "
                          f"{entry.task.name}")
            self.history_listbox.insert(tk.END, display_text)
    
    def update_stats(self):
        """Обновление статистики"""
        total = len(self.history)
        
        if total == 0:
            self.stats_label.config(text="📊 Статистика: нет выполненных задач")
            return
        
        # Подсчёт по типам
        type_counts = {"учёба": 0, "спорт": 0, "работа": 0}
        for entry in self.history:
            if entry.task.task_type in type_counts:
                type_counts[entry.task.task_type] += 1
        
        stats_text = (f"📊 Статистика | Всего: {total} | "
                     f"📚 Учёба: {type_counts['учёба']} | "
                     f"🏃 Спорт: {type_counts['спорт']} | "
                     f"💼 Работа: {type_counts['работа']}")
        
        # Проценты
        if total > 0:
            stats_text += f" | 📈 Выполнено: {total}"
        
        self.stats_label.config(text=stats_text)
    
    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            data = {
                "history": [entry.to_dict() for entry in self.history],
                "custom_tasks": [task.to_dict() for task in self.tasks 
                               if task not in self.default_tasks],
                "last_saved": datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загрузка истории
            self.history = [TaskHistoryEntry.from_dict(entry) 
                          for entry in data.get("history", [])]
            
            # Загрузка пользовательских задач
            custom_tasks = [Task.from_dict(task) 
                          for task in data.get("custom_tasks", [])]
            self.tasks = self.default_tasks.copy() + custom_tasks
            
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.history = []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", 
                              "⚠️ Вы уверены, что хотите очистить всю историю?\n"
                              "Это действие нельзя отменить!"):
            self.history = []
            self.save_data()
            self.refresh_history()
            self.update_stats()
            self.current_task_label.config(
                text="✨ История очищена. Сгенерируйте новую задачу! ✨",
                fg="#2196F3"
            )
            messagebox.showinfo("Очистка", "✅ История успешно очищена!")
    
    def flash_button(self):
        """Эффект мигания кнопки"""
        original_bg = self.generate_btn.cget("bg")
        self.generate_btn.config(bg="#FF9800")
        self.root.after(200, lambda: self.generate_btn.config(bg=original_bg))


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
