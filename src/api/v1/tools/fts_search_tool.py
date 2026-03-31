import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from langchain_core.tools import tool

load_dotenv()
_raw_conn = os.getenv("SQLALCHEMY_DATABASE_URL", "").replace("postgresql+psycopg", "postgresql")


def fts_search(query: str, k: int = 5, collection_name: str = "hr_support_desk") -> list[dict]:
   """
    Use this tool to retrieve HR information using exact keyword matching.
    Best suited for policy names, acronyms, fixed terms, and titles.
    Use when the user query contains specific or known HR terminology.
    Do not use for conversational or explanatory questions
   """
   sql = """
       SELECT
           e.document                                               AS content,
           e.cmetadata                                              AS metadata,
           ts_rank(
               to_tsvector('english', e.document),
               plainto_tsquery('english', %(query)s)
           )                                                        AS fts_rank
       FROM  langchain_pg_embedding  e
       JOIN  langchain_pg_collection c ON c.uuid = e.collection_id
       WHERE c.name = %(collection)s
         AND to_tsvector('english', e.document)
             @@ plainto_tsquery('english', %(query)s)
       ORDER BY fts_rank DESC
       LIMIT %(k)s;
   """
   with psycopg.connect(_raw_conn, row_factory=dict_row) as conn:
       with conn.cursor() as cur:
           cur.execute(sql, {"query": query, "collection": collection_name, "k": k})
           rows = cur.fetchall()


   return [
       {
           "content":  row["content"],
           "metadata": row["metadata"],
           "fts_rank": round(float(row["fts_rank"]), 4),
       }
       for row in rows
   ]