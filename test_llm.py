#!/usr/bin/env python3
"""
LLM功能测试脚本
用于测试集成的LLM分析功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:5001"
TEST_TEXT = "今天天气非常好，阳光明媚，微风轻拂。我心情愉悦，决定去公园散步。看到孩子们在玩耍，老人们在下棋，整个公园充满了生机和活力。这让我感到非常幸福和满足。"

def test_llm_health():
    """测试LLM健康检查"""
    print("🔍 测试LLM健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/api/llm/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_llm_sentiment():
    """测试LLM情感分析"""
    print("\n😊 测试LLM情感分析...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/llm/sentiment",
            headers={"Content-Type": "application/json"},
            json={"text": TEST_TEXT}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 情感分析成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ 情感分析失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 情感分析异常: {e}")
        return False

def test_llm_keywords():
    """测试LLM关键词提取"""
    print("\n🔑 测试LLM关键词提取...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/llm/keywords",
            headers={"Content-Type": "application/json"},
            json={"text": TEST_TEXT, "top_k": 5}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 关键词提取成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ 关键词提取失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 关键词提取异常: {e}")
        return False

def test_llm_summary():
    """测试LLM文本摘要"""
    print("\n📝 测试LLM文本摘要...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/llm/summary",
            headers={"Content-Type": "application/json"},
            json={"text": TEST_TEXT, "max_length": 100}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 文本摘要成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ 文本摘要失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 文本摘要异常: {e}")
        return False

def test_hybrid_analysis():
    """测试混合分析"""
    print("\n🔄 测试混合分析...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/hybrid/analysis",
            headers={"Content-Type": "application/json"},
            json={"text": TEST_TEXT}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 混合分析成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ 混合分析失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 混合分析异常: {e}")
        return False

def test_comprehensive_analysis():
    """测试综合分析"""
    print("\n🎯 测试综合分析...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/llm/comprehensive",
            headers={"Content-Type": "application/json"},
            json={"text": TEST_TEXT}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 综合分析成功: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"❌ 综合分析失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 综合分析异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 LLM功能测试开始")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(2)
    
    # 测试结果统计
    tests = [
        ("健康检查", test_llm_health),
        ("情感分析", test_llm_sentiment),
        ("关键词提取", test_llm_keywords),
        ("文本摘要", test_llm_summary),
        ("综合分析", test_comprehensive_analysis),
        ("混合分析", test_hybrid_analysis),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！LLM集成成功！")
    else:
        print("⚠️  部分测试失败，请检查配置和服务状态")
    
    print("\n💡 提示:")
    print("1. 确保后端服务已启动 (python3 app.py)")
    print("2. 确保Ollama服务已启动 (docker-compose -f docker-compose.ollama.yml up)")
    print("3. 检查环境配置文件 (.env)")
    print("4. 查看详细日志了解错误原因")

if __name__ == "__main__":
    main()
