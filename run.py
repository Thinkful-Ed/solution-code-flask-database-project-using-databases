# run.py
from flask import request, jsonify
from app import create_app, db
from models import AIModel

app = create_app()

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Hello, Flask with SQLAlchemy!"


@app.route('/models', methods=['POST'])
def add_multiple_models():
    # Get the models data from the request body
    models_data = request.get_json()

    # Validate the models data
    if not models_data or not isinstance(models_data, list):
        return jsonify({"message": "Invalid data provided"}), 400

    # Create and add the models to the database
    model_ids = []
    for model_data in models_data:
        if "name" in model_data and "description" in model_data:
            new_model = AIModel(
                name=model_data["name"], description=model_data["description"])
            db.session.add(new_model)
            db.session.commit()
            model_ids.append(new_model.id)
        else:
            return jsonify({"message": "Invalid model data provided"}), 400

    return jsonify({"message": f"Multiple AI models added to the database!", "model_ids": model_ids}), 201


@app.route('/models', methods=['GET'])
def view_models():
    # Query the database for all AI models
    models = AIModel.query.all()

    # Create a list of dictionaries containing the model's data
    models_data = [{"id": model.id, "name": model.name,
                    "description": model.description} for model in models]

    return jsonify(models_data)


@app.route('/models/<int:model_id>', methods=['PUT'])
def update_model(model_id):

    # Get the updated data from the request body
    updated_data = request.get_json()

    # Validate the updated data
    if not updated_data or not isinstance(updated_data, dict) or 'description' not in updated_data:
        return jsonify({"message": "Invalid data provided"}), 400

    # Query the database for the specific AI model
    model = AIModel.query.get_or_404(model_id)

    # Update the model's description
    model.description = updated_data['description']

    # Commit the changes
    db.session.commit()

    return jsonify({"message": f"AI model with ID {model_id} updated!"})


@app.route('/models/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    # Query the database for the specific AI model; return a 404 if not found
    model = AIModel.query.get_or_404(model_id)

    # Delete the model from the database
    db.session.delete(model)

    # Commit the changes
    db.session.commit()

    # Return a JSON response with a message and a 200 OK status code
    return jsonify({"message": f"AI model with ID {model_id} deleted!"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
