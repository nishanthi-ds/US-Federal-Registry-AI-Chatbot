
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_recent_documents",
            "description": "Fetch the most recent documents from the federal registry database",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of most recent documents to fetch"
                    }
                },
                "required": ["limit"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_topic",
            "description": "Search and return documents matching the given topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic or keyword to search in title and abstract"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_document_summary_by_number",
            "description": "Fetch a summary of the document using its document number",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_number": {
                        "type": "string",
                        "description": "Unique identifier of the document"
                    }
                },
                "required": ["document_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_agency",
            "description": "Fetch documents published by a specific agency",
            "parameters": {
                "type": "object",
                "properties": {
                    "agency_name": {
                        "type": "string",
                        "description": "Name of the agency to filter documents"
                    }
                },
                "required": ["agency_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_type",
            "description": "Fetch documents by their type, such as 'Rule', 'Notice', etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "description": "Type of document to search for (e.g., 'Rule', 'Notice')"
                    }
                },
                "required": ["doc_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_keyword_and_date",
            "description": "Search for documents using a keyword within a date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search in title, abstract, and description"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in format YYYY-MM-DD"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in format YYYY-MM-DD"
                    }
                },
                "required": ["keyword", "start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_agency_and_type",
            "description": "Fetch documents by both agency and document type",
            "parameters": {
                "type": "object",
                "properties": {
                    "agency": {
                        "type": "string",
                        "description": "Name of the agency"
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "Type of document (e.g., 'Rule', 'Notice')"
                    }
                },
                "required": ["agency", "doc_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_document_titles_by_keyword",
            "description": "Return a list of document titles matching the given keyword",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search in title, abstract, and description"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_documents_by_type_and_date",
            "description": "Returns all documents of a given type published on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "description": "Type of document, such as Rule, Notice, Proposed Rule, etc."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of publication in YYYY-MM-DD format"
                    }
                },
                "required": ["doc_type", "date"]
            }
        }
    }

]