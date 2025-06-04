# Qwen3iOS Tests

このディレクトリには、Qwen3iOSアプリケーションのユニットテストとインテグレーションテストが含まれています。

## テスト構造

```
Qwen3iOSTests/
├── ChatMessageTests.swift      # ChatMessageモデルのテスト
├── ChatViewModelTests.swift    # ChatViewModelのテスト
├── ModelDownloadServiceTests.swift # ModelDownloadServiceのテスト
├── TestHelpers.swift          # テストユーティリティとヘルパー
├── AllTests.swift             # テストスイートランナー
└── Info.plist                 # テストバンドル設定
```

## テストの実行

### Xcodeから実行
1. Xcodeでプロジェクトを開く
2. `Product` → `Test` (または `⌘U`) を選択
3. 特定のテストを実行するには、テストナビゲーター（`⌘6`）から選択

### コマンドラインから実行
```bash
# すべてのテストを実行
xcodebuild test -project Qwen3iOS.xcodeproj -scheme Qwen3iOS -destination 'platform=iOS Simulator,name=iPhone 15'

# 特定のテストクラスを実行
xcodebuild test -project Qwen3iOS.xcodeproj -scheme Qwen3iOS -only-testing:Qwen3iOSTests/ChatMessageTests
```

## テストカバレッジ

各コンポーネントのテストカバレッジ目標：

- **Models**: 90%以上
  - ChatMessage: ✅ 完全カバー
  - ModelInfo: ✅ 完全カバー

- **ViewModels**: 80%以上
  - ChatViewModel: ✅ 基本機能カバー
  - 非同期処理のテスト含む

- **Services**: 70%以上
  - ModelDownloadService: ✅ モックを使用したテスト
  - ネットワーク処理はモック化

## テスト記述ガイドライン

### 1. テスト命名規則
```swift
func test<機能>_<条件>_<期待結果>() {
    // 例: testSendMessage_WithValidInput_AddsMessageToList
}
```

### 2. AAA パターン
```swift
func testExample() {
    // Arrange (準備)
    let input = "テストデータ"
    
    // Act (実行)
    let result = functionUnderTest(input)
    
    // Assert (検証)
    XCTAssertEqual(result, expectedValue)
}
```

### 3. 非同期テスト
```swift
func testAsyncOperation() async {
    // XCTestの async/await サポートを使用
    let result = await asyncFunction()
    XCTAssertNotNil(result)
}
```

## モックとスタブ

### MockLlamaService
LLMの推論をシミュレートするモックサービス：
```swift
class MockLlamaService {
    var mockResponse = "モックレスポンス"
    var shouldThrowError = false
}
```

### MockFileManager
ファイル操作をモック化：
```swift
class MockFileManager {
    var filesExist: [String: Bool] = [:]
}
```

### MockURLSession
ネットワーク通信をモック化：
```swift
class MockURLSession {
    var mockData: Data?
    var mockError: Error?
}
```

## パフォーマンステスト

```swift
func testPerformance() {
    measure {
        // パフォーマンスを測定するコード
    }
}
```

## 継続的インテグレーション

GitHub ActionsやXcode Cloudでの自動テスト実行に対応：

```yaml
# .github/workflows/test.yml の例
- name: Run Tests
  run: |
    xcodebuild test \
      -project Qwen3iOS.xcodeproj \
      -scheme Qwen3iOS \
      -destination 'platform=iOS Simulator,name=iPhone 15'
```

## トラブルシューティング

### テストが失敗する場合
1. シミュレーターのリセット: `Device` → `Erase All Content and Settings`
2. DerivedDataの削除: `~/Library/Developer/Xcode/DerivedData`
3. クリーンビルド: `Product` → `Clean Build Folder` (`⇧⌘K`)

### 非同期テストのタイムアウト
```swift
// タイムアウトを延長
func testWithLongerTimeout() async throws {
    let expectation = XCTestExpectation()
    expectation.timeout = 30.0 // 30秒
}
```

## 今後の改善点

- [ ] UIテストの追加 (XCUITest)
- [ ] スナップショットテストの導入
- [ ] コードカバレッジレポートの自動生成
- [ ] モックデータの外部ファイル化
- [ ] パフォーマンスベンチマークの追加