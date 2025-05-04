import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from pathlib import Path



def get_online_stats(url: str) -> int:
    options = Options()
    options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        soup = bs(driver.page_source, "html.parser")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

    div_online_stats = soup.find('div', class_='apphub_Stats').find('span', class_='apphub_NumInApp')
    online_stats = int(div_online_stats.text.replace(',','').replace(' в игре', ''))
    print(online_stats)
    
    return online_stats


def write_online_stats_to_csv(online_stats):
    online_stats_data = {
        'time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'player_count' : online_stats
    }
    file = Path('online_stats.csv')
    df = pd.DataFrame([online_stats_data])
    df.to_csv('online_stats.csv', index=False, mode='a', header=not file.exists())

def main():
    a = get_online_stats("https://steamcommunity.com/app/730")
    write_online_stats_to_csv(a)

if __name__ == "__main__":
    main()