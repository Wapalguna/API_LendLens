"""Routes for module kategori"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

kategori_endpoints = Blueprint('kategori', __name__)
UPLOAD_FOLDER = "img"


@kategori_endpoints.route('/read', methods=['GET'])
def read():
    """Routes for module get list kategori"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM kategori"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200


@kategori_endpoints.route('/create', methods=['POST'])
def create():
    """Routes for module create a book"""
    nama_kategori = request.form['Nama_kategori']
    deskripsi = request.form['deskripsi']

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO kategori (Nama_kategori, deskripsi) VALUES (%s, %s)"
    request_insert = (nama_kategori, deskripsi)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit changes to the database
    cursor.close()
    new_id = cursor.lastrowid  # Get the newly inserted book's ID\
    if new_id:
        return jsonify({"title": nama_kategori, "message": "Inserted", "id_kategori": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

# @kategori_endpoints.route('/create', methods=['POST'])
# def create():
#     """Routes for module create a kategori"""
#     id_user = request.form['id_user']
#     nama_kategori = request.form['namaKategori']
#         connection = get_connection()
#         cursor = connection.cursor()
#         insert_query = "INSERT INTO container (id_user, namaKategori) VALUES (%s, %s)"
#         request_insert = (id_user, nama_kategori,)
#         cursor.execute(insert_query, request_insert)
#         connection.commit()  # Commit changes to the database
#         cursor.close()
#         new_id = cursor.lastrowid  # Get the newly inserted book's ID\
#         if new_id:
#             return jsonify({"title": namaKategori, "message": "Inserted", "id_kategori": new_id}), 201
#         return jsonify({"message": "Cant Insert Data"}), 500


@kategori_endpoints.route('/update/<product_id>', methods=['PUT'])
def update(product_id):
    """Routes for module update a book"""
    title = request.form['title']
    description = request.form['description']

    connection = get_connection()
    cursor = connection.cursor()

    update_query = "UPDATE tb_kategori SET title=%s, description=%s WHERE id_kategori=%s"
    update_request = (title, description, product_id)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    data = {"message": "updated", "id_kategori": product_id}
    return jsonify(data), 200


@kategori_endpoints.route('/delete/<product_id>', methods=['GET'])
def delete(product_id):
    """Routes for module to delete a book"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM tb_kategori WHERE id_kategori = %s"
    delete_id = (product_id,)
    cursor.execute(delete_query, delete_id)
    connection.commit()
    cursor.close()
    data = {"message": "Data deleted", "id_kategori": product_id}
    return jsonify(data)


@kategori_endpoints.route("/upload", methods=["POST"])
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "ok", "data": "uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400
