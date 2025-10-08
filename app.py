from flask import Flask
from routes.gate_routes import gate
from routes.admin_routes import admin

app = Flask(__name__)
app.register_blueprint(gate, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
