from flask import Flask, jsonify, request

app = Flask(__name__)

# Define sample quotes data
QUOTES = [
    {'id': 1, 'text': 'Be the change you wish to see in the world', 'author': 'Mahatma Gandhi'},
    {'id': 2, 'text': 'I have not failed. I’ve just found 10,000 ways that won’t work.', 'author': 'Thomas Edison'}
]

# Define endpoints
@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
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


if __name__ == '__main__':
    app.run()
