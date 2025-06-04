//
//  Use this file to import your target's public headers that you would like to expose to Swift.
//

#ifndef Qwen3iOS_Bridging_Header_h
#define Qwen3iOS_Bridging_Header_h

#ifdef __cplusplus
extern "C" {
#endif

// llama.cpp context
typedef void* llama_context;

// Initialize llama model
llama_context llama_init_model(const char* model_path);

// Generate text
const char* llama_generate(llama_context ctx, const char* prompt, float temperature, int max_tokens, float top_p);

// Free context
void llama_free_context(llama_context ctx);

// Model info
int llama_get_vocab_size(llama_context ctx);
int llama_get_context_size(llama_context ctx);

#ifdef __cplusplus
}
#endif

#endif /* Qwen3iOS_Bridging_Header_h */