
class Triple {
  head string @description("head entity of the triple ")
  relation "INTERACTS_WITH" @description("relationship type")
  tail string @description("tail entity name of the triple")
  // confidence ("high" | "low")? @description("if this relation was extracted with high confidence or not")
  @@dynamic
}

class Triples {
  triples Triple[] @description("list of triples that describe interactions between two biological entities")
}

class Entities {
  entities string[] @description("list of biological entities")
}

class Message {
  role "user" | "assistant"
  content string
}


function GeneralChatExtractRelationships(sys_prompt: string, text: string, messages: Message[]) -> Triples {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {{ _.role("system") }}
    {{ sys_prompt }}
    TEXT: {{ text }}
    {{ ctx.output_format(prefix="Use the following OUTPUT FORMAT:") }}
    {% for message in messages %}
      {{ _.role(message.role) }} 
      {{ message.content }}
    {% endfor %}
  "#
}

function ExtractNEs(sys_prompt: string, text: string, message: Message) -> Entities {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {{ _.role("system") }}
    {{ sys_prompt }}
    TEXT: {{ text }}
    {{ ctx.output_format(prefix="Use the following OUTPUT FORMAT:") }}
    USER QUESTION:
    {{ _.role(message.role) }} 
    {{ message.content }}
  "#
}
