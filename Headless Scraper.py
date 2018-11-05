
# coding: utf-8

# In[1]:


import requests, lxml.html
from bs4 import BeautifulSoup
import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime
import pickle


# In[2]:


# options = webdriver.ChromeOptions()
# options.add_argument('headless')

chromedriver = "/usr/lib/chromium-browser/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver) #chrome_options=options
driver.get('https://www.goodreads.com/user/sign_in')


# In[3]:


username =''
password =''

username_form= driver.find_element_by_id("user_email")
username_form.send_keys(username)

username_form= driver.find_element_by_id("user_password")
username_form.send_keys(password)
username_form.send_keys(Keys.RETURN)


# In[4]:


#['  Bitten by Witch Fever: Wallpaper & Arsenic in the Victorian Home', 
#'Hawksley, Lucinda', 
#'4.27', 
#'137', 
#'Oct 2016', 
#'really liked it', 
#'0', 
#'1', 
#'Aug 07, 2018', 
#'Aug 07, 2018', 
#'view']

def shelf_scraper(shelf_name, driver):
    books = driver.find_elements_by_class_name('bookalike')
    
    rating_dict = {'did not like it': 1,
          'it was ok': 2,
          'liked it': 3,
          'really liked it': 4,
          'it was amazing': 5,
          '1 of 5 stars': 0}
    
    for book in books:
        lbook = book.text.split('\n')
        title =  lbook[0].strip()
        author = lbook[1].replace('*','').strip()
        avg_rating = lbook[2]
        times_rated = lbook[3]
        rating_text = lbook[5]
        try:
            rating =  rating_dict[rating_text]
        except:
            rating_text
        comments = lbook[6]
        likes = lbook[7]
        date_added = lbook[-2]
        raw = book.get_attribute('innerHTML').strip()
        try:
            isbn_start = raw.find('isbn')
            isbn = raw[isbn_start+70:isbn_start+80]
            soup = BeautifulSoup(raw, 'lxml')
        except:
            isbn = ''
        review_url = soup.find('a', class_='nobreak').get('href') 
        a= (user, shelf_name, review_url, title, author, avg_rating, times_rated, rating, comments, likes, date_added, isbn)
        print(a)
        results.append(a)


# In[5]:


df = pd.read_csv('userids.csv', index_col=None, sep ='\t')
df.head()
userids =  list(df.userid.values)


# In[6]:


jar = []

for file in os.listdir():
    if file.split(' ')[-1]=='shelf.pkl':
        jar.append(int(file.split(' ')[0]))

print(len(userids))
for file in jar:
    userids.remove(file)
print(len(userids))


# In[ ]:


for user in userids:
    try:
        t0 = time.time()
        user= str(user)
        user_url = 'https://www.goodreads.com/review/list/'+user

        driver.get(user_url)

        possibles = driver.find_elements_by_class_name('actionLinkLite')

        #//*[@id="paginatedShelfList"]/div[8]/a[2]
        #//*[@id="shelves"]/div[1]/a[1]
        #//*[@id="shelves"]/div[2]/a[7]

        shelves = []

        for item in possibles:
            try:
                text = item.text.split(' ')[0]
                link = item.get_attribute('href')
                if text == 'Read' or text == 'Currently' or text == 'Want':
                    pass
                else:
                    if 'shelf' in link:
                        print  (link, text)
                        shelves.append((link, text))
            except:
                print(i, 'ERROR')

        results = []
        for shelf in shelves:
            shelf_url = shelf[0]
            shelf_name =  shelf[1]
            driver.get(shelf_url)

            settings = driver.find_element_by_id('shelfSettingsLink')
            settings.click()
            time.sleep(.1)
            list_button = driver.find_element_by_id('listFieldSetLink')
            list_button.click()
            position_button = driver.find_element_by_id('position_field')
            if position_button.is_selected():
                position_button.click()

            while True:
                t1 =time.time()
                time.sleep(.250)
                shelf_scraper(shelf_name, driver)
                print('')
                print (datetime.datetime.now())
                print('%d books %.3f seconds' % (len(results), time.time()-t1), shelf_name)
                print('')
                try:
                    nextpage = driver.find_element_by_class_name('next_page')
                except:
                    break
                if nextpage.get_attribute('href') == None:
                    break
                else:
                    try:
                        nextpage.click()
                    except:
                        break

        filename = user+' shelf.pkl'
        outfile = open(filename,'wb')
        pickle.dump(results,outfile)
        outfile.close()
        
        print ('%d TOTAL TIME: %.3f' % (len(results), time.time()-t0))
    except:
        pass

