from pathlib import Path
#pathlib join




from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import BasePromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama

from src.database import SessionLocal



with SessionLocal() as s:
    db = SQLDatabase(engine=s.bind)

llm = ChatOllama(
    base_url="host.docker.internal:11434",
    model="llama3.2",
    temperature=0,
)

if __name__ == "__main__":

    filename = Path(__file__).parent / "personas/sql_expert.txt"
    prompt = Path(filename).read_text()



    agent_executor = create_sql_agent(llm, db=db, verbose=True,
                                     #prompt=prompt,
                                     max_iterations=25)
    # resp = agent_executor.run("please create and execute a query that will Show me all trades by legislators for the last 3 days and return the rows.")
    resp = agent_executor.run("please return the trades from the trades table for the last 3 days and the legislators that made the trade. join tables where necessary")

    # BasePromptTemplate
    print(resp)



# llm = ChatCohere(model=”command-r-plus”, temperature=0) 
# agent_executor = create_sql_agent(llm, db=db, verbose=True) 
# resp = agent_executor.run(“Show me the first 5 rows of the ‘Album’ table.”) 
# print(resp.get(“output”))