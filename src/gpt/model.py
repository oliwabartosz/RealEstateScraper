# Config data
from src.config import config_data
from operator import itemgetter
from langchain.chat_models import ChatOpenAI

# Load model
config_data = config_data.get_config_data()
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(config_data)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)
