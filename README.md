# BiliAgint

BiliAgint 是一个基于大模型的 Bilibili 智能检索与分析系统，支持 B站 视频推荐查询、字幕智能提取与分析等多种 AI 能力，适合做数据分析、内容理解、自动推荐等场景。项目采用 FastAPI 作为后端，Streamlit 作为前端交互，灵活可扩展。

## 主要功能

- **Bilibili 视频推荐智能查询**：输入任意问题，基于多轮推理与大模型能力返回相关推荐视频及分析结果。
- **Bilibili 字幕提取与分析**：自动提取视频字幕，支持 AI 智能分析与摘要、对话式问答。
- **个性化推荐与扩展**：可集成更多 B 站数据相关功能，支持插件化扩展。
- **前后端分离设计**：FastAPI+Streamlit，便于本地部署和二次开发。

## 项目结构

```
app/
  ├── Bili视频查询.py           # Streamlit 页面：视频推荐对话
  ├── server.py                # FastAPI 后端服务主入口
  ├── utils.py                 # 工作流与大模型组件封装
  └── pages/
      └── Bili字幕提取.py      # Streamlit 页面：字幕提取与分析
bili_server/
  ├── document_loader.py, edges.py, generate_chain.py, graph.py, grader.py, nodes.py 等
bilibili_tools/
  ├── subtitle_fetcher.py      # 字幕抓取工具
  ├── subtitle_analysis.py     # 字幕智能分析
  ├── chat_bot.py              # AI 对话
```

## 快速开始

### 依赖安装

```bash
pip install -r requirements.txt
```

### 环境变量

请在根目录下创建 `.env` 文件，配置你的 OpenAI 或其他 LLM key 和相关模型参数，例如：

```
OPENAI_API_KEY=你的apikey
model=gpt-3.5-turbo
```

### 启动后端服务

```bash
cd app
python server.py
```

默认监听在 `localhost:8088`，提供 `/biliagent_chat` 接口。

### 启动前端页面

在 `app/` 或根目录下启动 Streamlit：

```bash
streamlit run app/Bili视频查询.py
# 或
streamlit run app/pages/Bili字幕提取.py
```

## 使用说明

- 访问 Streamlit 页面，体验 B 站视频智能检索、字幕提取与分析等功能。
- 后端 API 支持自定义接入，可集成至更多应用场景。

## 贡献与开发

欢迎 issue 与 PR！如需添加新功能或自定义模型，请参考 `app/utils.py` 与 `bili_server/` 下的模块设计。

## License

本项目暂未设置开源许可证，仅供学习与研究使用。

---

> 项目地址: [https://github.com/Suizz-z/BiliAgint](https://github.com/Suizz-z/BiliAgint)
>  
> 作者: [Suizz-z](https://github.com/Suizz-z)
