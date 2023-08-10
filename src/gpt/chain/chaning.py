from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


def create_llm_chain(llm, prompt: str, output_key: str):
    prompt = ChatPromptTemplate.from_template(prompt)
    return LLMChain(llm=llm, prompt=prompt, output_key=output_key)
