ProteinExamples = [
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

TfGeneExamples = [
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

LrExamples = [
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

ProteinNerExamples = [
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

TfGeneNerExamples = [
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
