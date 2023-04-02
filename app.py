import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

import constants

# Função para extrair o título do produto
def get_title(soup):

    try:
        # Objeto de tag externo
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Objeto NavigatableString interno
        title_value = title.text

        # Título como uma string
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Função para extrair o preço do produto
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # Se houver algum preço promocional
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Função para extrair a classificação do produto
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Função para extrair o número de avaliações de usuários
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Função para extrair o status de disponibilidade do produto
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Não disponível"	

    return available


def insert_data(tabela, df):

    ##Insere um dataframe em uma tabela do banco de dados utilizando Pandas e SQLAlchemy.
    conexao = f"postgresql://{constants.user}:{constants.password}@localhost:{constants.port}/{constants.database}"
    engine = create_engine(conexao)
    df.to_sql(tabela, engine, if_exists='append', index=False)




def main():
    # Adicionar o seu User-Agent
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'pt-BR, pt;q=0.5'})


    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    # URL da página web
    for number in range(1,constants.number_pages+1):
        URL = f"https://www.amazon.com/s?k=livros+{constants.key_word}&page={number}"

        # Requisição HTTP
        webpage = requests.get(URL, headers=HEADERS)

        # Objeto Soup contendo todos os dados
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Buscar links como uma lista de objetos de tag
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        # Armazenar os links
        links_list = []

        # Loop para extrair links dos objetos de tag
        for link in links:
                links_list.append(link.get('href'))
        
        # Loop para extrair os detalhes de cada produto a partir de cada link
        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Chamadas de função para exibir todas as informações do produto necessárias
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))
    
    # Montando dataframe
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df = amazon_df.drop_duplicates(['title','reviews'])
    amazon_df['extracted_at'] = datetime.datetime.today()
    insert_data(constants.table, amazon_df)
    return 'sucess' 

if __name__ == '__main__':
    main()