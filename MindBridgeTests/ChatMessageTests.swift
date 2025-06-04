import XCTest
@testable import MindBridge

final class ChatMessageTests: XCTestCase {
    
    // MARK: - Initialization Tests
    
    func testChatMessageInitialization() {
        // Given
        let content = "テストメッセージ"
        let isUser = true
        
        // When
        let message = ChatMessage(content: content, isUser: isUser)
        
        // Then
        XCTAssertEqual(message.content, content)
        XCTAssertEqual(message.isUser, isUser)
        XCTAssertNotNil(message.id)
        XCTAssertNotNil(message.timestamp)
    }
    
    func testUserMessageCreation() {
        // Given
        let userContent = "こんにちは、Qwen3！"
        
        // When
        let userMessage = ChatMessage(content: userContent, isUser: true)
        
        // Then
        XCTAssertTrue(userMessage.isUser)
        XCTAssertEqual(userMessage.content, userContent)
    }
    
    func testAIMessageCreation() {
        // Given
        let aiContent = "こんにちは！今日はどのようなお手伝いができますか？"
        
        // When
        let aiMessage = ChatMessage(content: aiContent, isUser: false)
        
        // Then
        XCTAssertFalse(aiMessage.isUser)
        XCTAssertEqual(aiMessage.content, aiContent)
    }
    
    // MARK: - Identifiable Protocol Tests
    
    func testUniqueIdentifiers() {
        // Given & When
        let message1 = ChatMessage(content: "メッセージ1", isUser: true)
        let message2 = ChatMessage(content: "メッセージ2", isUser: false)
        
        // Then
        XCTAssertNotEqual(message1.id, message2.id)
    }
    
    // MARK: - Timestamp Tests
    
    func testTimestampOrdering() {
        // Given
        let message1 = ChatMessage(content: "最初のメッセージ", isUser: true)
        
        // Small delay to ensure different timestamps
        Thread.sleep(forTimeInterval: 0.001)
        
        let message2 = ChatMessage(content: "次のメッセージ", isUser: false)
        
        // Then
        XCTAssertLessThan(message1.timestamp, message2.timestamp)
    }
    
    func testTimestampIsCurrentDate() {
        // Given
        let beforeCreation = Date()
        
        // When
        let message = ChatMessage(content: "テスト", isUser: true)
        let afterCreation = Date()
        
        // Then
        XCTAssertGreaterThanOrEqual(message.timestamp, beforeCreation)
        XCTAssertLessThanOrEqual(message.timestamp, afterCreation)
    }
    
    // MARK: - Content Tests
    
    func testEmptyContent() {
        // Given & When
        let message = ChatMessage(content: "", isUser: true)
        
        // Then
        XCTAssertEqual(message.content, "")
    }
    
    func testLongContent() {
        // Given
        let longContent = String(repeating: "あ", count: 1000)
        
        // When
        let message = ChatMessage(content: longContent, isUser: false)
        
        // Then
        XCTAssertEqual(message.content, longContent)
        XCTAssertEqual(message.content.count, 1000)
    }
    
    func testSpecialCharactersInContent() {
        // Given
        let specialContent = "絵文字😀、改行\n、タブ\t、記号!@#$%"
        
        // When
        let message = ChatMessage(content: specialContent, isUser: true)
        
        // Then
        XCTAssertEqual(message.content, specialContent)
    }
}