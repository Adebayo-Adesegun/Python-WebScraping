import asyncio
import aiohttp
import time
import async_timeout
from bs4 import BeautifulSoup
from saveToMongoDb import save_document_to_database
        
        
async def fetch_page(session, url):
    async with async_timeout.timeout(7200):
        start = time.time()
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
        
        title = soup_article.find_all('h1', class_='entry-title')[0].get_text()
        
        author = soup_article.find_all('div', class_='rtp-author-box rtp-no-avatar')[0]
        
        author = author.find_all('h2')[0].get_text()
        
        body = soup_article.find_all('div', class_='entry-content')
        
        date_pub = soup_article.find_all('span', class_='posted-on meta-tag')[0].find_all('a')[0].get_text()
        
        print(f'Date Published : {date_pub}')
        print('--------------------------------------------------------')
        
        x = body[0].find_all('p')
            
        # count = 0    
        #unifying the Paragraphs
        list_paragraphs = []
        for p in range(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
                
        content = final_article
        
        object_to_save = {
            "title" : title,
            "content" : content,
            "category" : "sport",
            "source" : "vanguard",
            "author" : author,
            "date_pub": date_pub
        }
        

        
        save_document_to_database(object_to_save)
        
        x.clear()
          
def scrapeDataFromLink(page_content):
    try:
        coverpage = page_content

        soup1 = BeautifulSoup(coverpage, 'html5lib')
        coverpage_news = soup1.find_all('article', class_='type-post')

        list_of_links = []
        
        coverage_news_length = len(coverpage_news)

        for i in range(0,coverage_news_length):
            link = coverpage_news[i].find('a')['href']
            list_of_links.append(link)
                   
        
        loop_innerpage = asyncio.get_event_loop()
        article_contents = loop_innerpage.run_until_complete(get_multiple_pages(loop_innerpage, *list_of_links))
        process_article_contents(article_contents)
         
    except Exception as e:
        print(e)
        pass
    

if __name__ == '__main__':
    
    def main():
        loop = asyncio.get_event_loop()
        total_pages = 4748
        list_all_urls = [f'https://www.vanguardngr.com/category/sports/page/{page_num}/' for page_num in range(3, total_pages)]
        
        start = time.time()
        
        pages = loop.run_until_complete(get_multiple_pages(loop, *list_all_urls))
       
              
        for page_content in pages:           
           scrapeDataFromLink(page_content)
           print(f'Total took {time.time() - start}')

    main()
    
     