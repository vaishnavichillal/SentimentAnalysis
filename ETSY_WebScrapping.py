
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3 as sql
from time import sleep
import requests

product_names=[]
list_of_reviews=[]
product_urls=[]

global browser
global search_url
search_url="https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers"

#function stores all the products from all pages 
def search_products(search_url):
    
  
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
        
        
        product_urls.append(product.get_attribute('href'))
        
    
    
    
    #next_page=soup.find("div",class_="wt-flex-xl-5 wt-flex-wrap").find("nav").find("ul").findAll("li")[-1].text
        
   
    #recurssively iterate over the next pages
    next_page=soup.find("div",class_="wt-show-lg appears-ready").find("nav").find("ul").findAll("li")[-1].text
    print(next_page.strip())
    
    
        
    if next_page.strip() == 'Next page':
        next_page_partial = soup.find("div",class_="wt-show-lg appears-ready").find("nav").find("ul").findAll("li")[-1].find('a')['href']
        #print(next_page_partial)
        next_page_url = next_page_partial
        print(next_page_url)
        
        search_products(next_page_url)
    else:
        None
        
    
    
        
        
   
        

#find reviews for each products
def find_reviews():
    
    for url in product_urls:
        try:
             browser=webdriver.Chrome(executable_path="chromedriver.exe")
        
             browser.get(url)
             product_html=browser.page_source
             bs=BeautifulSoup(product_html,'html')
                
    
                
             list_reviews=bs.find("div",{"class":"wt-grid wt-grid--block wt-mb-xs-0"})
             reviews_len=len(list_reviews.findAll("p",{"class":"wt-text-truncate--multi-line wt-break-word"}))
         
             product_names.append(bs.find("h1",class_="wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1").text.replace('/n','').strip())
             for i in range(1,reviews_len+1):
                 try:
           
                     list_of_reviews.append(bs.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                 except:
                     continue
            
       
       
        
             while(True):
                  try:
                      next_button = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
                      if next_button != None:
                          next_button.click()
                          sleep(5)
                          html = browser.page_source
                          bs = BeautifulSoup(html,'html')
                          list_reviews=bs.find("div",{"class":"wt-grid wt-grid--block wt-mb-xs-0"})
                          reviews_len=len(list_reviews.findAll("p",{"class":"wt-text-truncate--multi-line wt-break-word"}))
         
                
                          for i in range(1,reviews_len+1):
                              try:
                                  list_of_reviews.append(bs.select(f'#review-preview-toggle-{i}')[0].getText().strip())
                              except:
                                  continue
                            
                            
                  except Exception as e:
                      print('finsish : ', e)
                      break
            
        except:
            continue
    
        
   
                
    
     
  
    
    
   
    
   
    
    
    
#//*[@id="reviews"]/div[2]/nav/ul

   
       
    
    
            
        
        

def web_scrapping():
    

    search_products(search_url)
    find_reviews()


    print(len(list_of_reviews))
    scrappedReviews=pd.DataFrame(list_of_reviews,index=None,columns=['reviews'])
#scrappedReviews['reviews']=list_reviews

    scrappedReviews.to_csv('scrappedReviewsAll.csv')


    df = pd.read_csv('scrappedReviewsAll.csv')
    conn = sql.connect('scrappedReviewsAll.db')
    df.to_sql('scrappedReviewsAllTable', conn)  


    #reviews=None
    # product_names=None
    # list_of_reviews=None

if __name__=='__main__':
    web_scrapping()