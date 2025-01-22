from enum import Enum
from typing import List, Literal

from pydantic import BaseModel, Field


class PPI_Triple(BaseModel):
    head: str = Field(description="Head protein entity.")
    head_type: Literal["Protein"] = Field(
        description="Type of the head protein entity."
    )
    relation: Literal["INTERACTS_WITH"] = Field(description="Protein-protein relation.")
    tail: str = Field(description="Tail protein entity.")
    tail_type: Literal["Protein"] = Field(
        description="Type of the tail protein entity."
    )


class LR_Triple_SIMPLE(BaseModel):
    head: str = Field(description="Head ligand entity.")
    relation: Literal["INTERACTS_WITH"] = Field(description="Protein-protein relation.")
    tail: str = Field(description="Tail receptor entity.")


class TF_Triple(BaseModel):
    head: str = Field(description="Head gene entity")
    head_type: Literal["transcription_factor"] = Field(
        description="Type of the transcription factor entity."
    )
    relation: Literal["REGULATES"] = Field(
        description="Transcription factor-gene relation."
    )
    tail: str = Field(description="Tail gene entity.")
    tail_type: Literal["gene"] = Field(description="Type of the gene entity.")


class PPI_Triple_Simple(BaseModel):
    head: str = Field(description="Head protein entity.")
    relation: Literal["INTERACTS_WITH"] = Field(description="Protein-protein relation.")
    tail: str = Field(description="Tail protein entity.")


class PPI_Triples_Simple(BaseModel):
    """
    A class that contains a list of protein relations in the form of triples.
    """

    triples: List[PPI_Triple_Simple] = Field(
        description="List of all extracted Triples."
    )


class TF_Triple_Simple(BaseModel):
    head: str = Field(description="Head gene entity")
    relation: Literal["REGULATES"] = Field(
        description="Transcription factor-gene relation."
    )
    tail: str = Field(description="Tail gene entity.")


class PPI_Triples(BaseModel):
    """
    A class that contains a list of protein relations in the form of triples.
    """

    triples: List[PPI_Triple] = Field(description="List of all extracted Triples.")


class TF_Triples(BaseModel):
    """
    A class that contains a list of transcription factor/gene relations in the form of triples.
    """

    triples: List[TF_Triple] = Field(description="List of all extracted Triples.")


class LR_Triples_Simple(BaseModel):
    """
    A class that contains a list of ligand-receptor relations in the form of triples.
    """

    triples: List[LR_Triple_SIMPLE] = Field(
        description="List of all extracted Triples."
    )


class Triple(BaseModel):
    head: str = Field(description="Head gene entity")
    head_type: Literal["protein", "transcription_factor"] = Field(
        description="Type of the transcription factor entity."
    )
    relation: Literal["REGULATES", "INTERACTS_WITH"] = Field(
        description="Protein/protein or transcription factor/gene relation."
    )
    tail: str = Field(description="Tail gene entity.")
    tail_type: Literal["protein", "gene"] = Field(
        description="Tail of the gene entity."
    )


class Triple_Simple(BaseModel):
    head: str = Field(description="Head gene entity")
    relation: Literal["REGULATES", "INTERACTS_WITH"] = Field(
        description="Protein/protein or transcription factor/gene relation."
    )
    tail: str = Field(description="Tail gene entity.")


class Triples(BaseModel):
    """
    A class that contains a list of gene relations in the form of triples.
    """

    triples: List[Triple] = Field(description="List of all extracted Triples.")


class Triples_Simple(BaseModel):
    """
    A class that contains a list of gene relations in the form of triples.
    """

    triples: List[Triple_Simple] = Field(description="List of all extracted Triples.")


class TF_Triples_Simple(BaseModel):
    """
    A class that contains a list of transcription factor/gene relations in the form of triples.
    """

    triples: List[TF_Triple_Simple] = Field(
        description="List of all extracted Triples."
    )


class Proteins(BaseModel):
    """
    A class that contains a list of proteins.
    """

    proteins: List[str] = Field(description="List of all extracted proteins.")


class GenesAndTranscriptionFactors(BaseModel):
    """
    A class that contains a list of genes and transcription factors.
    """

    genes_and_transcriptionfactors: List[str] = Field(
        description="List of all extracted genes and transcription factors."
    )
