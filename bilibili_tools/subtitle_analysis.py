import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


llm = ChatOpenAI(
    api_key = "sk-6d33490b5a004811b2768193ffe9a72e",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    model = "qwq-32b",
    temperature=0,
    streaming=True
)


def get_subtitle_analysis(subtitle):
    subtitle_prompt_template = """
        作为资深数字内容分析师，请基于提供的视频字幕文本{subtitle}执行深度解析，按以下框架生成结构化报告：
            一、内容摘要（180-200字）
            要求：采用"总-分-总"结构，包含
            1. 核心主题识别（20字内精准定位）
            2. 内容架构拆解（按逻辑模块划分）
            3. 价值密度评估（信息有效性/新颖性）
            4. 观众收益说明（知识/情感/行动层面）
            
            二、关键洞察清单（5-7项）
            每项需包含：
            [时间戳]（如00:02:15-00:03:30）
            ▶ 论点类型：（概念阐述/案例论证/数据呈现/观点碰撞）
            ◉ 内容精要：（40字内精准提炼）
            ★ 价值标记：（创新性/实用性/争议性 三选一）
            
            三、专业注释（可选）
            - 逻辑连贯性评价（内容衔接度）
            - 叙事策略分析（悬念设置/情感曲线）
            - 潜在知识盲区提示（需验证的信息点）
            
            【格式规范】
            1. 使用Markdown层级标题（###）
            2. 关键项采用符号标记系统（▶◉★）
            3. 避免主观形容词，保持客观陈述
            4. 专业术语使用括号注释（首次出现时）
            5. 如果传入的视频非专业教学或科普视频则根据视频内容自由发挥即可
            
    """
    print("---开始创建链---")
    subtitle_prompt = PromptTemplate(
        template = subtitle_prompt_template,
        input_variables=["subtitle"]
    )

    subtitle_chain = subtitle_prompt | llm
    print("---开始流式输出---")
    for chunk in subtitle_chain.stream(subtitle):
        if chunk.content:
            yield chunk.content
    # return subtitle_chain
# if __name__ == "__main__":
#
#     res_chain = get_subtitle_analysis()
#
#     for chunk in res_chain.stream({"subtitle":"00:00:00,000 大家好00:00:00,000 我是word matrix00:00:01,000 在过去漫长的基础项目实战教程中00:00:04,000 经常会有同学提问00:00:05,000 说自己明明已经掌握了编程语言的语法00:00:08,000 但是对于如何设计自己的程序结构00:00:11,000 如何写下第一行有用的代码00:00:13,000 经常会感到无所适从00:00:14,000 对此我的回复常常是说00:00:16,000 多写代码00:00:17,000 多动手00:00:18,000 实践出真知00:00:19,000 书读百遍00:00:20,000 其义自现00:00:20,000 很多时候00:00:21,000 我们的代码设计思路00:00:22,000 都需要从项目的磨砺和反馈中获得"}):
#         if chunk.content:  # 过滤空内容块
#             print(chunk.content, end="", flush=True)
