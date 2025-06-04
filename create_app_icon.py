#!/usr/bin/env python3
"""
App Store用アイコン生成スクリプト
"""

import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_app_icon():
    """美しいApp Store用アイコンを作成"""
    
    # アイコンサイズ (App Store用)
    sizes = [
        (1024, 1024),  # App Store
        (180, 180),    # iPhone 6 Plus @3x
        (120, 120),    # iPhone @2x  
        (87, 87),      # iPhone @3x Settings
        (80, 80),      # iPhone @2x Spotlight
        (60, 60),      # iPhone @1x
        (58, 58),      # iPhone @2x Settings
        (40, 40),      # iPhone @2x Spotlight
        (29, 29),      # iPhone @1x Settings
        (20, 20)       # iPhone @1x Notification
    ]
    
    for width, height in sizes:
        # 新しい画像を作成（グラデーション背景）
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # 美しいグラデーション背景を作成
        create_gradient_background(draw, width, height)
        
        # AI/チャットアイコンを描画
        draw_ai_chat_icon(draw, width, height)
        
        # ファイル保存
        filename = f"AppIcon-{width}x{height}.png"
        img.save(filename, 'PNG', quality=100)
        print(f"✅ Created: {filename}")
    
    # App Store用メタデータも生成
    create_app_metadata()

def create_gradient_background(draw, width, height):
    """美しいグラデーション背景を作成"""
    # 青からシアンへのグラデーション
    for y in range(height):
        # グラデーション計算
        ratio = y / height
        r = int(65 + (100 - 65) * ratio)    # 青→シアン
        g = int(105 + (200 - 105) * ratio)
        b = int(225 + (255 - 225) * ratio)
        
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)

def draw_ai_chat_icon(draw, width, height):
    """AI/チャットアイコンを描画"""
    center_x, center_y = width // 2, height // 2
    
    # スケール調整
    scale = width / 1024.0
    
    # チャット吹き出し1 (大)
    bubble1_w = int(300 * scale)
    bubble1_h = int(200 * scale)
    bubble1_x = center_x - bubble1_w // 2
    bubble1_y = center_y - bubble1_h // 2 - int(50 * scale)
    
    # 角丸四角形を描画
    draw_rounded_rectangle(draw, 
                          bubble1_x, bubble1_y, 
                          bubble1_x + bubble1_w, bubble1_y + bubble1_h,
                          int(30 * scale), 
                          (255, 255, 255, 200))
    
    # チャット吹き出し2 (小)
    bubble2_w = int(200 * scale)
    bubble2_h = int(120 * scale)
    bubble2_x = center_x + int(20 * scale)
    bubble2_y = center_y + int(30 * scale)
    
    draw_rounded_rectangle(draw,
                          bubble2_x, bubble2_y,
                          bubble2_x + bubble2_w, bubble2_y + bubble2_h,
                          int(20 * scale),
                          (255, 255, 255, 150))
    
    # AI脳のアイコン（円 + 回路パターン）
    ai_size = int(80 * scale)
    ai_x = center_x - ai_size // 2
    ai_y = center_y - ai_size // 2 + int(100 * scale)
    
    # AI脳の円
    draw.ellipse([ai_x, ai_y, ai_x + ai_size, ai_y + ai_size],
                 fill=(255, 255, 255), outline=(100, 150, 255), width=int(4 * scale))
    
    # 回路パターン
    draw_circuit_pattern(draw, ai_x, ai_y, ai_size, scale)
    
    # 文字 "AI" を中央に
    if scale > 0.05:  # 小さすぎる場合は文字を描画しない
        try:
            font_size = max(int(40 * scale), 12)
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            text = "AI"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
            text_x = ai_x + ai_size // 2 - text_w // 2
            text_y = ai_y + ai_size // 2 - text_h // 2
            draw.text((text_x, text_y), text, fill=(100, 150, 255), font=font)
        except:
            # フォントが見つからない場合はスキップ
            pass

def draw_rounded_rectangle(draw, x1, y1, x2, y2, radius, fill):
    """角丸四角形を描画"""
    # 四角形の各部分を描画
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # 角の円を描画
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

def draw_circuit_pattern(draw, x, y, size, scale):
    """回路パターンを描画"""
    line_width = max(int(2 * scale), 1)
    color = (100, 150, 255)
    
    # 簡単な回路パターン
    center_x = x + size // 2
    center_y = y + size // 2
    
    # 十字パターン
    draw.line([center_x - size//3, center_y, center_x + size//3, center_y], 
              fill=color, width=line_width)
    draw.line([center_x, center_y - size//3, center_x, center_y + size//3], 
              fill=color, width=line_width)

def create_app_metadata():
    """App Store用メタデータファイルを作成"""
    metadata = {
        "app_name": "Qwen3 Chat",
        "version": "1.0.0",
        "build": "1",
        "description": "Qwen3-4B-Instructモデルを搭載したプライベートなAIチャットアプリ",
        "keywords": ["AI", "Chat", "Japanese", "Offline", "Privacy", "LLM"],
        "category": "Productivity",
        "content_rating": "4+",
        "copyright": "© 2025 Qwen3iOS Team",
        "privacy_policy": "https://example.com/privacy",
        "support_url": "https://example.com/support"
    }
    
    with open("app_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("✅ Created: app_metadata.json")

if __name__ == "__main__":
    print("🎨 App Store用アイコン生成中...")
    create_app_icon()
    print("✨ アイコン生成完了！")