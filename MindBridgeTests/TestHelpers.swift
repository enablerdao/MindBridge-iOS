import XCTest
import Foundation
@testable import MindBridge

// MARK: - XCTestCase Extensions

extension XCTestCase {
    /// Waits for an async operation with a timeout
    func waitForAsync(
        timeout: TimeInterval = 5.0,
        file: StaticString = #file,
        line: UInt = #line,
        operation: @escaping () async throws -> Void
    ) {
        let expectation = expectation(description: "Async operation")
        
        Task {
            do {
                try await operation()
                expectation.fulfill()
            } catch {
                XCTFail("Async operation failed: \(error)", file: file, line: line)
            }
        }
        
        wait(for: [expectation], timeout: timeout)
    }
}

// MARK: - Test Data Generators

struct TestDataGenerator {
    
    /// Generates a random Japanese string of specified length
    static func randomJapaneseString(length: Int) -> String {
        let hiragana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
        return String((0..<length).map { _ in hiragana.randomElement()! })
    }
    
    /// Generates a mock chat conversation
    static func mockConversation(messageCount: Int) -> [(content: String, isUser: Bool)] {
        let userPrompts = [
            "こんにちは！",
            "今日の天気はどうですか？",
            "プログラミングについて教えて",
            "Swift言語の特徴は？",
            "おすすめの本はありますか？"
        ]
        
        let aiResponses = [
            "こんにちは！今日はどのようなお手伝いができますか？",
            "申し訳ございませんが、リアルタイムの天気情報にはアクセスできません。",
            "プログラミングは、コンピュータに指示を与えるための言語を使って問題を解決する技術です。",
            "Swiftは、Appleが開発した安全で高速なプログラミング言語です。",
            "どのようなジャンルの本をお探しですか？"
        ]
        
        var conversation: [(String, Bool)] = []
        
        for i in 0..<messageCount {
            if i % 2 == 0 {
                conversation.append((userPrompts[i % userPrompts.count], true))
            } else {
                conversation.append((aiResponses[i % aiResponses.count], false))
            }
        }
        
        return conversation
    }
    
    /// Generates a mock model info
    @available(iOS 16.0, macOS 13.0, *)
    static func mockModelInfo(
        name: String = "Test Model",
        size: String = "1.0GB",
        quantization: String = "Q4_K_M"
    ) -> ModelInfo {
        return ModelInfo(
            name: name,
            fileName: "\(name.lowercased().replacingOccurrences(of: " ", with: "-")).gguf",
            url: "https://example.com/\(name.lowercased()).gguf",
            size: size,
            quantization: quantization
        )
    }
}

// MARK: - Performance Testing Helpers

struct PerformanceTestHelper {
    
    /// Measures the execution time of a block
    static func measureTime(block: () throws -> Void) rethrows -> TimeInterval {
        let startTime = CFAbsoluteTimeGetCurrent()
        try block()
        let endTime = CFAbsoluteTimeGetCurrent()
        return endTime - startTime
    }
    
    /// Measures memory usage before and after a block
    static func measureMemory(block: () throws -> Void) rethrows -> (before: Int, after: Int, delta: Int) {
        let beforeMemory = getMemoryUsage()
        try block()
        let afterMemory = getMemoryUsage()
        return (beforeMemory, afterMemory, afterMemory - beforeMemory)
    }
    
    private static func getMemoryUsage() -> Int {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size) / 4
        
        let result = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_,
                         task_flavor_t(MACH_TASK_BASIC_INFO),
                         $0,
                         &count)
            }
        }
        
        return result == KERN_SUCCESS ? Int(info.resident_size) : 0
    }
}

// MARK: - Async Testing Utilities

actor AsyncTestUtility {
    private var completedOperations: Set<String> = []
    
    func markCompleted(_ operation: String) {
        completedOperations.insert(operation)
    }
    
    func isCompleted(_ operation: String) -> Bool {
        return completedOperations.contains(operation)
    }
    
    func reset() {
        completedOperations.removeAll()
    }
}

// MARK: - Mock Network Session

class MockNetworkSession {
    var responses: [URL: (data: Data?, response: URLResponse?, error: Error?)] = [:]
    
    func setMockResponse(for url: URL, data: Data?, response: URLResponse?, error: Error?) {
        responses[url] = (data, response, error)
    }
    
    func data(from url: URL) async throws -> (Data, URLResponse) {
        guard let mockResponse = responses[url] else {
            throw URLError(.fileDoesNotExist)
        }
        
        if let error = mockResponse.error {
            throw error
        }
        
        let data = mockResponse.data ?? Data()
        let response = mockResponse.response ?? URLResponse(
            url: url,
            mimeType: "application/json",
            expectedContentLength: data.count,
            textEncodingName: nil
        )
        
        return (data, response)
    }
}