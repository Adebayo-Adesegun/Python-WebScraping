
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
    
def process_article_contents(article_content):
    
    for article_content in article_content:
            soup_article = BeautifulSoup(article_content, 'html5lib')
            
            author = soup_article.find_all('div', class_='entry-author')[0].find_all('a')[0].get_text().strip()
            
            print(f'author : {author}')
            
            title = soup_article.find_all('h1', class_='entry-title')[0].get_text().strip()
            
            print(f'title : {title}')
            
            date_pub = soup_article.find_all('span', class_='entry-date')[0].find_all('span')[0].get_text()
            
            print(f'Date Published : {date_pub}')
            
            body = soup_article.find_all('div', class_='entry-content')
            
            x = body[0].find_all('p')
            
            #unifying the Paragraphs
            list_paragraphs = []
            for p in range(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
            
            content = final_article  
        
            print(content)
            
            object_to_save = {
                "title" : title,
                "content" : content,
                "category" : "sport",
                "source" : "punch",
                "author" : author,
                "date_pub": date_pub
             }
        
        
            save_document_to_database(object_to_save)
            
            x.clear()

            
        
def scrapeDataFromLink(page_content):
    try:
        
        coverpage = page_content

        soup = BeautifulSoup(coverpage, 'html5lib')
        coverpage_news = soup.find_all('div', class_='entry-item-thumbnail')

        list_of_links = []

        coverage_news_length = len(coverpage_news)

        for i in range(0,coverage_news_length):
            link = coverpage_news[i].find('a')['href']
            print(link)
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
        total_pages = 1060
        list_all_urls = [f'https://punchng.com/topics/sports/page/{page_num}/' for page_num in range(1, total_pages)]
        
        start = time.time()
        
        pages = loop.run_until_complete(get_multiple_pages(loop, *list_all_urls))
       
        print(f'Number of pages found : {len(pages)}') 
           
        for page_content in pages:           
           scrapeDataFromLink(page_content)
           print(f'Total took {time.time() - start}')

    main()
    
     






        
    
    
