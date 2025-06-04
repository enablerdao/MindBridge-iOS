#!/bin/bash

# Qwen3iOS ビルドスクリプト

set -e

echo "🔨 Qwen3iOS ビルドスクリプト"
echo "=============================="

# カラー定義
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 1. llama.cpp サブモジュールの確認
echo "📦 llama.cpp サブモジュールをチェック中..."
if [ ! -d "Sources/LlamaCpp/.git" ]; then
    echo "llama.cpp サブモジュールを追加中..."
    git submodule add https://github.com/ggerganov/llama.cpp.git Sources/LlamaCpp
fi
git submodule update --init --recursive

# 2. モデルファイルの確認
MODEL_PATH="Resources/qwen3-4b-instruct-q4_k_m.gguf"
if [ ! -f "$MODEL_PATH" ]; then
    echo -e "${RED}⚠️  モデルファイルが見つかりません: $MODEL_PATH${NC}"
    echo "以下のコマンドでダウンロードしてください："
    echo "wget https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q4_k_m.gguf -P Resources/"
    exit 1
fi

# 3. Xcodeビルド
echo "🏗️  Xcodeプロジェクトをビルド中..."
xcodebuild clean build \
    -project Qwen3iOS.xcodeproj \
    -scheme Qwen3iOS \
    -configuration Release \
    -sdk iphoneos \
    CODE_SIGN_IDENTITY="" \
    CODE_SIGNING_REQUIRED=NO \
    CODE_SIGNING_ALLOWED=NO

# 4. シミュレータ用ビルド
echo "📱 シミュレータ用にビルド中..."
xcodebuild build \
    -project Qwen3iOS.xcodeproj \
    -scheme Qwen3iOS \
    -configuration Debug \
    -sdk iphonesimulator \
    -destination 'platform=iOS Simulator,name=iPhone 15'

echo -e "${GREEN}✅ ビルド完了！${NC}"
echo "Xcodeでプロジェクトを開いて実行してください："
echo "open Qwen3iOS.xcodeproj"