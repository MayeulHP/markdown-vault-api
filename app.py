from flask import Flask, request, jsonify
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

### Swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Obsidian Vault API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end Swagger specific ###

# Define the root directory of your Obsidian vault
VAULT_ROOT = os.environ.get("VAULT_ROOT", "/path/to/your/vault")  # Replace with the actual path

@app.route('/note/<path:note_path>', methods=['GET'])
def view_note(note_path):
    """View a note."""
    file_path = os.path.join(VAULT_ROOT, note_path + ".md")
    if not os.path.exists(file_path):
        return jsonify({"error": "Note not found"}), 404
    with open(file_path, 'r') as f:
        content = f.read()
    return jsonify({"content": content})


@app.route('/note/<path:note_path>', methods=['PUT'])
def edit_note(note_path):
    """Edit a note."""
    file_path = os.path.join(VAULT_ROOT, note_path + ".md")
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Missing 'content' in request body"}), 400

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return jsonify({"message": "Note updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/folder/<path:folder_path>', methods=['GET'])
def view_folder(folder_path):
    """View contents of a folder."""

    dir_path = os.path.join(VAULT_ROOT, folder_path)
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return jsonify({"error": "Folder not found or invalid path"}), 404

    try:
        contents = os.listdir(dir_path)
        return jsonify({"contents": contents})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
