import jieba
import jieba.analyse
import numpy as np
from snownlp import SnowNLP
from typing import Dict, Any, Optional
from llm_service import LLMService
from config import Config

class EnhancedTextAnalyzer:
    """增强版文本分析器，集成LLM和传统方法"""
    
    def __init__(self):
        self.config = Config()
        self.llm_service = LLMService()
        self.use_llm = self.config.LLM_PROVIDER != 'none'
        
    def sentiment_analysis(self, text: str, use_llm: Optional[bool] = None) -> Dict[str, Any]:
        """情感分析 - 支持LLM和传统方法"""
        if use_llm is None:
            use_llm = self.use_llm
            
        if use_llm:
            # 使用LLM进行分析
            result = self.llm_service.analyze_text(text, 'sentiment')
            if 'error' not in result:
                return result
        
        # 回退到传统方法
        return self._traditional_sentiment_analysis(text)
    
    def extract_keywords(self, text: str, top_k: int = 10, use_llm: Optional[bool] = None) -> Dict[str, Any]:
        """关键词提取 - 支持LLM和传统方法"""
        if use_llm is None:
            use_llm = self.use_llm
            
        if use_llm:
            # 使用LLM进行分析
            result = self.llm_service.analyze_text(text, 'keywords', top_k=top_k)
            if 'error' not in result:
                return result
        
        # 回退到传统方法
        return self._traditional_keywords_extraction(text, top_k)
    
    def generate_summary(self, text: str, max_length: int = 200, use_llm: Optional[bool] = None) -> Dict[str, Any]:
        """文本摘要生成 - 支持LLM和传统方法"""
        if use_llm is None:
            use_llm = self.use_llm
            
        if use_llm:
            # 使用LLM进行分析
            result = self.llm_service.analyze_text(text, 'summary', max_length=max_length)
            if 'error' not in result:
                return result
        
        # 回退到传统方法
        return self._traditional_summary_generation(text, max_length)
    
    def calculate_similarity(self, text1: str, text2: str, use_llm: Optional[bool] = None) -> Dict[str, Any]:
        """计算文本相似度 - 支持LLM和传统方法"""
        if use_llm is None:
            use_llm = self.use_llm
            
        if use_llm:
            # 使用LLM进行分析
            result = self.llm_service.analyze_text(text1, 'similarity', text2=text2)
            if 'error' not in result:
                return result
        
        # 回退到传统方法
        return self._traditional_similarity_calculation(text1, text2)
    
    def advanced_analysis(self, text: str) -> Dict[str, Any]:
        """高级文本分析 - 结合多种方法"""
        try:
            # 基础分析
            sentiment = self.sentiment_analysis(text, use_llm=False)
            keywords = self.extract_keywords(text, use_llm=False)
            summary = self.generate_summary(text, use_llm=False)
            
            # 文本统计
            stats = self._calculate_text_stats(text)
            
            # 主题分析
            topics = self._extract_topics(text)
            
            return {
                "sentiment": sentiment,
                "keywords": keywords,
                "summary": summary,
                "statistics": stats,
                "topics": topics,
                "analysis_method": "traditional"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def llm_analysis(self, text: str, analysis_type: str = 'comprehensive', **kwargs) -> Dict[str, Any]:
        """纯LLM分析"""
        if not self.use_llm:
            return {"error": "LLM服务未启用"}
        
        try:
            if analysis_type == 'comprehensive':
                # 综合分析
                sentiment = self.llm_service.analyze_text(text, 'sentiment')
                keywords = self.llm_service.analyze_text(text, 'keywords', **kwargs)
                summary = self.llm_service.analyze_text(text, 'summary', **kwargs)
                
                return {
                    "sentiment": sentiment,
                    "keywords": keywords,
                    "summary": summary,
                    "analysis_method": "llm",
                    "provider": self.config.LLM_PROVIDER
                }
            else:
                # 单一分析
                return self.llm_service.analyze_text(text, analysis_type, **kwargs)
                
        except Exception as e:
            return {"error": f"LLM分析失败: {str(e)}"}
    
    def hybrid_analysis(self, text: str, **kwargs) -> Dict[str, Any]:
        """混合分析 - 结合LLM和传统方法"""
        try:
            # 传统方法分析
            traditional_result = self.advanced_analysis(text)
            
            # LLM分析（如果可用）
            llm_result = {}
            if self.use_llm:
                try:
                    llm_result = self.llm_analysis(text, 'comprehensive', **kwargs)
                except Exception as e:
                    llm_result = {"error": f"LLM分析失败: {str(e)}"}
            
            return {
                "traditional": traditional_result,
                "llm": llm_result,
                "analysis_method": "hybrid",
                "recommendation": self._generate_recommendation(traditional_result, llm_result)
            }
        except Exception as e:
            return {"error": f"混合分析失败: {str(e)}"}
    
    # 传统方法实现
    def _traditional_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """传统情感分析"""
        try:
            s = SnowNLP(text)
            sentiment_score = s.sentiments
            if sentiment_score > 0.6:
                sentiment = "积极"
            elif sentiment_score < 0.4:
                sentiment = "消极"
            else:
                sentiment = "中性"
            return {
                "sentiment": sentiment,
                "score": round(sentiment_score, 3),
                "confidence": "高" if abs(sentiment_score - 0.5) > 0.2 else "中",
                "method": "traditional"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _traditional_keywords_extraction(self, text: str, top_k: int) -> Dict[str, Any]:
        """传统关键词提取"""
        try:
            keywords_tfidf = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
            keywords_textrank = jieba.analyse.textrank(text, topK=top_k, withWeight=True)
            
            return {
                "tfidf_keywords": [{"word": word, "weight": round(weight, 3)} for word, weight in keywords_tfidf],
                "textrank_keywords": [{"word": word, "weight": round(weight, 3)} for word, weight in keywords_textrank],
                "method": "traditional"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _traditional_summary_generation(self, text: str, max_length: int) -> Dict[str, Any]:
        """传统文本摘要生成"""
        try:
            sentences = text.split('。')
            if len(sentences) <= 3:
                return {"summary": text, "length": len(text), "method": "traditional"}
            
            summary_sentences = sentences[:3]
            summary = '。'.join(summary_sentences) + '。'
            
            return {
                "summary": summary,
                "length": len(summary),
                "original_length": len(text),
                "compression_ratio": round(len(summary) / len(text), 3),
                "method": "traditional"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _traditional_similarity_calculation(self, text1: str, text2: str) -> Dict[str, Any]:
        """传统文本相似度计算"""
        try:
            text1_lower = ''.join(c for c in text1.lower() if c.isalnum() or c == ' ')
            text2_lower = ''.join(c for c in text2.lower() if c.isalnum() or c == ' ')

            words1 = text1_lower.split()
            words2 = text2_lower.split()

            all_words = set(words1 + words2)
            vector1 = [words1.count(word) for word in all_words]
            vector2 = [words2.count(word) for word in all_words]

            dot_product = sum(a * b for a, b in zip(vector1, vector2))
            norm_a = np.sqrt(sum(a**2 for a in vector1))
            norm_b = np.sqrt(sum(b**2 for b in vector2))

            if norm_a == 0 or norm_b == 0:
                return {"similarity_score": 0.0, "similarity_percentage": 0.0, "interpretation": "无法计算相似度", "method": "traditional"}

            cosine_sim = dot_product / (norm_a * norm_b)
            
            return {
                "similarity_score": round(cosine_sim, 3),
                "similarity_percentage": round(cosine_sim * 100, 1),
                "interpretation": "高度相似" if cosine_sim > 0.8 else "中度相似" if cosine_sim > 0.5 else "低度相似",
                "method": "traditional"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_text_stats(self, text: str) -> Dict[str, Any]:
        """计算文本统计信息"""
        try:
            words = jieba.lcut(text)
            sentences = text.split('。')
            sentences = [s for s in sentences if s.strip()]
            
            return {
                "char_count": len(text),
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_sentence_length": round(len(words) / len(sentences), 2) if sentences else 0,
                "unique_words": len(set(words))
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_topics(self, text: str) -> Dict[str, Any]:
        """提取主题信息"""
        try:
            # 使用TextRank提取主题词
            topics = jieba.analyse.textrank(text, topK=5, withWeight=True)
            
            return {
                "main_topics": [{"topic": topic, "weight": round(weight, 3)} for topic, weight in topics],
                "topic_count": len(topics)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_recommendation(self, traditional_result: Dict[str, Any], llm_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析建议"""
        try:
            if 'error' in llm_result:
                return {
                    "method": "traditional_only",
                    "reason": "LLM分析失败，建议使用传统方法",
                    "confidence": "medium"
                }
            
            # 比较两种方法的结果
            if traditional_result.get('sentiment') and llm_result.get('sentiment'):
                sentiment_match = traditional_result['sentiment']['sentiment'] == llm_result['sentiment'].get('sentiment', '')
                confidence = "high" if sentiment_match else "medium"
                
                return {
                    "method": "hybrid",
                    "sentiment_agreement": sentiment_match,
                    "confidence": confidence,
                    "recommendation": "两种方法结果一致，可信度高" if sentiment_match else "两种方法结果不同，建议人工判断"
                }
            
            return {
                "method": "hybrid",
                "confidence": "medium",
                "recommendation": "建议结合两种方法的结果进行分析"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "analyzer_status": "healthy",
            "llm_status": self.llm_service.health_check(),
            "use_llm": self.use_llm,
            "provider": self.config.LLM_PROVIDER
        }
