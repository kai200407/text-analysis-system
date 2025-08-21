#!/bin/bash

echo "🚀 智能文本分析系统 - LLM集成启动脚本"
echo "=========================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查Docker服务是否运行
echo "🔍 检查Docker服务状态..."
if ! docker info &> /dev/null; then
    echo "⚠️  Docker服务未运行，尝试启动Docker..."
    
    # 尝试启动Docker Desktop (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🍎 检测到macOS，尝试启动Docker Desktop..."
        
        # 检查Docker Desktop是否已安装
        if [ -d "/Applications/Docker.app" ]; then
            echo "🚀 启动Docker Desktop..."
            open -a Docker
            
            # 等待Docker启动
            echo "⏳ 等待Docker服务启动..."
            for i in {1..30}; do
                if docker info &> /dev/null; then
                    echo "✅ Docker服务启动成功！"
                    break
                fi
                echo "⏳ 等待中... ($i/30)"
                sleep 2
            done
            
            # 最终检查
            if ! docker info &> /dev/null; then
                echo "❌ Docker服务启动失败，请手动启动Docker Desktop"
                echo "💡 提示：打开Applications文件夹，双击Docker.app启动"
                exit 1
            fi
        else
            echo "❌ Docker Desktop未安装，请先安装Docker Desktop"
            echo "💡 提示：运行 brew install --cask docker 安装"
            exit 1
        fi
    else
        # Linux系统尝试启动Docker服务
        echo "🐧 检测到Linux系统，尝试启动Docker服务..."
        if command -v systemctl &> /dev/null; then
            sudo systemctl start docker
            sleep 3
        elif command -v service &> /dev/null; then
            sudo service docker start
            sleep 3
        else
            echo "❌ 无法启动Docker服务，请手动启动"
            exit 1
        fi
        
        # 检查是否启动成功
        if ! docker info &> /dev/null; then
            echo "❌ Docker服务启动失败，请手动启动"
            exit 1
        fi
    fi
else
    echo "✅ Docker服务正在运行"
fi

echo "✅ Docker环境检查通过"

# 启动Ollama服务
echo "🐳 启动Ollama服务..."
docker-compose -f docker-compose.ollama.yml up -d ollama

# 等待Ollama服务启动
echo "⏳ 等待Ollama服务启动..."
sleep 10

# 检查Ollama服务状态
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama服务启动成功"
else
    echo "❌ Ollama服务启动失败，请检查日志"
    docker-compose -f docker-compose.ollama.yml logs ollama
    exit 1
fi

# 下载推荐模型
echo "📥 下载推荐模型 qwen2.5:7b..."
docker exec ollama ollama pull qwen2.5:7b

if [ $? -eq 0 ]; then
    echo "✅ 模型下载成功"
else
    echo "⚠️  模型下载失败，请手动下载：docker exec ollama ollama pull qwen2.5:7b"
fi

# 创建环境配置文件
echo "⚙️  创建环境配置文件..."
cat > backend/.env << EOF
# LLM配置
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# 基础配置
SECRET_KEY=your-secret-key-here-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this-in-production

# 数据库配置
DATABASE_URL=sqlite:///text_analysis.db

# 分析配置
MAX_TEXT_LENGTH=10000
DEFAULT_SUMMARY_LENGTH=200
DEFAULT_KEYWORDS_COUNT=10
EOF

echo "✅ 环境配置文件创建成功"

# 安装Python依赖
echo "📦 安装Python依赖..."
cd backend
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "❌ Python依赖安装失败，请手动安装"
fi

echo ""
echo "🎉 LLM集成配置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 启动后端服务：cd backend && python3 app.py"
echo "2. 启动前端服务：cd frontend && npm start"
echo "3. 测试LLM功能：访问 http://localhost:3000"
echo ""
echo "🔧 管理Ollama服务："
echo "- 查看日志：docker-compose -f docker-compose.ollama.yml logs ollama"
echo "- 停止服务：docker-compose -f docker-compose.ollama.yml down"
echo "- 重启服务：docker-compose -f docker-compose.ollama.yml restart ollama"
echo ""
echo "📚 更多信息请查看：backend/LLM_SETUP.md"
