from pymongo import MongoClient
from config import Config
from bson import ObjectId
from flask_caching import Cache

class BookService:
    def __init__(self, cache):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client['book']
        self.collection = self.db['book']
        self.cache = cache

    def create_book(self, data):
        result = self.collection.insert_one(data)
        book = self.collection.find_one({"_id": result.inserted_id})
        book['_id'] = str(book['_id']) 
        return book

    def get_book(self, book_id):
        if not ObjectId.is_valid(book_id):
            return None

        cached_book = self.cache.get(book_id)
        if cached_book:
            return cached_book

        try:
            book = self.collection.find_one({"_id": ObjectId(book_id)})
            if book:
                book['_id'] = str(book['_id'])
                self.cache.set(book_id, book)
            return book
        except Exception as e:
            print(f"Error retrieving book: {e}")
            return None
