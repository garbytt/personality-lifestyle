import streamlit as st
import json
from questions import BASIC_QUESTIONS, QUESTION_ORDER
from analyzer import analyze_personality, generate_recommendations

# ページ設定
st.set_page_config(
    page_title="個性診断・ライフスタイル提案",
    page_icon="✨",
    layout="wide"
)

# セッション状態の初期化
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_next' not in st.session_state:
    st.session_state.show_next = False
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

def render_question(question_data):
    """質問を表示し、回答を取得する"""
    question_id = question_data['id']
    question_text = question_data['question']
    question_type = question_data['type']
    
    if question_type == 'select':
        answer = st.selectbox(question_text, question_data['options'])
    elif question_type == 'text':
        answer = st.text_input(question_text)
    elif question_type == 'scale':
        answer = st.radio(question_text, question_data['options'])
    
    return answer

def calculate_progress():
    """全体の進捗を計算"""
    total_questions = sum(len(questions) for questions in BASIC_QUESTIONS.values())
    answered_questions = len(st.session_state.answers)
    return answered_questions / total_questions

def reset_session():
    """セッションをリセットする"""
    st.session_state.clear()
    st.session_state.current_step = 0
    st.session_state.current_question_index = 0
    st.session_state.answers = {}
    st.session_state.show_next = False
    st.session_state.show_results = False
    st.rerun()

def show_results():
    """結果を表示する"""
    # リセットボタン
    if st.button("診断をやり直す"):
        reset_session()
        return
    
    # 分析の実行
    with st.spinner("性格分析を実行中..."):
        personality_analysis = analyze_personality(json.dumps(st.session_state.answers, ensure_ascii=False))
    
    # 結果の表示
    st.header("🎯 性格分析結果")
    st.write(personality_analysis)
    
    # 提案の生成
    with st.spinner("ライフスタイル提案を生成中..."):
        recommendations = generate_recommendations(personality_analysis)
    
    # 提案の表示
    st.header("💡 パーソナライズされた提案")
    st.write(recommendations)

def main():
    st.title("✨ 個性診断・ライフスタイル提案")
    
    # 進捗バー
    progress = calculate_progress()
    st.progress(progress)
    
    # 結果表示モードの場合
    if st.session_state.show_results:
        show_results()
        return
    
    # 全ての質問が終わった場合
    if st.session_state.current_step >= len(QUESTION_ORDER):
        st.header("🎉 全ての質問が終わりました！")
        st.write("診断を開始するには、以下のボタンをクリックしてください。")
        if st.button("診断を開始"):
            st.session_state.show_results = True
            st.rerun()
        return
    
    # 現在のステップの質問カテゴリを取得
    current_category = QUESTION_ORDER[st.session_state.current_step]
    questions = BASIC_QUESTIONS[current_category]
    
    # カテゴリ内の質問が終わった場合
    if st.session_state.current_question_index >= len(questions):
        st.session_state.current_question_index = 0
        st.session_state.current_step += 1
        st.rerun()
        return
    
    # カテゴリタイトル
    st.header(f"Step {st.session_state.current_step + 1}: {current_category}")
    
    # 現在の質問を表示
    current_question = questions[st.session_state.current_question_index]
    answer = render_question(current_question)
    
    # 回答を保存
    st.session_state.answers[current_question['id']] = answer
    
    # 前の質問に戻るボタン
    if st.session_state.current_question_index > 0:
        if st.button("前の質問に戻る"):
            st.session_state.current_question_index -= 1
            st.rerun()
    
    # 次の質問ボタン
    if st.button("次の質問へ"):
        st.session_state.current_question_index += 1
        st.rerun()

if __name__ == "__main__":
    main() 