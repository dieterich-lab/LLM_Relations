client<llm> Llama38b {
  provider "openai-generic"
  options {
    base_url "http://10.250.135.153:11434/v1"
    model llama3.1-128k:8b
    max_tokens 10000
    temperature 0.0
    num_ctx 128000
  }
}
