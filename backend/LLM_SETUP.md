# LLM集成配置指南

## 概述

本项目现在支持集成本地部署的开源LLM模型，提供更智能的文本分析能力。支持多种LLM提供商，包括Ollama、OpenAI和本地模型。

## 支持的LLM提供商

### 1. Ollama（推荐）

Ollama是一个轻量级的本地LLM部署工具，支持多种开源模型。

#### 安装步骤

1. **安装Ollama**
   ```bash
   # macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # 下载安装包：https://ollama.ai/download
   ```

2. **启动Ollama服务**
   ```bash
   ollama serve
   ```

3. **下载模型**
   ```bash
   # 推荐模型（中文支持好）
   ollama pull qwen2.5:7b
   
   # 或者使用其他模型
   ollama pull llama3.1:8b
   ollama pull chatglm3:6b
   ```

4. **配置环境变量**
   创建 `.env` 文件：
   ```bash
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen2.5:7b
   ```

### 2. OpenAI（备用）

如果需要使用OpenAI的API服务：

1. **获取API密钥**
   - 访问 https://platform.openai.com/
   - 创建API密钥

2. **配置环境变量**
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### 3. 本地模型（开发中）

支持使用transformers库加载本地模型：

1. **安装依赖**
   ```bash
   pip install transformers torch sentence-transformers
   ```

2. **配置环境变量**
   ```bash
   LLM_PROVIDER=local
   LOCAL_MODEL_PATH=./models
   LOCAL_MODEL_NAME=chatglm3-6b
   ```

## 环境配置

在 `backend` 目录下创建 `.env` 文件：

```bash
# 基础配置
SECRET_KEY=your-secret-key-here-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this-in-production

# 数据库配置
DATABASE_URL=sqlite:///text_analysis.db

# LLM配置
LLM_PROVIDER=ollama  # ollama, openai, local, none

# Ollama配置（推荐）
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# OpenAI配置（备用）
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# 本地模型配置
LOCAL_MODEL_PATH=./models
LOCAL_MODEL_NAME=chatglm3-6b

# 分析配置
MAX_TEXT_LENGTH=10000
DEFAULT_SUMMARY_LENGTH=200
DEFAULT_KEYWORDS_COUNT=10
```

## 新功能

### 1. LLM专用API

- `POST /api/llm/sentiment` - LLM情感分析
- `POST /api/llm/keywords` - LLM关键词提取
- `POST /api/llm/summary` - LLM文本摘要
- `POST /api/llm/comprehensive` - LLM综合分析

### 2. 混合分析

- `POST /api/hybrid/analysis` - 结合传统方法和LLM的分析

### 3. 健康检查

- `GET /api/llm/health` - LLM服务状态检查

## 使用示例

### 情感分析

```bash
curl -X POST http://localhost:5001/api/llm/sentiment \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "今天天气很好，我很开心！"}'
```

### 综合分析

```bash
curl -X POST http://localhost:5001/api/hybrid/analysis \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "这是一段需要分析的文本内容..."}'
```

## 性能优化建议

### 1. 模型选择

- **qwen2.5:7b**: 中文支持好，性能平衡，推荐
- **llama3.1:8b**: 英文能力强，通用性好
- **chatglm3:6b**: 中文对话能力强

### 2. 硬件要求

- **最低配置**: 8GB RAM, 4核CPU
- **推荐配置**: 16GB RAM, 8核CPU
- **GPU加速**: 支持CUDA的GPU可以显著提升性能

### 3. 部署建议

- 生产环境建议使用GPU加速
- 可以部署多个模型实例进行负载均衡
- 考虑使用Redis等缓存LLM响应结果

## 故障排除

### 1. Ollama连接失败

```bash
# 检查Ollama服务状态
curl http://localhost:11434/api/tags

# 重启Ollama服务
ollama serve
```

### 2. 模型下载失败

```bash
# 清理缓存
ollama rm qwen2.5:7b
ollama pull qwen2.5:7b
```

### 3. 内存不足

- 使用更小的模型（如3B版本）
- 增加系统内存
- 使用GPU加速

## 开发计划

- [ ] 支持更多本地模型（ChatGLM、Baichuan等）
- [ ] 模型性能监控和自动切换
- [ ] 批量分析优化
- [ ] 模型微调支持
- [ ] 多语言支持增强

## 贡献

欢迎提交Issue和Pull Request来改进LLM集成功能！
