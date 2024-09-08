import wikipediaapi
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

from pandas import DataFrame

POPULATION_COL_NAME = 'Population (1 July 2022)'  # will change
wiki_wiki = wikipediaapi.Wikipedia('test-wikipedia')
# https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
page = wiki_wiki.page('List_of_countries_by_population_(United_Nations)')


def remove_square_brackets(text):
    """
    :param text: XXXX[a]
    :return: XXXX
    """
    text_without_square_brackets = re.sub(r'\[.*?\]', '', text).strip()
    return re.sub(r'\(.*?\)', '', text_without_square_brackets).strip()


def extract_tables_from_wikipedia(page) -> DataFrame:
    url = page.fullurl
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    data_frames = []
    for table in tables:
        df = pd.read_html(str(table))[0]
        data_frames.append(df)
    population_by_country = data_frames[0]
    population_by_country['Country'] = population_by_country['Country'].apply(remove_square_brackets)
    return population_by_country


def choose_one_country(df: DataFrame):
    pd.set_option('display.float_format', '{:.10f}'.format)
    df = df.iloc[1:].reset_index(drop=True)  # remove the line "World"
    population = df[POPULATION_COL_NAME]
    countries = df['Country']
    weights = population / population.sum()
    country = np.random.choice(countries, p=weights)
    print(country)


populations_by_country_df = extract_tables_from_wikipedia(page)
choose_one_country(populations_by_country_df)
