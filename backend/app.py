from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import jieba
import jieba.analyse
from snownlp import SnowNLP
import numpy as np
import os
from datetime import datetime, timedelta
from config import Config
from enhanced_analyzer import EnhancedTextAnalyzer

app = Flask(__name__)
config = Config()
app.config.from_object(config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# 初始化增强版分析器
enhanced_analyzer = EnhancedTextAnalyzer()

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    analyses = db.relationship('Analysis', backref='user', lazy=True)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 文本分析类
class TextAnalyzer:
    @staticmethod
    def sentiment_analysis(text):
        """情感分析"""
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
                "confidence": "高" if abs(sentiment_score - 0.5) > 0.2 else "中"
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def extract_keywords(text, top_k=10):
        """关键词提取"""
        try:
            # 使用TF-IDF方法提取关键词
            keywords_tfidf = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
            # 使用TextRank方法提取关键词
            keywords_textrank = jieba.analyse.textrank(text, topK=top_k, withWeight=True)
            
            return {
                "tfidf_keywords": [{"word": word, "weight": round(weight, 3)} for word, weight in keywords_tfidf],
                "textrank_keywords": [{"word": word, "weight": round(weight, 3)} for word, weight in keywords_textrank]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def generate_summary(text, max_length=200):
        """文本摘要生成"""
        try:
            sentences = text.split('。')
            if len(sentences) <= 3:
                return {"summary": text, "length": len(text)}
            
            # 简单的摘要算法：选择前几个句子
            summary_sentences = sentences[:3]
            summary = '。'.join(summary_sentences) + '。'
            
            return {
                "summary": summary,
                "length": len(summary),
                "original_length": len(text),
                "compression_ratio": round(len(summary) / len(text), 3)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_similarity(text1, text2):
        """计算文本相似度"""
        try:
            # 将文本转换为小写并去除标点符号，以便进行更准确的比较
            text1_lower = ''.join(c for c in text1.lower() if c.isalnum() or c == ' ')
            text2_lower = ''.join(c for c in text2.lower() if c.isalnum() or c == ' ')

            # 计算词频向量
            words1 = text1_lower.split()
            words2 = text2_lower.split()

            # 创建词汇表
            all_words = set(words1 + words2)
            vector1 = [words1.count(word) for word in all_words]
            vector2 = [words2.count(word) for word in all_words]

            # 计算余弦相似度
            dot_product = sum(a * b for a, b in zip(vector1, vector2))
            norm_a = np.sqrt(sum(a**2 for a in vector1))
            norm_b = np.sqrt(sum(b**2 for b in vector2))

            if norm_a == 0 or norm_b == 0:
                return {"similarity_score": 0.0, "similarity_percentage": 0.0, "interpretation": "无法计算相似度"}

            cosine_sim = dot_product / (norm_a * norm_b)
            
            return {
                "similarity_score": round(cosine_sim, 3),
                "similarity_percentage": round(cosine_sim * 100, 1),
                "interpretation": "高度相似" if cosine_sim > 0.8 else "中度相似" if cosine_sim > 0.5 else "低度相似"
            }
        except Exception as e:
            return {"error": str(e)}

# API路由
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已存在"}), 400
    
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "注册成功"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # 将用户ID转换为字符串，因为JWT期望字符串类型的identity
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "登录成功",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200
    
    return jsonify({"error": "用户名或密码错误"}), 401

@app.route('/api/sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment():
    user_id = int(get_jwt_identity())  # 将字符串ID转换为整数
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = TextAnalyzer.sentiment_analysis(text)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='sentiment',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/keywords', methods=['POST'])
@jwt_required()
def extract_keywords():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    top_k = data.get('top_k', 10)
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = TextAnalyzer.extract_keywords(text, top_k)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='keywords',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/summary', methods=['POST'])
@jwt_required()
def generate_summary():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    max_length = data.get('max_length', 200)
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = TextAnalyzer.generate_summary(text, max_length)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='summary',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/similarity', methods=['POST'])
@jwt_required()
def calculate_similarity():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text1 = data.get('text1')
    text2 = data.get('text2')
    
    if not text1 or not text2:
        return jsonify({"error": "请提供两段文本内容"}), 400
    
    result = TextAnalyzer.calculate_similarity(text1, text2)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=f"文本1: {text1[:100]}... | 文本2: {text2[:100]}...",
        analysis_type='similarity',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    analyses = Analysis.query.filter_by(user_id=user_id).order_by(Analysis.created_at.desc()).limit(20).all()
    
    history = []
    for analysis in analyses:
        history.append({
            "id": analysis.id,
            "text": analysis.text[:100] + "..." if len(analysis.text) > 100 else analysis.text,
            "analysis_type": analysis.analysis_type,
            "result": analysis.result,
            "created_at": analysis.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({"history": history}), 200

@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = int(get_jwt_identity())
    total_analyses = Analysis.query.filter_by(user_id=user_id).count()
    
    # 按类型统计
    sentiment_count = Analysis.query.filter_by(user_id=user_id, analysis_type='sentiment').count()
    keywords_count = Analysis.query.filter_by(user_id=user_id, analysis_type='keywords').count()
    summary_count = Analysis.query.filter_by(user_id=user_id, analysis_type='summary').count()
    similarity_count = Analysis.query.filter_by(user_id=user_id, analysis_type='similarity').count()
    
    return jsonify({
        "total_analyses": total_analyses,
        "sentiment_count": sentiment_count,
        "keywords_count": keywords_count,
        "summary_count": summary_count,
        "similarity_count": similarity_count
    }), 200

# LLM相关API端点
@app.route('/api/llm/sentiment', methods=['POST'])
@jwt_required()
def llm_sentiment_analysis():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = enhanced_analyzer.sentiment_analysis(text, use_llm=True)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='llm_sentiment',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/llm/keywords', methods=['POST'])
@jwt_required()
def llm_extract_keywords():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    top_k = data.get('top_k', 10)
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = enhanced_analyzer.extract_keywords(text, top_k, use_llm=True)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='llm_keywords',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/llm/summary', methods=['POST'])
@jwt_required()
def llm_generate_summary():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    max_length = data.get('max_length', 200)
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = enhanced_analyzer.generate_summary(text, max_length, use_llm=True)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='llm_summary',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/llm/comprehensive', methods=['POST'])
@jwt_required()
def llm_comprehensive_analysis():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = enhanced_analyzer.llm_analysis(text, 'comprehensive')
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='llm_comprehensive',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/hybrid/analysis', methods=['POST'])
@jwt_required()
def hybrid_analysis():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "请提供文本内容"}), 400
    
    result = enhanced_analyzer.hybrid_analysis(text)
    
    # 保存分析记录
    analysis = Analysis(
        user_id=user_id,
        text=text,
        analysis_type='hybrid_analysis',
        result=str(result)
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result), 200

@app.route('/api/llm/health', methods=['GET'])
def llm_health_check():
    """LLM服务健康检查"""
    return jsonify(enhanced_analyzer.health_check()), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002) 