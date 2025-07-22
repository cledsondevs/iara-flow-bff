import sqlite3
from datetime import datetime
import uuid

def add_test_review():
    conn = sqlite3.connect('./iara_flow.db')
    cursor = conn.cursor()

    review_id = str(uuid.uuid4())
    package_name = 'com.example.app'
    store = 'google_play'
    user_name = 'Test User'
    rating = 1
    content = 'This app is very bad and slow. It has many bugs.'
    review_date = datetime.now().isoformat()
    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO reviews (id, package_name, store, review_id, user_name, rating, content, review_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (review_id, package_name, store, review_id, user_name, rating, content, review_date, created_at))
    
    conn.commit()
    conn.close()
    print(f"Review de teste adicionado para {package_name}")

if __name__ == '__main__':
    add_test_review()


