'''
This script allows the user to determine the average salary of the top
125 paid players in baseball.

This script pulls the table data from the following link:
`https://questionnaire-148920.appspot.com/swe/data.html`


This script requires that `bs4`, `matplotlib`, `requests` and `numpy` are installed within the Python
environment you are running this script in.

This script also contains the following functions:

  * `salary_map` - maps a table row item to a player salary (int)
  * `get_soup_html` - gets table rows that contain player information
  * `show_bandw` - creates box and whisker plot
  * `show_hist` - creates histogram
'''

import argparse
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import re
import requests

LINK = 'https://questionnaire-148920.appspot.com/swe/data.html'

def add_arguments():
  '''Add command line argument for Palindrome string'''

  parser.add_argument("-b", "--box-and-whisker", action='store_true',
          help=("This option will create a box and whisker plot and save it in the `figures` dir."))
  parser.add_argument("-hist", "--histogram", action='store_true',
          help=("This option will create a histogram and save it in the `figures` dir."))

def get_soup_html(link):
    '''This function returns parsed HTML from player salary webpage

    Parameters
    ----------
    link: str
        link to webpage

    Returns
    -------
    rows: list<BeautifulSoup(), <tr> tag>
        class: player-name - str
            Last, First name
        class: player-salary - str, None
            $\d,\d
        class: player-year: str
            \d{4}
        class: player-level: str
            MLB
    '''
    try:
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'html.parser')

        rows = soup.find_all('tr')
    except:
        raise Exception(f'Could not retrieve salary data from {link}')
    return rows

def salary_map(player_obj):
    '''This function returns valid player salaries from player row

    If the player salary is invalid, the function returns `None`. If there is a `ValueError` while
    trying to type the salary as an int. This assumes salaries are logged in WHOLE dollar amounts.

    Parameters
    ----------
    player_obj: BeautifulSoup(), <tr> tag
        class: player-name - str
            Last, First name
        class: player-salary - str, None
            $\d,\d
        class: player-year: str
            \d{4}
        class: player-level: str
            MLB

    Returns
    -------
        salary | None
        salary: int
            player salary represented as an integer
    '''

    try:
        salary = ''.join(re.findall('\d', player_obj.find('td', {'class': 'player-salary'}).text))

        return int(salary)
    except ValueError:
        return None

    try:
        player_name = player_obj.find('td', {'class': 'player-name'}).text
        print(f'Could not parse player salary for player {player_name}')
    except:
        print('Could not parse player salary')
    return None

def show_bandw(sorted_salaries):
  '''Represents the top 125 salaries in a box and whisker diagram

  Parameters
  ----------
  sorted_salaries: list<int>
    Top 125 player salaries sorted (reverse)
  '''

  fig = plt.figure(figsize=(10,10))
  plt.title('Box and Whisker Salary')
  plt.xlabel('Salary (1e7 USD)', fontsize=15)
  plt.boxplot(sorted_salaries, vert=False)
  fig.savefig('./figures/box.png')

def show_hist(sorted_salaries, qaulifying_offer):
  '''Represents the top 125 salaries with a histogram

  Parameters
  ----------
  sorted_salaries: list<int>
    Top 125 player salaries sorted (reverse)

  qualifying_offer: float
    average of top 125 salaries
  '''
  percentile_90 = np.percentile(sorted_salaries, 90)
  percentile_75 = np.percentile(sorted_salaries, 75)
  percentile_25 = np.percentile(sorted_salaries, 25)

  qual_offer_label = '{:,.0f}'.format(np.mean(qualifying_offer))
  ninety_label = '{:,.0f}'.format(np.mean(percentile_90))
  seventy_label = '{:,.0f}'.format(np.mean(percentile_75))
  quarter_label = '{:,.0f}'.format(np.mean(percentile_25))

  fig = plt.figure(figsize=(15,15))
  plt.hist(sorted_salaries, bins=20, align=('mid'))
  plt.title('Distribution of Top 125 Salaries', fontsize=20)
  plt.xlabel('Salary (1e7 USD)', fontsize=15)
  plt.ylabel('Number of Players', fontsize=15)
  plt.axvline(qualifying_offer, color='k', linestyle='dashed', linewidth=2, label=f'Qualifying Offer= ${qual_offer_label}')
  plt.axvline(percentile_90, color='r', linestyle='dashed', linewidth=2, label=f'90th Percentile= ${ninety_label}')
  plt.axvline(percentile_75, color='m', linestyle='dashed', linewidth=2, label=f'75th Percentile= ${seventy_label}')
  plt.axvline(percentile_25, color='orange', linestyle='dashed', linewidth=2, label=f'25th Percentile= ${quarter_label}')
  plt.legend(fontsize=15)
  fig.savefig('./figures/hist.png')

if __name__ == '__main__':
  ''' Get all player salaries, sort (reversed), and return top 125 results'''

  parser = argparse.ArgumentParser()

  add_arguments()
  args = parser.parse_args()

  salaries = [salary for salary in map(salary_map, get_soup_html(LINK)) if salary]
  sorted_salaries = sorted(salaries, reverse=True)[:125]

  ''' Calculate qaulifying offer '''
  qualifying_offer = np.mean(sorted_salaries)

  qual_offer_str = '{:,.2f}'.format(np.mean(qualifying_offer))
  print(f'The qualifying offer is ${qual_offer_str}')

  if args.box_and_whisker:
    show_bandw(sorted_salaries)

  if args.histogram:
    show_hist(sorted_salaries, qualifying_offer)