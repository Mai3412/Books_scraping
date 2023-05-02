import requests
from bs4 import BeautifulSoup
import csv

BASE_URL= "https://books.toscrape.com/"

def recup_data(url):
    """transforme les données homepage en html"""
    response = requests.get(url)
    return BeautifulSoup(response.content,"html.parser")


def get_category_url():
    """récupère les urls de toutes les catégories"""
    soup = recup_data(BASE_URL)
    div=soup.find("div","side_categories")
    result=[]
    for link in div.find_all("a"):
        result.append(BASE_URL+link.get("href"))
    return result[1:]

def get_book_url(url):
    """récupère les urls des livres"""
    soup = recup_data(url)
    result = []
    for h3 in soup.find_all("h3"):
        a=h3.select("a").txt
        result.append(('https://books.toscrape.com/catalogue/'+a.select("href"))
# ici code qui effectue la requete et récupére les urls des livres    
    go_next_page = True
    page_number = 1
    while go_next_page:
        if page_number == 1:
            url = result
        else:
            url = result.replace("index.html", f"page-{page_number}.html")
 # test if a button next page exists       
        next_page_button = soup.find('li', class_="next")
        if next_page_button is None:
            go_next_page = False
        page_number += 1
    return result

def get_book_data(url):
    """récupère les données d'un livre"""
    soup = recup_data(url)
    BeautifulSoup(soup.content, "html.parser")
    product_page_url = soup
    universal_product_code = soup.find_all('tr')[0].get_text()
    title = soup.find('h1').get_text()
    price_including_tax = soup.find_all('tr')[3].get_text()
    price_excluding_tax = soup.find_all('tr')[2].get_text()
    number_available = soup.find_all('tr')[5].get_text()
    product_description_head = soup.find_all('h2')[0].get_text()
    product_description = soup.find_all('p')[3].get_text()
    category = soup.find_all('a')[3].get_text()
    review_rating = soup.find_all('tr')[6].get_text()
    image_url = soup.find_all('img')[0]['src']

def save_data_to_csv(en_tete_file,book_data):
    """écriture fichier csv livre """
    en_tete_file = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    book_data = ['url_livre', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    with open('données_livre.csv','w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=en_tete_file)
        writer.writeheader()
    for data in book_data:
        writer.writerow(book_data)

""""
def save_image ():
    with open(os.path.join(path,f'{title}.jpg'),'ab') as file:
	    image = requests.get(image_url).content
	    file.write(image)


"""
def main():
    categories=get_category_url()
    for category in categories:
        books=get_book_url(category)
        
        for book in books:
            infos=get_book_data(books["url"])
            book["infos"]=infos
        save_data_to_csv()
        save_image()

if __name__ == '__main__':
    main()

