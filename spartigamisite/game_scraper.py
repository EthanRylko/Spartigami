import django, os
import spartigamisite.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartigamisite.settings')
django.setup()

from spartigamiapp.models import Game

# for individual seasons/games
# https://www.sports-reference.com/cfb/schools/michigan-state/{year}-schedule.html

# for which years have data
# https://www.sports-reference.com/cfb/schools/michigan-state/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

options = Options()
#options.add_argument('--headless=new')
options.add_argument('--disable-web-security')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
#options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

driver.get('https://www.sports-reference.com/cfb/schools/michigan-state/')

MONTH_MAP = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
             'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
             'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}


def reformat_day(input):
    day = input[:len(input) - 1]
    if len(day) == 1: day = '0' + day
    return day

def get_rank(input):
    if input[0] == '(':
        close_idx = input.find(')')
        rank = input[1:close_idx]
        rank = int(rank)
        return rank, input[close_idx + 2:]
    return 0, input

def get_years():
    year_list = list()

    try:
        table = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'michigan-state')))
        table = table.find_element(By.TAG_NAME, 'tbody')
    except TimeoutException:
        return None
    
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells):
            cell = cells[0]
            year_list.append(cell.text)
    return year_list


def get_game_data_from(year):
    link = f'https://www.sports-reference.com/cfb/schools/michigan-state/{year}-schedule.html'
    driver.get(link)
    data = list()

    try:
        table = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'schedule')))
        head = table.find_element(By.TAG_NAME, 'thead')
        table = table.find_element(By.TAG_NAME, 'tbody')
    except TimeoutException:
        return None

    time = False
    if head.find_elements(By.TAG_NAME, 'th')[2].text == 'Time':
        time = True

    for row in table.find_elements(By.TAG_NAME, 'tr'):
        game = list()
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells):
            date = cells[0].text.split(' ')

            # manip into datetime format
            month = MONTH_MAP[date[0]]
            day = reformat_day(date[1])
            yr = date[2]
            date = f'{yr}-{month}-{day}'

            if time:
                day, home, opp = cells[2].text, cells[4].text, cells[5].text
                conf, win = cells[6].text, cells[7].text
                msu_pt, opp_pt = cells[8].text, cells[9].text

                msu_rk, msu = get_rank(cells[3].text)
                opp_rk, opp = get_rank(opp)
            else:
                day, home, opp = cells[1].text, cells[3].text, cells[4].text
                conf, win = cells[5].text, cells[6].text
                msu_pt, opp_pt = cells[7].text, cells[8].text

                msu_rk, msu = get_rank(cells[2].text)
                opp_rk, opp = get_rank(opp)

            season = year

            if home == '': home = 'H'

            game = [date, day, home, msu_rk, opp_rk, opp, conf, win, msu_pt, opp_pt, season]
            data.append(game)
        

    return data


def upload_data(data):
    games_in_db = Game.objects.all()
    games_in_db_strs = [str(g) for g in games_in_db]

    for row in game_data:
        if row[0] in games_in_db_strs:
            print(f'Game of {row[0]} already in database')
            continue

        entry = dict()
        entry['date'] = row[0]
        entry['day'] = row[1]
        entry['home'] = row[2]
        entry['msu_rank'] = row[3]
        entry['opp_rank'] = row[4]
        entry['opponent'] = row[5]
        entry['conference'] = row[6]
        entry['win'] = row[7]
        entry['msu_score'] = row[8]
        entry['opp_score'] = row[9]
        entry['season'] = row[10]

        instance = Game.objects.create(**entry)
        instance.save()
    
    print('sucessfully uploaded data')


year_list = get_years()
print(year_list)

game_data = list()
for year in year_list:
    year_data = get_game_data_from(year)
    for data in year_data:
        game_data.append(data)
        print(data)

upload_data(game_data)
driver.quit()