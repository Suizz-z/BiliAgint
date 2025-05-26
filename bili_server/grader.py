import os

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class GraderUtils:
    def __init__(self,model):
        self.model = model

    def create_retrieval_grader(self):

        grader_prompt = PromptTemplate(
            template = """
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing relevance of a retrieved document to a user question.If the document contains keywords related to the user's question (including synonyms, contextual references, or loosely matching terms).
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            
            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {input} \n
            <|eot_id|>
            <|start_header_id|>assistant</end_header_id>
            """,
            input_variables=["document","input"],
        )

        retriever_grader = grader_prompt | self.model |JsonOutputParser()

        return retriever_grader

    def create_hallucination_grader(self):
        """
        Creates a hallucination grader that assesses whether an answer is grounded in/supported by a set of facts.

        Returns:
            A callable function that takes a generation (answer) and a list of documents (facts) as input and returns a JSON object with a binary score indicating whether the answer is grounded in/supported by the facts.
        """
        hallucination_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing whether an answer is grounded in / supported by a set of facts. Give a binary score 'yes' or 'no' score to indicate whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents}
            \n ------- \n
            Here is the answer: {generation}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )

        hallucination_chain = hallucination_prompt | self.model | JsonOutputParser()

        return hallucination_chain


    def create_code_evaluator(self):
        eval_template = PromptTemplate(
            template="""**<|begin_of_text|><|start_header_id|>system</end_header_id|>You are a code evaluator assessing whether the generated code correctly addresses the user's question. 
            Provide a JSON response with the following keys:
            
                'score': A binary score 'yes' or 'no' indicating whether the code is correct and relevant.
                'feedback': A brief explanation of your evaluation, including any issues or improvements needed.
            
            <|eot_id|>
            <|start_header_id|>user</end_header_id|>
            Here is the generated code:
            \n --- \n
            {generation}
            \n --- \n
            Here is the question: {input}
            \n --- \n
            Here are the relevant documents: {documents}
            <|eot_id|>
            <|start_header_id|>assistant</end_header_id|>**""",
            input_variables=["generation", "input", "documents"],
            )
        code_evaluator_chain = eval_template | self.model | JsonOutputParser()

        return code_evaluator_chain

    def create_question_rewriter(self):
        """
        Creates a question rewriter chain that rewrites a given question to improve its clarity and relevance.

        Returns:
            A callable function that takes a question as input and returns the rewritten question as a string.
        """
        re_write_prompt = PromptTemplate(
            template="""
            You a question re-writer that converts an input question to a better version that is optimized for vectorstore retrieval. Look at the input and try to reason about the underlying sematic intent / meaning.

            Here is the initial question: {input}

            Formulate an improved question.""",

            input_variables=["input"],
        )

        question_re_chain = re_write_prompt | self.model | StrOutputParser()

        return question_re_chain

if __name__ == '__main__':
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model=os.getenv("model"),
    )

    grader = GraderUtils(llm)

    # retrieval_grader = grader.create_retrieval_grader()
    #
    # retrieval_grader_results = retrieval_grader.invoke({
    #     "document" : "hahaha",
    #     "input" : "我想要学习langchain"
    # })
    #
    # print(retrieval_grader_results)

    # 创建一个检测大模型幻觉的生成器
    hallucination_grader = grader.create_hallucination_grader()

    # 这是出现幻觉的回答
    hallucination_grader_results = hallucination_grader.invoke({
        "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
        "generation": "你好"
    })
    #
    # # 这是基于检索内容生成的回答
    # hallucination_grader_results = hallucination_grader.invoke({
    #     "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    #     "generation": "一般对于ChatGLM3-6B模型的热门视频，可以从安装部署、微调、训练等方向来思考"
    # })
    #
    print(f"hallucination_grader_results:{hallucination_grader_results}")