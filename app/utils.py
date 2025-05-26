from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph

from bili_server.document_loader import DocumentLoader
from bili_server.edges import EdgeGraph
from bili_server.generate_chain import create_generate_chain
from bili_server.graph import GraphState
from bili_server.grader import GraderUtils
from bili_server.nodes import GraphNodes

from langgraph.graph import END, StateGraph


def create_parser_components(api_key: str,model: str):
    """
    创建并初始化解析器组件和评分器实例

    Args:
        api_key(str): 用于访问大模型的API密钥
        model : 使用的模型

    Returns:
        dict: 包含所有创建的组件实例的字典。
    """

    retrieve = DocumentLoader()

    llm = ChatOpenAI(
        api_key = 'sk-6d33490b5a004811b2768193ffe9a72e',
        model = model,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature = 0,
    )

    generate_chain = create_generate_chain(llm)

    grader = GraderUtils(llm)

    retrieval_grader = grader.create_retrieval_grader()

    hallucination_grader = grader.create_hallucination_grader()

    code_evaluator = grader.create_code_evaluator()

    question_rewriter = grader.create_retrieval_grader()

    return {
        "llm" : llm,
        "retrieve": retrieve,
        "generate_chain": generate_chain,
        "retrieval_grader": retrieval_grader,
        "hallucination_grader":hallucination_grader,
        "code_evaluator": code_evaluator,
        "question_rewriter": question_rewriter
    }

def create_workflow(api_key:str,model:str)->  CompiledGraph:
    """
    创建并初始化工作流以及组成的节点和边

    Returns:
        StateGraph: 完全初始化和编译好的工作流对象。
    """

    components = create_parser_components(api_key,model)
    llm = components["llm"]
    retrieve = components["retrieve"]
    generate_chain = components["generate_chain"]
    retrieval_grader = components["retrieval_grader"]  # 注意拼写一致性
    hallucination_grader = components["hallucination_grader"]
    code_evaluator = components["code_evaluator"]
    question_rewriter = components["question_rewriter"]

    workflow = StateGraph(GraphState)

    graph_nodes = GraphNodes(llm,retrieve,retrieval_grader,hallucination_grader,code_evaluator,question_rewriter)

    edges_graph = EdgeGraph(hallucination_grader,code_evaluator)

    workflow.add_node("retrieve",graph_nodes.retrieve)
    workflow.add_node("grade_documents",graph_nodes.grade_documents)
    workflow.add_node("generate",graph_nodes.generate)
    workflow.add_node("transform_query", graph_nodes.transform_query)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve","grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        edges_graph.decide_to_generate,
        {
            "transform_query":"transform_query",
            "generate":"generate"
        }
    )
    workflow.add_edge("transform_query","retrieve")
    workflow.add_conditional_edges(
        "generate",
        edges_graph.grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query"
        }
    )

    chain = workflow.compile()
    print(type(chain))
    return chain

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv,find_dotenv
    load_dotenv(find_dotenv())

    create_workflow("sk-6d33490b5a004811b2768193ffe9a72e",
                    os.getenv('model'))