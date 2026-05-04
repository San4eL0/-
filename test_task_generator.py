"""
Модульные тесты для Random Task Generator
Автор: Алексей Иванов
"""

import unittest
import json
import os
import tempfile
import random
from datetime import datetime
from task_generator import Task, TaskHistoryEntry, TaskGeneratorApp
import tkinter as tk


class TestTask(unittest.TestCase):
    """Тесты для класса Task"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.test_task = Task("Тестовая задача", "учёба")
    
    def test_task_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.test_task.name, "Тестовая задача")
        self.assertEqual(self.test_task.task_type, "учёба")
    
    def test_task_with_spaces(self):
        """Тест задачи с пробелами"""
        task = Task("  Задача с пробелами  ", "спорт")
        self.assertEqual(task.name, "Задача с пробелами")
    
    def test_task_to_dict(self):
        """Тест преобразования в словарь"""
        task_dict = self.test_task.to_dict()
        self.assertEqual(task_dict, {"name": "Тестовая задача", "type": "учёба"})
    
    def test_task_from_dict(self):
        """Тест создания из словаря"""
        data = {"name": "Восстановленная задача", "type": "работа"}
        task = Task.from_dict(data)
        self.assertEqual(task.name, "Восстановленная задача")
        self.assertEqual(task.task_type, "работа")
    
    def test_all_task_types(self):
        """Тест всех типов задач"""
        types = ["учёба", "спорт", "работа"]
        for task_type in types:
            task = Task(f"Задача {task_type}", task_type)
            self.assertEqual(task.task_type, task_type)


class TestTaskHistoryEntry(unittest.TestCase):
    """Тесты для класса TaskHistoryEntry"""
    
    def setUp(self):
        self.task = Task("Историческая задача", "учёба")
        
    def test_entry_creation_without_timestamp(self):
        """Тест создания записи без временной метки"""
        entry = TaskHistoryEntry(self.task)
        self.assertEqual(entry.task.name, "Историческая задача")
        self.assertIsNotNone(entry.timestamp)
    
    def test_entry_creation_with_timestamp(self):
        """Тест создания записи с временной меткой"""
        timestamp = "2024-01-15 10:30:00"
        entry = TaskHistoryEntry(self.task, timestamp)
        self.assertEqual(entry.timestamp, timestamp)
    
    def test_entry_to_dict(self):
        """Тест преобразования записи в словарь"""
        timestamp = "2024-01-15 10:30:00"
        entry = TaskHistoryEntry(self.task, timestamp)
        entry_dict = entry.to_dict()
        self.assertEqual(entry_dict["name"], "Историческая задача")
        self.assertEqual(entry_dict["type"], "учёба")
        self.assertEqual(entry_dict["timestamp"], timestamp)
    
    def test_entry_from_dict(self):
        """Тест восстановления записи из словаря"""
        data = {
            "name": "Восстановленная запись",
            "type": "работа",
            "timestamp": "2024-01-15 12:00:00"
        }
        entry = TaskHistoryEntry.from_dict(data)
        self.assertEqual(entry.task.name, "Восстановленная запись")
        self.assertEqual(entry.task.task_type, "работа")
        self.assertEqual(entry.timestamp, "2024-01-15 12:00:00")
    
    def test_timestamp_format(self):
        """Тест формата временной метки"""
        entry = TaskHistoryEntry(self.task)
        # Проверка формата ГГГГ-ММ-ДД ЧЧ:ММ:СС
        import re
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        self.assertTrue(re.match(pattern, entry.timestamp))


class TestFileOperations(unittest.TestCase):
    """Тесты файловых операций"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_json_save_and_load(self):
        """Тест сохранения и загрузки JSON"""
        test_data = {
            "history": [
                {"name": "Тест1", "type": "учёба", "timestamp": "2024-01-15 10:00:00"},
                {"name": "Тест2", "type": "спорт", "timestamp": "2024-01-15 11:00:00"}
            ],
            "custom_tasks": [
                {"name": "Пользовательская задача", "type": "работа"}
            ],
            "total_tasks_generated": 2
        }
        
        # Сохранение
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Загрузка
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(len(loaded_data["history"]), 2)
        self.assertEqual(len(loaded_data["custom_tasks"]), 1)
        self.assertEqual(loaded_data["custom_tasks"][0]["name"], "Пользовательская задача")
        self.assertEqual(loaded_data["total_tasks_generated"], 2)
    
    def test_empty_json_handling(self):
        """Тест обработки пустого JSON"""
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data, {})
    
    def test_invalid_json_handling(self):
        """Тест обработки некорректного JSON"""
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            f.write("{некорректный json")
        
        # Должен быть exception при попытке чтения
        with self.assertRaises(json.JSONDecodeError):
            with open(self.temp_file.name, 'r', encoding='utf-8') as f:
                json.load(f)
    
    def test_unicode_support(self):
        """Тест поддержки Unicode (русский язык)"""
        test_data = {
            "history": [
                {"name": "Русское название задачи", "type": "учёба", "timestamp": "2024-01-15 10:00:00"}
            ]
        }
        
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data["history"][0]["name"], "Русское название задачи")


class TestValidation(unittest.TestCase):
    """Тесты валидации"""
    
    def test_empty_string_validation(self):
        """Тест проверки пустой строки"""
        empty_string = ""
        self.assertEqual(len(empty_string.strip()), 0)
        
        string_with_spaces = "   "
        self.assertEqual(len(string_with_spaces.strip()), 0)
    
    def test_min_length_validation(self):
        """Тест минимальной длины (3 символа)"""
        short_string = "ab"
        self.assertLess(len(short_string), 3)
        
        valid_string = "abc"
        self.assertGreaterEqual(len(valid_string), 3)
        
        edge_string = "a" * 3
        self.assertEqual(len(edge_string), 3)
    
    def test_max_length_validation(self):
        """Тест максимальной длины (100 символов)"""
        long_string = "a" * 101
        self.assertGreater(len(long_string), 100)
        
        valid_string = "a" * 100
        self.assertLessEqual(len(valid_string), 100)
        
        edge_string = "a" * 100
        self.assertEqual(len(edge_string), 100)
    
    def test_duplicate_validation(self):
        """Тест проверки дубликатов"""
        tasks = ["Задача1", "Задача2", "Задача3", "Задача1", "Задача2"]
        
        # Поиск дубликатов
        seen = set()
        duplicates = set()
        for task in tasks:
            if task in seen:
                duplicates.add(task)
            seen.add(task)
        
        self.assertEqual(len(duplicates), 2)
        self.assertIn("Задача1", duplicates)
        self.assertIn("Задача2", duplicates)
    
    def test_case_insensitive_duplicate(self):
        """Тест проверки дубликатов без учёта регистра"""
        task1 = "Задача"
        task2 = "ЗАДАЧА"
        
        self.assertEqual(task1.lower(), task2.lower())


class TestRandomGeneration(unittest.TestCase):
    """Тесты случайной генерации"""
    
    def test_random_selection_from_list(self):
        """Тест случайного выбора из списка"""
        tasks = ["Задача 1", "Задача 2", "Задача 3", "Задача 4", "Задача 5"]
        
        # Проверка, что функция возвращает элемент из списка
        for _ in range(100):
            selected = random.choice(tasks)
            self.assertIn(selected, tasks)
    
    def test_random_distribution(self):
        """Тест распределения случайных значений"""
        tasks = ["A", "B", "C"]
        counts = {"A": 0, "B": 0, "C": 0}
        
        iterations = 1000
        for _ in range(iterations):
            selected = random.choice(tasks)
            counts[selected] += 1
        
        # Каждый элемент должен быть выбран примерно iterations/3 раз
        for count in counts.values():
            self.assertGreater(count, iterations // 4)  # Не менее 25%
            self.assertLess(count, iterations // 2)    # Не более 50%
    
    def test_filtered_random_selection(self):
        """Тест случайного выбора с фильтрацией"""
        tasks = [
            {"name": "Учёба 1", "type": "учёба"},
            {"name": "Спорт 1", "type": "спорт"},
            {"name": "Учёба 2", "type": "учёба"},
            {"name": "Спорт 2", "type": "спорт"},
            {"name": "Работа 1", "type": "работа"}
        ]
        
        # Фильтр по учёбе
        filtered = [t for t in tasks if t["type"] == "учёба"]
        self.assertEqual(len(filtered), 2)
        
        # Проверка, что выборка только из отфильтрованных
        for _ in range(50):
            selected = random.choice(filtered)
            self.assertEqual(selected["type"], "учёба")
        
        # Фильтр по спорту
        filtered = [t for t in tasks if t["type"] == "спорт"]
        self.assertEqual(len(filtered), 2)
        
        for _ in range(50):
            selected = random.choice(filtered)
            self.assertEqual(selected["type"], "спорт")
    
    def test_random_with_empty_list(self):
        """Тест случайного выбора из пустого списка"""
        empty_list = []
        
        # Должен вызывать исключение
        with self.assertRaises(IndexError):
            random.choice(empty_list)


class TestTaskGeneratorAppIntegration(unittest.TestCase):
    """Интеграционные тесты для приложения"""
    
    def setUp(self):
        """Создание тестового приложения"""
        self.root = tk.Tk()
        self.root.withdraw()  # Скрываем окно для тестов
        self.app = TaskGeneratorApp(self.root)
    
    def tearDown(self):
        """Уничтожение приложения"""
        self.root.destroy()
    
    def test_app_initialization(self):
        """Тест инициализации приложения"""
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.tasks)
        self.assertIsNotNone(self.app.history)
        self.assertEqual(len(self.app.default_tasks), 12)
    
    def test_get_available_tasks_no_filter(self):
        """Тест получения задач без фильтра"""
        available = self.app.get_available_tasks()
        self.assertEqual(len(available), len(self.app.tasks))
    
    def test_get_available_tasks_with_filter(self):
        """Тест получения задач с фильтром"""
        self.app.current_filter = "учёба"
        available = self.app.get_available_tasks()
        for task in available:
            self.assertEqual(task.task_type, "учёба")
    
    def test_add_valid_task(self):
        """Тест добавления валидной задачи"""
        initial_count = len(self.app.tasks)
        self.app.task_name_entry.insert(0, "Новая тестовая задача")
        self.app.task_type_var.set("спорт")
        self.app.add_task()
        self.assertEqual(len(self.app.tasks), initial_count + 1)
        
        # Проверка, что задача добавилась
        task_names = [task.name for task in self.app.tasks]
        self.assertIn("Новая тестовая задача", task_names)
    
    def test_add_duplicate_task(self):
        """Тест добавления дубликата"""
        initial_count = len(self.app.tasks)
        first_task_name = self.app.tasks[0].name
        self.app.task_name_entry.insert(0, first_task_name)
        self.app.task_type_var.set("учёба")
        self.app.add_task()
        # Количество задач не должно измениться
        self.assertEqual(len(self.app.tasks), initial_count)


def run_all_tests():
    """Запуск всех тестов с детальным выводом"""
    print("=" * 70)
    print("🧪 ЗАПУСК ТЕСТОВ Random Task Generator")
    print("=" * 70)
    print()
    
    # Создание загрузчика тестов
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавление всех тестов
    suite.addTests(loader.loadTestsFromTestCase(TestTask))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskHistoryEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestRandomGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskGeneratorAppIntegration))
    
    # Запуск тестов
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Вывод статистики
    print()
    print("=" * 70)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"✅ Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Ошибок: {len(result.failures)}")
    print(f"⚠️ Исключений: {len(result.errors)}")
    print(f"📈 Всего тестов: {result.testsRun}")
    print("=" * 70)
    
    return result


if __name__ == "__main__":
    run_all_tests()"""
Модульные тесты для Random Task Generator
"""

import unittest
import json
import os
import tempfile
from datetime import datetime
from task_generator import Task, TaskHistoryEntry, TaskGeneratorApp
import tkinter as tk


class TestTask(unittest.TestCase):
    """Тесты для класса Task"""
    
    def test_task_creation(self):
        """Тест создания задачи"""
        task = Task("Тестовая задача", "учёба")
        self.assertEqual(task.name, "Тестовая задача")
        self.assertEqual(task.task_type, "учёба")
    
    def test_task_to_dict(self):
        """Тест преобразования в словарь"""
        task = Task("Задача", "спорт")
        task_dict = task.to_dict()
        self.assertEqual(task_dict, {"name": "Задача", "type": "спорт"})
    
    def test_task_from_dict(self):
        """Тест создания из словаря"""
        data = {"name": "Восстановленная задача", "type": "работа"}
        task = Task.from_dict(data)
        self.assertEqual(task.name, "Восстановленная задача")
        self.assertEqual(task.task_type, "работа")
    
    def test_task_strip_whitespace(self):
        """Тест удаления пробелов"""
        task = Task("  Задача с пробелами  ", "учёба")
        self.assertEqual(task.name, "Задача с пробелами")


class TestTaskHistoryEntry(unittest.TestCase):
    """Тесты для класса TaskHistoryEntry"""
    
    def test_entry_creation(self):
        """Тест создания записи истории"""
        task = Task("Историческая задача", "учёба")
        entry = TaskHistoryEntry(task)
        self.assertEqual(entry.task.name, "Историческая задача")
        self.assertIsNotNone(entry.timestamp)
    
    def test_entry_to_dict(self):
        """Тест преобразования записи в словарь"""
        task = Task("Запись", "спорт")
        timestamp = "2024-01-15 10:30:00"
        entry = TaskHistoryEntry(task, timestamp)
        entry_dict = entry.to_dict()
        self.assertEqual(entry_dict["name"], "Запись")
        self.assertEqual(entry_dict["type"], "спорт")
        self.assertEqual(entry_dict["timestamp"], timestamp)
    
    def test_entry_from_dict(self):
        """Тест восстановления записи из словаря"""
        data = {
            "name": "Восстановленная запись",
            "type": "работа",
            "timestamp": "2024-01-15 12:00:00"
        }
        entry = TaskHistoryEntry.from_dict(data)
        self.assertEqual(entry.task.name, "Восстановленная запись")
        self.assertEqual(entry.timestamp, "2024-01-15 12:00:00")


class TestFileOperations(unittest.TestCase):
    """Тесты файловых операций"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_json_save_load(self):
        """Тест сохранения и загрузки JSON"""
        test_data = {
            "history": [
                {"name": "Тест1", "type": "учёба", "timestamp": "2024-01-15 10:00:00"},
                {"name": "Тест2", "type": "спорт", "timestamp": "2024-01-15 11:00:00"}
            ],
            "custom_tasks": [
                {"name": "Пользовательская задача", "type": "работа"}
            ]
        }
        
        # Сохранение
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Загрузка
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(len(loaded_data["history"]), 2)
        self.assertEqual(len(loaded_data["custom_tasks"]), 1)
        self.assertEqual(loaded_data["custom_tasks"][0]["name"], "Пользовательская задача")
    
    def test_empty_json_handling(self):
        """Тест обработки пустого JSON"""
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data, {})


class TestValidation(unittest.TestCase):
    """Тесты валидации"""
    
    def test_empty_string_validation(self):
        """Тест проверки пустой строки"""
        empty_string = ""
        self.assertEqual(len(empty_string.strip()), 0)
    
    def test_min_length_validation(self):
        """Тест минимальной длины"""
        short_string = "ab"
        self.assertLess(len(short_string), 3)
        
        valid_string = "abc"
        self.assertGreaterEqual(len(valid_string), 3)
    
    def test_max_length_validation(self):
        """Тест максимальной длины"""
        long_string = "a" * 101
        self.assertGreater(len(long_string), 100)
        
        valid_string = "a" * 100
        self.assertLessEqual(len(valid_string), 100)
    
    def test_duplicate_validation(self):
        """Тест проверки дубликатов"""
        tasks = ["Задача1", "Задача2", "Задача1"]
        duplicates = [task for task in tasks if tasks.count(task) > 1]
        self.assertEqual(len(set(duplicates)), 1)


class TestRandomGeneration(unittest.TestCase):
    """Тесты случайной генерации"""
    
    def test_random_selection(self):
        """Тест случайного выбора"""
        import random
        tasks = ["Задача 1", "Задача 2", "Задача 3"]
        
        # Проверка, что функция возвращает элемент из списка
        for _ in range(100):
            selected = random.choice(tasks)
            self.assertIn(selected, tasks)
    
    def test_filtered_random(self):
        """Тест случайного выбора с фильтром"""
        tasks = [
            {"name": "Учёба 1", "type": "учёба"},
            {"name": "Спорт 1", "type": "спорт"},
            {"name": "Учёба 2", "type": "учёба"}
        ]
        
        filtered = [t for t in tasks if t["type"] == "учёба"]
        self.assertEqual(len(filtered), 2)
        
        # Проверка, что выборка только из отфильтрованных
        for _ in range(50):
            selected = random.choice(filtered)
            self.assertEqual(selected["type"], "учёба")


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTask))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskHistoryEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestRandomGeneration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Запуск тестов Random Task Generator")
    print("=" * 60)
    run_tests()
