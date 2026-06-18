# 🍳 AI 私人厨师 | Personal Chief

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.137+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.3+-orange.svg)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于 **LangChain + LangGraph** 构建的智能食谱推荐 Agent。上传食材图片或描述现有食材，由大模型驱动的 Agent 自动识别食材、联网检索菜谱，并生成个性化烹饪建议。

---

## ✨ 功能特性

- **多模态食材识别**：支持上传图片（通过 GPT-4V / 通义千问视觉能力）或文字描述食材
- **Agent 自主决策**：基于 LangGraph 编排 LLM 推理 + 工具调用的循环工作流，Agent 自主判断何时搜索、何时追问
- **联网菜谱检索**：封装 Tavily Search 为自定义 LangChain Tool，实时搜索网络菜谱
- **智能推荐排序**：从营养价值与制作难度两个维度对菜谱量化打分，简单且营养的优先推荐
- **记忆持久化**：采用 SQLite 存储对话历史与用户偏好，支持跨会话上下文保持
- **流式输出**：基于 SSE（Server-Sent Events）的实时流式响应，打字机效果逐字输出
- **会话管理**：支持多会话独立上下文，可查询历史消息、清空会话

---

## 🛠 技术栈

| 层级 | 技术 |
|---|---|
| **Agent 框架** | LangChain + LangGraph |
| **后端** | FastAPI + Uvicorn |
| **大模型** | 通义千问 3.5 Plus（阿里百炼 API，OpenAI 兼容模式） |
| **网络搜索** | Tavily Search API |
| **记忆持久化** | SQLite（LangGraph SQLite Checkpointer） |
| **图片上传** | 阿里云 OSS |
| **前端** | Next.js 静态导出 + Tailwind CSS（霓虹深色主题） |
| **依赖管理** | uv |
| **可观测性** | LangSmith（可选） |

---

## 📁 项目结构

```
PythonProject1/
├── .env                          # 环境变量（需自行创建）
├── pyproject.toml                # 项目依赖
├── langgraph.json                # LangGraph 配置
├── app/
│   ├── main.py                   # FastAPI 应用入口
│   ├── agents/
│   │   └── Recipe_Search.py      # 🔥 Agent 核心：工具定义 + 工作流 + System Prompt
│   ├── api/v1/
│   │   ├── chat.py               # 对话 API 路由（流式 + 历史 + 清空）
│   │   └── oss.py                # OSS 图片上传预签名 API
│   ├── models/
│   │   └── schemas.py            # Pydantic 请求/响应模型
│   ├── common/
│   │   └── logger.py             # 日志配置
│   └── static/                   # 前端静态资源（Next.js 构建产物）
├── Chapter01/                    # 学习笔记：OpenAI SDK 示例
├── Chapter02/                    # 学习笔记：LangChain 基础
└── db/
    └── Recipes.db                # SQLite 数据库（Agent 对话持久化）
```

---

## 🚀 快速开始

### 前置条件

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-chef-agent.git
cd ai-chef-agent
```

### 2. 安装依赖

```bash
uv sync
```

或使用 pip：

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件，参考以下模板：

```env
# ========== 必填：模型 API ==========
# 阿里百炼 API Key（通义千问模型）
DASHSCOPE_API_KEY=sk-your-dashscope-api-key

# 阿里百炼 API 端点（通常不需要改）
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# ========== 必填：网络搜索 ==========
# Tavily Search API Key（用于菜谱联网检索）
# 免费配额每天 1000 次：https://app.tavily.com/
TAVILY_API_KEY=tvly-dev-your-tavily-key

# ========== 可选：图片上传 (OSS) ==========
# 如果不使用图片上传功能，以下三个可不填
OSS_ACCESS_KEY_ID=LTAI5txxxxxxxxxxxx
OSS_ACCESS_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
OSS_BUCKET=your-bucket-name

# ========== 可选：LangSmith 追踪 ==========
# 用于调试 Agent 执行过程，不需要可删除以下三行
LANGSMITH_API_KEY=lsv2_pt_your-langsmith-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=lc-recipe
```

### 4. 启动服务

```bash
python -m app.main
```

或：

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

启动后访问：
- **前端界面**：http://127.0.0.1:8001
- **API 文档 (Swagger)**：http://127.0.0.1:8001/docs

---

## 📡 API 接口

### 流式对话（核心接口）

```
POST /api/v1/chat/stream
Content-Type: application/json
```

**请求体：**

```json
{
  "message": "冰箱里有鸡蛋、西红柿和青椒，能做什么菜？",
  "image_url": "https://your-oss-bucket.oss-cn-beijing.aliyuncs.com/fridge.jpg",
  "thread_id": "session_abc123"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `message` | string | 是 | 用户的文本消息 |
| `image_url` | string | 否 | OSS 图片 URL，为空则只走文本识别 |
| `thread_id` | string | 是 | 会话 ID，同一会话保持上下文 |

**响应：** SSE 流式输出，`Content-Type: text/event-stream`

### 获取历史消息

```
GET /api/v1/chat/messages?thread_id=session_abc123
```

### 清空会话

```
DELETE /api/v1/chat/messages?thread_id=session_abc123
```

### 获取 OSS 上传预签名 URL

```
GET /api/v1/oss/presign?filename=fridge.jpg
```

返回预签名上传链接，前端可直接 PUT 上传图片到 OSS。

---

## 🔧 自定义修改指南

### 更换大模型

编辑 `app/agents/Recipe_Search.py`：

```python
# 第 42 行附近，修改 model_name 和 provider
self.model = init_chat_model(
    model="你的模型名",       # 如 deepseek-chat / gpt-4o
    provider="openai",        # 兼容 OpenAI 协议的 provider
    api_key=os.getenv("你的API_KEY环境变量"),
    base_url=os.getenv("你的BASE_URL环境变量"),
)
```

同步在 `.env` 中添加对应的 `API_KEY` 和 `BASE_URL`。

### 自定义 System Prompt

编辑 `app/agents/Recipe_Search.py` 中 `self.system_prompt` 变量的文本内容，调整 Agent 的行为风格、推荐偏好或输出格式。

### 调整搜索工具

搜索参数在 `app/agents/Recipe_Search.py` 的 `websearch` 函数中：

```python
response = self.search_client.search(
    query,
    max_results=5,      # 返回结果数
    topic="general",    # general / news
)
```

### 更换记忆后端

当前使用 SQLite（`SqliteSaver`），数据库文件位于 `db/Recipes.db`。如需切换为 Redis 或 Postgres，可替换 `langgraph-checkpoint-sqlite` 为对应的 checkpointer 包，并修改 `Recipe_Search.py` 中的 checkpointer 初始化代码。

### 前端样式

前端为 Next.js 静态导出产物，位于 `app/static/`。如需二次修改：

1. CSS 主题变量在 `app/static/_next/static/chunks/c13dc4b283c0c8d9.css` 的 `:root` 中
2. HTML 结构在 `app/static/index.html` 中（内联 Tailwind 类名）
3. 修改后**务必强制刷新浏览器**（`Ctrl+Shift+R`），因为 CSS 文件名未变，浏览器会缓存旧版本

---

## 📸 界面预览

> （可在此处放置项目截图）

---

## 📝 License

MIT

---

## 🙏 致谢

- [LangChain](https://www.langchain.com/) — Agent 框架
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Agent 编排引擎
- [Tavily](https://tavily.com/) — AI 搜索引擎
- [通义千问](https://tongyi.aliyun.com/) — 大语言模型
- [Claude Code](https://claude.ai/) — 前端样式 AI 辅助优化
*（内容由AI生成，仅供参考）*
