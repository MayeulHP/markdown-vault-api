# Markdown Vault API

This API allows you to interact with your Obsidian vault (or any directory of markdown files) through a RESTful interface.  It provides endpoints for viewing, editing, appending to, and searching notes, as well as viewing folder contents.

## Setup

1. **Install Dependencies:**

```bash
pip install Flask flask-swagger-ui
```

2. **Set Vault Path:**
    - Set the `VAULT_ROOT` environment variable to the absolute path of your Obsidian vault.
    - Alternatively, you can hardcode the path in the `app.py` file (replace `/path/to/your/vault` with the actual path).

3. **Run the App:**

```bash
FLASK_APP=app.py flask run
```

## API Endpoints

You can access the Swagger UI documentation at `http://127.0.0.1:5000/swagger/` after running the app.  This documentation provides details on each endpoint, including request parameters and response formats.

Here's a summary of the available endpoints:

- **View a Note:** `/note/<path:note_path>` (GET)
- **Edit a Note:** `/note/<path:note_path>` (PUT)
- **Append to a Note:** `/note/<path:note_path>` (PATCH)
- **Search within a Note:** `/note/<path:note_path>/search` (GET)
- **Search across the Entire Vault:** `/search` (GET)
- **View Folder Contents:** `/folder/<path:folder_path>` (GET)
- **View Specific Lines of a Note:** `/note/<path:note_path>/lines/<int:start_line>-<int:end_line>` (GET)
- **Edit Specific Lines of a Note:** `/note/<path:note_path>/lines/<int:start_line>-<int:end_line>` (PATCH)


## Example Usage


**View a note:**

```bash
curl http://127.0.0.1:5000/note/MyNote
```

**Edit a note:**

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"content": "# New Content"}' http://127.0.0.1:5000/note/MyNote
```

**Append to a note:**

```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"content": "Appended text"}' http://127.0.0.1:5000/note/MyNote
```


## Contributing


Feel free to contribute to this project by submitting pull requests or reporting issues.


## License


This project is licensed under the [MIT License](LICENSE).
