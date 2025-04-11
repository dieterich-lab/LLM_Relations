
class AltNames {
  alt_names string[] @description("A list containing alternative names for a protein")
}

function CreateAltNames(input: string) -> AltNames {
  client Llama38b // will be overruled by the client registry
  prompt #"
    Generate at least 10 synonyms, genereric names or abbreviatons for the protein provided by the user down below.

    {{ ctx.output_format(prefix="Use the following OUTPUT FORMAT:") }}

    {{ _.role("user") }}

    {{ input }}
  "#
}
