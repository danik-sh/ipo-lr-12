# generate_html.py - УПРОЩЕННАЯ РАБОЧАЯ ВЕРСИЯ
import json
import os
from datetime import datetime

print("=" * 50)
print("Генератор HTML страницы")
print("=" * 50)

# 1. Проверяем наличие data.json
if not os.path.exists('data.json'):
    print("❌ ОШИБКА: Файл data.json не найден!")
    print("Сначала запустите main.py для парсинга данных")
    input("Нажмите Enter для выхода...")
    exit(1)

# 2. Читаем данные
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ Файл data.json прочитан успешно")
except Exception as e:
    print(f"❌ Ошибка чтения JSON: {e}")
    input("Нажмите Enter для выхода...")
    exit(1)

# 3. Проверяем структуру данных
if 'repositories' not in data:
    print("❌ В data.json нет ключа 'repositories'")
    print(f"Ключи в data.json: {list(data.keys())}")
    input("Нажмите Enter для выхода...")
    exit(1)

repos = data['repositories']
print(f"📊 Найдено репозиториев: {len(repos)}")

# 4. Создаем простой HTML
html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GitHub Trending</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            text-align: center;
            border-bottom: 2px solid #764ba2;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th {
            background: #764ba2;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .stars {
            background: #ffd700;
            color: #333;
            padding: 4px 8px;
            border-radius: 10px;
            font-weight: bold;
            display: inline-block;
        }
        .source-link {
            display: block;
            text-align: center;
            margin: 20px auto;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            width: 250px;
        }
        .source-link:hover {
            background: #5a67d8;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            font-size: 14px;
        }
        .repo-name {
            font-weight: bold;
            color: #0366d6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⭐ GitHub Trending Repositories</h1>
        
        <table>
            <tr>
                <th>#</th>
                <th>Repository</th>
                <th>Stars</th>
            </tr>
'''

# 5. Добавляем данные в таблицу
for i, repo in enumerate(repos, 1):
    name = repo.get('name', 'Unknown')
    stars = repo.get('stars', 0)
    
    # Форматируем число с разделителями
    stars_formatted = f"{stars:,}".replace(',', ' ')
    
    html += f'''
            <tr>
                <td>{i}</td>
                <td class="repo-name">{name}</td>
                <td><span class="stars">⭐ {stars_formatted}</span></td>
            </tr>
'''

# 6. Завершаем HTML
html += f'''
        </table>
        
        <a href="https://github.com/trending" class="source-link" target="_blank">
            🔗 Перейти на GitHub Trending
        </a>
        
        <div class="footer">
            <p>📅 Данные собраны: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
            <p>📊 Всего репозиториев: {len(repos)}</p>
            <p>⚡ Сгенерировано программой GitHub Parser</p>
        </div>
    </div>
</body>
</html>
'''

# 7. Сохраняем HTML
try:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML страница успешно создана: index.html")
    
    # Показываем информацию о файле
    file_size = os.path.getsize('index.html')
    print(f"📁 Размер файла: {file_size} байт")
    
    # Показываем путь
    file_path = os.path.abspath('index.html')
    print(f"📍 Путь к файлу: {file_path}")
    
    # Предлагаем открыть
    print("\nЧтобы открыть страницу:")
    print("1. Найдите файл 'index.html'")
    print("2. Дважды кликните по нему")
    print("3. Или откройте в браузере")
    
except Exception as e:
    print(f"❌ Ошибка при сохранении HTML: {e}")

# 8. Ждем нажатия Enter перед выходом
input("\nНажмите Enter для выхода...")