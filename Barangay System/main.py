from app import app
import user
import document_type
import resident
import payment
import request_txn
import request_api

if __name__ == "__main__":
    app.run(debug=True, port=5050)
