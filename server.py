import os
from dotenv import load_dotenv

load_dotenv()

# 載入Flask套件
from flask import Flask, jsonify
from flask_restful import Api

# 創建Flask app物件
app = Flask(__name__)
app.json.sort_keys = False
api = Api(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=os.getenv("APP_MODE") == "development")
