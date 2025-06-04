import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ContentView: View {
    @StateObject private var chatViewModel = ChatViewModel()
    @StateObject private var localizationManager = LocalizationManager.shared
    @State private var messageText = ""
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            VStack {
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 16) {
                            ForEach(chatViewModel.messages) { message in
                                MessageBubble(message: message)
                                    .id(message.id)
                            }
                            
                            if isLoading {
                                HStack {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle())
                                    Text("思考中...")
                                        .foregroundColor(.gray)
                                }
                                .padding()
                            }
                        }
                        .padding()
                    }
                    .onChange(of: chatViewModel.messages.count) { _ in
                        withAnimation {
                            proxy.scrollTo(chatViewModel.messages.last?.id, anchor: .bottom)
                        }
                    }
                }
                
                HStack {
                    TextField("メッセージを入力", text: $messageText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .disabled(isLoading)
                    
                    Button(action: sendMessage) {
                        Image(systemName: "paperplane.fill")
                            .foregroundColor(.white)
                            .padding(8)
                            .background(messageText.isEmpty || isLoading ? Color.gray : Color.blue)
                            .cornerRadius(8)
                    }
                    .disabled(messageText.isEmpty || isLoading)
                }
                .padding()
            }
            .navigationTitle("Qwen3-4B Chat")
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button(action: { chatViewModel.showSettings = true }) {
                        Image(systemName: "gear")
                    }
                }
            }
        }
        .sheet(isPresented: $chatViewModel.showSettings) {
            SettingsView(viewModel: chatViewModel)
        }
        .onAppear {
            chatViewModel.initializeModel()
        }
    }
    
    private func sendMessage() {
        let userMessage = messageText
        messageText = ""
        isLoading = true
        
        Task {
            await chatViewModel.sendMessage(userMessage)
            isLoading = false
        }
    }
}

@available(iOS 16.0, macOS 13.0, *)
struct MessageBubble: View {
    let message: ChatMessage
    
    var body: some View {
        HStack {
            if message.isUser {
                Spacer()
            }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                Text(message.isUser ? "あなた" : "Qwen3")
                    .font(.caption)
                    .foregroundColor(.gray)
                
                Text(message.content)
                    .padding(12)
                    .background(message.isUser ? Color.blue : Color.gray.opacity(0.2))
                    .foregroundColor(message.isUser ? .white : .primary)
                    .cornerRadius(16)
            }
            
            if !message.isUser {
                Spacer()
            }
        }
    }
}

@available(iOS 16.0, macOS 13.0, *)
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}