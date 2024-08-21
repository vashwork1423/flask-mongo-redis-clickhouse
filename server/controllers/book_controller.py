from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.book_service import BookService
from extensions import cache
from clickhouse_driver import Client

book_bp = Blueprint('book', __name__)
book_service = BookService(cache)
client = Client(host='localhost', port=9000, user='default', password='')

@book_bp.route('', methods=['POST'])
def create_book():
    data = request.get_json()
    try:
        user = book_service.create_book(data)

        title = data.get('title')
        year = data.get('year')
        author = data.get('author')
        create_user = 'test'

        query = f'''
            INSERT INTO logs.book_logs (title, year, author, create_user)
            VALUES ('{title}', {year}, '{author}', '{create_user}')
        '''
        
        client.execute(query)

        return jsonify(user), 201
    except Exception as e:
        print(f'Error creating book: {e}')
        return jsonify({'message': 'Internal Server Error'}), 500

@book_bp.route('/<string:book_id>', methods=['GET'])
def get_book(book_id):
    if not ObjectId.is_valid(book_id):
        return jsonify({'message': 'Invalid book ID'}), 400

    try:
        book = book_service.get_book(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify(book), 200
    except Exception as e:
        print(f'Error retrieving book: {e}')
        return jsonify({'message': 'Internal Server Error'}), 500
