from marshal import dumps
import os

from langchain_core.documents import Document
from bilibili_tools import get_bilibili
from typing import List,Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
import asyncio

load_dotenv(find_dotenv())

class DocumentLoader:
    """
    This class uses the get_docs function to take a Keyword as input , and outputs a list of documents (including metadata).
    """
    async def get_docs(self,keywords:List[str],page:int) -> List[Document]:
        """
        Asynchronously retrieves documents based on specific keywords from the BiliBili API.
        This function utilizes a pipeline to fetch and format video data, returning it as Document objects.

        Args:
            keywords (List[str]):A list of keywords used to query the BiliBili API.
            page (int): The page number in the API request, used for pagination.

        Returns:
            List[Document]: A list of Document objects containing the retrieved content.
        """

        raw_docs = await get_bilibili.bilibili_detail_pipline(keywords=keywords,page=page)

        docs = [Document(page_content=doc["real_data"]) for doc in raw_docs]

        return docs

    async def create_vector_store(self,docs,store_path: Optional[str] = None)-> 'FAISS':
        """
            Creates a FAISS vector store from a list of documents.

            Args:
                docs (List[Document]): A list of Document objects containing the content to be stored.
                store_path (Optional[str]): The path to store the vector store locally.If None, the vector store will be created in memory and not persisted to disk.
            Return:
                FAISS: The FAISS vector store containing the documents.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        texts = text_splitter.split_documents(docs)

        embedding_model = DashScopeEmbeddings(
            model='text-embedding-v3',
            dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )

        # 分批处理（每批10个）
        batch_size = 10
        vector_store = None

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            if not batch:
                continue

            # 异步处理嵌入
            embeddings = await asyncio.get_event_loop().run_in_executor(
                None,  # 使用默认执行器
                lambda: embedding_model.embed_documents([doc.page_content for doc in batch])
            )

            # 创建临时存储
            temp_store = FAISS.from_embeddings(
                text_embeddings=list(zip(
                    [doc.page_content for doc in batch],
                    embeddings
                )),
                embedding=embedding_model,
                metadatas=[doc.metadata for doc in batch]
            )

            # 合并存储
            if vector_store is None:
                vector_store = temp_store
            else:
                vector_store.merge_from(temp_store)

        if store_path and vector_store:
            await asyncio.get_event_loop().run_in_executor(
                None, vector_store.save_local, store_path
            )

        return vector_store or FAISS.from_documents([], embedding_model)

    async def get_retriever(self,keywords: List[str],page:int):
        """
        Retrieves documents and returns a retriever based on the documents

        Args:
           keywords (List[str]): Keywords to search documents.
           page(int): Page number for pagination of results.

        Return:
            Retriever instance or FAISS vector store.
        """

        print(f"开始实时查询BiliBiliAPI获取数据")
        docs = await self.get_docs(keywords,page)
        print(f"接收到的BiliBili数据为:{docs}")
        print("---------------------------")
        print(f"开始进行向量数据库存储")
        vector_store = await self.create_vector_store(docs)
        print(f"成功完成向量数据库存储")
        print("---------------------------")
        print(f"开始进行文本检索")
        retriever = vector_store.as_retriever(search_kwargs={"k":6})
        retriever_result = retriever.invoke(str(keywords))
        print(f"检索到的数据为：{retriever_result}")
        return retriever_result

if __name__ == '__main__':
    import asyncio
    async def main():
        loader = DocumentLoader()
        await loader.get_retriever(keywords=["ChatGLM3-6b"],page=1)
    asyncio.run(main())