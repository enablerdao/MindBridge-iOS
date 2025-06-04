#ifndef LLAMA_H
#define LLAMA_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Forward declarations
struct llama_model;
struct llama_context;

typedef int32_t llama_pos;
typedef int32_t llama_token;
typedef int32_t llama_seq_id;

// Model parameters
struct llama_model_params {
    int32_t n_gpu_layers;
    int32_t main_gpu;
    const float * tensor_split;
    bool vocab_only;
    bool use_mmap;
    bool use_mlock;
};

// Context parameters  
struct llama_context_params {
    uint32_t seed;
    uint32_t n_ctx;
    uint32_t n_batch;
    uint32_t n_threads;
    uint32_t n_threads_batch;
    int8_t   rope_scaling_type;
    float    rope_freq_base;
    float    rope_freq_scale;
    uint32_t yarn_ext_factor;
    float    yarn_attn_factor;
    float    yarn_beta_fast;
    float    yarn_beta_slow;
    uint32_t yarn_orig_ctx;
    float    defrag_thold;
    bool     embeddings;
    bool     offload_kqv;
    bool     do_pooling;
};

// Batch
struct llama_batch {
    int32_t n_tokens;
    llama_token  * token;
    float        * embd;
    llama_pos    * pos;
    int32_t      * n_seq_id;
    llama_seq_id ** seq_id;
    int8_t       * logits;
    llama_pos all_pos_0;
    llama_pos all_pos_1;
    llama_seq_id all_seq_id;
};

// Token data
struct llama_token_data {
    llama_token id;
    float logit;
    float p;
};

struct llama_token_data_array {
    llama_token_data * data;
    size_t size;
    bool sorted;
};

// API functions
void llama_backend_init(void);
void llama_backend_free(void);

struct llama_model_params llama_model_default_params(void);
struct llama_context_params llama_context_default_params(void);

struct llama_model * llama_load_model_from_file(
    const char * path_model,
    struct llama_model_params params);

void llama_free_model(struct llama_model * model);

struct llama_context * llama_new_context_with_model(
    struct llama_model * model,
    struct llama_context_params params);

void llama_free(struct llama_context * ctx);

int32_t llama_n_vocab(const struct llama_model * model);
int32_t llama_n_ctx(const struct llama_context * ctx);

struct llama_batch llama_batch_init(int32_t n_tokens, int32_t embd, int32_t n_seq_max);
void llama_batch_free(struct llama_batch batch);
void llama_batch_clear(struct llama_batch * batch);
void llama_batch_add(struct llama_batch * batch, llama_token id, llama_pos pos, const llama_seq_id * seq_ids, bool logits);

int32_t llama_tokenize(
    const struct llama_model * model,
    const char * text,
    int32_t text_len,
    llama_token * tokens,
    int32_t n_max_tokens,
    bool add_bos,
    bool special);

int32_t llama_token_to_piece(
    const struct llama_model * model,
    llama_token token,
    char * buf,
    int32_t length,
    int32_t lstrip,
    bool special);

int32_t llama_decode(struct llama_context * ctx, struct llama_batch batch);

float * llama_get_logits(struct llama_context * ctx);
float * llama_get_logits_ith(struct llama_context * ctx, int32_t i);

bool llama_token_is_eog(const struct llama_model * model, llama_token token);

// Sampling functions
void llama_sample_top_k(struct llama_context * ctx, llama_token_data_array * candidates, int32_t k, size_t min_keep);
void llama_sample_top_p(struct llama_context * ctx, llama_token_data_array * candidates, float p, size_t min_keep);
void llama_sample_temp(struct llama_context * ctx, llama_token_data_array * candidates, float temp);
llama_token llama_sample_token(struct llama_context * ctx, llama_token_data_array * candidates);

#ifdef __cplusplus
}
#endif

#endif // LLAMA_H