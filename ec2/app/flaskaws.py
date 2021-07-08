from flask import Flask, jsonify, render_template
import boto3

server = Flask(__name__)


@server.route('/')
def index():
    try:
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('fotos')
        response = table.scan()
        items = response['Items']
        return render_template("index.html", items = items)
    except Exception as ex:
        return jsonify({"error" : "Error interno en el servidor"}), 500    
    
if __name__ == '__main__':
    server.run()
	
