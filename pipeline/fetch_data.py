import requests
from datetime import date, timedelta, datetime


def fetch_documents(START_DATE, STOP_DATE=date.today()):
    FEDERAL_API = "https://www.federalregister.gov/api/v1/documents.json"


    #two_months_ago = today - timedelta(days=60)

    all_documents = []
    page = 1

    while True:
        print("start")
        params = {
            "per_page": 1000,
            "page": page,
            "order": "newest",
            "conditions[publication_date][gte]": START_DATE,
            "conditions[publication_date][lte]": STOP_DATE,
        }

        response = requests.get(FEDERAL_API, params=params)
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            break

        all_documents.extend(results)
        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break

        page += 1

    return all_documents



def fetch_today_documents():
    FEDERAL_API = "https://www.federalregister.gov/api/v1/documents.json"

    today = date.today()
    
    all_documents = []
    page = 1

    while True:
        print(f"Fetching page {page}...")

        params = {
            "per_page": 1000,
            "page": page,
            "order": "newest",
            "conditions[publication_date][gte]": today.isoformat(),
            "conditions[publication_date][lte]": today.isoformat(),
        }

        response = requests.get(FEDERAL_API, params=params)
        response.raise_for_status()  # add this to raise an exception on error
        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        all_documents.extend(results)
        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break

        page += 1

    return all_documents



# get metadata
async def get_metadata(documents):
    all_data = []

    for i, doc in enumerate(documents):

        all_data.append({
            'title': doc.get('title'),
            'type': doc.get('type'),
            'abstract': doc.get('abstract') or 'No Abstract Available',
            'document_number': doc.get('document_number'),
            # 'html_url': doc.get('html_url'),
            'pdf_url': doc.get('pdf_url'),
            # 'public_inspection_pdf_url': doc.get('public_inspection_pdf_url'),
            'publication_date': doc.get('publication_date'),  # date format Y-M-D
            'agencies': ", ".join([a.get('raw_name', 'No Agency Available') for a in doc.get('agencies', [])]),
            # 'excerpts': doc.get('excerpts'),
            'description': " "
        })

    return all_data