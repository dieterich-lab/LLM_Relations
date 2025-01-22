TRIPLE_TEMPLATE = """Based on the following example, extract entities and 
relations from the provided text.

Use the following entity types, don't use other entity that is not defined below:

### Entity Types::

{node_labels}

Use the following relation types, don't use any other relation that is not defined below:

### Relation Types:

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### Examples:

{examples}

For the following text, extract entities and relations as in the provided example:

### Format instructions:

{format_instructions}

### Text: 
 
{input}
"""

TRIPLE_TEMPLATE_SIMPLE = """Based on the following example, extract entities and 
relations from the provided text.

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES:

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### Examples:

{examples}

Use the following JSON format:

### Format Instructions:

{format_instructions}

### Text: 

{input}
"""

PPI_INDIVIDUAL_TEMPLATE_ALL_NERS = """In the following you'll find a list of 
PROTEINS  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only of those PROTEINS, that interact with each other, based on the text.

IMPORTANT: Read the TEXT carefully. Not all PROTEINS are candidates for interactions.

### PROTEINS

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### EXAMPLES

{examples}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

PPI_INDIVIDUAL_TEMPLATE_TRUE_NERS = """In the following you'll find a list of 
PROTEINS  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only of those PROTEINS, that interact with each other, based on the text.

### PROTEINS

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### EXAMPLES

{examples}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

PPI_INDIVIDUAL_TEMPLATE_NO_EXAMPLES = """In the following you'll find a list of 
PROTEINS  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only of those PROTEINS, that interact with each other, based on the text.

IMPORTANT: Read the TEXT carefully. Not all PROTEINS are candidates for interactions.

### PROTEINS

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

TF_INDIVIDUAL_TEMPLATE_ALL_NERS = """In the following you'll find a list of 
TRANSCRIPTION FACTORS and GENES  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only beteween those TRANSCRIPTION FACTORS and GENES that interact with each other, based on the text.

IMPORTANT: Read the TEXT carefull. Not all TRANSCRIPTION FACTORS and GENES are candidates for interactions.

### TRANSCRIPTION FACTORS and GENES

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### EXAMPLES

{examples}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

TF_INDIVIDUAL_TEMPLATE_TRUE_NERS = """In the following you'll find a list of 
TRANSCRIPTION FACTORS and GENES  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only beteween those TRANSCRIPTION FACTORS and GENES that interact with each other, based on the text.

### TRANSCRIPTION FACTORS and GENES

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Below are a number of examples of text and their extracted entities and relationships.

### EXAMPLES

{examples}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

TF_INDIVIDUAL_TEMPLATE_NO_EXAMPLES = """In the following you'll find a list of 
TRANSCRIPTION FACTORS and GENES  that have been extracted from the provided TEXT that is listed at the end of this prompt.
You are now to extract relations only beteween those TRANSCRIPTION FACTORS and GENES that interact with each other, based on the text.

IMPORTANT: Read the TEXT carefull. Not all TRANSCRIPTION FACTORS and GENES are candidates for interactions.

### TRANSCRIPTION FACTORS and GENES

{entities}

Use the following relation types, don't use any other relation that is not defined below:

### RELATION TYPES

{rel_types}

Be aware that the relationships signal also the direction of the participants. Use the following JSON format:

### FORMAT INSTRUCTIONS

{format_instructions}

### TEXT: 

{input}
"""

PPI_NER_TEMPLATE = """Based on the following example, extract all proteins
from the provided text.

Below are a number of examples of text passages and corresponding extracted proteins.

### Examples:

{examples}

Use and adhere to the following JSON format:

### Format instructions:

{format_instructions}

### Text: 

{input}
"""

PPI_NER_TEMPLATE_TOOLCALL = """
Extract all proteins from the provided TEXT.

Use and adhere to the following JSON format:

### FORMAT INSTRUCTIONS:

{format_instructions}

### TEXT: 

{input}

* IMPORTANT: Please be greedy, meaning you should extract as many entities (proteins) as possible. You will have the possibility to filter the results in a second step.
"""

TF_NER_TEMPLATE_TOOLCALL = """
Extract all transcription factors and genes from the provided TEXT.

Use and adhere to the following JSON format:

### FORMAT INSTRUCTIONS:

{format_instructions}

### TEXT: 

{input}

* IMPORTANT: Please be greedy, meaning you should extract as many entities (transcription factors and genes) as possible. You will have the possibility to filter the results in a second step.
"""

TF_NER_TEMPLATE = """Based on the following example, extract all genes and transcription factors
from the provided text.

Below are a number of examples of text passages and corresponding extracted genes and transcription factors.

### Examples:

{examples}

Use and adhere to the following JSON format:

### Format instructions:

{format_instructions}

### Text: 

{input}
"""

PPI_EXAMPLES = [
    {
        "text": ("BNIP-2 Interacts with LATS1 to Promote YAP Cytosolic Localization"),
        "head": "BNIP-2",
        "head_type": "Protein",
        "relation": "INTERACTS_WITH",
        "tail": "LATS1",
        "tail_type": "Protein",
    },
    {
        "text": (
            "CBY1 interacts with DZIP1 and "
            "localizes to the basal body in developing mitral valves."
        ),
        "head": "CBY1",
        "head_type": "Protein",
        "relation": "INTERACTS_WITH",
        "tail": "DZIP1",
        "tail_type": "Protein",
    },
    {
        "text": (
            "CAMK2 kinase induces cardiac hypertrophy and "
            "activates MEF2 transcription factor in vivo."
        ),
        "head": "CAMK2",
        "head_type": "Protein",
        "relation": "INTERACTS_WITH",
        "tail": "MEF2",
        "tail_type": "Protein",
    },
    {
        "text": "The reduced 14-3-3 co-immunoprecipitation experiments suggest that PKA inhibits HDAC4 activity.",
        "head": "PKA",
        "head_type": "Protein",
        "relation": "INTERACTS_WITH",
        "tail": "HDAC4",
        "tail_type": "Protein",
    },
    {
        "text": "TEL2 binds to TTI1 and both TEL2 and TTI1 are necessary and sufficient to stabilize and activate both mTORC1 and mTORC2 signalling pathways.",
        "head": "TEL2",
        "head_type": "Protein",
        "relation": "INTERACTS_WITH",
        "tail": "TTI1",
        "tail_type": "Protein",
    },
]

PPI_EXAMPLES_SIMPLE = [
    {
        "text": ("BNIP-2 Interacts with LATS1 to Promote YAP Cytosolic Localization"),
        "head": "BNIP-2",
        "relation": "INTERACTS_WITH",
        "tail": "LATS1",
    },
    {
        "text": (
            "CBY1 interacts with DZIP1 and "
            "localizes to the basal body in developing mitral valves."
        ),
        "head": "CBY1",
        "relation": "INTERACTS_WITH",
        "tail": "DZIP1",
    },
    {
        "text": (
            "CAMK2 kinase induces cardiac hypertrophy and "
            "activates MEF2 transcription factor in vivo."
        ),
        "head": "CAMK2",
        "relation": "INTERACTS_WITH",
        "tail": "MEF2",
    },
    {
        "text": "The reduced 14-3-3 co-immunoprecipitation experiments suggest that PKA inhibits HDAC4 activity.",
        "head": "PKA",
        "relation": "INTERACTS_WITH",
        "tail": "HDAC4",
    },
    {
        "text": "TEL2 binds to TTI1 and both TEL2 and TTI1 are necessary and sufficient to stabilize and activate both mTORC1 and mTORC2 signalling pathways.",
        "head": "TEL2",
        "relation": "INTERACTS_WITH",
        "tail": "TTI1",
    },
]

TF_EXAMPLES = [
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "head": "MEF2A",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "ZEB2",
        "tail_type": "gene",
    },
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "head": "MEF2A",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "CTNNB1",
        "tail_type": "gene",
    },
    {
        "text": (
            "CREM regulate the circadian expression of CYP51 and "
            "other cholesterogenic genes in the human heart."
        ),
        "head": "CREM",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "CYP51",
        "tail_type": "gene",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "IL-1",
        "tail_type": "gene",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "IL-6",
        "tail_type": "gene",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "IL-12",
        "tail_type": "gene",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "head_type": "transcription_factor",
        "relation": "REGULATES",
        "tail": "TNF-α",
        "tail_type": "gene",
    },
]

TF_EXAMPLES_SIMPLE = [
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "head": "MEF2A",
        "relation": "REGULATES",
        "tail": "ZEB2",
    },
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "head": "MEF2A",
        "relation": "REGULATES",
        "tail": "CTNNB1",
    },
    {
        "text": (
            "CREM regulate the circadian expression of CYP51 and "
            "other cholesterogenic genes in the human heart."
        ),
        "head": "CREM",
        "relation": "REGULATES",
        "tail": "CYP51",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "relation": "REGULATES",
        "tail": "IL-1",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "relation": "REGULATES",
        "tail": "IL-6",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "relation": "REGULATES",
        "tail": "IL-12",
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "STAT3",
        "relation": "REGULATES",
        "tail": "TNF-α",
    },
]

LR_EXAMPLES_SIMPLE = [
    {
        "text": (
            "We have applied the multiscale framework to the interaction between ligand TNFα and its receptor TNFR1 as a test model."
        ),
        "head": "TNFα",
        "relation": "INTERACTS_WITH",
        "tail": "TNFR1",
    },
    {
        "text": (
            "INS binds to the insulin receptor (IR) on the plasma membrane (PM) and triggers the activation of signaling cascades to regulate metabolism and cell growth."
        ),
        "head": "INS",
        "relation": "INTERACTS_WITH",
        "tail": "IR",
    },
    {
        "text": (
            "The binding of the epidermal growth factor (EGF) to its receptor (EGFR) triggers a large set of downstream processes, ultimately causing cell growth, differentiation and proliferation"
        ),
        "head": "EGF",
        "relation": "INTERACTS_WITH",
        "tail": "EGFR",
    },
    {
        "text": (
            "TGFBR1 is the key component in passing extracellular stimulation to the downstream TGF-β signaling pathway."
        ),
        "head": "TGF-β",
        "relation": "INTERACTS_WITH",
        "tail": "TGFBR1",
    },
    {
        "text": (
            "TGFBR2 is the receptor that TGF-β binds directly, and thus it serves as a gatekeeper for the activation of downstream signaling."
        ),
        "head": "TGF-β",
        "relation": "INTERACTS_WITH",
        "tail": "TGFBR2",
    },
    {
        "text": (
            "PDGFRA can bind to and dimerize the PDGF ligands"
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "head": "PDGF",
        "relation": "INTERACTS_WITH",
        "tail": "PDGFRA",
    },
    {
        "text": (
            "Gq-dependent pathway- Ang II as a ligand (L) binds to AT1R (GPCR), activates Gq protein subunits which recruit the GRKs to the receptor."
        ),
        "head": "Ang II",
        "relation": "INTERACTS_WITH",
        "tail": "AT1R",
    },
]

PPI_NER_EXAMPLES_SIMPLE = [
    {
        "text": ("BNIP-2 Interacts with LATS1 to Promote YAP Cytosolic Localization"),
        "proteins": ["BNIP-2", "LATS1"],
    },
    {
        "text": (
            "CBY1 interacts with DZIP1 and "
            "localizes to the basal body in developing mitral valves."
        ),
        "proteins": ["CBY1", "DZIP1"],
    },
    {
        "text": (
            "CAMK2 kinase induces cardiac hypertrophy and "
            "activates MEF2 transcription factor in vivo."
        ),
        "proteins": ["CAMK2", "MEF2"],
    },
    {
        "text": "The reduced 14-3-3 co-immunoprecipitation experiments suggest that PKA inhibits HDAC4 activity.",
        "proteins": ["PKA", "HDAC4"],
    },
    {
        "text": "TEL2 binds to TTI1 and both TEL2 and TTI1 are necessary and sufficient to stabilize and activate both mTORC1 and mTORC2 signalling pathways.",
        "proteins": ["TEL2", "TTI1"],
    },
]

TF_NER_EXAMPLES_SIMPLE = [
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "protiens": ["MEF2A", "ZEB2"],
    },
    {
        "text": (
            "MEF2A transcriptionally upregulates the expression of ZEB2 and CTNNB1"
        ),
        "proteins": ["MEF2A", "CTNNB1"],
    },
    {
        "text": (
            "CREM regulate the circadian expression of CYP51 and "
            "other cholesterogenic genes in the human heart."
        ),
        "proteins": ["CREM", "CYP51"],
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "proteins": ["STAT3", "IL-1"],
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "proteins": ["STAT3", "IL-6"],
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "proteins": ["STAT3", "IL-12"],
    },
    {
        "text": (
            "STAT3 then travels to the nucleus where it stimulates the transcription of specific genes, "
            "which in-turn are thought to abrogate the inflammatory response by transcriptionally repressing "
            "proinflammatory cytokine genes such as IL-1, IL-6, IL-12, and TNF-α."
        ),
        "proteins": ["STAT3", "TNF-α"],
    },
]

PPI_NODE_LABELS = ["protein"]
LR_NODE_LABELS = ["ligand", "receptor"]
PPI_INTERACTIONS = ["INTERACTS_WITH"]
LR_INTERACTIONS = ["INTERACTS_WITH"]
TF_NODE_LABELS = ["transcription_factor", "gene"]
TF_INTERACTIONS = ["REGULATES"]
