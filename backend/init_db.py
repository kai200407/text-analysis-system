#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建数据库表结构
"""

from app import app, db

def init_database():
    """初始化数据库"""
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("✅ 数据库表创建成功！")
            
            # 检查表是否创建成功
            from app import User, Analysis
            user_count = User.query.count()
            analysis_count = Analysis.query.count()
            print(f"📊 当前数据库状态：")
            print(f"   - 用户表记录数：{user_count}")
            print(f"   - 分析记录表记录数：{analysis_count}")
            
        except Exception as e:
            print(f"❌ 数据库初始化失败：{e}")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 开始初始化数据库...")
    if init_database():
        print("🎉 数据库初始化完成！")
    else:
        print("💥 数据库初始化失败！")
