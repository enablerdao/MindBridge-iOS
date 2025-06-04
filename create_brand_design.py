#!/usr/bin/env python3
"""
MindBridge ブランドデザイン・ロゴ生成スクリプト
"""

from PIL import Image, ImageDraw, ImageFont
import json
import math

def create_mindbridge_brand():
    """MindBridge ブランドのロゴとデザインを作成"""
    
    # ブランドカラーパレット
    brand_colors = {
        "primary": (106, 90, 255),      # 紫ブルー
        "secondary": (255, 107, 107),    # コーラルピンク  
        "accent": (72, 219, 251),        # シアン
        "dark": (30, 30, 35),            # ダークグレー
        "light": (248, 249, 250),        # ライトグレー
        "gradient_start": (106, 90, 255),
        "gradient_end": (72, 219, 251)
    }
    
    # メインロゴ作成
    create_main_logo(brand_colors)
    
    # アプリアイコン（全サイズ）
    create_app_icons(brand_colors)
    
    # GitHubロゴ・バナー
    create_github_assets(brand_colors)
    
    # ブランドガイド保存
    save_brand_guide(brand_colors)

def create_main_logo(colors):
    """メインロゴを作成"""
    width, height = 800, 300
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景グラデーション
    create_gradient_background(draw, width, height, colors["gradient_start"], colors["gradient_end"])
    
    # "Mind" + "Bridge" のビジュアル表現
    center_x, center_y = width // 2, height // 2
    
    # 左側の"Mind"を表現する脳の形
    mind_x = center_x - 120
    draw_brain_icon(draw, mind_x, center_y, 80, colors["light"])
    
    # 中央のブリッジ（接続線）
    bridge_start_x = mind_x + 80
    bridge_end_x = center_x + 40
    draw_neural_bridge(draw, bridge_start_x, center_y, bridge_end_x, center_y, colors["accent"])
    
    # 右側の"Bridge"を表現するデバイス
    device_x = center_x + 80
    draw_device_icon(draw, device_x, center_y, 60, colors["light"])
    
    # テキストロゴ
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 48)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        
        # "MindBridge"
        text_y = center_y + 60
        draw.text((center_x - 120, text_y), "MindBridge", fill=colors["light"], font=title_font, anchor="mm")
        
        # サブタイトル
        subtitle_y = text_y + 50
        draw.text((center_x - 120, subtitle_y), "Private AI Assistant", fill=colors["light"], font=subtitle_font, anchor="mm")
        
    except:
        pass
    
    img.save("MindBridge_Logo.png", 'PNG')
    print("✅ Created: MindBridge_Logo.png")

def create_app_icons(colors):
    """アプリアイコン（全サイズ）を作成"""
    sizes = [
        (1024, 1024), (180, 180), (120, 120), (87, 87), (80, 80),
        (60, 60), (58, 58), (40, 40), (29, 29), (20, 20)
    ]
    
    for width, height in sizes:
        img = Image.new('RGB', (width, height), colors["primary"])
        draw = ImageDraw.Draw(img)
        
        # 円形グラデーション背景
        create_circular_gradient(draw, width, height, colors["primary"], colors["accent"])
        
        # アイコンデザイン
        center_x, center_y = width // 2, height // 2
        scale = width / 1024.0
        
        # 脳とデバイスを接続するシンプルなデザイン
        draw_brain_bridge_icon(draw, center_x, center_y, int(200 * scale), colors["light"], scale)
        
        # 保存
        filename = f"AppIcon-{width}x{height}.png"
        img.save(filename, 'PNG', quality=100)
        print(f"✅ Created: {filename}")

def create_github_assets(colors):
    """GitHub用アセットを作成"""
    
    # GitHub バナー
    banner_width, banner_height = 1280, 640
    banner = Image.new('RGB', (banner_width, banner_height), colors["dark"])
    draw = ImageDraw.Draw(banner)
    
    # グラデーション背景
    create_gradient_background(draw, banner_width, banner_height, 
                             colors["primary"], colors["accent"])
    
    # ロゴとテキスト
    center_x, center_y = banner_width // 2, banner_height // 2
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        
        # タイトル
        draw.text((center_x, center_y - 80), "🧠 MindBridge", fill=(255, 255, 255), 
                 font=title_font, anchor="mm")
        
        # サブタイトル
        draw.text((center_x, center_y - 20), "Private AI Assistant for iOS", 
                 fill=(255, 255, 255), font=subtitle_font, anchor="mm")
        
        # 説明
        draw.text((center_x, center_y + 30), "Qwen3-4B • Offline • Open Source • Privacy-First", 
                 fill=(200, 200, 200), font=desc_font, anchor="mm")
        
    except:
        pass
    
    banner.save("GitHub_Banner.png", 'PNG', quality=100)
    print("✅ Created: GitHub_Banner.png")
    
    # GitHub アバター/ロゴ
    avatar_size = 400
    avatar = Image.new('RGB', (avatar_size, avatar_size), colors["primary"])
    draw = ImageDraw.Draw(avatar)
    
    # 円形背景
    draw.ellipse([10, 10, avatar_size-10, avatar_size-10], fill=colors["primary"])
    
    # シンプルなアイコン
    center = avatar_size // 2
    draw_brain_bridge_icon(draw, center, center, 150, colors["light"], 1.0)
    
    avatar.save("GitHub_Avatar.png", 'PNG', quality=100)
    print("✅ Created: GitHub_Avatar.png")

def draw_brain_icon(draw, x, y, size, color):
    """脳のアイコンを描画"""
    # シンプルな脳の形（楕円とカーブ）
    brain_width = int(size * 0.8)
    brain_height = int(size * 0.6)
    
    # メイン部分
    draw.ellipse([x - brain_width//2, y - brain_height//2, 
                  x + brain_width//2, y + brain_height//2], fill=color)
    
    # 脳のしわを表現
    for i in range(3):
        offset_y = (i - 1) * 15
        draw.arc([x - brain_width//2 + 10, y + offset_y - 10, 
                  x + brain_width//2 - 10, y + offset_y + 10], 
                 0, 180, fill=color, width=3)

def draw_device_icon(draw, x, y, size, color):
    """デバイスアイコンを描画"""
    # スマートフォンの形
    device_width = int(size * 0.4)
    device_height = int(size * 0.7)
    
    # 本体
    draw_rounded_rectangle(draw, x - device_width//2, y - device_height//2,
                          x + device_width//2, y + device_height//2,
                          8, color)
    
    # 画面
    screen_margin = 4
    draw_rounded_rectangle(draw, x - device_width//2 + screen_margin, 
                          y - device_height//2 + screen_margin*2,
                          x + device_width//2 - screen_margin, 
                          y + device_height//2 - screen_margin*3,
                          4, (100, 100, 100))

def draw_neural_bridge(draw, x1, y1, x2, y2, color):
    """ニューラルネットワーク風の接続線を描画"""
    # メインライン
    draw.line([x1, y1, x2, y2], fill=color, width=4)
    
    # パーティクル効果
    for i in range(5):
        ratio = (i + 1) / 6
        px = int(x1 + (x2 - x1) * ratio)
        py = int(y1 + (y2 - y1) * ratio)
        radius = 3 + (i % 2) * 2
        draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=color)

def draw_brain_bridge_icon(draw, center_x, center_y, size, color, scale):
    """アプリアイコン用のシンプルな脳-ブリッジアイコン"""
    # 左の円（脳）
    left_radius = int(size * 0.15)
    left_x = center_x - int(size * 0.2)
    draw.ellipse([left_x - left_radius, center_y - left_radius,
                  left_x + left_radius, center_y + left_radius], fill=color)
    
    # 右の円（デバイス）
    right_radius = int(size * 0.12)
    right_x = center_x + int(size * 0.2)
    draw.ellipse([right_x - right_radius, center_y - right_radius,
                  right_x + right_radius, center_y + right_radius], fill=color)
    
    # 接続線
    line_width = max(int(4 * scale), 2)
    draw.line([left_x + left_radius, center_y, right_x - right_radius, center_y], 
              fill=color, width=line_width)
    
    # 中央のノード
    center_radius = max(int(8 * scale), 3)
    draw.ellipse([center_x - center_radius, center_y - center_radius,
                  center_x + center_radius, center_y + center_radius], fill=color)

def create_gradient_background(draw, width, height, start_color, end_color):
    """グラデーション背景を作成"""
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)

def create_circular_gradient(draw, width, height, center_color, edge_color):
    """円形グラデーションを作成"""
    center_x, center_y = width // 2, height // 2
    max_radius = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = min(distance / max_radius, 1.0)
            
            r = int(center_color[0] + (edge_color[0] - center_color[0]) * ratio)
            g = int(center_color[1] + (edge_color[1] - center_color[1]) * ratio)
            b = int(center_color[2] + (edge_color[2] - center_color[2]) * ratio)
            
            draw.point((x, y), fill=(r, g, b))

def draw_rounded_rectangle(draw, x1, y1, x2, y2, radius, fill):
    """角丸四角形を描画"""
    # メイン四角形
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # 角の円
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

def save_brand_guide(colors):
    """ブランドガイドをJSONで保存"""
    brand_guide = {
        "brand_name": "MindBridge",
        "tagline": "Private AI Assistant",
        "description": "Connect your mind to AI, privately and securely",
        "colors": {
            "primary": f"rgb{colors['primary']}",
            "secondary": f"rgb{colors['secondary']}",
            "accent": f"rgb{colors['accent']}",
            "dark": f"rgb{colors['dark']}",
            "light": f"rgb{colors['light']}"
        },
        "fonts": {
            "primary": "Arial Bold",
            "secondary": "Arial",
            "code": "Monaco, Menlo, monospace"
        },
        "tone": [
            "Professional yet approachable",
            "Privacy-focused",
            "Innovation-driven",
            "User-centric"
        ],
        "key_features": [
            "🧠 AI-powered conversations",
            "🔒 Complete privacy protection", 
            "📱 iOS optimized",
            "⚡ Fast offline processing",
            "🌍 Multi-language support"
        ]
    }
    
    with open("MindBridge_Brand_Guide.json", "w", encoding="utf-8") as f:
        json.dump(brand_guide, f, ensure_ascii=False, indent=2)
    
    print("✅ Created: MindBridge_Brand_Guide.json")

if __name__ == "__main__":
    print("🎨 MindBridge ブランドデザイン生成中...")
    create_mindbridge_brand()
    print("✨ ブランドデザイン完成！")