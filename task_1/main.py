import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def main():
    print("Парсинг GitHub Trending...")
    
    # URL для парсинга
    url = "https://github.com/trending"
    
    # Заголовки для запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Получаем страницу
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все репозитории
        repos = []
        articles = soup.find_all('article', class_='Box-row')
        
        print(f"Найдено репозиториев: {len(articles)}")
        
        for i, article in enumerate(articles[:10], 1):  # Берем первые 10
            # Извлекаем название
            title_elem = article.find('h2')
            if title_elem:
                repo_name = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
            else:
                continue
            
            # Извлекаем звезды
            stars_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
            stars = 0
            if stars_elem:
                stars_text = stars_elem.get_text(strip=True)
                stars = int(stars_text.replace(',', '')) if stars_text.replace(',', '').isdigit() else 0
            
            # Добавляем в список
            repos.append({
                'name': repo_name,
                'stars': stars
            })
            
            # Выводим на экран
            print(f"{i}. Repository: {repo_name}; Stars: {stars:,}")
        
        # Сохраняем в JSON
        data = {
            'timestamp': datetime.now().isoformat(),
            'repositories': repos
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nДанные сохранены в data.json")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()