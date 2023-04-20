from flask import Flask, jsonify, request
import random
app = Flask(__name__)

# Define sample quotes data
QUOTES = [
    {'id': 1, 'text': 'Be the change you wish to see in the world', 'author': 'Mahatma Gandhi'},
    {'id': 2, 'text': 'I have not failed. I’ve just found 10,000 ways that won’t work.', 'author': 'Thomas Edison'}
]

USERS = [{"username":"user1", "password":"password1"}]

TOKENS_DB =  dict()

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    for user in USERS:
        if user["username"] == data["username"] and user["password"] == data["password"]:
            _token = generate_token()
            TOKENS_DB[_token] = "quotes"
            print("Token Appended:")
            print(TOKENS_DB)
            return jsonify({'message': 'Login successful!', 'token': _token}), 200
    return jsonify({'error': 'Invalid username or password!'}), 401


# Define endpoints
@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
    #Covers each endpoint before it checks the method
    _token = request.headers.get("Authorization")
    if not _token in TOKENS_DB.keys(): #authorized
        return 403
    if not "quotes" in TOKENS_DB[_token]: #authenticated
        return 401
    if request.method == 'GET':
        # Get all quotes
        return jsonify(QUOTES)
    elif request.method == 'POST':
        # Create a new quote
        new_quote = request.json
        new_quote['id'] = len(QUOTES) + 1
        QUOTES.append(new_quote)
        return jsonify({'message': 'Quote created successfully!', 'quote': new_quote})

@app.route('/quotes/<int:id>', methods=['PUT', 'DELETE'])
def quote(id):
    #Covers each endpoint before it checks the method
    _token = request.headers.get("Authorization")
    if not _token in TOKENS_DB.keys(): #authorized
        return 403
    if not "quotes" in TOKENS_DB[_token]: #authenticated
        return 401
    # Find the quote with the given ID
    quote = next((q for q in QUOTES if q['id'] == id), None)
    if not quote:
        return jsonify({'error': 'Quote not found!'}), 404

    if request.method == 'PUT':
        # Update the quote with the given ID
        updated_quote = request.json
        quote.update(updated_quote)
        return jsonify({'message': 'Quote updated successfully!', 'quote': quote})

    elif request.method == 'DELETE':
        # Delete the quote with the given ID
        QUOTES.remove(quote)
        return jsonify({'message': 'Quote deleted successfully!'})



def generate_token():
    generated_token = ""
    for i in range(10):
       generated_token = generated_token + str(random.randint(1,9))
    return generated_token

   
if __name__ == '__main__':
    app.run()