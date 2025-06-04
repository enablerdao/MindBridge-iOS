# 🧠 MindBridge - AI聊天助手

[![Swift](https://img.shields.io/badge/Swift-6.0-orange.svg)](https://swift.org)
[![iOS](https://img.shields.io/badge/iOS-16.0+-blue.svg)](https://developer.apple.com/ios/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**MindBridge** 是一款完全在设备上运行的私密AI聊天应用，采用Qwen3-4B-Instruct模型，提供真正的隐私保护。

## ✨ 主要特性

### 🔒 完全私密
- **设备端处理**: 所有AI计算都在您的设备上完成
- **零数据传输**: 对话内容绝不会发送到外部服务器
- **离线工作**: 设置完成后无需互联网连接

### 🇯🇵 优秀的多语言支持
- **原生日语支持**: 自然流畅的日语对话
- **多语言能力**: 支持日语、英语、中文、韩语等
- **文化理解**: 理解不同文化背景和商务习惯

### ⚡ 高性能AI
- **Qwen3-4B-Instruct**: 最先进的轻量级语言模型
- **Metal优化**: 充分利用Apple芯片的GPU性能
- **实时响应**: 快速的文本生成和回复

### 🎯 多样化应用
- 编程学习与辅助
- 创意写作支持
- 教育学习助手
- 商务咨询顾问
- 日常对话伙伴

## 📱 系统要求

- iOS 16.0 或更高版本
- A14仿生芯片或更高配置
- 约4GB存储空间（包含模型文件）
- 仅首次下载时需要网络连接

## 🚀 快速开始

### 安装

1. **克隆仓库**:
   ```bash
   git clone https://github.com/enablerdao/MindBridge-iOS.git
   cd MindBridge-iOS
   ```

2. **在Xcode中打开**:
   ```bash
   open Package.swift
   ```

3. **构建和运行**:
   - 在Xcode中选择目标设备
   - 按 `Cmd + R` 构建并运行

### 首次设置

1. 启动应用
2. 首次运行时会自动下载AI模型（约3.5GB）
3. 下载完成后即可开始对话

## 🛠️ 技术架构

### 核心技术
- **SwiftUI**: 现代化iOS用户界面
- **llama.cpp**: 高效的本地AI推理引擎
- **Metal Performance Shaders**: GPU加速计算
- **Core Data**: 本地数据存储和加密

### 项目结构
```
Sources/
├── MindBridge/
│   ├── ContentView.swift          # 主界面
│   ├── Models/
│   │   └── ChatMessage.swift      # 聊天消息模型
│   ├── ViewModels/
│   │   └── ChatViewModel.swift    # 聊天视图模型
│   ├── Views/
│   │   └── SettingsView.swift     # 设置界面
│   ├── Services/
│   │   ├── LlamaService.swift     # AI推理服务
│   │   ├── ModelDownloadService.swift # 模型下载
│   │   └── LocalizationManager.swift  # 多语言管理
│   └── Resources/                 # 多语言资源
│       ├── en.lproj/
│       ├── ja.lproj/
│       ├── zh-Hans.lproj/
│       └── ko.lproj/
└── LlamaCpp/                     # llama.cpp集成
```

## 🌐 多语言支持

MindBridge支持以下语言：
- 🇺🇸 English
- 🇯🇵 日本語 
- 🇨🇳 简体中文
- 🇰🇷 한국어

## 🧪 测试

运行测试套件：
```bash
swift test
```

包括的测试：
- 单元测试：消息模型、视图模型
- 集成测试：AI服务、模型下载
- UI测试：聊天界面、设置界面

## 📦 发布

### 手动构建
1. 在Xcode中选择 "Product" → "Archive"
2. 在Organizer中选择archive
3. 点击 "Distribute App"
4. 选择分发方式

### 自动化构建
我们使用GitHub Actions进行CI/CD：
- 自动测试所有pull request
- 发布时自动构建和分发

## 🤝 贡献

欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)。

### 开发流程
1. Fork此仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🙏 致谢

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - 高效的LLM推理
- [Qwen](https://github.com/QwenLM/Qwen) - 优秀的语言模型
- [SwiftUI](https://developer.apple.com/xcode/swiftui/) - 现代iOS开发框架

## 📞 支持

如有问题或建议，请：
- 查看[FAQ](docs/FAQ.md)
- 创建[Issue](https://github.com/enablerdao/MindBridge-iOS/issues)
- 参与[讨论](https://github.com/enablerdao/MindBridge-iOS/discussions)

---

**MindBridge** - 您的私人AI助手，保护隐私，增强智能。