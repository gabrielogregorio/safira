from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


data = []

@app.route('/gravar/', methods=['POST'])
def gravar_dados():
    dicionario = request.get_json()

    if not isinstance(dicionario, dict):
        return jsonify({'no_please':'você está certo'})

    data.append(dicionario)

    return jsonify({'deu certo?':'Não sei!'})


@app.route('/', methods=['GET'])
def consultar():
    return jsonify(data)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5723
    debug=True

    app.run(host=host, port=port, debug=debug)