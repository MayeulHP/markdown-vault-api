import re
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


@app.route('/note/<path:note_path>', methods=['PATCH'])
def append_to_note(note_path):
    """Append content to a note."""
    file_path = os.path.join(VAULT_ROOT, note_path + ".md")
    if not os.path.exists(file_path):
        return jsonify({"error": "Note not found"}), 404

    content_to_append = request.json.get('content')
    if not content_to_append:
        return jsonify({"error": "Missing 'content' in request body"}), 400

    try:
        with open(file_path, 'a') as f:
            f.write(content_to_append)
        return jsonify({"message": "Content appended successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/note/<path:note_path>/search', methods=['GET'])
def search_in_note(note_path):
    """Search for a string within a note."""
    file_path = os.path.join(VAULT_ROOT, note_path + ".md")
    if not os.path.exists(file_path):
        return jsonify({"error": "Note not found"}), 404

    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing 'q' query parameter"}), 400

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        matches = [match.start() for match in re.finditer(re.escape(query), content)]
        return jsonify({"matches": matches})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/search', methods=['GET'])
def search_vault():
    """Search for a string across the entire vault."""

    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing 'q' query parameter"}), 400

    results = []
    try:
        for root, _, files in os.walk(VAULT_ROOT):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    if query in content:
                        results.append(os.path.relpath(file_path, VAULT_ROOT))
        return jsonify({"results": results})
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


@app.route('/note/<path:note_path>/lines/<int:start_line>-<int:end_line>', methods=['GET'])
def view_part_of_note(note_path, start_line, end_line):
    """View a specific part of a note."""

    file_path = os.path.join(VAULT_ROOT, note_path + ".md")
    if not os.path.exists(file_path):
        return jsonify({"error": "Note not found"}), 404

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return jsonify({"error": "Invalid line range"}), 400


        partial_content = "".join(lines[start_line-1:end_line])
        return jsonify({"content": partial_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
