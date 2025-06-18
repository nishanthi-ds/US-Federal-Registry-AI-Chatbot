from pipeline.fetch_data import fetch_documents, get_metadata
import asyncio  
from pipeline.preprocess import process_pdfs
import pandas as pd
from database.connect_mysql import get_connection
from database.db_manipulation import insert_data_to_db
from agent.llm_agent import chat_with_agent
from database.updated_date import get_last_updated_date


conn = get_connection()
cursor = conn.cursor()
# start_date= get_last_updated_date(conn,cursor)
# raw_data= fetch_documents(start_date)

# df = pd.DataFrame(raw_data)

# all_data = asyncio.run(get_metadata(raw_data))
# descriptions = asyncio.run(process_pdfs(df))
# df["description"] = descriptions


conn= get_connection()
cursor = conn.cursor()   
# insert_data_to_db(df,  conn, cursor) # create_table(cursor)

asyncio.run(chat_with_agent())