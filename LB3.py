from flask import Flask, jsonify, request

app = Flask(__name__)

# Дані для прикладу
items = {
    1: {"name": "Laptop", "price": 1000},
    2: {"name": "Smartphone", "price": 700},
    3: {"name": "Tablet", "price": 300}
}


# Кореневий маршрут
@app.route('/')
def home():
    return "Welcome to the REST API! Use /items to interact with the catalog."


# Ігнорування запиту favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204


# Маршрут для роботи з усіма товарами
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return jsonify(items)  # Повертає весь каталог у форматі JSON

    if request.method == 'POST':
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            return jsonify({"message": "Invalid data"}), 400
        item_id = max(items.keys()) + 1
        items[item_id] = {"name": data["name"], "price": data["price"]}
        return jsonify({"message": "Item added", "id": item_id}), 201


# Маршрут для роботи з конкретним товаром
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    if item_id not in items:
        return jsonify({"message": "Item not found"}), 404

    if request.method == 'GET':
        return jsonify(items[item_id])  # Повертає інформацію про товар

    if request.method == 'PUT':
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            return jsonify({"message": "Invalid data"}), 400
        items[item_id].update({"name": data["name"], "price": data["price"]})
        return jsonify({"message": "Item updated"})

    if request.method == 'DELETE':
        del items[item_id]
        return jsonify({"message": "Item deleted"})


# Запуск сервера
if __name__ == '__main__':
    app.run(port=8000, debug=True)