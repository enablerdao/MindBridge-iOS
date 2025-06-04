#!/bin/bash

echo "🔍 Checking test compilation..."
echo "==============================="

# Change to project directory
cd "$(dirname "$0")"

# Compile each test file individually to check for syntax errors
TEST_FILES=(
    "Qwen3iOSTests/TestHelpers.swift"
    "Qwen3iOSTests/ChatMessageTests.swift"
    "Qwen3iOSTests/ChatViewModelTests.swift"
    "Qwen3iOSTests/ModelDownloadServiceTests.swift"
    "Qwen3iOSTests/AllTests.swift"
)

# First compile the main module files that tests depend on
echo "📦 Compiling main module dependencies..."
swiftc -parse \
    -target arm64-apple-ios16.0-simulator \
    -sdk $(xcrun --sdk iphonesimulator --show-sdk-path) \
    Sources/Qwen3iOS/Models/ChatMessage.swift \
    Sources/Qwen3iOS/Services/ModelDownloadService.swift \
    Sources/Qwen3iOS/ViewModels/ChatViewModel.swift \
    2>&1 | grep -E "(error:|warning:|note:)" || echo "✅ Main module files compiled successfully"

echo ""
echo "🧪 Compiling test files..."

for file in "${TEST_FILES[@]}"; do
    echo -n "  Checking $file... "
    
    # Try to parse the file for syntax errors
    if swiftc -parse \
        -target arm64-apple-ios16.0-simulator \
        -sdk $(xcrun --sdk iphonesimulator --show-sdk-path) \
        -I Sources/Qwen3iOS \
        -enable-testing \
        "$file" 2>&1 | grep -E "(error:|warning:|note:)"; then
        echo "❌ Errors found"
    else
        echo "✅ OK"
    fi
done

echo ""
echo "✨ Compilation check complete!"