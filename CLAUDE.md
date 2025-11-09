# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 Python 的内存管理 MCP (Model Context Protocol) 项目，使用 LangChain 框架。项目名称为 `hc-mem`，目前处于早期开发阶段 (v0.1.0)。

## 项目结构

```
├── main.py                    # 主入口文件
├── src/
│   ├── app/                  # 应用层
│   │   └── demo/            # 演示模块
│   │       └── langchain-memory.py  # LangChain 内存演示
│   └── inf/                 # 基础设施层
│       └── env/            # 环境配置
│           └── env_conf.py  # 环境配置文件
├── pyproject.toml           # 项目配置文件
└── README.md               # 项目说明文档
```

## 开发环境设置

### 依赖管理
项目使用 `uv` 作为包管理器，Python 版本要求 >= 3.12

主要依赖：
- `langchain>=1.0.5` - LangChain 框架

### 常用命令

```bash
# 安装依赖
uv sync

# 运行主程序
uv run python main.py

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

## 架构说明

项目采用分层架构：

- **应用层 (src/app/)**: 包含业务逻辑和演示代码
  - `demo/` 目录下的 `langchain-memory.py` 用于演示 LangChain 内存功能
- **基础设施层 (src/inf/)**: 包含环境配置等基础设施组件
  - `env/env_conf.py` 处理环境配置

## 开发注意事项

1. 项目目前处于初始化阶段，大部分文件为空
2. 使用 LangChain 框架进行内存管理相关开发
3. 遵循分层架构原则，业务逻辑放在 app 层，基础设施放在 inf 层