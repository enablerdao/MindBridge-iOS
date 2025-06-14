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
                                    Text("thinking".localized)
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
                    TextField("chat_placeholder".localized, text: $messageText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .disabled(isLoading)
                        .accessibilityLabel("accessibility_message_input".localized)
                    
                    Button(action: sendMessage) {
                        Image(systemName: "paperplane.fill")
                            .foregroundColor(.white)
                            .padding(8)
                            .background(messageText.isEmpty || isLoading ? Color.gray : Color.blue)
                            .cornerRadius(8)
                    }
                    .disabled(messageText.isEmpty || isLoading)
                    .accessibilityLabel("accessibility_send_button".localized)
                }
                .padding()
            }
            .navigationTitle("app_name".localized)
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button(action: { chatViewModel.showSettings = true }) {
                        Image(systemName: "gear")
                    }
                    .accessibilityLabel("accessibility_settings_button".localized)
                }
            }
        }
        .sheet(isPresented: $chatViewModel.showSettings) {
            SettingsView(viewModel: chatViewModel)
        }
        .localized()
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
                Text(message.isUser ? "user_message".localized : "ai_message".localized)
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