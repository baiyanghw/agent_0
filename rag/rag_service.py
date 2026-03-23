"""
总结服务，用户提问，搜索参考资料，将提问与参考资料交给模型，让模型总结回复
"""
from typing import List
from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser


def print_template(template):
    print("="*20)
    print(template.to_string())
    print("="*20)
    return template


class RagSummaryService(object):
    def __init__(self):
        self.vector_store=VectorStoreService()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text=load_rag_prompts()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain=self._init_chain()

    def _init_chain(self):
        chain=self.prompt_template | print_template|chat_model | StrOutputParser()
        return chain

    def retriever_docs(self,query:str)->List[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self,query:str)-> str:
        context_docs=self.retriever_docs(query)
        context=""
        counter=0
        for doc in context_docs:
            counter+=1
            context+=f"[参考资料{counter}]:参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input":query,
                "context":context
            }
        )

if __name__=="__main__":
    rag=RagSummaryService()
    print(rag.rag_summarize("小户型适合哪种扫地机器人"))

