import requests
import json
import logging
from typing import Dict, Any, Optional
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """LLM服务类，支持多种提供商"""
    
    def __init__(self):
        self.config = Config()
        self.provider = self.config.LLM_PROVIDER
        
    def analyze_text(self, text: str, analysis_type: str, **kwargs) -> Dict[str, Any]:
        """统一的文本分析接口"""
        try:
            if self.provider == 'ollama':
                return self._analyze_with_ollama(text, analysis_type, **kwargs)
            elif self.provider == 'openai':
                return self._analyze_with_openai(text, analysis_type, **kwargs)
            elif self.provider == 'local':
                return self._analyze_with_local_model(text, analysis_type, **kwargs)
            else:
                raise ValueError(f"不支持的LLM提供商: {self.provider}")
        except Exception as e:
            logger.error(f"LLM分析失败: {str(e)}")
            return {"error": f"LLM分析失败: {str(e)}"}
    
    def _analyze_with_ollama(self, text: str, analysis_type: str, **kwargs) -> Dict[str, Any]:
        """使用Ollama进行分析"""
        try:
            # 构建提示词
            prompt = self._build_prompt(text, analysis_type, **kwargs)
            
            # 调用Ollama API
            response = requests.post(
                f"{self.config.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.config.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ollama_response(result, analysis_type)
            else:
                logger.error(f"Ollama API调用失败: {response.status_code}")
                return {"error": f"Ollama API调用失败: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama请求异常: {str(e)}")
            return {"error": f"Ollama请求异常: {str(e)}"}
    
    def _analyze_with_openai(self, text: str, analysis_type: str, **kwargs) -> Dict[str, Any]:
        """使用OpenAI进行分析"""
        if not self.config.OPENAI_API_KEY:
            return {"error": "OpenAI API密钥未配置"}
        
        try:
            # 构建提示词
            prompt = self._build_prompt(text, analysis_type, **kwargs)
            
            # 调用OpenAI API
            response = requests.post(
                f"{self.config.OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.config.OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的文本分析助手，请按照要求分析文本。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_openai_response(result, analysis_type)
            else:
                logger.error(f"OpenAI API调用失败: {response.status_code}")
                return {"error": f"OpenAI API调用失败: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI请求异常: {str(e)}")
            return {"error": f"OpenAI请求异常: {str(e)}"}
    
    def _analyze_with_local_model(self, text: str, analysis_type: str, **kwargs) -> Dict[str, Any]:
        """使用本地模型进行分析"""
        # 这里可以集成transformers库来加载本地模型
        # 为了简化，暂时返回错误信息
        return {"error": "本地模型集成功能开发中，请使用Ollama或OpenAI"}
    
    def _build_prompt(self, text: str, analysis_type: str, **kwargs) -> str:
        """构建分析提示词"""
        base_prompt = f"请分析以下文本，要求：\n\n文本内容：{text}\n\n"
        
        if analysis_type == 'sentiment':
            prompt = base_prompt + """
请进行情感分析，分析结果请以JSON格式返回，包含以下字段：
- sentiment: 情感倾向（积极/消极/中性）
- score: 情感得分（0-1之间的小数）
- confidence: 置信度（高/中/低）
- reasoning: 分析理由（简要说明）

请确保返回的是有效的JSON格式。"""
            
        elif analysis_type == 'keywords':
            top_k = kwargs.get('top_k', 10)
            prompt = base_prompt + f"""
请提取关键词，要求：
- 提取{top_k}个最重要的关键词
- 分析结果请以JSON格式返回，包含以下字段：
  - keywords: 关键词列表，每个关键词包含word和weight字段
  - reasoning: 提取理由（简要说明）

请确保返回的是有效的JSON格式。"""
            
        elif analysis_type == 'summary':
            max_length = kwargs.get('max_length', 200)
            prompt = base_prompt + f"""
请生成文本摘要，要求：
- 摘要长度控制在{max_length}字以内
- 保持原文的核心信息和逻辑结构
- 分析结果请以JSON格式返回，包含以下字段：
  - summary: 摘要内容
  - length: 摘要长度
  - original_length: 原文长度
  - compression_ratio: 压缩比
  - key_points: 关键要点列表

请确保返回的是有效的JSON格式。"""
            
        elif analysis_type == 'similarity':
            text2 = kwargs.get('text2', '')
            prompt = base_prompt + f"""
请分析两段文本的相似度，要求：
- 文本1: {text}
- 文本2: {text2}
- 分析结果请以JSON格式返回，包含以下字段：
  - similarity_score: 相似度得分（0-1之间的小数）
  - similarity_percentage: 相似度百分比
  - interpretation: 相似度解释（高度相似/中度相似/低度相似）
  - reasoning: 分析理由（简要说明）

请确保返回的是有效的JSON格式。"""
            
        else:
            prompt = base_prompt + "请进行通用文本分析。"
        
        return prompt
    
    def _parse_ollama_response(self, response: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """解析Ollama响应"""
        try:
            content = response.get('response', '')
            # 尝试提取JSON内容
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # 如果没有找到JSON，返回原始响应
                return {"raw_response": content, "analysis_type": analysis_type}
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return {"error": f"响应解析失败: {str(e)}", "raw_response": response.get('response', '')}
    
    def _parse_openai_response(self, response: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """解析OpenAI响应"""
        try:
            content = response['choices'][0]['message']['content']
            # 尝试提取JSON内容
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # 如果没有找到JSON，返回原始响应
                return {"raw_response": content, "analysis_type": analysis_type}
                
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"OpenAI响应解析失败: {str(e)}")
            return {"error": f"响应解析失败: {str(e)}", "raw_response": str(response)}
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            if self.provider == 'ollama':
                response = requests.get(f"{self.config.OLLAMA_BASE_URL}/api/tags", timeout=10)
                if response.status_code == 200:
                    return {"status": "healthy", "provider": "ollama", "models": response.json().get('models', [])}
                else:
                    return {"status": "unhealthy", "provider": "ollama", "error": f"HTTP {response.status_code}"}
            elif self.provider == 'openai':
                if not self.config.OPENAI_API_KEY:
                    return {"status": "unhealthy", "provider": "openai", "error": "API密钥未配置"}
                return {"status": "healthy", "provider": "openai"}
            else:
                return {"status": "unknown", "provider": self.provider}
                
        except Exception as e:
            return {"status": "error", "provider": self.provider, "error": str(e)}
