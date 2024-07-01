"""Routes for module books"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

barang_endpoints = Blueprint('barang', __name__)
UPLOAD_FOLDER = "img"


@barang_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list barang"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM barang"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

# @barang_endpoints.route('/read/<id_kategori>', methods=['GET'])
# def readbyid(id_kategori):
#     """Routes for module get list container"""
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)
#     select_query = "SELECT * FROM barang where id_kategori=%s"
#     select_id = (id_kategori,)
#     cursor.execute(select_query, select_id)
#     results = cursor.fetchall()
#     cursor.close()  # Close the cursor after query execution
#     connection.close()
#     return jsonify({"message": "OK", "datas": results}), 200

@barang_endpoints.route('/read/<id_kategori>', methods=['GET'])
def readByUserId(id_kategori):
    """Routes for module get list pengguna with pagination"""
    try:
        # Get the page parameter from the query string, default to 1 if not provided
        page = request.args.get('page', default=1, type=int)
        per_page = 6  # Fixed items per page

        # Calculate the offset
        offset = (page - 1) * per_page

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Modify the query to include LIMIT and OFFSET for pagination
        select_query = "SELECT * FROM barang WHERE id_kategori = %s LIMIT %s OFFSET %s"
        select_request = (id_kategori, per_page, offset)
        cursor.execute(select_query, select_request)
        results = cursor.fetchall()

        # Get the total count of the items for the given id_kategori
        count_query = "SELECT COUNT(*) as total FROM barang WHERE id_kategori = %s"
        cursor.execute(count_query, (id_kategori,))
        total_count = cursor.fetchone()['total']
        
    except mysql.connector.Error as err:
        return jsonify({"message": "Error", "error": str(err)}), 500
    finally:
        cursor.close()  # Pastikan cursor selalu ditutup
        connection.close()  # Pastikan koneksi selalu ditutup

    return jsonify({
        "message": "OK",
        "datas": results,
        "page": page,
        "per_page": per_page,
        "total": total_count,
        "total_pages": (total_count + per_page - 1) // per_page  # Menghitung jumlah total halaman
    }), 200

# @barang_endpoints.route('/read/<id_kategori>', methods=['GET'])
# def readbyid(id_kategori):
#     """Routes for module get list container with pagination"""
#     page = request.args.get('page', default=1, type=int)  # Get the page number from query parameters, default is 1
#     per_page = 6  # Number of items per page
    
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)
    
#     # Calculate the offset for the SQL query
#     offset = (page - 1) * per_page
    
#     select_query = """
#         SELECT * FROM barang
#         WHERE id_kategori=%s
#         LIMIT %s OFFSET %s
#     """
#     cursor.execute(select_query, (id_kategori, per_page, offset))
#     results = cursor.fetchall()
    
#     # Check if there are more items for the next page
#     next_query = """
#         SELECT COUNT(*) as count FROM barang
#         WHERE id_kategori=%s AND id > (SELECT MAX(id) FROM barang WHERE id_kategori=%s LIMIT %s OFFSET %s)
#     """
#     cursor.execute(next_query, (id_kategori, id_kategori, per_page, offset))
#     next_result = cursor.fetchone()
#     has_more = next_result['count'] > 0
    
#     cursor.close()  # Close the cursor after query execution
#     connection.close()
    
#     return jsonify({"message": "OK", "datas": results, "has_more": has_more}), 200

    
@barang_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    id_kategori = request.form['id_kategori']
    nama_barang = request.form["nama_barang"]
    jumlah_barang = request.form['jumlah_barang']
    deskripsi_barang = request.form['deskripsi_barang']
    
    uploaded_file = request.files['gambar_barang']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        connection = get_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO barang (nama_barang, jumlah_barang, id_kategori, gambar_barang, deskripsi_barang) VALUES (%s, %s, %s, %s, %s)"
        request_insert = (nama_barang, jumlah_barang, id_kategori, uploaded_file.filename, deskripsi_barang)
        cursor.execute(insert_query, request_insert)
        connection.commit()  # Commit changes to the database
        cursor.close()
        new_id = cursor.lastrowid  # Get the newly inserted book's ID\
        if new_id:
            return jsonify({"title": nama_barang, "message": "Inserted", "id_barang": new_id}), 201
        return jsonify({"message": "Cant Insert Data"}), 500


@barang_endpoints.route('/update/<id_barang>', methods=['POST'])
def update(id_barang):
    """Routes for module update a book"""
    nama_barang = request.form['nama_barang']
    jumlah_barang = request.form['jumlah_barang']
    deskripsi_barang = request.form['deskripsi_barang']

    uploaded_file = request.files['gambar_barang']
    connection = get_connection()
    cursor = connection.cursor()

    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)

        update_query = "UPDATE barang SET nama_barang=%s, jumlah_barang=%s, deskripsi_barang=%s, gambar_barang=%s WHERE id_barang=%s"
        update_request = (nama_barang, jumlah_barang, deskripsi_barang, uploaded_file.filename, id_barang)
    else:
        update_query = "UPDATE barang SET nama_barang=%s, jumlah_barang=%s, deskripsi_barang=%s WHERE id_barang=%s"
        update_request = (nama_barang, jumlah_barang, deskripsi_barang, id_barang)

    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    connection.close()

    data = {"message": "updated", "id_barang": id_barang}
    return jsonify(data), 200



@barang_endpoints.route('/delete/<id_barang>', methods=['DELETE'])
def delete(id_barang):
    """Routes for module to delete a book"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM barang WHERE id_barang = %s"
    delete_id = (id_barang,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    data = {"message": "Data deleted", "id_barang": id_barang} # type: ignore
    return jsonify(data)


@barang_endpoints.route("/upload", methods=["POST"])
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400

@barang_endpoints.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')  # Mendapatkan parameter 'keyword' dari query string
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Melakukan pencarian berdasarkan nama_wisata yang mengandung keyword
        search_query = "SELECT * FROM barang WHERE nama_barang LIKE %s"
        search_request = (f"%{keyword}%",)
        cursor.execute(search_query, search_request)
        results = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify({"message": "OK", "datas": results}), 200
    
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
@barang_endpoints.route('/user/<int:id_user>', methods=['GET'])
def readFavorit(id_user):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = """
        SELECT barang.*
        FROM cart
        JOIN barang ON cart.id_barang = barang.id_barang
        WHERE cart.id_user = %s
    """
    cursor.execute(select_query, (id_user,))
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@barang_endpoints.route('/remove', methods=['POST'])
def remove():
    data = request.get_json()
    id_user = data.get('id_user')
    id_barang = data.get('id_barang')

    if not id_user or not id_barang:
        return jsonify({"error": "Invalid request, missing id_user or id_barang"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        delete_query = "DELETE FROM cart WHERE id_user = %s AND id_barang = %s"
        cursor.execute(delete_query, (id_user, id_barang))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Barang berhasil dihapus dari cart"}), 200
    except Exception as e:
        cursor.close()
        return jsonify({"error": str(e)}), 500

@barang_endpoints.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    id_user = data.get('id_user')
    id_barang = data.get('id_barang')

    if not id_user or not id_barang:
        return jsonify({"error": "Invalid request, missing id_user or id_barang"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        insert_query = "INSERT INTO cart (id_user, id_barang) VALUES (%s, %s)"
        cursor.execute(insert_query, (id_user, id_barang))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Wisata berhasil ditambahkan ke favorit"}), 200
    except Exception as e:
        cursor.close()
        return jsonify({"error": str(e)}), 500
