from datetime import date 


def get_last_updated_date(conn, cursor):
    cursor.execute("SELECT MAX(publication_date) FROM federal_documents")
    result = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()
    return result[0] or date(2000, 1, 1)  # Default fallback