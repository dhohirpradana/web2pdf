import uuid
from flask import Flask, request, jsonify, send_file
from screenshot import handler as screenshot_handler

app = Flask(__name__)


@app.route('/page2pdf', methods=['GET'])
def generate_pdf():
    # get params url, file_name and wait
    url = request.args.get('url')
    file_name = request.args.get('filename')
    wait = request.args.get('wait')

    # validate params
    if not url or url == '':
        return jsonify({'message': 'url is required'}), 400

    if not file_name or file_name == '':
        return jsonify({'message': 'file_name is required'}), 400

    if not wait or wait == '':
        return jsonify({'message': 'wait is required'}), 400

    # validate filename cannot contain extension
    if '.' in file_name:
        return jsonify({'message': 'file_name cannot contain extension'}), 400

    # join url and all params except filename and wait
    for param in request.args:
        if param != 'filename' and param != 'wait' and param != 'long':
            url += f'&{param}={request.args.get(param)}'

    print("URL: ", url)

    wait = int(wait)

    # randomize filename
    file_name = f'{file_name}_{uuid.uuid4()}'

    ss = screenshot_handler(url, wait, file_name)

    if not ss:
        return jsonify({'message': 'Something went wrong'}), 500

    pdf_path = f'{file_name}.pdf'

    try:
        with open(pdf_path, 'rb') as file:
            return send_file(pdf_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
