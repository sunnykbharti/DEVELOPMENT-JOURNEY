from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

books = [
    {"id" : 1, "author" : "Bruno", "title" : "Burnt at Stake"},
    {"id" : 2, "author" : "Pluto", "title" : "The Planet"},
    {"id" : 3, "author" : "Brown", "title" : "Brown Munda"},
    {"id" : 4, "author" : "James", "title" : "The India"},
    {"id" : 5, "author" : "Rachi", "title" : "Jharkhandi"}
]

class Books(Resource) : 
    def get(self, book_id=None) :
        if book_id is None:
            return books, 200
        
        book = next((book for book in books if book["id"] == book_id), None)

        if book : 
            return book, 200
        return {"error" : "Book Not Found!"}, 404
    
    def post(self) : 
        new_book = request.json
        books.append(new_book)
        return new_book, 201
    
    def put(self, book_id):
        book = next((book for book in books if book["id"] == book_id), None)
        if not book : 
            return {"error" : "Book not Found!"}, 404
        
        data = request.json
        book.update(data)
        return book, 200
    
    def delete(self, book_id):
        global books
        books = [book for book in books if book["id"] != book_id]
        return {"message" : "Book Deleted!"}, 202

api.add_resource(Books, '/books', '/books/<int:book_id>')

if __name__ == "__main__" :
    app.run(debug=True)