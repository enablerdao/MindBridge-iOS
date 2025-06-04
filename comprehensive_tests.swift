#!/usr/bin/env swift

import Foundation

// MARK: - Test Framework
class TestCase {
    var passed = 0
    var failed = 0
    var testName = ""
    
    func describe(_ name: String, _ tests: () -> Void) {
        print("\n🧪 \(name)")
        print(String(repeating: "=", count: 50))
        testName = name
        tests()
    }
    
    func it(_ description: String, _ test: () throws -> Void) {
        do {
            try test()
            passed += 1
            print("  ✅ \(description)")
        } catch {
            failed += 1
            print("  ❌ \(description) - Error: \(error)")
        }
    }
    
    func expect<T: Equatable>(_ actual: T) -> Expectation<T> {
        return Expectation(actual)
    }
    
    func summary() {
        print("\n📊 テスト結果サマリー")
        print(String(repeating: "=", count: 50))
        print("✅ 成功: \(passed)")
        print("❌ 失敗: \(failed)")
        print("📝 合計: \(passed + failed)")
        let successRate = Double(passed) / Double(passed + failed) * 100
        print("📈 成功率: \(String(format: "%.1f", successRate))%")
        
        if failed == 0 {
            print("\n🎉 すべてのテストが成功しました！")
        } else {
            print("\n⚠️  一部のテストが失敗しました")
        }
    }
}

class Expectation<T: Equatable> {
    let actual: T
    
    init(_ actual: T) {
        self.actual = actual
    }
    
    func toBe(_ expected: T) throws {
        if actual != expected {
            throw TestError.assertionFailed(
                "Expected \(expected) but got \(actual)"
            )
        }
    }
    
    func toBeTrue() throws where T == Bool {
        if actual != true {
            throw TestError.assertionFailed(
                "Expected true but got false"
            )
        }
    }
}

enum TestError: Error {
    case assertionFailed(String)
}

// MARK: - Mock Objects
struct ChatMessage {
    let id = UUID()
    let content: String
    let isUser: Bool
    let timestamp = Date()
}

class MockLlamaService {
    var temperature: Double = 0.7
    var maxTokens: Double = 512
    var topP: Double = 0.9
    
    func generateResponse(prompt: String, completion: @escaping (String) -> Void) {
        // シミュレート応答
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            switch prompt.lowercased() {
            case let p where p.contains("計算"):
                completion("計算結果: 123 + 456 = 579 です。")
            case let p where p.contains("qwen"):
                completion("私はQwen3-4Bモデルです。日本語を含む多言語に対応しています。")
            case let p where p.contains("天気"):
                completion("申し訳ございませんが、リアルタイムの天気情報は提供できません。")
            default:
                completion("ご質問ありがとうございます。どのようにお手伝いしましょうか？")
            }
        }
    }
    
    func loadModel() throws {
        // モデル読み込みのシミュレート
        Thread.sleep(forTimeInterval: 0.1)
    }
}

class MockChatViewModel {
    var messages: [ChatMessage] = []
    let llamaService = MockLlamaService()
    
    func sendMessage(_ content: String) {
        messages.append(ChatMessage(content: content, isUser: true))
        
        llamaService.generateResponse(prompt: content) { response in
            self.messages.append(ChatMessage(content: response, isUser: false))
        }
    }
    
    func clearMessages() {
        messages.removeAll()
    }
}

// MARK: - Tests
let test = TestCase()

// ChatMessage Tests
test.describe("ChatMessage モデルテスト") {
    test.it("メッセージが正しく作成される") {
        let message = ChatMessage(content: "Hello", isUser: true)
        try test.expect(message.content).toBe("Hello")
        try test.expect(message.isUser).toBeTrue()
    }
    
    test.it("各メッセージが一意のIDを持つ") {
        let message1 = ChatMessage(content: "Test1", isUser: true)
        let message2 = ChatMessage(content: "Test2", isUser: false)
        try test.expect(message1.id == message2.id).toBe(false)
    }
}

// LlamaService Tests
test.describe("LlamaService モックテスト") {
    test.it("モデルが正常に読み込まれる") {
        let service = MockLlamaService()
        do {
            try service.loadModel()
            try test.expect(true).toBeTrue()
        } catch {
            throw error
        }
    }
    
    test.it("設定値が正しく保持される") {
        let service = MockLlamaService()
        try test.expect(service.temperature).toBe(0.7)
        try test.expect(service.maxTokens).toBe(512)
        try test.expect(service.topP).toBe(0.9)
    }
    
    test.it("計算リクエストに正しく応答する") {
        let service = MockLlamaService()
        let expectation = DispatchSemaphore(value: 0)
        var response = ""
        
        service.generateResponse(prompt: "計算して: 123 + 456") { result in
            response = result
            expectation.signal()
        }
        
        expectation.wait()
        try test.expect(response.contains("579")).toBeTrue()
    }
}

// ChatViewModel Tests
test.describe("ChatViewModel テスト") {
    test.it("メッセージが正しく送信される") {
        let viewModel = MockChatViewModel()
        viewModel.sendMessage("テストメッセージ")
        
        try test.expect(viewModel.messages.count).toBe(1)
        try test.expect(viewModel.messages[0].content).toBe("テストメッセージ")
        try test.expect(viewModel.messages[0].isUser).toBeTrue()
    }
    
    test.it("AIの応答が追加される") {
        let viewModel = MockChatViewModel()
        let expectation = DispatchSemaphore(value: 0)
        
        viewModel.sendMessage("Qwenについて")
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            expectation.signal()
        }
        
        expectation.wait()
        try test.expect(viewModel.messages.count).toBe(2)
        try test.expect(viewModel.messages[1].isUser).toBe(false)
    }
    
    test.it("メッセージ履歴がクリアされる") {
        let viewModel = MockChatViewModel()
        viewModel.sendMessage("メッセージ1")
        viewModel.sendMessage("メッセージ2")
        viewModel.clearMessages()
        
        try test.expect(viewModel.messages.count).toBe(0)
    }
}

// Performance Tests
test.describe("パフォーマンステスト") {
    test.it("応答時間が1秒以内") {
        let service = MockLlamaService()
        let start = Date()
        let expectation = DispatchSemaphore(value: 0)
        
        service.generateResponse(prompt: "テスト") { _ in
            expectation.signal()
        }
        
        expectation.wait()
        let elapsed = Date().timeIntervalSince(start)
        try test.expect(elapsed < 1.0).toBeTrue()
    }
    
    test.it("複数のメッセージを高速に処理") {
        let viewModel = MockChatViewModel()
        let start = Date()
        
        for i in 1...10 {
            viewModel.sendMessage("メッセージ \(i)")
        }
        
        let elapsed = Date().timeIntervalSince(start)
        try test.expect(elapsed < 0.1).toBeTrue() // 同期的な追加は高速
    }
}

// Edge Cases Tests
test.describe("エッジケーステスト") {
    test.it("空の入力を処理できる") {
        let viewModel = MockChatViewModel()
        viewModel.sendMessage("")
        try test.expect(viewModel.messages.count).toBe(1)
    }
    
    test.it("長い入力を処理できる") {
        let longText = String(repeating: "あ", count: 1000)
        let viewModel = MockChatViewModel()
        viewModel.sendMessage(longText)
        try test.expect(viewModel.messages[0].content.count).toBe(1000)
    }
    
    test.it("特殊文字を含む入力を処理できる") {
        let specialText = "Hello 🚀 こんにちは 👋 ñ"
        let viewModel = MockChatViewModel()
        viewModel.sendMessage(specialText)
        try test.expect(viewModel.messages[0].content).toBe(specialText)
    }
}

// Integration Tests
test.describe("統合テスト") {
    test.it("完全なチャットフローが動作する") {
        let viewModel = MockChatViewModel()
        let expectation = DispatchSemaphore(value: 0)
        
        // ユーザーメッセージ送信
        viewModel.sendMessage("計算: 100 + 200")
        
        // AI応答を待つ
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            expectation.signal()
        }
        
        expectation.wait()
        
        // 結果を検証
        try test.expect(viewModel.messages.count).toBe(2)
        try test.expect(viewModel.messages[0].isUser).toBeTrue()
        try test.expect(viewModel.messages[1].isUser).toBe(false)
    }
}

// Run all tests
test.summary()

// Exit with appropriate code
exit(test.failed > 0 ? 1 : 0)