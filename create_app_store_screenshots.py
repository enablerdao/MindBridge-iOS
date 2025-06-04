#!/usr/bin/env python3
"""
App Store用スクリーンショット生成スクリプト
"""

from PIL import Image, ImageDraw, ImageFont
import json

def create_app_store_screenshots():
    """App Store用の美しいスクリーンショットを作成"""
    
    # iPhone 6.7インチ用 (iPhone 14 Pro Max, 15 Pro Max)
    screenshot_size = (1290, 2796)
    
    screenshots = [
        {
            "name": "01_main_chat",
            "title": "🤖 AI チャット",
            "subtitle": "Qwen3-4Bとの自然な日本語会話",
            "description": "オフラインで動作するプライベートなAIアシスタント"
        },
        {
            "name": "02_programming_help", 
            "title": "👨‍💻 プログラミング支援",
            "subtitle": "コード生成・解説・デバッグ",
            "description": "Swift、Python、JavaScript等に対応"
        },
        {
            "name": "03_creative_writing",
            "title": "✍️ 創作支援", 
            "subtitle": "小説・俳句・詩の創作",
            "description": "日本語の美しい表現力を活用"
        },
        {
            "name": "04_multilingual",
            "title": "🌍 多言語対応",
            "subtitle": "日本語・英語・中国語",
            "description": "複数言語での自然な対話"
        },
        {
            "name": "05_settings",
            "title": "⚙️ 高度な設定",
            "subtitle": "AI パラメータ調整",
            "description": "Temperature、Top-p等を自由にカスタマイズ"
        }
    ]
    
    for i, screenshot in enumerate(screenshots):
        create_single_screenshot(screenshot, i + 1, screenshot_size)
    
    # App Store用説明画像も作成
    create_feature_showcase()

def create_single_screenshot(screenshot_data, number, size):
    """個別のスクリーンショットを作成"""
    width, height = size
    
    # ベース画像を作成
    img = Image.new('RGB', (width, height), color=(15, 15, 15))  # ダークグレー
    draw = ImageDraw.Draw(img)
    
    # 背景グラデーション
    create_dark_gradient(draw, width, height)
    
    # スマートフォンフレームを描画
    draw_phone_frame(draw, width, height)
    
    # コンテンツエリアの計算
    content_width = int(width * 0.85)
    content_height = int(height * 0.75)
    content_x = (width - content_width) // 2
    content_y = int(height * 0.12)
    
    # チャット画面を模擬
    draw_chat_interface(draw, content_x, content_y, content_width, content_height, screenshot_data)
    
    # タイトルと説明を追加
    add_screenshot_text(draw, width, height, screenshot_data)
    
    # 保存
    filename = f"Screenshot_{number:02d}_{screenshot_data['name']}.png"
    img.save(filename, 'PNG', quality=100)
    print(f"✅ Created: {filename}")

def create_dark_gradient(draw, width, height):
    """ダークテーマのグラデーション背景"""
    for y in range(height):
        ratio = y / height
        # ダークブルーからブラックへ
        r = int(15 + (5 - 15) * ratio)
        g = int(25 + (10 - 25) * ratio)  
        b = int(45 + (25 - 45) * ratio)
        color = (max(0, r), max(0, g), max(0, b))
        draw.line([(0, y), (width, y)], fill=color)

def draw_phone_frame(draw, width, height):
    """スマートフォンのフレームを描画"""
    # 角丸四角形でフレーム
    margin = 30
    corner_radius = 40
    
    # 外枠
    draw_rounded_rect(draw, margin, margin, width - margin, height - margin, 
                      corner_radius, None, (80, 80, 80), 3)

def draw_chat_interface(draw, x, y, width, height, screenshot_data):
    """チャット画面のインターフェースを描画"""
    
    # ヘッダー部分
    header_height = 80
    draw_rounded_rect(draw, x, y, x + width, y + header_height, 
                      20, (30, 30, 35), None, 0)
    
    # ヘッダーテキスト
    try:
        header_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 24)
        draw.text((x + 20, y + 25), "Qwen3 Chat", fill=(255, 255, 255), font=header_font)
        
        status_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        draw.text((x + 20, y + 50), "オンライン • Qwen3-4B", fill=(100, 200, 100), font=status_font)
    except:
        pass
    
    # チャットメッセージエリア
    chat_y = y + header_height + 20
    chat_height = height - header_height - 100
    
    # サンプルメッセージを描画
    draw_sample_messages(draw, x, chat_y, width, chat_height, screenshot_data)
    
    # 入力エリア
    input_y = y + height - 60
    draw_rounded_rect(draw, x + 10, input_y, x + width - 10, input_y + 50,
                      25, (40, 40, 45), (100, 100, 105), 2)
    
    try:
        input_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        draw.text((x + 25, input_y + 15), "メッセージを入力...", fill=(150, 150, 150), font=input_font)
    except:
        pass

def draw_sample_messages(draw, x, y, width, height, screenshot_data):
    """サンプルメッセージを描画"""
    message_data = get_sample_messages(screenshot_data['name'])
    
    current_y = y + 20
    message_margin = 15
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        bold_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 16)
    except:
        font = ImageFont.load_default()
        bold_font = font
    
    for message in message_data:
        if current_y + 100 > y + height:
            break
            
        is_user = message['sender'] == 'user'
        
        # メッセージの幅と位置を計算
        msg_width = min(int(width * 0.75), 400)
        msg_x = x + width - msg_width - 20 if is_user else x + 20
        
        # メッセージテキストの高さを計算
        lines = wrap_text(message['text'], msg_width - 30, font)
        line_height = 22
        msg_height = len(lines) * line_height + 20
        
        # メッセージ背景
        bg_color = (0, 122, 255) if is_user else (50, 50, 55)
        draw_rounded_rect(draw, msg_x, current_y, msg_x + msg_width, current_y + msg_height,
                          18, bg_color, None, 0)
        
        # メッセージテキスト
        text_color = (255, 255, 255) if is_user else (255, 255, 255)
        text_y = current_y + 10
        
        for line in lines:
            draw.text((msg_x + 15, text_y), line, fill=text_color, font=font)
            text_y += line_height
        
        current_y += msg_height + message_margin

def get_sample_messages(screenshot_type):
    """スクリーンショットタイプに応じたサンプルメッセージ"""
    messages = {
        "01_main_chat": [
            {"sender": "user", "text": "こんにちは！今日はどんな質問に答えてもらえますか？"},
            {"sender": "ai", "text": "こんにちは！私は様々な質問にお答えできます。プログラミング、創作、学習支援、日常の相談など、何でもお気軽にお聞きください。"},
            {"sender": "user", "text": "ストレス解消法を教えて"},
            {"sender": "ai", "text": "効果的なストレス解消法をご提案します：\n• 深呼吸・瞑想（5-10分）\n• 軽い運動や散歩\n• 好きな音楽を聴く\n• 温かいお茶でリラックス"}
        ],
        "02_programming_help": [
            {"sender": "user", "text": "SwiftでHTTP通信のコードを書いて"},
            {"sender": "ai", "text": "URLSessionを使用したHTTP通信のコード例です：\n\n```swift\nfunc fetchData(from url: String) {\n    guard let url = URL(string: url) else { return }\n    \n    URLSession.shared.dataTask(with: url) { data, response, error in\n        // データ処理\n    }.resume()\n}\n```"},
            {"sender": "user", "text": "エラーハンドリングも追加して"},
            {"sender": "ai", "text": "エラーハンドリングを追加したコードです：\n\n```swift\nif let error = error {\n    print(\"エラー: \\(error.localizedDescription)\")\n    return\n}\n\nguard let data = data else {\n    print(\"データが見つかりません\")\n    return\n}\n```"}
        ],
        "03_creative_writing": [
            {"sender": "user", "text": "桜をテーマにした俳句を作って"},
            {"sender": "ai", "text": "桜をテーマにした俳句をお作りしました：\n\n```\n桜散り\n風に舞い踊る\n春の夢\n```\n\n```\n一輪の\n桜に込めし\n母の愛\n```"},
            {"sender": "user", "text": "短編小説の冒頭も書ける？"},
            {"sender": "ai", "text": "もちろんです！どのようなジャンルやテーマの短編小説をお書きになりたいですか？SF、ファンタジー、日常系、ミステリーなど、お好みをお聞かせください。"}
        ],
        "04_multilingual": [
            {"sender": "user", "text": "Hello! Can you help me with English?"},
            {"sender": "ai", "text": "Hello! I'd be happy to help you with English. I can assist with grammar, vocabulary, writing, translation, and conversation practice. What would you like to work on?"},
            {"sender": "user", "text": "中文怎么说\"你好\"？"},
            {"sender": "ai", "text": "\"你好\"就是中文的问候语，发音是\"nǐ hǎo\"。这是最常用的打招呼方式。还有其他表达：\n• 您好 (nín hǎo) - 更正式\n• 大家好 (dàjiā hǎo) - 对多人\n• 早上好 (zǎoshang hǎo) - 早安"}
        ],
        "05_settings": [
            {"sender": "user", "text": "設定画面について教えて"},
            {"sender": "ai", "text": "設定画面では以下を調整できます：\n\n• Temperature: 創造性レベル (0.1-1.0)\n• Top-p: 応答の多様性 (0.1-1.0)\n• Max Tokens: 最大応答長\n• System Prompt: AI の性格設定\n• モデル選択: Q4_K_M / Q5_K_M / Q6_K"},
            {"sender": "user", "text": "おすすめの設定は？"},
            {"sender": "ai", "text": "用途別おすすめ設定：\n\n📝 文章作成: Temperature 0.8, Top-p 0.9\n🧮 計算・分析: Temperature 0.2, Top-p 0.5\n💬 日常会話: Temperature 0.6, Top-p 0.8\n👨‍💻 プログラミング: Temperature 0.3, Top-p 0.6"}
        ]
    }
    
    return messages.get(screenshot_type, messages["01_main_chat"])

def wrap_text(text, max_width, font):
    """テキストを指定幅で折り返し"""
    lines = []
    words = text.split(' ')
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        # Pillow >= 10.0.0 では textbbox を使用
        try:
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
        except:
            # 古いバージョンの場合は textsize を使用
            width, _ = font.getsize(test_line)
        
        if width <= max_width - 30:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def draw_rounded_rect(draw, x1, y1, x2, y2, radius, fill=None, outline=None, width=0):
    """角丸四角形を描画"""
    if fill:
        # 塗りつぶし部分
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        
        # 角の円
        draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
        draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
        draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
        draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)
    
    if outline:
        # 枠線
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

def add_screenshot_text(draw, width, height, screenshot_data):
    """スクリーンショットにタイトルと説明を追加"""
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 32)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = title_font
        desc_font = title_font
    
    # タイトルエリアの背景
    title_y = height - 180
    draw_rounded_rect(draw, 20, title_y, width - 20, height - 20, 
                      20, (0, 0, 0, 200), None, 0)
    
    # テキスト描画
    text_x = 40
    
    # タイトル
    draw.text((text_x, title_y + 20), screenshot_data['title'], 
              fill=(255, 255, 255), font=title_font)
    
    # サブタイトル
    draw.text((text_x, title_y + 60), screenshot_data['subtitle'], 
              fill=(200, 200, 200), font=subtitle_font)
    
    # 説明
    draw.text((text_x, title_y + 95), screenshot_data['description'], 
              fill=(180, 180, 180), font=desc_font)

def create_feature_showcase():
    """機能紹介用の画像を作成"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color=(20, 20, 25))
    draw = ImageDraw.Draw(img)
    
    # タイトル
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 48)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = title_font
    
    title_text = "🤖 Qwen3 Chat - AI アシスタント"
    draw.text((50, 50), title_text, fill=(255, 255, 255), font=title_font)
    
    subtitle_text = "プライベート・オフライン・高性能"
    draw.text((50, 120), subtitle_text, fill=(100, 200, 255), font=subtitle_font)
    
    # 機能リスト
    features = [
        "🔒 完全オフライン動作 - インターネット不要",
        "🚀 高速応答 - 平均2秒以内で回答",
        "🇯🇵 日本語特化 - JMT 0.66相当の高品質",
        "💻 プログラミング支援 - コード生成・解説",
        "✍️ 創作支援 - 小説・俳句・詩の作成",
        "🌍 多言語対応 - 日英中韓4言語",
        "⚙️ カスタマイズ - AI動作を細かく調整",
        "📱 iOS最適化 - Metal GPU加速対応"
    ]
    
    y = 200
    for feature in features:
        draw.text((50, y), feature, fill=(255, 255, 255), font=subtitle_font)
        y += 50
    
    img.save("Feature_Showcase.png", 'PNG', quality=100)
    print("✅ Created: Feature_Showcase.png")

if __name__ == "__main__":
    print("📱 App Store用スクリーンショット生成中...")
    create_app_store_screenshots()
    print("✨ スクリーンショット生成完了！")