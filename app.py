"""Small apps to demonstrate endpoints with basic feature - CRUD"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from api.books.endpoints import books_endpoints
from api.kategori.endpoints import kategori_endpoints
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints
from config import Config
from static.static_file_server import static_file_server
from api.barang.endpoints import barang_endpoints
from api.peminjam.endpoints import peminjam_endpoints
from api.pengelolaan.endpoints import pengelolaan_endpoints
from api.pengembalian.endpoints import pengembalian_endpoints
# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


jwt.init_app(app)

# register the blueprint
app.register_blueprint(auth_endpoints, url_prefix='/api/v1/auth')
app.register_blueprint(protected_endpoints,
                       url_prefix='/api/v1/protected')
app.register_blueprint(books_endpoints, url_prefix='/api/v1/books')
app.register_blueprint(kategori_endpoints, url_prefix='/api/v1/kategori')
app.register_blueprint(static_file_server, url_prefix='/static/')
app.register_blueprint(barang_endpoints, url_prefix='/api/v1/barang')
app.register_blueprint(peminjam_endpoints, url_prefix='/api/v1/peminjam')
app.register_blueprint(pengelolaan_endpoints, url_prefix='/api/v1/pengelolaan')
app.register_blueprint(pengembalian_endpoints, url_prefix='/api/v1/pengembalian')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
