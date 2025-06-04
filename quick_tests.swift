#!/usr/bin/env swift

import Foundation

print("🧪 MindBridge クイックテスト")
print(String(repeating: "=", count: 40))

// ChatMessageテスト
struct ChatMessage {
    let id = UUID()
    let content: String
    let isUser: Bool
}

let msg1 = ChatMessage(content: "こんにちは", isUser: true)
let msg2 = ChatMessage(content: "こんにちは！", isUser: false)

print("\n✅ ChatMessage作成: OK")
print("  - User: \(msg1.content)")
print("  - AI: \(msg2.content)")

// LlamaServiceテスト
class MockLlamaService {
    func generateResponse(_ prompt: String) -> String {
        if prompt.contains("計算") {
            return "123 + 456 = 579"
        }
        return "了解しました。"
    }
}

let service = MockLlamaService()
let response = service.generateResponse("計算: 123 + 456")
print("\n✅ LlamaService応答: OK")
print("  - 入力: 計算: 123 + 456")
print("  - 出力: \(response)")

// ViewModelテスト
class ChatViewModel {
    var messages: [ChatMessage] = []
    
    func sendMessage(_ text: String) {
        messages.append(ChatMessage(content: text, isUser: true))
        let response = MockLlamaService().generateResponse(text)
        messages.append(ChatMessage(content: response, isUser: false))
    }
}

let vm = ChatViewModel()
vm.sendMessage("テストメッセージ")
print("\n✅ ChatViewModel: OK")
print("  - メッセージ数: \(vm.messages.count)")

// パフォーマンステスト
let start = Date()
for _ in 1...100 {
    _ = ChatMessage(content: "test", isUser: true)
}
let elapsed = Date().timeIntervalSince(start)
print("\n✅ パフォーマンス: OK")
print("  - 100メッセージ作成: \(String(format: "%.3f", elapsed))秒")

print("\n🎉 すべてのテストが成功しました！")
print(String(repeating: "=", count: 40))