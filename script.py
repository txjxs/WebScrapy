from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'B_NuCI'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("div", attrs={'class':'_30jeq3 _16Jk6d'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
       rating = soup.find("span", attrs={'class':'_2_R_DZ'}).find('span').text.replace('\xa0&\xa06','')
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating


def get_data(URL):
    # add your user agent 
        HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

        # The webpage URL
        # URL = 'https://www.flipkart.com/search?q=airpods%20pro%202'

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class' : '_2rpwqI'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
                links_list.append(link.get('href'))

        d = {"title":[], "price":[], "rating":[]}
        
        # Loop for extracting product details from each link 
        for link in links_list:
            new_webpage = requests.get('https://flipkart.com' + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))

        
        flipkart_df = pd.DataFrame.from_dict(d)
        flipkart_df['title'].replace('', np.nan, inplace=True)
        flipkart_df = flipkart_df.dropna(subset=['title'])
        return flipkart_df

if __name__ == "__main__":
    get_data()
