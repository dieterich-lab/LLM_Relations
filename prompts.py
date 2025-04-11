from parser import args

rel_system_prompt = (
    "You are a top-tier molecular biologist specialized in the field of cardiology and molecular biology. "
    "Following, you'll find a scientific TEXT, a desired OUTPUT FORMAT and a USER QUESTION. "
    "First, read the TEXT and study the OUTPUT FORMAT, then answer the USER QUESTION."
)

cot_models = ["llama33", "llama31", "llama33regu", "llama31regu"]
cot_prompt = (
    "Let's think step by step. " if args.model in cot_models and args.force_cot else ""
)
confidence_prompt = (
    "Whenever you are unsure about a relation set the 'confidence' attribute to 'low', otherwise to 'high'."
    if not args.noconfidence
    else ""
)

judge_system_prompt = (
    "You are a top-tier molecular biologist specialized in the field of cardiology and molecular biology. "
    "Following, you'll find a TEXT in the form of a scientific paper, "
    "a TRIPlE that specifies a molecular relationship, "
    "REASONING THOUGHTS denoting why this relationship has been extractd from the TEXT "
    " and a USER QUESTION. "
    "First, examine the TEXT, the TRIPLE and the REASONING THOUGHTS, then answer the USER QUESTION."
)

judge_prompt = (
    "The TRIPLE has been extracted by an AI, but an expert analysis shows "
    "that the relationship is factual wrong. Please analyse the TEXT with regards to the "
    "the REASONING THOUGHTS of the AI and explain very briefely why the reasoning process of the AI lead to the "
    "erroneous relationship. "
    "Use the given JSON OUTPUT FORMAT to summarize why the AI incorrectly inferred this relationship, e.g.: "
    '```json { "reason": "The AI incorrectly assumed... "```'
)

corrector_system_prompt = (
    "You are a top-tier molecular biologist specialized in the field of cardiology and molecular biology. "
    "Following, you'll find a TEXT in the form of a scientific paper, "
    "a TRIPlE that specifies a molecular relationship, "
    "REASONING THOUGHTS denoting why this relationship has been extractd from the TEXT "
    " and a USER QUESTION. "
    "First, examine the TEXT, the TRIPLE and the REASONING THOUGHTS, then answer the USER QUESTION."
)

corrector_prompt = (
    "The TRIPLE has been extracted by an AI. You, as an expert analyst,  are tasked to re-evaluate the relationship "
    "and tell us if this triple is factually correct or incorrect. To do so, you will inspect the TEXT and the previous "
    "REASONING THOUGHTS of the AI and then output 'correct' or 'incorrect' dependent on your judgement. "
    "Use the given json OUTPUT FORMAT to output your answer."
)

ppi_ner_list_prompt = (
    "Now look at the list of extracted proteins above and use it for the following task:"
    if args.extractionmode in ["nerrel", "lookup"]
    else ""
)

lookup_prompt = (
    "We also provided above some insightful BACKGROUND KNOWLEDGE for each extracted protein. Use it as additional support. "
    if args.chattype == "lookup"
    else ""
)

dynex_prompt = (
    "Following, you find an EXAMPLE of a similar texts and ground truth relations. Use it as support for your decision. "
    if args.dynex
    else ""
)


if not args.recall:
    ppi_prompt = f"{ppi_ner_list_prompt}  Extract all the protein-protein interactions involved in signalling pathways from the text. Please only extract protein pairs which directly interact with each other (i.e. through binding, phosphorylation, sumoylation, etc). Do not misinterpret functional relationships, co-occurrence, structural similarity, or indirect regulatory effects for direct interactions. {lookup_prompt}{dynex_prompt}"
else:
    ppi_prompt = f"{ppi_ner_list_prompt}  Extract ALL the relations between molecular entities from the text. Be as greedy as possible, we will filter the relations for correctness later in a second step {lookup_prompt}"

ppi_neg_ex = f"""
Below you find some examples of false positives and the reason why you should not extract those:
* 'KRAS and BRAF cooperate in the MAPK signaling cascade to promote cell proliferation.': Although the two proteins are in the same signalling system, the text does not provide evidence of a direct interaction.
* 'p53 and Protein MYC are both found in the same signaling complex.': Incorrect assumptions based on co-occurrence or proximity.
* 'TNF and IL6 accumulate at DNA damage sites.': Co-localization but no evidence of direct relation/interaction between the two.
* 'Gene TNF regulates the expression of Gene IL6': Misinterpretation of genetic or signalling pathways as protein interactions.
* 'Prmt5 shares 80% sequence identity with Protein Prmt7, which is known to bind BRAF.': Incorrect assumptions based on structural similarity.
* 'PTEN was pulled down in a co-IP assay with CDKN2A.': Incorrect interpretations of experimental methods.
"""

ppi_pos_ex = """
Below you find some positive examples of relations that give you an idea of what we are looking for:
[
    {
        'text': (
            'This cytokine induces the p53 into a mutant-like conformation that forms a complex with Sp1' 
        ),
        'head': 'p53',
        'relation': 'INTERACTS_WITH',
        'tail': 'Sp1',
    },
    {
        'text': (
            'These findings suggest that the STAT3-NRF2 complex accelerates BLBC growth and progression by augmenting IL-23A expression.' 
        ),
        'head': 'STAT3',
        'relation': 'INTERACTS_WITH',
        'tail': 'NRF2',
    },
    {
        'text': (
            'HIF1A forms a transcriptional complex with ARNT under hypoxia.' 
        ),
        'head': 'HIF1A',
        'relation': 'INTERACTS_WITH',
        'tail': 'ARNT',
    },
    {
        'text': (
            'PRMT1 methylates cGAS and suppresses cGAS/STING signaling in cancer cells' 
        ),
        'head': 'PRMT1',
        'relation': 'INTERACTS_WITH',
        'tail': 'cGAS',
    },
    {
        'text': (
            'TRAF6 ubiquitinates TGFβ type I receptor to promote its cleavage and nuclear translocation in cancer.' 
        ),
        'head': 'TRAF6',
        'relation': 'INTERACTS_WITH',
        'tail': 'TGFβ',
    },
    {
        'text': 'AKT1 phosphorylates AKT1S1 at Thr-246.',
        'head': 'AKT1',
        'relation': 'INTERACTS_WITH',
        'tail': 'AKT1S1',
    },
    {
        'text': 'PIAS1 sumoylates PNKP in cells.',
        'head': 'PIAS1',
        'relation': 'INTERACTS_WITH',
        'tail': 'PNKP',
    },
{
        'text': 'CBP, but not p/CAF, acetylates GATA-1 at two highly conserved lysine-rich motifs present at the C-terminal tails of both zinc fingers.',
        'head': 'CBP',
        'relation': 'INTERACTS_WITH',
        'tail': 'GATA-1',
    },
]
"""

ppi_ex = f"{ppi_pos_ex if args.examples in ['negpos', 'pos'] else ''}{ppi_neg_ex if args.examples in ['negpos', 'neg'] else ''}"

chat_prompts = {
    "direct": {
        "oneshot": {
            "ppi": [
                f"{ppi_prompt} "
                f"{ppi_ex} "
                "Please stick to the desired OUTPUT FORMAT. "
                f"{confidence_prompt}{cot_prompt}",
            ],
            "tf": [
                "Extract all the relations involving transcription factors to the target genes they regulate from the text. "
                "Please stick to the desired OUTPUT FORMAT ."
                f"{confidence_prompt}{cot_prompt}",
            ],
        },
        "stepwise": {
            "ppi": [
                f"{ppi_prompt} "
                f"{ppi_ex} "
                "Please stick to the desired OUTPUT FORMAT. "
                f"{confidence_prompt}{cot_prompt}",
                "Now review your extracted protein-protein interactions (PPI's) to determine if "
                "they are specific to signaling pathways. Retain only signalling pathway interactions "
                "and remove the rest. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Review one more time the protein-protein interactions (PPI's) to  "
                "determine whether there are in the list regulations that are of a transcriptional or gene  "
                "regulatory nature. Retain those interactions that are only specific to PPI's in cell  "
                "signalling and remove those relations that represent relations between transcription factors "
                "to their gene targets. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
            ],
            "tf": [
                "Extract all the relations involving transcription factors to the target genes they regulate from the text.",
                "Please stick to the desired OUTPUT FORMAT. "
                f"{confidence_prompt}{cot_prompt}",
                "Now review your extracted transcription factor (TF) to gene relations to determine if "
                "they are specific to gene regulatory networks. Retain those interactions that are only "
                "involving TF's and their gene targets and remove those that are not. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Review one more time the transcription factor to gene relations  "
                "to determine whether there are in the list relations that are protein-protein "
                "interactions (PPI's) network or involved in protein signalling networks. Retain interactions  "
                "of gene regulatory networks involve a transcription factor and the gene whose expression  "
                "they regulate. Remove those relations that involve interactions between two signalling protein "
                "and PPI's. "
                "Use again the desired json OUTPUT FORMAT to format your answer. ",
            ],
        },
    },
    "nerrel": {
        "oneshot": {
            "ppi": [
                "Extract all the proteins that appear in the text.",
                f"{ppi_prompt} " "Please stick to the desired OUTPUT FORMAT.",
                f"{ppi_ex} "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Review one more time the transcription factor to gene relations  ",
            ],
            "tf": [
                "Extract all transcription factors and genes from the text. "
                "Please stick to the desired OUTPUT FORMAT.",
                "Look at the list above containing extracted transcription factors and genes. Use it to extract all the relations involving transcription factors to the target genes they regulate from the text. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
            ],
        },
        "stepwise": {
            "ppi": [
                "Extract all the proteins that appear in the text.",
                f"{ppi_prompt} "
                f"{ppi_ex} "
                "Please stick to the desired OUTPUT FORMAT. "
                f"{confidence_prompt}{cot_prompt}",
                "Now review your extracted protein-protein interactions (PPI's) to determine if "
                "they are specific to signaling pathways. Retain only signalling pathway interactions "
                "and remove the rest. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Review one more time the protein-protein interactions (PPI's) to  "
                "determine whether there are in the list regulations that are of a transcriptional or gene  "
                "regulatory nature. Retain those interactions that are only specific to PPI's in cell  "
                "signalling and remove those relations that represent relations between transcription factors "
                "to their gene targets. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
            ],
            "tf": [
                "Extract all transcription factors and genes from the text. "
                "Please stick to the desired OUTPUT FORMAT.",
                "Look at the list above containing extracted transcription factors and genes. Use it to extract all the relations involving transcription factors to the target genes they regulate from the text. ",
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Now review your extracted transcription factor (TF) to gene relations to determine if "
                "they are specific to gene regulatory networks. Retain those interactions that are only "
                "involving TF's and their gene targets and remove those that are not. ",
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
                "Review one more time the transcription factor to gene relations  "
                "to determine whether there are in the list relations that are protein-protein "
                "interactions (PPI's) network or involved in protein signalling networks. Retain interactions  "
                "of gene regulatory networks involve a transcription factor and the gene whose expression  "
                "they regulate. Remove those relations that involve interactions between two signalling protein "
                "and PPI's. "
                "Use again the desired json OUTPUT FORMAT to format your answer. "
                f"{confidence_prompt}{cot_prompt}",
            ],
        },
    },
}

mode_lookup = args.extractionmode if not args.all_ners_given else "nerrel"
chat_lookup = "stepwise" if args.chattype == "lookup" else args.chattype
prompts = chat_prompts[mode_lookup][chat_lookup][args.target]

OUTPUT_FORMAT = """
{
    // list of triples that describe interactions between two biological entities
    triples: [
    {
        // head entity of the triple 
        head: string,
        // relationship type
        relation: "INTERACTS_WITH",
        // tail entity name of the triple
        tail: string,
    }
    ],
}
"""
