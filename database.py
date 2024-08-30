import sqlite3
from cryptography.fernet import Fernet

def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials
                 (site TEXT, username TEXT, password BLOB)''')
    conn.commit()
    conn.close()

def save_credentials(site, username, password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("INSERT INTO credentials (site, username, password) VALUES (?, ?, ?)",
              (site, username, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_credentials(key):
    f = Fernet(key)
    
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT site, username, password FROM credentials")
    rows = c.fetchall()
    conn.close()
    
    credentials = []
    for row in rows:
        site, username, encrypted_password = row
        decrypted_password = f.decrypt(encrypted_password).decode()
        credentials.append({"site": site, "username": username, "password": decrypted_password})
    
    return credentials
