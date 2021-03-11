
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3 as sql
from time import sleep
import requests

product_names=[]
reviews_list=[]
urls=[]

global browser
global search_url
search_url="https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers"
# grab_urls=requests.get(search_url)
# soup=BeautifulSoup(grab_urls.text,'html')

# pages=soup.find(class_="wt-action-group__item-container")
# all_pages=pages.findAll('a')
# print(len(all_pages))
# for link in soup.find("div",class_="wt-show-lg appears-ready").find("nav").find("ul").findAll("li")[-1].findAll('a'):
#     urls.append(link.get_attribute('href'))
#browser=webdriver.Chrome("D:/Forsk/VIDEOS/chromedriver.exe")


def search_products(search_url):
    
    urls=[]
    
  
    browser=webdriver.Chrome(executable_path="chromedriver.exe")
    browser.get(search_url)
    sleep(5)
    html=browser.page_source
    #print(html)

    soup = BeautifulSoup(html,'html')
    
    list_product=soup.find("ul",{"class":"responsive-listing-grid wt-grid wt-grid--block wt-justify-content-flex-start wt-list-unstyled pl-xs-0"})
    
    total_length=len(list_product.findAll("li"))
    for i in range(1,total_length+1):
        
        product = browser.find_element_by_xpath(f'//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div/ul/li[{i}]/div/a')
        
        
        urls.append(product.get_attribute('href'))
        
    for url in urls:
        try:
            
            find_reviews(url)
        except:
            continue
    
    
    #next_page=bs.find("div",class_="wt-flex-xl-5 wt-flex-wrap").find("nav").find("ul").findAll("li")[-1].text
        
   
    
    next_page=soup.find("div",class_="wt-show-lg appears-ready").find("nav").find("ul").findAll("li")[-1].text
    print(next_page.strip())
    
    
        
    if next_page.strip() == 'Next page':
        next_page_partial = soup.find("div",class_="wt-show-lg appears-ready").find("nav").find("ul").findAll("li")[-1].find('a')['href']
        #print(next_page_partial)
        next_page_url = next_page_partial
        print(next_page_url)
        
        yield browser.get
    else:
          return None
    
    
        
        
   
        
   
        


def find_reviews(product_url):
    
        
    
        
    browser=webdriver.Chrome(executable_path="chromedriver.exe")
        
    browser.get(product_url)
    product_html=browser.page_source
    bs=BeautifulSoup(product_html,'html')
                
    
                
    list_reviews=bs.find("div",{"class":"wt-grid wt-grid--block wt-mb-xs-0"})
    total_reviews=len(list_reviews.findAll("p",{"class":"wt-text-truncate--multi-line wt-break-word"}))
    print(total_reviews)
    product_names.append(bs.find("h1",class_="wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1").text.replace('/n','').strip())
    for i in range(total_reviews):
        try:
           
            reviews_list.append(bs.select(f'#review-preview-toggle-{i}')[0].getText().strip())
        except:
            continue
            
       
       
        
    while(True):
        try:
            next_button = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
            if next_button != None:
                next_button.click()
                sleep(5)
                html = browser.page_source
                soup = BeautifulSoup(html,'html')
                list_reviews=soup.find("div",{"class":"wt-grid wt-grid--block wt-mb-xs-0"})
                
                reviews_len=len(list_reviews.findAll("p",{"class":"wt-text-truncate--multi-line wt-break-word"}))
         
                #print(reviews_len)
                for i in range(reviews_len):
                    try:
                        #product_names.append(bs.find("h1",class_="wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1").text.replace('/n','').strip())
                        reviews_list.append(soup.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                    except:
                        continue
                            
                            
        except Exception as e:
            print('finsish : ', e)
            break
                
    #return reviews_list
     
  
    
    
   
    
   
    
    
    
#//*[@id="reviews"]/div[2]/nav/ul

   
       
    
    
            
        
        



search_products(search_url)

scrappedReviews=pd.DataFrame()

scrappedReviews['Product']=product_names
scrappedReviews['Reviews']=reviews_list

scrappedReviews.to_csv('scrappedReviewsAll.csv')


df = pd.read_csv('scrappedReviewsAll.csv')
conn = sql.connect('scrappedReviewsAll.db')
df.to_sql('scrappedReviewsAllTable', conn)  


reviews=None
product_names=None
reviews_list=None

# # for review in reviews[1,10]:
# #     print(review)