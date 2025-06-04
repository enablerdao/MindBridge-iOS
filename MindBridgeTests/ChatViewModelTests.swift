import XCTest
@testable import MindBridge

@available(iOS 16.0, macOS 13.0, *)
final class ChatViewModelTests: XCTestCase {
    
    var viewModel: ChatViewModel!
    
    @MainActor
    override func setUp() {
        super.setUp()
        viewModel = ChatViewModel()
    }
    
    @MainActor
    override func tearDown() {
        viewModel = nil
        super.tearDown()
    }
    
    // MARK: - Initialization Tests
    
    @MainActor
    func testInitialState() {
        // Then
        XCTAssertFalse(viewModel.showSettings)
        XCTAssertFalse(viewModel.isModelLoaded)
        XCTAssertEqual(viewModel.modelLoadingProgress, 0)
        XCTAssertEqual(viewModel.messages.count, 1)
        XCTAssertFalse(viewModel.messages[0].isUser)
        XCTAssertTrue(viewModel.messages[0].content.contains("Qwen3-4B"))
    }
    
    // MARK: - Message Management Tests
    
    @MainActor
    func testSendMessage() async {
        // Given
        let initialMessageCount = viewModel.messages.count
        let testMessage = "テストメッセージです"
        
        // When
        await viewModel.sendMessage(testMessage)
        
        // Then
        XCTAssertGreaterThan(viewModel.messages.count, initialMessageCount)
        
        // Check if user message was added
        let userMessage = viewModel.messages[viewModel.messages.count - 2]
        XCTAssertEqual(userMessage.content, testMessage)
        XCTAssertTrue(userMessage.isUser)
    }
    
    @MainActor
    func testClearChat() {
        // Given
        Task {
            await viewModel.sendMessage("メッセージ1")
            await viewModel.sendMessage("メッセージ2")
        }
        
        // When
        viewModel.clearChat()
        
        // Then
        XCTAssertEqual(viewModel.messages.count, 1)
        XCTAssertFalse(viewModel.messages[0].isUser)
        XCTAssertTrue(viewModel.messages[0].content.contains("クリアされました"))
    }
    
    // MARK: - Model Loading Tests
    
    @MainActor
    func testModelInitialization() {
        // Given
        XCTAssertFalse(viewModel.isModelLoaded)
        XCTAssertEqual(viewModel.modelLoadingProgress, 0)
        
        // When
        viewModel.initializeModel()
        
        // Then - Check that loading has started
        // Note: In real tests, we'd use XCTestExpectation for async operations
        XCTAssertGreaterThan(viewModel.modelLoadingProgress, 0)
    }
    
    // MARK: - Settings Tests
    
    @MainActor
    func testToggleSettings() {
        // Given
        let initialState = viewModel.showSettings
        
        // When
        viewModel.showSettings.toggle()
        
        // Then
        XCTAssertNotEqual(viewModel.showSettings, initialState)
    }
    
    // MARK: - Message Order Tests
    
    @MainActor
    func testMessageOrdering() async {
        // Given
        let messages = ["最初", "二番目", "三番目"]
        
        // When
        for message in messages {
            await viewModel.sendMessage(message)
        }
        
        // Then
        // Verify messages are in chronological order
        for i in 1..<viewModel.messages.count - 1 {
            XCTAssertLessThan(
                viewModel.messages[i].timestamp,
                viewModel.messages[i + 1].timestamp
            )
        }
    }
}

// MARK: - Mock LlamaService for Testing

class MockLlamaService {
    var shouldThrowError = false
    var responseDelay: TimeInterval = 0.1
    var mockResponse = "これはモックレスポンスです。"
    
    func loadModel() async throws {
        if shouldThrowError {
            throw LlamaServiceError.modelLoadFailed
        }
        // Simulate loading time
        try await Task.sleep(nanoseconds: UInt64(responseDelay * 1_000_000_000))
    }
    
    func generateResponse(prompt: String) async throws -> String {
        if shouldThrowError {
            throw LlamaServiceError.generationFailed
        }
        // Simulate processing time
        try await Task.sleep(nanoseconds: UInt64(responseDelay * 1_000_000_000))
        return mockResponse
    }
}

enum LlamaServiceError: Error, LocalizedError {
    case modelLoadFailed
    case generationFailed
    
    var errorDescription: String? {
        switch self {
        case .modelLoadFailed:
            return "モデルの読み込みに失敗しました"
        case .generationFailed:
            return "レスポンスの生成に失敗しました"
        }
    }
}