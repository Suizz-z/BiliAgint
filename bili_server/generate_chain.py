import os

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv,find_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv())

def create_generate_chain(llm):
    """
    Creates a generate chain for answering bilibili-related questions.

    Args:
        llm(LLM): llm(LLM):The language model to use for generating responses.

    Return:
        A callable function that takes a context and a question as input and returns a string response.

    """

    generate_template="""
    You are an AI personal assistant named HuHu. Users will pose questions related to BiliBili website data, which are presentde in the parts enclosed by <context></context> tags.
    
    Use this information to formulate your answers.
    
    When a user's question requires fetching data using the BiliBili API, you may proceed accordingly.
    If you cannot find an answer, please respond honestly that you do not know. Do not attempt to fabricate an answer.
    If the question is unrelated to the context, politely respond that you can only answer questions related to the context provided.
    
    For questions involving data analysis, please write the code in Python and provide a detailed analysis of the results to offer as comprehensive an answer as possible
    
    <context>
    {context}
    </context>
    
    <question>
    {input}
    </question>
    """

    generate_prompt = PromptTemplate(template=generate_template,input_variables=["context","input"])

    generate_chain = generate_prompt | llm | StrOutputParser()

    return generate_chain

if __name__ == '__main__':


    llm = ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
    )

    generate_chain = create_generate_chain(llm)
    final_answer = generate_chain.invoke({
        "context": "[\"类型:activity\\n作者:\\n分类:\\n视频链接:\\n标题:AI大模型入门！近期最火的9篇AIGC论文精讲+代码复现\\n描述:\\n播放量:0\\n弹幕数:0\\n收藏数:0\\n标签:\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:大模型官方课程\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113684026232679\\n标题:【全748集】目前B站最全最细的AI大模型零基础全套教程，2025最新版，包含所有干货！七天就能从小白到大神！少走99%的弯路！存下吧！很难找全的！\\n描述:【视频配套籽料、学习路线、GitHub项目、实战案例集、电子书+问题解答请看 ”置顶平论” 自取哦】\\r\\n本套教程从零开始讲解，手把手教学，包含Python快速入门、AI开发环境搭建及提示词工程、Transformer架构和预训练、SFT、RLHF等一些基础概念、RAG、Agent、Langchain、大模型微调和私有化部署\\r\\n无论是新手小白，还是有一定编码经验的选手，皆可学习\\r\\n如果视频对你有用的话请 一键三连【长按点赞】支持一下UP哦，拜托，这对我真的很重要！\\n播放量:1064390\\n弹幕数:3402\\n收藏数:53856\\n标签:RAG,大模型,Transformer,Agent,LLM,私有化部署,AI大模型,提示词工程,Langchain,大模型微调\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:咕泡AI大模型\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113677265081065\\n标题:【AI大模型】十分钟彻底搞懂AI大模型底层原理！带你从0构建对大模型的认知！小白也能看懂！\\n描述:最后给大家准备了一套我花一个月收集整理的大模型学习资料，一定对你有用，内容包括大模型学习路线，大模型实战案例、大模型学习视频、大模型书籍PDF等等，带你从零基础系统性的学好大模型。\\n播放量:91395\\n弹幕数:199\\n收藏数:3811\\n标签:人工智能,AI,干货,机器学习,深度学习,大模型,LLM,AI大模型,大语言模型,大模型教程\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:李宏毅大模型\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av1905814039\\n标题:【李宏毅】2024年公认最好的【LLM大模型】教程！大模型入门到进阶，一套全解决！2024生成式人工智慧-附带课件代码\\n描述:NLP大语言模型学习资料和课程PPT都已经打包好了!!\\r\\n有需要的话可以在下方三连+留言领取！！！\\n播放量:224164\\n弹幕数:1446\\n收藏数:14244\\n标签:人工智能,机器学习,李宏毅,神经网络,深度学习,自然语言处理,大模型,agent,LLM,大模型微调\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:OpenBMB\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av428567377\\n标题:【清华NLP】刘知远团队大模型公开课全网首发｜带你从入门到实战\\n描述:制作不易，大家记得点个关注，一键三连呀【点赞、投币、收藏】感谢支持~\\nOpenBMB携手清华大学自然语言处理实验室，共同推出《大模型交叉研讨课》，意在为对大模型感兴趣的同学提供相关资源，为大模型领域的探索打下基础。本课程将手把手带领同学从深度学习开始快速了解大模型的相关理论和实践，最后利用所学知识进行前沿问题的探索。\\n播放量:601553\\n弹幕数:2838\\n收藏数:47286\\n标签:大模型,预训练语言模型,自然语言处理,神经网络,Transformer,BMInf,BMTrain,BMCook,Prompt Tuning,Delta Tuning\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:大模型开发\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av114216266630072\\n标题:爆肝1个月打造！这绝对是2025年最强的大模型学习路线图！底层原理+应用技术+开发框架工具栈+企业级实战！\\n描述:这绝对是2025年最强的大模型学习路线图！\\n播放量:865\\n弹幕数:34\\n收藏数:14\\n标签:人工智能,神经网络,深度学习,大模型,LLM,多模态大模型,大模型学习,大模型入门,大模型开发,DeepSeek爆火\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:马士兵IT课堂\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113821247082740\\n标题:马士兵-AI大模型全套教程（AI学习路线+LLM大语言模型+RAG实战+Langchain+ChatGLM-4+Transformer+DeepSeek部署）\\n描述:AI大模型全套教学视频持续更新中...【后续视频配套籽料+问题解答请看”平论区置顶”自取哦】\\n播放量:197645\\n弹幕数:1014\\n收藏数:18894\\n标签:技术宅,计算机,程序员,编程,公开课,机器学习,深度学习,编程开发,AI大模型,大语言模型 (LLM)\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:AI界扛霸子\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113955397703305\\n标题:【B站首推】浙江大学大模型公开课，2025最新浙大内部VIP大模型课程，大模型原理与技术教程，从入门到进阶，全程干货讲解，拿走不谢！\\n描述:【B站首推】浙江大学大模型公开课，2025最新浙大内部VIP大模型课程，大模型原理与技术教程，从入门到进阶，全程干货讲解，拿走不谢！\\n播放量:43861\\n弹幕数:110\\n收藏数:4541\\n标签:人工智能,机器学习,神经网络,深度学习,OpenAI,LLM,AI大模型,大语言模型,大模型课程,DeepSeek\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:AI大模型全栈\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av1904333047\\n标题:【全748集】清华大佬终于把AI大模型（LLM）讲清楚了！通俗易懂，2024最新内部版！拿走不谢，学不会我退出IT圈！\\n描述:【视频配套籽料+问题解答请看”平论区置顶”自取哦】\\r\\n视频制作不易，如果视频对你有用的话请一键三连【长按点赞】支持一下up哦，拜托，这对我真的很重要！\\n播放量:442043\\n弹幕数:1563\\n收藏数:42232\\n标签:计算机,程序员,人工智能,AI,深度学习,计算机技术,LLM,AI大模型,ChatGPT,大语言模型\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:马士兵官方账号\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113696558814120\\n标题:AI大模型全套教程（LLM+RAG+Langchain+国产大模型ChatGLM-4+NLP新模型Transformer+DeepSeek部署）-马士兵\\n描述:具备Al大模型应用开发技能的专业人才往往能够获得更具竞争力，为未来的职业发展带来更高的薪资回报\\n播放量:320333\\n弹幕数:1161\\n收藏数:23445\\n标签:计算机,程序员,编程,公开课,人工智能,机器学习,深度学习,AI大模型,ChatGPT,大语言模型 (LLM)\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:大模型教程K\\n分类:野生技能协会\\n视频链接:http://www.bilibili.com/video/av114216518293976\\n标题:【速成版】目前B站最全最细的大模型零基础全套教程，2025最新版，包含所有干货！七天就能从小白到大神！少走99%的弯路！存下吧！很难找全的！大模型|LLM\\n描述:【视频配套籽料、配套教程视频+问题解答请看 ”置顶平论” 自取哦】\\n本套教程从零开始讲解，手把手教学，包含基础、进阶、实战\\n无论是新手小白，还是有一定编码经验的选手，皆可学习\\n如果视频对你有用的话请 一键三连【长按点赞】支持一下UP哦，拜托，这对我真的很重要！\\n播放量:5711\\n弹幕数:130\\n收藏数:129\\n标签:互联网,人工智能,AI,RAG,AGI,大模型,Agent,大语言模型,大模型应用,大模型学习\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:大模型入门教程\\n分类:野生技能协会\\n视频链接:http://www.bilibili.com/video/av114143067638011\\n标题:【全368集】花2w买的大模型入门教程！我付费，你白嫖，全程干货无废话！全网最详细的大模型入门教程，存下吧，比啃书强太多！\\n描述:教程持续更新中，感谢各位观众老爷们的观看！\\n包含【视频配套籽料、学习笔记、实战案例、电子书+问题解答】等！\\n您的三连是我更新的动力！\\n播放量:7464\\n弹幕数:136\\n收藏数:337\\n标签:绘画,入门教程,学习,AI,生活记录,ai,大模型,大模型学习,大模型入门,大模型教程\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:林亦LYi\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av1750586968\\n标题:从零开始学习大语言模型（一）\\n描述:从零开始学习大语言模型（一）\\n播放量:477023\\n弹幕数:742\\n收藏数:26676\\n标签:教程,人工智能,机器学习,神经网络,大模型,反向传播,超参数,损失函数,大语言模型,知识前沿派对\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:盘古-大模型\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av114222776256107\\n标题:翻遍B站！这绝对是B站最全最详细的大模型RAG实战教程！从工作原理-向量数据库-知识库搭建-索引增强全套干货教程，无废话！学完少走99%的弯路！存下吧，很难找全\\n描述:【视频配套籽料、学习路线、GitHub项目、实战案例集、电子书+问题解答请看 ”置顶平论” 自取哦】\\n本套教程从零开始讲解，无论是小白，还是有一定编码经验的选手，皆可学习\\n如果视频对你有用的话请 一键三连【长按点赞】支持一下UP哦，拜托，这对我真的很重要！\\n播放量:2800\\n弹幕数:324\\n收藏数:1125\\n标签:程序员,RAG,工作原理,LLM,知识库搭建,AI大模型,向量数据库,大模型RAG,RAG实战,RAG索引增强\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:AI大模型全栈\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113876444257825\\n标题:2025吃透LangChain大模型全套教程（LLM+RAG+OpenAI+Agent）通俗易懂，学完即就业!拿走不谢，学不会我退出IT圈！！！\\n描述:【视频配套籽料+问题解答请看”平论区置顶”自取哦】\\r\\n视频制作不易，如果视频对你有用的话请一键三连【长按点赞】支持一下up哦，拜托，这对我真的很重要！\\n播放量:149573\\n弹幕数:1541\\n收藏数:8253\\n标签:计算机,科技,程序员,AI,RAG,OpenAI,Agent,LLM,AI大模型,LangChain\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:新石器公园\\n分类:科学科普\\n视频链接:http://www.bilibili.com/video/av114081746919054\\n标题:万字科普DeepSeek R1底层原理，DeepSeek是从0到1的创新吗？\\n描述:DeepSeek的底层原理是什么？\\n为什么DeepSeek R1能够震动世界？\\nDeepSeek到底在什么方面实现了突破？\\n大模型的发展方向会发生变化吗？\\n本视频由浅入深的为你解释DeepSeek R1的技术路线，让你明白DeepSeek和OpenAI的差别到底在哪里？为什么说DeepSeek的创新是开宗立派的。\\n播放量:341756\\n弹幕数:1814\\n收藏数:14477\\n标签:科学,科普,计算机,知识,人工智能,AI,OpenAI,大模型,万物研究所,DeepSeek,格致科学季有奖征稿\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:吴恩达深度学习\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113662232692793\\n标题:【吴恩达】2024年公认最好的【LLM大模型】教程！大模型入门到进阶，一套全解决！附带课件代码-Generative AI for Everyone\\n描述:由AI先驱Andrew Ng指导，《面向每个人的生成式AI》课程提供他独特的视角，以帮助您和您的工作实现生成式AI的能力。Andrew将引导您了解生成式AI的工作原理以及它可以（和不能）做什么。课程包括实践练习，您将学习如何使用生成式AI来帮助日常工作，并获得有效的提示工程技巧，同时学习如何超越提示，实现更高级的AI应用。\\n播放量:126210\\n弹幕数:349\\n收藏数:8877\\n标签:程序员,编程,人工智能,AI,RAG,吴恩达,大模型,生成式AI,ChatGPT,大模型微调\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:吴恩达大模型\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113869917855493\\n标题:(超爽中英!) 2024公认最全的【吴恩达大模型LLM】系列教程！附代码_LangChain_微调ChatGPT提示词_RAG模型应用_agent_生成式AI\\n描述:视频来源:DeepLearning.Al\\n翻译来源:宝玉老师/GPT中英字幕老师\\n持续更新中!记得收藏哦~求三连支持!\\n播放量:69744\\n弹幕数:6\\n收藏数:5520\\n标签:科学,科技,人工智能,机器学习,计算机技术,大模型,LLM,生成式AI,吴恩达大模型,色度学习\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:毛玉仁\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av113750984168088\\n标题:【浙江大学-大模型原理与技术】1-0 序言\\n描述:《大模型原理与技术》视频课程将包含：1. 语言模型基础；2. 大语言模型架构；3. Prompt工程；4. 参数高效微调；5. 模型编辑；6. 检索增强生成，共计六个章节。本课程是2024学年冬学期我在浙江大学软件学院讲授的对应课程的实录，第一次录制课程，内容还很粗糙，里面还有一些口误或错误，恳请大家批评指正，我们也会根据大家的建议发布勘误表。本课程的内容基于浙江大学的开源教材《大模型基础》。大家可以从Github链接 https://github.com/ZJU-LLMs/Foundations-of-\\n播放量:82640\\n弹幕数:62\\n收藏数:9461\\n标签:学习,人工智能,大模型,大语言模型\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:设计师Omega\\n分类:科学科普\\n视频链接:http://www.bilibili.com/video/av533792936\\n标题:【科普】如何感性的理解AI大模型是什么\\n描述:通过几个例子来实现感性的理解AI大模型是什么~清晰易懂，求个赞~\\n播放量:84723\\n弹幕数:134\\n收藏数:3469\\n标签:科普,人工智能,AI,OpenAI,大模型,AI大模型,chatGPT,分享我的专业知识,万物研究所·奖学金计划,AI agent,longchain\\n发布曰期:0\\n评论:\", \"类型:video\\n作者:大模型布道者\\n分类:计算机技术\\n视频链接:http://www.bilibili.com/video/av114220846809887\\n标题:大模型时代人工智能系统学习指南：从核心原理、多模态技术到实战路线全解析（入门基础+保姆级规划）\\n描述:\\n播放量:2761\\n弹幕数:18\\n收藏数:35\\n标签:人工智能,机器学习,深度学习,计算机技术,AI大模型,大模型入门,llama3,大模型学习路线,llama3部署,llama3教程\\n发布曰期:0\\n评论:\"]",
        "input": "请帮我梳理下热门视频的信息描述"
    })
    print(final_answer)