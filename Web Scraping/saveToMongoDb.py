from pymongo import MongoClient




# def is_database_exist():
#     dblist = myclient.list_database_names()
#     if "NG_NewsPaper_Corpus" in dblist:
#         return True
#     return False

# def is_collection_exist():
#     collist = mydb.list_collection_names()
#     if "customers" in collist:
#         print("The collection exists.")
    
    
def save_document_to_database(object):
    myclient  = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["NG_NewsPaper_Corpus"] 
    mycol = mydb["Articles"]
    
    print('starting save to database')    
    
    # article = { 
    #            "title": object['title'], # title of the news paper article
    #            "date_pub": object['published'], # Publish date of the news paper article
    #            "category" : object['category'], # category of the news paper article
    #            "content" : object['content'], # content of the news paper article
    #            "author" : object['author'], # author of the news paper article
    #            "source"  : object['source'], #news paper name
    #          }
    

    x = mycol.insert_one(object)
    
    
    
    print(f'inserted Id {x.inserted_id}')
    