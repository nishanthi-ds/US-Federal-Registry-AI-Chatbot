
def get_recent_documents(cursor,limit: int = 5) -> list:
    query = "SELECT title, publication_date, document_number FROM federal_documents ORDER BY publication_date DESC LIMIT %s"
    cursor.execute(query, (int(limit),))
    return cursor.fetchall() # title, publication_date, document_number


def get_documents_by_topic(cursor, topic: str) -> list:
    query = """
        SELECT title, publication_date, abstract
        FROM federal_documents 
        WHERE title LIKE %s OR abstract LIKE %s 
        ORDER BY publication_date DESC
    """
    like_pattern = f"%{topic}%"
    cursor.execute(query, (like_pattern, like_pattern))
    return cursor.fetchall()  # title, publication_date, abstract


def get_document_summary_by_number(cursor, document_number: str) -> dict:
    query = "SELECT title, publication_date, abstract, description, document_number FROM federal_documents WHERE document_number = %s"
    cursor.execute(query, (document_number,))
    return cursor.fetchall() # title, publication date, abstract, description


def get_documents_by_agency(cursor,agency_name: str) -> list:
    query = "SELECT title, publication_date FROM federal_documents WHERE agencies LIKE %s ORDER BY publication_date DESC"
    cursor.execute(query, ('%' + agency_name + '%',))
    return cursor.fetchall() #title, publication_date


def get_documents_by_type(cursor,doc_type: str) -> list:
    query = "SELECT title, publication_date, document_number FROM federal_documents WHERE type = %s ORDER BY publication_date DESC"
    cursor.execute(query, (doc_type,))
    return cursor.fetchall()


def get_documents_by_keyword_and_date(cursor, keyword: str, start_date: str, end_date: str) -> list:
    query = """
        SELECT title, type, publication_date, document_number
        FROM federal_documents
        WHERE (title LIKE %s OR abstract LIKE %s OR description LIKE %s)
          AND publication_date BETWEEN %s AND %s
        ORDER BY publication_date DESC
    """
    keyword_pattern = f"%{keyword}%"
    cursor.execute(query, (keyword_pattern, keyword_pattern, keyword_pattern, start_date, end_date))
    return cursor.fetchall()


def get_documents_by_agency_and_type(cursor, agency: str, doc_type: str) -> list:
    query = """
        SELECT title, type, publication_date, document_number
        FROM federal_documents
        WHERE agencies LIKE %s AND type = %s
        ORDER BY publication_date DESC
    """
    agency_pattern = f"%{agency}%"
    cursor.execute(query, (agency_pattern, doc_type))
    return cursor.fetchall()


def get_document_titles_by_keyword(cursor, keyword: str) -> list:
    query = """
        SELECT title
        FROM federal_documents
        WHERE title LIKE %s OR abstract LIKE %s OR description LIKE %s
        ORDER BY publication_date DESC
    """
    keyword_pattern = f"%{keyword}%"
    cursor.execute(query, (keyword_pattern, keyword_pattern, keyword_pattern))
    results = cursor.fetchall()
    return [row[0] for row in results]  # Return only titles as a list


def get_documents_by_type_and_date(cursor, doc_type: str, date: str) -> list:
    query = """
        SELECT title, publication_date, document_number
        FROM federal_documents
        WHERE type = %s AND publication_date = %s
        ORDER BY publication_date DESC;
    """
    cursor.execute(query, (doc_type, date))
    return cursor.fetchall()


TOOL_MAP = {
    "get_recent_documents": get_recent_documents,
    "get_documents_by_topic": get_documents_by_topic,
    "get_document_summary_by_number": get_document_summary_by_number,
    "get_documents_by_agency": get_documents_by_agency,
    "get_documents_by_type": get_documents_by_type,
    "get_documents_by_keyword_and_date": get_documents_by_keyword_and_date,
    "get_documents_by_agency_and_type": get_documents_by_agency_and_type,
    "get_document_titles_by_keyword": get_document_titles_by_keyword,
    "get_documents_by_type_and_date": get_documents_by_type_and_date
}