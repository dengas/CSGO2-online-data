import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from pathlib import Path
import csv


def get_online_stats(url: str) -> tuple[str, int]:
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        soup = bs(driver.page_source, "html.parser")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

    game_name = str(soup.find('div', class_='apphub_AppDetails').find('div', class_='apphub_AppName ellipsis').text)
    div_online_stats = soup.find('div', class_='apphub_Stats').find('span', class_='apphub_NumInApp')
    online_stats = int(div_online_stats.text.replace(',','').replace(' в игре', ''))
    print(f"Name: {game_name}, Online: {online_stats}")
    
    return game_name, online_stats


def write_online_stats_to_csv(game_name, online_stats):
    online_stats_data = {
        "name" : f"{game_name}",
        "player_count" : online_stats,
        "time" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    file = Path('online_stats.csv')
    df = pd.DataFrame([online_stats_data])
    df.to_csv('online_stats.csv', index=False, mode='a', header=not file.exists(), quoting=csv.QUOTE_NONNUMERIC)


def find_game_by_appid(name: str):
    df = pd.read_csv("datasets/games_march2025_cleaned.csv")
    match = df[df['name'] == name]
    if not match.empty:
        url = f"https://steamcommunity.com/app/{match.iloc[0]['appid']}"
    
    game_name, online_stats = get_online_stats(url)
    write_online_stats_to_csv(game_name, online_stats)


def main():
    find_game_by_appid("Counter-Strike 2")


if __name__ == "__main__":
    main()