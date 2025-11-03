"""
Refactored prompts.py - A more maintainable and pythonic approach to prompt management.
"""

from dataclasses import dataclass
from parser import args
from typing import Any, Dict, List, Optional


@dataclass
class ExtractionConfig:
    """Configuration for extraction settings."""

    target: str  # "ppi", "tf", or "ppitf"
    extraction_mode: str  # "direct" or "nerrel"
    chat_type: str  # "oneshot" or "stepwise"
    model: str
    force_cot: bool
    noconfidence: bool
    recall: bool
    examples: str  # "negpos", "pos", "neg", or ""
    all_nes_given: bool
    true_nes_given: bool
    spacy_nes_given: bool
    lookup: bool
    dynex_k: int

    @classmethod
    def from_args(cls) -> "ExtractionConfig":
        """Create config from global args."""
        return cls(
            target=args.target,
            extraction_mode=args.extractionmode,
            chat_type=args.chattype,
            model=args.model,
            force_cot=args.force_cot,
            noconfidence=args.noconfidence,
            recall=args.recall,
            examples=args.examples,
            all_nes_given=args.all_nes_given,
            true_nes_given=args.true_nes_given,
            spacy_nes_given=args.spacy_nes_given,
            lookup=args.lookup,
            dynex_k=args.dynex_k,
        )


@dataclass
class TargetConfig:
    """Configuration for different target types."""

    targets: str
    anti_targets: str
    target: str
    interactions_type: str
    anti_interactions_type: str

    @classmethod
    def for_target(cls, target: str) -> "TargetConfig":
        """Factory method to create target config based on target type."""
        configs = {
            "ppi": cls(
                targets="proteins",
                anti_targets="transcription factors and genes",
                target="protein",
                interactions_type="protein-protein",
                anti_interactions_type="transcription factor/gene",
            ),
            "tf": cls(
                targets="transcription factors and genes",
                anti_targets="proteins",
                target="transcription factor/gene",
                interactions_type="transcription factor-to-gene",
                anti_interactions_type="protein-protein",
            ),
            "ppitf": cls(
                targets="proteins and transcription factors and genes",
                anti_targets="",
                target="protein and transcription factor/gene",
                interactions_type="protein-protein and transcription factor-to-gene",
                anti_interactions_type="",
            ),
        }
        if target not in configs:
            raise ValueError(
                f"Unknown target type: {target}. Must be one of: {list(configs.keys())}"
            )
        return configs[target]


class ExamplesData:
    """Container for all example data."""

    PPI_POSITIVE = """
Below, you find some positive examples of protein-protein relations that give you an idea of what we are looking for:

P1: This cytokine induces p53 into a mutant-like conformation that forms a complex with Sp1
A1: p53	INTERACTS_WITH	Sp1
P2: These findings suggest that the STAT3-NRF2 complex accelerates BLBC growth and progression by augmenting IL-23A expression.
A2: STAT3	INTERACTS_WITH	NRF2
P3: HIF1A forms a transcriptional complex with ARNT under hypoxia.
A3: HIF1A	INTERACTS_WITH	ARNT
P4: PRMT1 methylates cGAS and suppresses cGAS/STING signalling in cancer cells
A4: PRMT1	INTERACTS_WITH	cGAS
P5: TRAF6 ubiquitinates TGFβ type I receptor to promote its cleavage and nuclear translocation in cancer.
A5: TRAF6	INTERACTS_WITH	TGFβ
P6: AKT1 phosphorylates AKT1S1 at Thr-246.
A6: AKT1	INTERACTS_WITH	AKT1S1
P7: PIAS1 sumoylates PNKP in cells.
A7: PIAS1	INTERACTS_WITH	PNKP
P8: CBP, but not p/CAF, acetylates GATA-1 at two highly conserved lysine-rich motifs present at the C-terminal tails of both zinc fingers.
A8: CBP	INTERACTS_WITH	GATA-1
P9: Experimental analysis revealed a chemical cross-linking between Hsp90 and the (CDK4)-cyclin D1 complex, stabilising their association during signal transduction.
A9: Hsp90	INTERACTS_WITH	CDK4
P10: Similar to the CREB proteins, NFIX serves as a direct substrate of SRC1 and functions as a signal-responsive transcription factor.
A10: NFIX	INTERACTS_WITH	SRC1
P11: The N-terminal transactivation domain of p53 binds directly to the hydrophobic pocket of MDM2 to regulate its stability
A11: p53	INTERACTS_WITH	MDM2
P12: Under physiological conditions, 14-3-3ζ exhibits weak, transient binding to Bad, allowing rapid modulation of apoptotic signalling.
A12: 14-3-3ζ	INTERACTS_WITH	Bad
P13: The tumor suppressor BRCA1 interacts with DNA repair proteins like RAD51 to facilitate homologous recombination.
A13: BRCA1	INTERACTS_WITH	RAD51
"""

    PPI_NEGATIVE = """
Below you find some examples of false positive protein-protein relations and the reason why you should not extract those:

P1: KRAS and BRAF cooperate in the MAPK signalling cascade to promote cell proliferation.
A1: Although the two proteins are in the same signalling system, the text does not provide evidence of a direct interaction.
P2: p53 and Protein MYC are both found in the same signalling complex.
A2: Incorrect assumptions based on co-occurrence or proximity.
P3: TNF and IL6 accumulate at DNA damage sites.
A3: Co-localisation, but no evidence of direct relation/interaction between the two.
P4: Gene TNF regulates the expression of Gene IL6.
A4: Misinterpretation of genetic or signalling pathways as protein interactions.
P5: Prmt5 shares 80% sequence identity with Protein Prmt7, which is known to bind BRAF.
A5: Incorrect assumptions based on structural similarity.
P6: PTEN was pulled down in a co-IP assay with CDKN2A.
A6: Incorrect interpretations of experimental methods.
"""

    TF_POSITIVE = """
Below you find some positive examples of transcription factor-to-gene relations that give you an idea of what we are looking for:

P1: MYC target genes that are involved in cell cycle such as Cyclin D1
A1: MYC	INTERACTS_WITH	Cyclin D1
P2: STAT3 can induce the expression of anti-apoptotic genes like Bcl-2, which help in cell survival.
A2: STAT3	INTERACTS_WITH	Bcl-2
P3: Tbx1 activates transcription of the fibroblast growth factor genes Fgf8 and Fgf10 to maintain proliferative expansion and inhibit differentiation of cardiopharyngeal precursor cells
A3: Tbx1	INTERACTS_WITH	Fgf8;	Tbx1	INTERACTS_WITH	Fgf10
P4: Overexpression of MECP2 leads to the suppression of IFN-γ transcription, which is linked to impaired TH1 responses in both children and mice with MECP2 duplication syndrome.
A4: MECP2	INTERACTS_WITH	IFN-γ
P5: In humans, FOXO regulates the expression of core small RNA pathway genes, including AGO2.
A5: FOXO	INTERACTS_WITH	AGO2
"""

    TF_NEGATIVE = """
Below you find some false positive examples of relations between transcription factor-to-gene relations and the reason why you should not extract those:
P1: This cytokine induces p53 into a mutant-like conformation that forms a complex with Sp1.
A1: This is a complex formation and does not involve transcription factor to gene relations.
P2: HIF1A forms a transcriptional complex with ARNT under hypoxia.
A2: This relation represents two transcription factor proteins interacting with each other, and the text does not reflect that they target the regulation of any specific gene.
P3: RMT1 methylates cGAS and suppresses cGAS/STING signalling in cancer cells.
A3: This is a methylation interaction and not a transcription factor to gene relation.
P4: Gene MYC and gene STAT3 share a common promoter region.
A4: This is not explicitly a relation between a transcription factor and its target gene.
P5: AKT1 phosphorylates AKT1S1 at Thr-246.
A5: This is a phosphorylation interaction and not a transcription factor to gene relation.
"""

    @classmethod
    def get_examples(cls, target: str, example_type: str) -> str:
        """Get examples based on target and type."""
        examples_map = {
            ("ppi", "pos"): cls.PPI_POSITIVE,
            ("ppi", "neg"): cls.PPI_NEGATIVE,
            ("tf", "pos"): cls.TF_POSITIVE,
            ("tf", "neg"): cls.TF_NEGATIVE,
            ("ppitf", "pos"): cls.PPI_POSITIVE + "\n" + cls.TF_POSITIVE,
            ("ppitf", "neg"): cls.PPI_NEGATIVE + "\n" + cls.TF_NEGATIVE,
        }
        return examples_map.get((target, example_type), "")


class PromptBuilder:
    """Builds prompts based on configuration.

    This class encapsulates all prompt construction logic for molecular interaction extraction.
    It handles different target types (PPI, TF, PPITF), extraction modes, and chat types.
    """

    # Constants
    COT_MODELS = ["llama33", "llama31", "llama33regu", "llama31regu"]
    VALID_TARGETS = ["ppi", "tf", "ppitf"]
    VALID_MODES = ["direct", "nerrel"]
    VALID_CHAT_TYPES = ["oneshot", "stepwise", "lookup"]
    VALID_EXAMPLES = ["", "pos", "neg", "negpos"]

    SYSTEM_PROMPT = (
        "You are an expert molecular biologist specializing in protein-protein interactions and gene regulatory networks. "
        "Your TASK is to extract molecular relationships from scientific texts with high precision. "
        "You understand the difference between direct physical interactions, functional relationships, and regulatory effects. "
        "When extracting relationships, focus on evidence-based direct interactions rather than indirect associations."
    )

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

    def __init__(self, config: ExtractionConfig, target_config: TargetConfig):
        self.config = config
        self.target_config = target_config

    def build_cot_prompt(self) -> str:
        """Build chain-of-thought prompt."""
        if self.config.model in self.COT_MODELS and self.config.force_cot:
            return "Let's think step by step. "
        return ""

    def build_confidence_prompt(self) -> str:
        """Build confidence prompt."""
        if not self.config.noconfidence:
            return "Whenever you are unsure about a relation set the 'confidence' attribute to 'low', otherwise to 'high'."
        return ""

    def build_ner_list_prompt(self) -> str:
        """Build NER list prompt based on configuration."""
        if self.config.all_nes_given:
            return (
                f"Look at the list above. These are the ground truth {self.target_config.targets} "
                f"that are found in the abstract. But be wary, not all of them will necessarily be a "
                f"participant in {self.target_config.interactions_type} relations. Use this list for the following TASK."
            )
        elif self.config.true_nes_given:
            return (
                f"Look at the list above. These are the ground truth {self.target_config.targets} "
                f"that are found in the abstract and also take part in {self.target_config.interactions_type} "
                "relations. Use this list for the following TASK."
            )
        elif self.config.spacy_nes_given:
            return (
                f"Look at the list above. These are {self.target_config.targets} that have been "
                "extracted by a ScispaCy biomedical NER model from the given TEXT. Use this list for the following TASK."
            )
        elif self.config.extraction_mode == "nerrel":
            # if not (
            #     self.config.all_nes_given
            #     or self.config.true_nes_given
            #     or self.config.spacy_nes_given
            # ):
            return f"Now look at your extracted {self.target_config.targets} above and use it for the following TASK:"
        return ""

    def build_ner_prompt(self) -> str:
        """Build NER prompt modifier."""
        if (
            self.config.true_nes_given
            or self.config.all_nes_given
            or self.config.spacy_nes_given
        ):
            return "for the entities in the NE LIST above that are "
        return ""

    def build_lookup_prompt(self) -> str:
        """Build lookup prompt."""
        if self.config.lookup:
            return "We also provided above some insightful BACKGROUND KNOWLEDGE for each extracted protein. Use it as additional support. "
        return ""

    def build_dynex_prompt(self) -> str:
        """Build dynamic example prompt."""
        if self.config.dynex_k > 0:
            return "Following, you find EXAMPLES with of similar texts and ground truth relations. Use it as support for your decision. "
        return ""

    def build_main_prompt(self) -> str:
        """Build the main extraction prompt."""
        ner_list = self.build_ner_list_prompt()
        ner_modifier = self.build_ner_prompt()
        lookup = self.build_lookup_prompt()
        dynex = self.build_dynex_prompt()

        if not self.config.recall:
            if self.config.target == "tf":
                return (
                    f"\n\nTASK: {ner_list} Extract all the {self.target_config.interactions_type} interactions "
                    f"{ner_modifier} involved in gene regulatory networks from the TEXT. Please only extract "
                    f"{self.target_config.target} pairs of direct relations between a transcription factor and the gene that it regulates. "
                    f"Do not misinterpret functional relationships, co-occurrence, structural similarity, or indirect "
                    f"regulatory effects for direct interactions. {lookup}{dynex}"
                )
            else:
                return (
                    f"\n\nTASK: {ner_list} Extract all the {self.target_config.interactions_type} interactions "
                    f"{ner_modifier}from the TEXT. Focus on direct physicical interactions where proteins "
                    f"bind to each other, modify each other, or form complexes. Only extract {self.target_config.target} pairs that "
                    f"directly interact through: binding, phosphorylation, ubiquitination, methylation, acetylation, "
                    f"sumoylation, or other post-translational modifications. EXCLUDE: functional relationships, "
                    f"co-expression, co-localization, signaling cascades without direct contact, or indirect regulatory effects. "
                    f"{lookup}{dynex}"
                )
        else:
            return (
                f"\n\nTASK: {ner_list} Extract ALL the relations between molecular entities from the TEXT. "
                f"Be as greedy as possible, we will filter the relations for correctness later in a second step {lookup}"
            )

    def build_examples(self) -> str:
        """Build examples string based on configuration."""
        if self.config.target == "ppi":
            pos = (
                ExamplesData.get_examples("ppi", "pos")
                if self.config.examples in ["negpos", "pos"]
                else ""
            )
            neg = (
                ExamplesData.get_examples("ppi", "neg")
                if self.config.examples in ["negpos", "neg"]
                else ""
            )
            return pos + neg
        elif self.config.target == "tf":
            pos = (
                ExamplesData.get_examples("tf", "pos")
                if self.config.examples in ["negpos", "pos"]
                else ""
            )
            neg = (
                ExamplesData.get_examples("tf", "neg")
                if self.config.examples in ["negpos", "neg"]
                else ""
            )
            return pos + neg
        elif self.config.target == "ppitf":
            pos = (
                ExamplesData.get_examples("ppitf", "pos")
                if self.config.examples in ["negpos", "pos"]
                else ""
            )
            neg = (
                ExamplesData.get_examples("ppitf", "neg")
                if self.config.examples in ["negpos", "neg"]
                else ""
            )
            return pos + neg
        return ""

    def build_chat_prompts(self) -> List[str]:
        """Build the final chat prompts based on configuration."""
        main_prompt = self.build_main_prompt()
        examples = self.build_examples()
        confidence = self.build_confidence_prompt()
        cot = self.build_cot_prompt()

        # Determine mode
        mode = self.config.extraction_mode
        if self.config.all_nes_given or self.config.true_nes_given:
            mode = "nerrel"

        base_prompt = f"{main_prompt} {examples} {confidence}{cot}"

        # Build prompts based on mode and chat type
        if mode == "direct":
            if self.config.chat_type == "oneshot":
                return [base_prompt]
            elif self.config.chat_type == "stepwise":
                if self.config.target == "tf":
                    return [
                        base_prompt,
                        f"Now review your extracted {self.target_config.interactions_type} interactions to determine if "
                        "they are specific to gene regulatory networks. Retain only direct transcription factor-to-gene "
                        "regulations and remove indirect effects or protein-protein interactions. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                        f"Review one more time the {self.target_config.interactions_type} interactions to ensure "
                        "they represent direct transcriptional regulation rather than post-translational modifications "
                        "or protein complex formations. Retain only true TF-gene regulatory relationships. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                    ]
                else:
                    return [
                        base_prompt,
                        f"Now review your extracted {self.target_config.interactions_type} interactions to determine if "
                        "they are specific to signaling pathways. Retain only signalling pathway interactions "
                        "and remove the rest. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                        f"Review one more time the {self.target_config.interactions_type} interactions to  "
                        f"determine whether there are in the list regulations that are of a {self.target_config.anti_interactions_type} "
                        f"regulatory nature. Retain those interactions that are only specific to {self.target_config.interactions_type} interactions in cell  "
                        f"signalling and remove those relations that represent relations between {self.target_config.anti_targets}. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                    ]
        elif mode == "nerrel":
            ner_prompt = f"\n\nTASK: Extract all the {self.target_config.targets} that appear in the TEXT. "
            rel_prompt = base_prompt

            if self.config.chat_type == "oneshot":
                return [ner_prompt, rel_prompt]
            elif self.config.chat_type in ["stepwise", "lookup"]:
                if self.config.target == "tf":
                    return [
                        f"\n\nTASK: Extract all the {self.target_config.targets} that appear in the TEXT. ",
                        rel_prompt,
                        f"Now review your extracted {self.target_config.interactions_type} interactions to determine if "
                        "they are specific to gene regulatory networks. Retain only direct transcription factor-to-gene "
                        "regulations and remove indirect effects or protein-protein interactions. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                        f"Review one more time the {self.target_config.interactions_type} interactions to ensure "
                        "they represent direct transcriptional regulation rather than post-translational modifications "
                        "or protein complex formations. Retain only true TF-gene regulatory relationships. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                    ]
                else:
                    return [
                        f"\n\nTASK: Extract all the {self.target_config.targets} that appear in the TEXT.",
                        rel_prompt,
                        f"Now review your extracted {self.target_config.interactions_type} interactions to determine if "
                        "they are specific to signaling pathways. Retain only signalling pathway interactions "
                        "and remove the rest. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                        f"Review one more time the {self.target_config.interactions_type} interactions to  "
                        f"determine whether there are in the list regulations that are of a {self.target_config.anti_interactions_type} "
                        f"regulatory nature. Retain those interactions that are only specific to {self.target_config.interactions_type} interactions in cell  "
                        f"signalling and remove those relations that represent relations between {self.target_config.anti_targets}. "
                        "Use again the desired json OUTPUT FORMAT to format your answer. "
                        f"{confidence}{cot}",
                    ]

        # Handle special case for ppitf stepwise
        if self.config.target == "ppitf" and self.config.chat_type == "stepwise":
            prompts = self.build_chat_prompts()
            return prompts[:-1]  # Remove last prompt for ppitf stepwise

        return []


def create_prompt_builder() -> PromptBuilder:
    """Factory function to create a prompt builder from global args."""
    config = ExtractionConfig.from_args()
    target_config = TargetConfig.for_target(config.target)
    return PromptBuilder(config, target_config)


# ============================================================================
# Tree-of-Thoughts (ToT) Prompts
# ============================================================================

TOT_STRATEGY_GENERATION_PROMPT = """
You are designing extraction strategies for identifying {interactions_type} interactions from scientific text.

Generate {n_paths} different reasoning approaches/strategies for extracting these relations. Each strategy should focus on a different aspect:
- Strategy 1: Focus on explicit interaction verbs (binds, phosphorylates, activates, etc.)
- Strategy 2: Focus on experimental evidence (co-IP, pull-down, reporter assays, etc.)
- Strategy 3: Focus on functional descriptions and mechanistic details
{extra_strategy}

For each strategy, provide:
1. A brief name (3-5 words)
2. What textual patterns to look for
3. What to avoid (common false positives for this approach)

Output your strategies in this JSON format:
{{
    "strategies": [
        {{
            "name": "Strategy name",
            "focus": "What to focus on",
            "avoid": "What to avoid"
        }}
    ]
}}
"""

TOT_PATH_EXTRACTION_PROMPT = """
Now, using ONLY the following extraction strategy, extract {interactions_type} interactions:

STRATEGY: {strategy_name}
FOCUS ON: {strategy_focus}
AVOID: {strategy_avoid}

Apply this strategy systematically to the text. {confidence_prompt}
"""

TOT_EVALUATION_PROMPT = """
You have extracted {interactions_type} interactions using a specific strategy.

Review your extracted relations and evaluate:
1. How many relations did you find?
2. How confident are you in each relation (based on textual evidence)?
3. Are there any potential false positives?

For each triple, assign a quality score from 1-10 where:
- 10 = Explicit, clear interaction with strong textual evidence
- 7-9 = Clear interaction but less explicit evidence
- 4-6 = Possible interaction but ambiguous
- 1-3 = Weak evidence, likely false positive

Output in this JSON format:
{{
    "evaluation": [
        {{
            "head": "protein1",
            "relation": "INTERACTS_WITH",
            "tail": "protein2",
            "score": 9,
            "evidence": "Brief quote from text supporting this relation"
        }}
    ],
    "summary": "Brief assessment of this extraction path"
}}
"""

TOT_MERGE_PROMPT = """
You have extracted {interactions_type} interactions using {n_paths} different reasoning strategies.

Below are the results from each strategy with quality scores:

{all_extractions}

Now, combine these results using the following approach:
- Include relations that appear in multiple strategies (higher confidence)
- Include relations with score ≥ 8 even if only found by one strategy
- Exclude relations with score < 5 unless they appear in ≥2 strategies
- Resolve conflicts (e.g., different relation types for same entity pair)

Output the final merged set of relations using the standard OUTPUT FORMAT.
{confidence_prompt}
"""


# ============================================================================
# Main Interface - Backward Compatibility
# ============================================================================

# Create the prompt builder instance
_builder = create_prompt_builder()

# Export the prompts and constants for backward compatibility
rel_system_prompt = PromptBuilder.SYSTEM_PROMPT
prompts = _builder.build_chat_prompts()
OUTPUT_FORMAT = PromptBuilder.OUTPUT_FORMAT

# ToT prompts (keeping original names for compatibility)
tot_strategy_generation_prompt = TOT_STRATEGY_GENERATION_PROMPT
tot_path_extraction_prompt = TOT_PATH_EXTRACTION_PROMPT
tot_evaluation_prompt = TOT_EVALUATION_PROMPT
tot_merge_prompt = TOT_MERGE_PROMPT
