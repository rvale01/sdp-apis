import mysql.connector
DB_NAME = 'akxgfb7wff6k2npl'

  
def get_connection():
    conn = mysql.connector.connect(host='uyu7j8yohcwo35j3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                                   user='nq3i5nayr8zyaj25',
                                   password='ghkrutm249i1ou8x',
                                   port='3306',
                                   database='akxgfb7wff6k2npl')
    return conn