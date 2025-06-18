def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS federal_documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            type VARCHAR(255),
            publication_date DATE,
            abstract TEXT,
            pdf_url TEXT,
            document_number VARCHAR(255) UNIQUE,
            agencies TEXT,
            description LONGTEXT
        )
    ''')

def insert_data_to_db(data, conn, cursor):

    # cursor.execute("DELETE FROM federal_documents")
    query ='''
        INSERT INTO federal_documents 
        (title, type, publication_date, abstract, pdf_url, document_number, agencies, description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for doc in data:
        cursor.execute(query, (
            doc['title'],
            doc['type'],
            doc['publication_date'],
            doc['abstract'],
            doc['pdf_url'],
            doc['document_number'],
            doc['agencies'],
            doc['description']
        ))
    conn.commit()
    cursor.close()
    conn.close()
