from langchain_cohere import CohereRagRetriever, ChatCohere
from langchain.retrievers import WikipediaRetriever
# let me get an interface to make this use pydantic

# what are other good mvps,?
class CohereWikipediaTTTChain:
    def __init__(self, api_key: str):
        self.cohere_chat_model = ChatCohere(api_key=api_key)
        self.wiki_retriever = WikipediaRetriever()
        self.rag = CohereRagRetriever(llm=self.cohere_chat_model)

    def _call(self, text_dict: dict) -> str:
        text = text_dict['text']
        wiki_docs = self.wiki_retriever.get_relevant_documents(text)
        document_contents = "\n\n".join([doc.page_content for doc in wiki_docs])
        query_with_context = f"{text}\n\n{document_contents}"
        docs = self.rag.invoke(input=query_with_context)
        response = docs[-1].page_content if docs else "No relevant documents found."
        return {"text": response}
