from src.config import config_data
from operator import itemgetter
from langchain.llms import OpenAI
from src.handlers.file_handler import load_txt_file, save_txt_file, FILE_PATH_GPT_INPUT, FILE_PATH_GPT_OUTPUT

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

data = config_data.get_config_data()
text = load_txt_file(FILE_PATH_GPT_INPUT)
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(data)

# llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)
# answer = llm.predict(text)
# print(answer)


chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
answer = chat.predict_messages([HumanMessage(content=f"{text}")])

save_txt_file(FILE_PATH_GPT_OUTPUT, answer.content)
print("Done.")