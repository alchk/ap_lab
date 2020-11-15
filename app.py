from flask import Flask


app = Flask("__name__")

@app.route("/api/v1/hello-world-1")
def index():
    return "Hello World-1"


if __name__ == '__main__':
    app.run()