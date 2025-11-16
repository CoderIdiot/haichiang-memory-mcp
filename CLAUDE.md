# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

`hc-mem` 是一个基于 Python 的内存管理 MCP (Model Context Protocol) 项目，使用 LangChain 框架和阿里云百炼平台。项目版本为 v0.1.0，主要提供向量嵌入服务和对话功能，支持多 LLM 供应商集成。

## 核心架构

### 分层架构设计
- **应用层 (`src/app/`)**: 包含业务逻辑、演示代码和 LangChain 研究
- **基础设施层 (`src/inf/`)**: 包含环境配置、LLM 客户端等基础设施组件
- **全局配置**: 基于 Pydantic 的类型安全配置系统 (`G_Settings`)

### 关键组件
- **QwenLLMClient**: 阿里云百炼向量嵌入服务
- **DeepSeekLLMClient**: DeepSeek 对话模型客户端
- **LangChain 集成**: 基于 LangGraph 的内存存储和语义搜索
- **配置系统**: 环境变量驱动的类型安全配置管理

## 开发环境设置

### 依赖管理
项目使用 `uv` 作为包管理器，Python 版本要求 >= 3.12

核心依赖：
- `langchain>=1.0.5` - LangChain 框架
- `openai>=2.8.0` - OpenAI 兼容客户端
- `pydantic>=2.0.0` - 数据验证
- `pydantic-settings>=2.0.0` - 设置管理

### 必要的环境变量配置
```env
# 阿里云百炼 API (必需)
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# DeepSeek API (可选)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1
```

### 常用开发命令

```bash
# 安装依赖
uv sync

# 运行主程序
uv run python main.py

# 运行 LangChain 内存演示
uv run python src/app/lang_chain_study/langchain-memory.py

# 测试 LLM 客户端
uv run python src/inf/llm/qwen.py
uv run python src/inf/llm/deepseek.py

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
```

## 代码结构和模式

### 配置系统 (`src/inf/env/env_conf.py`)
全局 `G_Settings` 类管理所有配置项，支持：
- 环境变量自动加载和别名映射
- 类型验证和默认值设置
- API Key 掩码显示保护

### LLM 客户端架构
- **统一接口**: 基于 OpenAI 兼容 API
- **延迟初始化**: 客户端实例按需创建
- **批量处理**: 支持向量嵌入的批量生成
- **流式响应**: 支持对话的流式输出

### LangChain 内存管理
- 使用 `InMemoryStore` 进行内存存储
- 支持用户和应用上下文隔离
- 基于向量嵌入的语义搜索和内容检索

## 开发规范

### 代码风格
1. 注释内容使用中文，标点符号使用英文
2. 函数和类必须使用类型注解
3. 遵循 PEP 8 代码风格
4. 错误信息使用中文描述

### 架构原则
1. 分层架构：业务逻辑与基础设施分离
2. 配置驱动：通过环境变量管理配置
3. 类型安全：全面使用 Pydantic 数据验证
4. 工厂模式：客户端实例通过工厂函数创建

### 导入约定
```python
# 配置和日志
from conf import logger
from src.inf.env.env_conf import G_Settings

# LLM 客户端
from src.inf.llm.qwen import G_QwenLLMClient, create_qwen_client
from src.inf.llm.deepseek import G_DeepSeekLLMClient, create_deepseek_client
```
