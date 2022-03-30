
# importing the necessary packages
from aiohttp import connector
import requests
import uuid
import asyncio
import aiohttp
import time
import async_timeout
from bs4 import BeautifulSoup


def saveTextToFile(text, fileName):
    try:
        f = open(f"Premium_Times_Sport_Data/{fileName}.txt","w+")
        f.writelines(text)
        f.close() 
        print('save successfully to file')  
    except Exception as e:
        print(e) 
        
        
async def fetch_page(session, url):
    async with async_timeout.timeout(7200):
        start = time.time()
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        #async with session.get(url,headers=headers) as response:
        async with session.get(url) as response:
            print(f'{url} took {time.time() - start}')
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks
    

def process_article_contents(articleContents):
    
    for article_content in articleContents:
        
        soup_article = BeautifulSoup(article_content, 'html5lib')
        
        body = soup_article.find_all('div', class_='content-inner')        
        
        # if len(body) == 0:
        #     return "" #return and do nothing
        x = body[0].find_all('p')
        
        print(f'The number of paragraphs found : {len(x)}')
            
        count = 0    
        #unifying the Paragraphs
        list_paragraphs = []
        for p in range(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
                
                
        random_string = uuid.uuid4().hex[:10].upper().replace('0','X').replace('O','Y')
        
        file_name = f'sport__{random_string}'
        
        saveTextToFile(final_article, file_name) 
                             
        count = count + 1
        x.clear()
          
def scrapeDataFromLink(page_content):
    try:
        coverpage = page_content

        soup1 = BeautifulSoup(coverpage, 'html5lib')
        
        coverpage_news = soup1.find_all('article', class_='jeg_post jeg_pl_lg_2 format-standard')
        
        list_of_links = []

        coverage_news_length = len(coverpage_news)

        for i in range(0,coverage_news_length):
            #title = coverpage_news[i].find('h2').get_text()
            link = coverpage_news[i].find('a')['href']
            
            print(link)
            
            list_of_links.append(link)
            #articles_titles.append(title)
            
        
        
        loop_innerpage = asyncio.get_event_loop()
        article_contents = loop_innerpage.run_until_complete(get_multiple_pages(loop_innerpage, *list_of_links))
        
        print(f'The length of article contents {len(article_contents)}')
        
        process_article_contents(article_contents)
         
    except Exception as e:
        print(e)
        pass
    

if __name__ == '__main__':
    
    def main():
        loop = asyncio.get_event_loop()
        total_pages = 398
        list_all_urls = [f'https://www.premiumtimesng.com/category/sports/page/{page_num}/' for page_num in range(1, total_pages)]
        
        start = time.time()
        
        pages = loop.run_until_complete(get_multiple_pages(loop, *list_all_urls))
       
              
        for page_content in pages:           
           scrapeDataFromLink(page_content)
           print(f'Total took {time.time() - start}')

    main()
    
     






        
    
    
