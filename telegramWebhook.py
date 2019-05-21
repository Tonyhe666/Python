# !/usr/bin/python
# _*_ coding:utf-8 _*_

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/hi', methods=['GET', 'POST'])
def hi():
    request.method
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True)