
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

// Tree-of-Thoughts (ToT) classes
class ExtractionStrategy {
  name string @description("Brief name for this extraction strategy (3-5 words)")
  focus string @description("What textual patterns and evidence types this strategy should focus on")
  avoid string @description("What common false positives this strategy should avoid")
}

class ExtractionStrategies {
  strategies ExtractionStrategy[] @description("List of different reasoning approaches for extracting relations")
}

class EvaluatedTriple {
  head string @description("head entity of the triple")
  relation "INTERACTS_WITH" @description("relationship type")
  tail string @description("tail entity of the triple")
  score int @description("Quality score from 1-10 based on textual evidence strength")
  evidence string @description("Brief quote or description from text supporting this relation")
}

class PathEvaluation {
  evaluated_triples EvaluatedTriple[] @description("List of extracted relations with quality scores")
  summary string @description("Brief assessment of this extraction path's overall quality")
}


function GeneralChatExtractRelationships(messages: Message[]) -> Triples {
// function GeneralChatExtractRelationships(sys_prompt: string, text: string, messages: Message[]) -> Triples {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {% for message in messages %}
      {{ _.role(message.role) }} 
      {{ message.content }}\n\n
    {% endfor %}
    {{ ctx.output_format(prefix="\n\nUse the following OUTPUT FORMAT:") }}
    Remember to ONLY extract relations from the given TEXT, not from prior knowledge or examples.
  "#
}

// function ExtractNEs(sys_prompt: string, text: string, message: Message) -> Entities {
function ExtractNEs(messages: Message[]) -> Entities {
  client Llama38b // will be overruled by the client registry
  prompt #"
    {% for message in messages %}
      {{ _.role(message.role) }} 
      {{ message.content }}
      \n
    {% endfor %}
    {{ ctx.output_format(prefix="\nUse the following OUTPUT FORMAT:") }}
  "#
}

// Tree-of-Thoughts functions
function GenerateToTStrategies(task_description: string, n_paths: int, text: string) -> ExtractionStrategies {
  client Llama38b
  prompt #"
    {{ _.role("system") }}
    You are an expert in designing systematic extraction strategies for biomedical relation extraction.
    
    {{ _.role("user") }}
    Your task: {{ task_description }}
    
    Generate {{ n_paths }} different reasoning strategies for extracting these relations from scientific text.
    Each strategy should focus on a different aspect of how relations are described in biomedical literature.
    
    Consider strategies based on:
    - Explicit interaction verbs (binds, phosphorylates, activates, etc.)
    - Experimental evidence (co-IP, pull-down, Y2H, etc.)
    - Mechanistic details (domains, residues, stoichiometry)
    - Signaling pathway context (cascades, upstream/downstream)
    - Post-translational modifications (kinase-substrate, PTMs)
    
    For each strategy, specify:
    1. A clear name
    2. What textual patterns to focus on
    3. What common false positives to avoid
    
    TEXT (for context): {{ text }}
    
    {{ ctx.output_format }}
  "#
}

function EvaluateToTPath(text: string, extracted_triples: Triples, strategy_name: string, task_description: string) -> PathEvaluation {
  client Llama38b
  prompt #"
    {{ _.role("system") }}
    You are an expert evaluator of biomedical relation extraction quality.
    
    {{ _.role("user") }}
    Task: {{ task_description }}
    Strategy used: {{ strategy_name }}
    
    TEXT: {{ text }}
    
    EXTRACTED RELATIONS:
    {% for triple in extracted_triples.triples %}
    - {{ triple.head }} → {{ triple.relation }} → {{ triple.tail }}
    {% endfor %}
    
    For each extracted relation, evaluate:
    1. Quality score (1-10) based on textual evidence:
       - 10: Explicit, clear interaction with strong evidence
       - 7-9: Clear interaction with good evidence
       - 4-6: Possible interaction but ambiguous
       - 1-3: Weak evidence, likely false positive
    
    2. Supporting evidence: Quote or describe the text that supports this relation
    
    Also provide a brief summary of this extraction path's overall quality.
    
    {{ ctx.output_format }}
  "#
}
