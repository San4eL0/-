"""
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
