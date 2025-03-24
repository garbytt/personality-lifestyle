import google.generativeai as genai
import os
# from dotenv import load_dotenv
import streamlit as st

# 環境変数の読み込み
# load_dotenv()

# Gemini APIの設定
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def analyze_personality(user_data):
    """
    ユーザーの回答データから性格分析を行う
    """
    # プロンプトの作成
    prompt = f"""
    以下のユーザーデータを分析し、主要な性格特性、強み、課題点、潜在的な適性を特定してください：

    {user_data}

    分析結果は以下のフォーマットで出力してください：
    1. 主要性格特性（5つ）とその程度
    2. 特性間の相互関係
    3. 環境に応じた行動パターンの変化
    4. 特定された強み（3-5つ）
    5. 成長可能性のある領域（2-3つ）

    分析結果にはidの文字列は含めないでください。
    """

    # Gemini APIの呼び出し
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    response = model.generate_content(prompt)
    
    return response.text

def generate_recommendations(personality_analysis):
    """
    性格分析結果に基づいてライフスタイル提案を生成する
    """
    prompt = f"""
    以下の性格プロファイルに基づき、このユーザーの特性を最大限に
    活かすための具体的な提案を生成してください：

    {personality_analysis}

    以下の領域について、具体的かつ実行可能な提案を提示してください：
    1. 日常習慣の最適化
    2. 仕事/学習効率の向上
    3. 人間関係の充実
    4. 余暇活動の充実
    5. 精神的健康の維持
    """

    # Gemini APIの呼び出し
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')
    response = model.generate_content(prompt)
    
    return response.text 