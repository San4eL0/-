import json
import random
import tkinter as tk
from tkinter import messagebox, ttk

# Предопределённые задачи
DEFAULT_TASKS = [
    {"text": "Прочитать статью по Python", "type": "учёба"},
    {"text": "Сделать утреннюю зарядку", "type": "спорт"},
    {"text": "Написать еженедельный отчёт", "type": "работа"},
    {"text": "Посмотреть вебинар по Git", "type": "учёба"},
    {"text": "Пробежка 5 км", "type": "спорт"},
    {"text": "Обновить документацию проекта", "type": "работа"},
    {"text": "Решить 3 задачи на LeetCode", "type": "учёба"},
    {"text": "Отжаться 50 раз", "type": "спорт"},
    {"text": "Ответить на рабочие письма", "type": "работа"}
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        # Загружаем данные
        self.tasks = self.load_tasks()
        self.history = self.load_history()
        
        # Создаём интерфейс
        self.create_widgets()
        
        # Обновляем отображение
        self.update_filtered_list()
    
    def load_tasks(self):
        """Загрузка задач из JSON"""
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет, сохраняем задачи по умолчанию
            self.save_tasks_to_file(DEFAULT_TASKS)
            return DEFAULT_TASKS.copy()
    
    def save_tasks_to_file(self, tasks):
        """Сохранение задач в JSON"""
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """Загрузка истории из JSON"""
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_history_to_file(self):
        """Сохранение истории в JSON"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        # ===== Верхняя панель - Генерация задачи =====
        top_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        top_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(top_frame, text="🎲 ГЕНЕРАТОР ЗАДАЧ", font=("Arial", 16, "bold"), 
                 bg="#f0f0f0").pack(pady=10)
        
        self.task_label = tk.Label(top_frame, text="Нажмите кнопку ниже", 
                                    font=("Arial", 12), wraplength=550, 
                                    bg="#f0f0f0", fg="#555")
        self.task_label.pack(pady=10)
        
        self.gen_button = tk.Button(top_frame, text="✨ Сгенерировать задачу ✨", 
                                     command=self.generate_task,
                                     font=("Arial", 12, "bold"),
                                     bg="#4CAF50", fg="white", 
                                     padx=20, pady=5)
        self.gen_button.pack(pady=10)
        
        # ===== Панель добавления задачи =====
        add_frame = tk.LabelFrame(self.root, text="➕ Добавить новую задачу", 
                                   font=("Arial", 10, "bold"))
        add_frame.pack(pady=10, padx=10, fill="x")
        
        # Текст задачи
        tk.Label(add_frame, text="Текст задачи:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.new_task_entry = tk.Entry(add_frame, width=45, font=("Arial", 10))
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Тип задачи
        tk.Label(add_frame, text="Тип задачи:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.type_var = tk.StringVar(value="учёба")
        type_combobox = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                      values=["учёба", "спорт", "работа"], 
                                      state="readonly", width=42)
        type_combobox.grid(row=1, column=1, padx=5, pady=10)
        
        # Кнопка добавления
        self.add_button = tk.Button(add_frame, text="➕ Добавить задачу", 
                                     command=self.add_task,
                                     bg="#2196F3", fg="white", 
                                     font=("Arial", 10, "bold"))
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # ===== Панель фильтрации =====
        filter_frame = tk.LabelFrame(self.root, text="🔍 Фильтр истории по типу", 
                                      font=("Arial", 10, "bold"))
        filter_frame.pack(pady=10, padx=10, fill="x")
        
        self.filter_var = tk.StringVar(value="все")
        
        filter_all = tk.Radiobutton(filter_frame, text="📋 Все", variable=self.filter_var, 
                                     value="все", command=self.on_filter_change,
                                     font=("Arial", 10))
        filter_study = tk.Radiobutton(filter_frame, text="📚 Учёба", variable=self.filter_var, 
                                       value="учёба", command=self.on_filter_change,
                                       font=("Arial", 10))
        filter_sport = tk.Radiobutton(filter_frame, text="🏃 Спорт", variable=self.filter_var, 
                                       value="спорт", command=self.on_filter_change,
                                       font=("Arial", 10))
        filter_work = tk.Radiobutton(filter_frame, text="💼 Работа", variable=self.filter_var, 
                                      value="работа", command=self.on_filter_change,
                                      font=("Arial", 10))
        
        filter_all.pack(side="left", padx=15, pady=10)
        filter_study.pack(side="left", padx=15, pady=10)
        filter_sport.pack(side="left", padx=15, pady=10)
        filter_work.pack(side="left", padx=15, pady=10)
        
        # ===== Список истории =====
        history_frame = tk.LabelFrame(self.root, text="📜 История сгенерированных задач", 
                                       font=("Arial", 10, "bold"))
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Создаём скроллируемый список
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(history_frame, height=12, 
                                           font=("Arial", 10),
                                           yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопка очистки истории
        clear_button = tk.Button(history_frame, text="🗑 Очистить историю", 
                                  command=self.clear_history,
                                  bg="#f44336", fg="white",
                                  font=("Arial", 9, "bold"))
        clear_button.pack(pady=5)
    
    def add_task(self):
        """Валидация и добавление новой задачи"""
        task_text = self.new_task_entry.get().strip()
        
        # Проверка на пустую строку
        if not task_text:
            messagebox.showwarning("Ошибка ввода", "❌ Текст задачи не может быть пустым!")
            return
        
        # Проверка на дубликат
        for task in self.tasks:
            if task["text"].lower() == task_text.lower():
                messagebox.showwarning("Ошибка ввода", f"⚠️ Задача '{task_text}' уже существует!")
                return
        
        # Добавляем задачу
        new_task = {"text": task_text, "type": self.type_var.get()}
        self.tasks.append(new_task)
        self.save_tasks_to_file(self.tasks)
        
        # Очищаем поле ввода
        self.new_task_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"✅ Задача '{task_text}' успешно добавлена!")
    
    def generate_task(self):
        """Генерация случайной задачи"""
        if not self.tasks:
            messagebox.showwarning("Нет задач", "⚠️ Список задач пуст! Добавьте хотя бы одну задачу.")
            return
        
        # Выбираем случайную задачу
        selected_task = random.choice(self.tasks)
        
        # Добавляем в историю
        self.history.append(selected_task)
        self.save_history_to_file()
        
        # Отображаем задачу
        self.task_label.config(text=f"🎯 {selected_task['text']}\n\n📌 Тип: {selected_task['type']}", 
                                fg="#2E7D32", font=("Arial", 11, "bold"))
        
        # Обновляем список истории
        self.update_filtered_list()
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history_to_file()
            self.update_filtered_list()
            messagebox.showinfo("Успех", "История очищена!")
    
    def on_filter_change(self):
        """Обработчик изменения фильтра"""
        self.update_filtered_list()
    
    def update_filtered_list(self):
        """Обновление списка с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        
        selected_filter = self.filter_var.get()
        
        if not self.history:
            self.history_listbox.insert(tk.END, "📭 История пуста")
            return
        
        for index, task in enumerate(self.history, 1):
            if selected_filter == "все" or task["type"] == selected_filter:
                # Определяем эмодзи для типа
                if task["type"] == "учёба":
                    emoji = "📚"
                elif task["type"] == "спорт":
                    emoji = "🏃"
                elif task["type"] == "работа":
                    emoji = "💼"
                else:
                    emoji = "📌"
                
                display_text = f"{index}. {emoji} {task['text']}  —  [{task['type']}]"
                self.history_listbox.insert(tk.END, display_text)

def main():
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
