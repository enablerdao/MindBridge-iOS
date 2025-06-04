#!/usr/bin/env python3
"""
Qwen3iOS インタラクティブデモ
実際のiOSアプリの動作をシミュレート
"""

import time
import sys
import os
import random
from datetime import datetime

class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_splash_screen():
    clear_screen()
    splash = f"""
{Color.CYAN}
    ╔═══════════════════════════════╗
    ║                               ║
    ║        Qwen3-4B Chat         ║
    ║                               ║
    ║         for iOS 16+          ║
    ║                               ║
    ║      Powered by llama.cpp     ║
    ║                               ║
    ╚═══════════════════════════════╝
{Color.END}
    """
    print(splash)
    time.sleep(2)

def show_loading_model():
    clear_screen()
    print(f"{Color.BOLD}📱 Qwen3-4B Chat{Color.END}")
    print("="*40)
    print(f"\n{Color.YELLOW}🧠 モデルを初期化中...{Color.END}\n")
    
    steps = [
        ("モデルファイルを確認", 0.5),
        ("Metal GPUを初期化", 0.7),
        ("メモリアロケーション", 0.8),
        ("推論エンジン起動", 0.6),
        ("チャットセッション準備", 0.4)
    ]
    
    for step, duration in steps:
        print(f"  • {step}...", end='', flush=True)
        time.sleep(duration)
        print(f" {Color.GREEN}✓{Color.END}")
    
    print(f"\n{Color.GREEN}✨ 準備完了！{Color.END}")
    time.sleep(1)

def format_message(content, is_user=True):
    """メッセージをフォーマット"""
    if is_user:
        return f"{Color.BLUE}あなた{Color.END}: {content}"
    else:
        return f"{Color.GREEN}Qwen3{Color.END}: {content}"

def typing_effect(text, delay=0.03):
    """タイピングエフェクト"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def generate_response(prompt):
    """Qwen3の応答を生成（シミュレーション）"""
    responses = {
        "こんにちは": "こんにちは！今日はどのようなお手伝いができますか？",
        "天気": "申し訳ございませんが、リアルタイムの天気情報にはアクセスできません。お住まいの地域の天気予報サービスをご確認ください。",
        "計算": "数式を教えていただければ、計算をお手伝いします。例: 「123 + 456を計算して」",
        "プログラミング": "プログラミングについて何か具体的にお聞きになりたいことはありますか？Python、Swift、JavaScriptなど、様々な言語についてお答えできます。",
        "Qwen": "私はQwen3-4Bモデルです。Alibaba Cloudによって開発された言語モデルで、日本語を含む多言語に対応しています。",
        "iPhone": "このアプリはiPhone 12以降のデバイスで最適に動作します。Metal GPUアクセラレーションにより、高速な推論が可能です。",
        "さようなら": "さようなら！またお話ししましょう。良い一日をお過ごしください！",
        "ありがとう": "どういたしまして！お役に立てて嬉しいです。他に何かございましたらお聞きください。"
    }
    
    # キーワードマッチング
    prompt_lower = prompt.lower()
    for keyword, response in responses.items():
        if keyword.lower() in prompt_lower:
            return response
    
    # 計算リクエストの処理
    if any(op in prompt for op in ['+', '-', '*', '/', '計算']):
        try:
            # 簡単な計算を試みる
            result = eval(prompt.replace('計算', '').replace('して', '').strip())
            return f"計算結果: {result}"
        except:
            return "計算式を正しく入力してください。例: 123 + 456"
    
    # デフォルト応答
    default_responses = [
        f"「{prompt}」について理解しました。もう少し詳しく教えていただけますか？",
        f"なるほど、「{prompt}」についてですね。どのような観点からお答えすればよいでしょうか？",
        f"興味深い質問ですね。「{prompt}」に関して、具体的にどのような情報をお求めですか？"
    ]
    return random.choice(default_responses)

def show_chat_interface():
    """チャットインターフェース"""
    clear_screen()
    print(f"{Color.BOLD}📱 Qwen3-4B Chat{Color.END}")
    print("="*40)
    print(f"{Color.CYAN}💡 ヒント: 'exit'または'quit'で終了{Color.END}")
    print("="*40)
    
    # 初期メッセージ
    print(f"\n{Color.GREEN}Qwen3{Color.END}: ", end='')
    typing_effect("こんにちは！Qwen3-4Bモデルを使用したチャットアプリです。何かお手伝いできることはありますか？")
    
    chat_history = []
    
    while True:
        try:
            # ユーザー入力
            user_input = input(f"\n{Color.BLUE}あなた{Color.END}: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'さようなら']:
                print(f"\n{Color.GREEN}Qwen3{Color.END}: ", end='')
                typing_effect("さようなら！またお会いしましょう。")
                break
            
            if not user_input:
                continue
            
            # 思考中表示
            print(f"\n{Color.YELLOW}🤔 思考中...{Color.END}", end='', flush=True)
            time.sleep(random.uniform(0.5, 1.5))  # ランダムな遅延
            print("\r" + " "*20 + "\r", end='')  # 思考中を消去
            
            # 応答生成
            response = generate_response(user_input)
            print(f"{Color.GREEN}Qwen3{Color.END}: ", end='')
            typing_effect(response)
            
            # 履歴に追加
            chat_history.append({"user": user_input, "assistant": response})
            
        except KeyboardInterrupt:
            print(f"\n\n{Color.RED}⚠️  チャットを終了します{Color.END}")
            break
        except Exception as e:
            print(f"\n{Color.RED}エラーが発生しました: {e}{Color.END}")

def show_system_info():
    """システム情報表示"""
    print(f"\n{Color.BOLD}📊 システム情報:{Color.END}")
    print(f"  • モデル: Qwen3-4B-Instruct (Q4_K_M)")
    print(f"  • メモリ使用量: 2.7GB")
    print(f"  • 推論速度: ~40 トークン/秒")
    print(f"  • Metal GPU: 有効")
    print(f"  • コンテキスト長: 4096トークン")
    print(f"  • 対応言語: 日本語、英語、中国語 他")

def main():
    """メイン実行"""
    try:
        # スプラッシュスクリーン
        show_splash_screen()
        
        # モデル読み込み
        show_loading_model()
        
        # チャットインターフェース
        show_chat_interface()
        
        # システム情報
        show_system_info()
        
        print(f"\n{Color.CYAN}ありがとうございました！{Color.END}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Color.RED}⚠️  アプリを終了しました{Color.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()