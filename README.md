# 智能文本分析系统 - LLM增强版

## 项目简介

本项目是一个基于 Web 的智能文本分析系统，**现已集成本地部署的开源LLM模型**，提供更智能的文本分析能力。系统采用前后端分离架构，前端使用 React.js，后端使用 Python Flask，数据库使用 SQLite，并支持多种LLM提供商。

## 🚀 新功能特性

### LLM集成功能
- **智能文本分析**：使用本地部署的开源LLM模型进行分析
- **多模型支持**：支持Ollama、OpenAI、本地模型等多种提供商
- **混合分析**：结合传统方法和LLM的混合分析模式
- **智能提示词**：自动构建优化的分析提示词
- **结果对比**：传统方法与LLM方法的分析结果对比

### 原有功能增强
- 文本情感分析：支持LLM和传统方法
- 关键词提取：智能关键词提取和权重分析
- 文本摘要生成：基于LLM的智能摘要生成
- 文本相似度计算：深度语义相似度分析
- 用户管理：用户注册、登录、个人中心
- 历史记录：保存用户的分析历史

## 技术栈

- 前端：React.js + Ant Design
- 后端：Python Flask + SQLAlchemy + LLM集成
- 数据库：SQLite
- 文本分析：jieba、snownlp、sklearn + 开源LLM
- LLM支持：Ollama、OpenAI、本地模型
- 部署：Docker + Docker Compose

## 项目结构

```
text-analysis-system/
├── frontend/          # 前端代码
├── backend/           # 后端代码
├── database/          # 数据库文件
├── docs/             # 文档
└── docker-compose.yml # Docker配置·
```

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd text

# 2. 一键启动LLM服务
./start_llm.sh

# 3. 启动后端服务
cd backend && python3 app.py

# 4. 启动前端服务
cd frontend && npm start

# 5. 访问系统
open http://localhost:3000
```

### 方式二：手动配置

```bash
# 1. 启动Ollama服务
docker-compose -f docker-compose.ollama.yml up -d

# 2. 下载模型
docker exec ollama ollama pull qwen2.5:7b

# 3. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件配置LLM参数

# 4. 安装依赖
cd backend && pip install -r requirements.txt

# 5. 启动服务
python3 app.py
```

### 系统要求

- **最低配置**: 8GB RAM, 4核CPU
- **推荐配置**: 16GB RAM, 8核CPU  
- **GPU加速**: 支持CUDA的GPU（可选）
- **存储空间**: 至少10GB可用空间

## 📚 详细文档

- [LLM集成配置指南](backend/LLM_SETUP.md) - 详细的LLM配置说明
- [API文档](backend/README.md) - 后端API接口文档
- [前端开发指南](frontend/README.md) - 前端开发说明

## 🧪 测试

```bash
# 测试LLM功能
python3 test_llm.py

# 测试传统功能
cd backend && python3 -m pytest tests/
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_PROVIDER` | LLM提供商 | `ollama` |
| `OLLAMA_MODEL` | Ollama模型名称 | `qwen2.5:7b` |
| `OLLAMA_BASE_URL` | Ollama服务地址 | `http://localhost:11434` |

### 支持的模型

- **qwen2.5:7b**: 中文支持好，性能平衡（推荐）
- **llama3.1:8b**: 英文能力强，通用性好
- **chatglm3:6b**: 中文对话能力强

## 🚀 性能优化

- 使用GPU加速可显著提升分析速度
- 支持模型缓存和结果缓存
- 可配置分析超时和重试机制

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 开发团队

- 开发者：[您的姓名]
- 指导教师：[教师姓名]
- 完成时间：2024 年
