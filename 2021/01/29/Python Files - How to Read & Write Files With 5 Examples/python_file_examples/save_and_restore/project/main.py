from flask import Flask, Blueprint, redirect, url_for

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)