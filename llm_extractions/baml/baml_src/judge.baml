
class Reason {
  reason string @description("a concise scientific one-sentence that reason about a question")
}

function Judge(sys_prompt: string, text: string, reasoning: string, triple: string, prompt: string) -> Reason {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {{ _.role("system") }}
    {{ sys_prompt }}
    TEXT: {{ text }}
    TRIPLE: {{ triple }}
    REASONING: {{ reasoning }}
    USER QUESTION:
    {{ _.role("user") }}
    {{ prompt }}
    {{ ctx.output_format(prefix="Use the following OUTPUT FORMAT:") }}
  "#
}

class Judgement {
  judgement "correct" | "incorrect" @description("the answer if a given evaluation was correct or incorrect")
}

function Correct(sys_prompt: string, text: string, reasoning: string, triple: string, prompt: string) -> Judgement {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {{ _.role("system") }}
    {{ sys_prompt }}
    TEXT: {{ text }}
    TRIPLE: {{ triple }}
    REASONING: {{ reasoning }}
    USER QUESTION:
    {{ _.role("user") }}
    {{ prompt }}
    {{ ctx.output_format(prefix="Use the following OUTPUT FORMAT:") }}
  "#
}
