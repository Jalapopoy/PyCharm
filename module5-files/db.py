from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'db_api_sia101_jem'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)