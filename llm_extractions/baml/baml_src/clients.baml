// // Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

// // https://docs.boundaryml.com/docs/snippets/clients/retry
// retry_policy Constant {
//   max_retries 3
//   // Strategy is optional
//   strategy {
//     type constant_delay
//     delay_ms 200
//   }
// }


client<llm> Llama33 {
  provider "openai-generic"
//   retry_policy Exponential
//   retry_policy Constant
  options {
    base_url "http://10.250.135.153:11434/v1"
    model llama3.3-128k:70b
    max_tokens 10000
    temperature 0.0
  }
}

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

client<llm> Deepseek8b {
  provider "openai-generic"
  options {
    base_url "http://10.250.135.153:11434/v1"
    model deepseek-r1-128k:8b
    max_tokens 10000
    temperature 0.0
  }
}

client<llm> Deepseek70b {
  provider "openai-generic"
  options {
    base_url "http://10.250.135.153:11434/v1"
    model deepseek-r1-128k:70b
    max_tokens 10000
    temperature 0.0
  }
}

// retry_policy Exponential {
//   max_retries 2
//   // Strategy is optional
//   strategy {
//     type exponential_backoff
//     delay_ms 300
//     mutliplier 1.5
//     max_delay_ms 10000
//   }
