import os
import tempfile
import requests
from flask import Flask, request, jsonify, make_response

from extract_text import file_to_text
from text_summarizer import summarise_text


app = Flask(__name__)


def download_file(file_url):
    if file_url is None:
        return jsonify({"error": "Missing 'file' parameter in the URL"}), 400
    try:
        # Set allow_redirects=True to follow redirects
        response = requests.get(file_url, stream=True, allow_redirects=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error downloading the file: {str(e)}"}), 400

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name

    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return temp_file_path


@app.route("/summarise")
def summarise():
    file_url = request.args.get("file")
    temp_file_path = download_file(file_url)

    extracted_text = file_to_text(temp_file_path)

    text_summary = summarise_text(extracted_text)

    # return jsonify({"temp_file_path": temp_file_path, "text_summary": text_summary})

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Text Summary</title>
    </head>
    <body>
        <h1>Podsumowanie przetargu</h1>
        <p>{text_summary}</p>
    </body>
    </html>
    """

    return make_response(html, 200)


if __name__ == "__main__":
    app.run(debug=True)
