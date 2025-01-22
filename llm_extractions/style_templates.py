style_dict = {
    1: {
        "simple": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) in the text, focusing on proteins involved in signaling pathways.",
                "Now review your extracted protein-protein interactions (PPI's) to determine if "
                "they are specific to signaling pathways. Retain only signalling pathway interactions "
                "and remove the rest.",
                "Review one more time the protein-protein interactions (PPI's) to  "
                "determine whether there are in the list regulations that are of a transcriptional or gene  "
                "regulatory nature. Retain those interactions that are only specific to PPI's in cell  "
                "signalling and remove those relations that represent relations between transcription factors "
                "to their gene targets.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all transcription factor (TF) "
                "to gene relations in the text. The source of the relations that you identify should be a "
                "TF, while the target should be genes who are regulated by the TF.",
                "Now review your extracted transcription factor (TF) to gene relations to determine if "
                "they are specific to gene regulatory networks. Retain those interactions that are only "
                "involving TF's and their gene targets and remove those that are not.",
                "Review one more time the transcription factor to gene relations  "
                "to determine whether there are in the list relations that are protein-protein "
                "interactions (PPI's) network or involved in protein signalling networks. Retain interactions  "
                "of gene regulatory networks involve a transcription factor and the gene whose expression  "
                "they regulate. Remove those relations that involve interactions between two signalling protein "
                "and PPI's.",
            ],
            "lr": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all the interactions "
                "involved in cell communication networks as well as interactions between ligands "
                "and their receptor targets. Please provide the relations "
                "specifying the ligand name as the source and receptor name as the target."
            ],
        },
        "nerrel_conversational": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) in the text, focusing on proteins involved in signaling pathways.",
                "Now review the extracted proteins and extract portein-protein interactions (PPIs) between them "
                "that are specific to signaling pathways. Retain those PPI's that are specific to "
                "signalling and remove those that are not.",
                "Review one more time the protein-protein interactions (PPI'S) to determine"
                "whether there are in the list regulations that are of a transcriptional or gene regulatory"
                "nature. Retain those interactions that are only specific to PPI's in cell signalling and remove "
                "those relations that show transcription factor to their gene targets.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all transcription factor (TF) "
                "to gene relations in the text. The source of the relations that you identify should be a "
                "TF, while the target should be genes who are regulated by the TF.",
                "Now review extracted transcription factors and genes to determine interactions between them  "
                "that are specific to gene regulatory networks. Extract those relations that are only "
                "involving TF's and their gene targets and remove those that are not.",
                "Review one more time the transcription factor (TF) to gene relations "
                "to determine whether there are in the list relations that are of a protein-protein "
                "interaction (PPI's) or protein signalling nature. Retain those relations which involve "
                "a transcription factor and the gene whose expression they regulate. Remove those "
                "relations that involve interactions between two signalling protein and PPI's.",
            ],
        },
        "nerrel_individual": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all proteins "
                "in the text, focusing on proteins involved in signaling pathways.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) in the text, focusing on proteins involved in signaling pathways.",
                "Now review your extracted protein-protein interactions (PPI's) to determine if "
                "they are specific to signaling pathways. Retain those PPI's that are specific to "
                "signalling and remove those that are not.",
                "Review one more time the protein-protein interactions (PPI'S) to determine"
                "whether there are in the list regulations that are of a transcriptional or gene regulatory"
                "nature. Retain those interactions that are only specific to PPI's in cell signalling and remove "
                "those relations that show transcription factor to their gene targets.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all transcription factor (TF) "
                "to gene relations in the text. The source of the relations that you identify should be a "
                "TF, while the target should be genes who are regulated by the TF.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all transcription factor (TF) "
                "to gene relations in the text. The source of the relations that you identify should be a "
                "TF, while the target should be genes who are regulated by the TF.",
                "Now review the transcription factor (TF) to gene relations to determine if  "
                "they are specific to gene regulatory networks. Retain those relations that are only "
                "involving TF's and their gene targets and remove those that are not.",
                "Review one more time the transcription factor (TF) to gene relations "
                "to determine whether there are in the list relations that are of a protein-protein "
                "interaction (PPI's) or protein signalling nature. Retain those relations which involve "
                "a transcription factor and the gene whose expression they regulate. Remove those "
                "relations that involve interactions between two signalling protein and PPI's.",
            ],
        },
    },
    2: {
        "simple": {
            "both": [
                "You are a top-tier molecular biologist specialized in the field of  "
                "cardiology and molecular biology. Now, in step 1, your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, in step 2,  review the extracted relations from step 1. Please retain those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling (e.g. through binding, activation, inhibition, phosphorylation, "
                "etc.). Please remove those transcription factor to gene relations that are involved "
                "in gene regulatory networks (e.g. regulation of expression or suppression of a gene).",
                "Review the extracted relations from step 1 again. Please retain those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks (e.g. regulation of "
                "expression or suppression of a gene). Please remove those relations which correspond to "
                "protein-protein interactions that are involved in cell-signalling (e.g. through binding, "
                "activation, inhibition, phosphorylation, etc.).",
            ],
            "lr": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all the interactions "
                "involved in cell communication networks as well as interactions between ligands "
                "and their receptor targets. Please provide the relations "
                "specifying the ligand name as the source and receptor name as the target.",
                "Now, review the extracted relations. Please retain those relations which "
                "correspond to ligand-receptor interactions and make sure that they do not "
                "correspond to any type of interaction such as intra-cellular protein-protein "
                "interactions or transcription factor to gene target relations of a gene regulatory "
                "network.",
            ],
        },
        # "complex": {
        #     "both": [
        #         "You are a top-tier molecular biologist specialized in the field of  "
        #         "cardiology and molecular biology. Now, in step 1, your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, in step 2, review the extracted relations. Please retain those relations which "
        #         "correspond to protein-protein interactions (PPI's) that are involved in "
        #         "cell-signalling (e.g. through binding, activation, inhibition, phosphorylation, "
        #         "etc.). Please remove those transcription factor (TF) to gene relations that are involved "
        #         "in gene regulatory networks (e.g. regulation of expression or suppression of a gene). "
        #         "For context, here is a good example to fulfil this request: "
        #         "'JAKs phosphorylate cytokine receptors which can bind a protein called Grb2. "
        #         "Grb2 then activates SOS proteins which stimulate MAPK signalling. MAPK can also "
        #         "phosphorylate STATs. Phosphorylated cytokine receptors can also be bound by PI3K, "
        #         "which allows activation of AKT. There is a broad range of genes that are regulated "
        #         "by STATs and none likely have as many broad functions as c-Fos and HIF-1α. STAT3 "
        #         "target genes include cyclin D1, BclXL, c-Myc, β-catenin, nuclear factor-κB (NF-κB)'."
        #         "Here a good output would be giving relations involving protein interactions such as: "
        #         "JAK phosphorylates cytokine receptors; cytokine receptors bind to Grb2; Grb2 activates "
        #         "SOS; SOS stimulates MAPK; MAPK phosphorylates STATS; Grb2 activates SOS; "
        #         "cytokine receptors binds PI3K; PI3K activates AKT."
        #         "Here a bad output would be giving relations involving gene regulatory relations such as:"
        #         "STATs regulates c-Fos; STATs regulate HIF-1α; STAT3 targets Cyclin D1; STAT3 targets BclXL; "
        #         "STAT3 targets y-Myc; STAT3 targets β-catenin; STAT3 targets NF-κB.",
        #         "Review the extracted relations from step 1 again. Please retain those transcription factor (TF) "
        #         "to gene relations that are involved in gene regulatory networks (e.g. regulation of  "
        #         "expression or suppression of a gene). Please remove those relations which correspond to  "
        #         "protein-protein interactions (PPI's) that are involved in cell-signalling (e.g. through  "
        #         "binding, activation, inhibition, phosphorylation, etc.). "
        #         "For context, here is a good example to fulfil this request: "
        #         "'JAKs phosphorylate cytokine receptors which can bind a protein called Grb2.  "
        #         "Grb2 then activates SOS proteins which stimulate MAPK signalling. MAPK can also  "
        #         "phosphorylate STATs. Phosphorylated cytokine receptors can also be bound by PI3K,  "
        #         "which allows activation of AKT. There is a broad range of genes that are regulated  "
        #         "by STATs and none likely have as many broad functions as c-Fos and HIF-1α. STAT3  "
        #         "target genes include cyclin D1, BclXL, c-Myc, β-catenin, nuclear factor-κB (NF-κB)'. "
        #         "Here a good output would be giving relations involving gene regulatory relations such as: "
        #         "STATs regulates c-Fos; STATs regulate HIF-1α; STAT3 targets Cyclin D1; STAT3 targets BclXL; "
        #         "STAT3 targets y-Myc; STAT3 targets β-catenin; STAT3 targets NF-κB. "
        #         "Here a bad output would be giving relations involving protein interactions such as: "
        #         "JAK phosphorylates cytokine receptors; cytokine receptors bind to Grb2; Grb2 activates "
        #         "SOS; SOS stimulates MAPK; MAPK phosphorylates STATS; Grb2 activates SOS; "
        #         "cytokine receptors binds PI3K; PI3K activates AKT.",
        #     ],
        # },
    },
    3: {
        "simple": {
            "both": [
                "You are a top-tier molecular biologist specialized in the field of  "
                "cardiology and molecular biology. Now, in step 1, your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, in step 2, review the extracted relations from step 1. Please retain those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks (e.g. regulation of "
                "expression or suppression of a gene). Please remove those relations which correspond to "
                "protein-protein interactions that are involved in cell-signalling (e.g. through binding, "
                "activation, inhibition, phosphorylation, etc.).",
                "Now, review the extracted relations from step 1 again. Please retain those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling (e.g. through binding, activation, inhibition, phosphorylation, "
                "etc.). Please remove those transcription factor to gene relations that are involved "
                "in gene regulatory networks (e.g. regulation of expression or suppression of a gene).",
            ],
            "lr": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all the interactions "
                "involved in cell communication networks as well as interactions between ligands "
                "and their receptor targets. Please provide the relations "
                "specifying the ligand name as the source and receptor name as the target.",
                "Now, review the extracted relations. Please retain those relations which "
                "correspond to ligand-receptor interactions and make sure that they do not "
                "correspond to any type of interaction such as intra-cellular protein-protein "
                "interactions or transcription factor to gene target relations of a gene regulatory "
                "network."
                "Please keep in mind that a ligand can be hormones, growth factors, chemokines, "
                "cytokines and neurotransmitters. Receptors can be proteins or protein complexes "
                "situated in the membrane of the receiver cells.",
            ],
        },
        # "complex": {
        #     "both": [
        #         "You are a top-tier molecular biologist specialized in the field of  "
        #         "cardiology and molecular biology. Now, in step 1, your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations from step 1. Please retain those transcription factor (TF) "
        #         "to gene relations that are involved in gene regulatory networks (e.g. regulation of  "
        #         "expression or suppression of a gene). Please remove those relations which correspond to  "
        #         "protein-protein interactions (PPI's) that are involved in cell-signalling (e.g. through  "
        #         "binding, activation, inhibition, phosphorylation, etc.). "
        #         "For context, here is a good example to fulfil this request: "
        #         "'JAKs phosphorylate cytokine receptors which can bind a protein called Grb2.  "
        #         "Grb2 then activates SOS proteins which stimulate MAPK signalling. MAPK can also  "
        #         "phosphorylate STATs. Phosphorylated cytokine receptors can also be bound by PI3K,  "
        #         "which allows activation of AKT. There is a broad range of genes that are regulated  "
        #         "by STATs and none likely have as many broad functions as c-Fos and HIF-1α. STAT3  "
        #         "target genes include cyclin D1, BclXL, c-Myc, β-catenin, nuclear factor-κB (NF-κB)'. "
        #         "Here a good output would be giving relations involving gene regulatory relations such as: "
        #         "STATs regulates c-Fos; STATs regulate HIF-1α; STAT3 targets Cyclin D1; STAT3 targets BclXL; "
        #         "STAT3 targets y-Myc; STAT3 targets β-catenin; STAT3 targets NF-κB. "
        #         "Here a bad output would be giving relations involving protein interactions such as: "
        #         "JAK phosphorylates cytokine receptors; cytokine receptors bind to Grb2; Grb2 activates "
        #         "SOS; SOS stimulates MAPK; MAPK phosphorylates STATS; Grb2 activates SOS; "
        #         "cytokine receptors binds PI3K; PI3K activates AKT.",
        #         "Now, review the extracted relations from step 1 again. Please retain those relations which "
        #         "correspond to protein-protein interactions (PPI's) that are involved in "
        #         "cell-signalling (e.g. through binding, activation, inhibition, phosphorylation, "
        #         "etc.). Please remove those transcription factor (TF) to gene relations that are involved "
        #         "in gene regulatory networks (e.g. regulation of expression or suppression of a gene). "
        #         "For context, here is a good example to fulfil this request: "
        #         "'JAKs phosphorylate cytokine receptors which can bind a protein called Grb2. "
        #         "Grb2 then activates SOS proteins which stimulate MAPK signalling. MAPK can also "
        #         "phosphorylate STATs. Phosphorylated cytokine receptors can also be bound by PI3K, "
        #         "which allows activation of AKT. There is a broad range of genes that are regulated "
        #         "by STATs and none likely have as many broad functions as c-Fos and HIF-1α. STAT3 "
        #         "target genes include cyclin D1, BclXL, c-Myc, β-catenin, nuclear factor-κB (NF-κB)'."
        #         "Here a good output would be giving relations involving protein interactions such as: "
        #         "JAK phosphorylates cytokine receptors; cytokine receptors bind to Grb2; Grb2 activates "
        #         "SOS; SOS stimulates MAPK; MAPK phosphorylates STATS; Grb2 activates SOS; "
        #         "cytokine receptors binds PI3K; PI3K activates AKT."
        #         "Here a bad output would be giving relations involving gene regulatory relations such as:"
        #         "STATs regulates c-Fos; STATs regulate HIF-1α; STAT3 targets Cyclin D1; STAT3 targets BclXL; "
        #         "STAT3 targets y-Myc; STAT3 targets β-catenin; STAT3 targets NF-κB.",
        #     ],
        # },
        "simple": {
            "both": [
                "You are a top-tier molecular biologist specialized in the field of  "
                "cardiology and molecular biology. Now, in step 1, your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins, genes and transcription factors that are mentioned in the text.",
                "Now, in step 2, review the extracted entities from step 1. Please  output those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks (e.g. regulation of "
                "expression or suppression of a gene). Please remove those relations which correspond to "
                "protein-protein interactions that are involved in cell-signalling (e.g. through binding, "
                "activation, inhibition, phosphorylation, etc.).",
                "Now, review the extracted entities from step 1 and the relations from step 2 again. Please output those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling (e.g. through binding, activation, inhibition, phosphorylation, "
                "etc.). Please ignore those transcription factor to gene relations that are involved "
                "in gene regulatory networks (e.g. regulation of expression or suppression of a gene).",
            ],
        },
    },
    4: {
        "simple": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please retain those relations which "
                "correspond to protein-protein interactions that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please retain those transcription factor to "
                "gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
            ],
            "lr": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all the interactions "
                "involved in cell communication networks as well as interactions between ligands "
                "and their receptor targets. Please provide the relations "
                "specifying the ligand name as the source and receptor name as the target.",
                "Now, review the extracted relations. Please retain those relations which "
                "correspond to ligand-receptor interactions and make sure that they do not "
                "correspond to any type of interaction such as intra-cellular protein-protein "
                "interactions or transcription factor to gene target relations of a gene regulatory "
                "network."
                "The nature of the interaction that you report can be of the following types: "
                "i) Autocrine (intracellular communication whereby cells secrete ligands that are used "
                "to induce a cellular in receptors expressed on the same cell); ii) Paracrine (where "
                "the interaction depends on the diffusion of signalling molecules from one cell to another "
                "after secretion); and iii) Endocrine (whereby ligands are secreted and travel long "
                "distances through extracellular fluids such as the blood plasma; typical mediators of "
                "this communication are hormones).",
            ],
        },
        # "complex": {
        #     "ppi": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations. Please retain those relations which "
        #         "correspond to protein-protein interactions that are involved in cell-signalling.  "
        #         "Please remove those transcription factor (Tf) to gene relations that are involved  "
        #         "in gene regulatory networks. "
        #         "For context, here are provided a list of interactions types that are involved in  "
        #         "cell-signalling that you might find in text and which might help you correctly  "
        #         "identify protein-protein interaction pairs which you need to keep: "
        #         "i) Physical interactions (e.g. binding, dimerization, oligomerizationm, protein "
        #         "complexes). "
        #         "ii) Enzymatic modifications (e.g. phosphorylation, ubiquitination, acetylation, "
        #         "methylation, proteolytic Cleavage). "
        #         "iii) Regulatory interactions (e.g. activation, inhibition, interaction) "
        #         "iv) Signaling interactions (e.g. signaling cascades, signaling pathways, "
        #         "signal transduction, scaffolding) "
        #         "v) Transport and localization (e.g. chaperone interaction, anchor and localization)",
        #     ],
        #     "tf": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations. Please retain those transcription factor (TF) "
        #         "to gene relations that are involved in gene regulatory networks. Please remove those "
        #         "relations which correspond to protein-protein interactions (PPI'S) that are involved in "
        #         "cell-signalling. "
        #         "For context, here are provided a list of relations types that are involved in gene "
        #         "regulatory networks that you might find in text and which might help you correctly "
        #         "identify TF-Gene relation pairs which you need to keep: "
        #         "i) Gene activation (when a TF promotes the transcription of a target gene, leading "
        #         "to increased expression of that gene) "
        #         "ii) Gene supression (when a TF suppresses the transcription of a target gene, leading  "
        #         "to decreased expression of that gene) "
        #         "iii) Epigenetic regulation (modifications that affect gene accessibility)",
        #     ],
        # },
        "nerrel_conversational": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "Now, review the extracted proteins. Please retain those relations which "
                "correspond to protein-protein interactions that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "Now, review the extracted genes and transcription factors. Please retain those transcription factor to "
                "gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
            ],
        },
        "nerrel_individual": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now review your extracted protein-protein interactions (PPI's) to determine if "
                "correspond to protein-protein interactions that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please retain those transcription factor to "
                "gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions (PPI's) that are involved in "
                "cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
            ],
        },
    },
    5: {
        "simple": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now review the extracted relations. Please retain those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
                "Review one more time the protein-protein interactions (PPI'S) and remove "
                "those relation that are of a transcriptional or gene regulatory nature. For context, "
                "here are provided a list of relations types that are involved in gene regulatory networks"
                "that you might find in text and which might help you correctly identify transcription factor (TF) "
                "to gene relation pairs before removing them: activation or supression of a gene and epigenetic "
                "regulation.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please retain those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions that are involved in cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
                "Review one more time the transcription factor (TF) to gene relations "
                "and remove those relations which correspond to protein-protein interactions that are involved in "
                "cell-signalling. For context, here are provided a list of interactions types that are involved in "
                "cell-signalling that you might find in text and which might help you correctly "
                "identify protein-protein interaction pairs which you need to remove: binding, protein"
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
            "lr": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all the interactions "
                "involved in cell communication networks as well as interactions between ligands "
                "and their receptor targets. Please provide the relations "
                "specifying the ligand name as the source and receptor name as the target.",
                "Now, review the extracted relations. Please retain those relations which "
                "correspond to ligand-receptor interactions and make sure that they do not "
                "correspond to any type of interaction such as intra-cellular protein-protein "
                "interactions or transcription factor to gene target relations of a gene regulatory "
                "network."
                "Please keep in mind that a ligand can be hormones, growth factors, chemokines, "
                "cytokines and neurotransmitters. Receptors can be proteins or protein complexes "
                "situated in the membrane of the receiver cells. The nature of the interaction that "
                "you report can be of the following types: i) Autocrine (intracellular communication "
                "whereby cells secrete ligands that are used to induce a cellular in receptors expressed "
                "on the same cell); ii) Paracrine (where the interaction depends on the diffusion of s "
                "ignalling molecules from one cell to another after secretion); and iii) Endocrine (whereby "
                "ligands are secreted and travel long distances through extracellular fluids such as the "
                "blood plasma; typical mediators of this communication are hormones).",
            ],
        },
        # "complex": {
        #     "ppi": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations. Please retain those relations which "
        #         "correspond to protein-protein interactions that are involved in cell-signalling.  "
        #         "Please remove those transcription factor (TF) to gene relations that are involved  "
        #         "in gene regulatory networks. "
        #         "For context, here are provided a list of interactions types that are involved in  "
        #         "cell-signalling that you might find in text and which might help you correctly  "
        #         "identify protein-protein interaction pairs which you need to keep: "
        #         "i) Physical interactions (e.g. binding, dimerization, oligomerizationm, protein "
        #         "complexes). "
        #         "ii) Enzymatic modifications (e.g. phosphorylation, ubiquitination, acetylation, "
        #         "methylation, proteolytic Cleavage). "
        #         "iii) Regulatory interactions (e.g. activation, inhibition, interaction) "
        #         "iv) Signaling interactions (e.g. signaling cascades, signaling pathways, "
        #         "signal transduction, scaffolding) "
        #         "v) Transport and localization (e.g. chaperone interaction, anchor and localization)",
        #         "Review one more time the protein-protein interactions (PPI's) and remove "
        #         "those relation that are of a transcriptional or gene regulatory nature. For context,  "
        #         "here are provided a list of relations types that are involved in gene regulatory networks "
        #         "that you might find in text and which might help you correctly identify transcription factor (TF)  "
        #         "to gene relation pairs before removing them: "
        #         "i) Gene activation (when a TF promotes the transcription of a target gene, leading to increased  "
        #         "expression of that gene) "
        #         "ii) Gene supression (when a TF suppresses the transcription of a target gene, leading to decreased  "
        #         "expression of that gene) "
        #         "iii) Epigenetic regulation (modifications that affect gene accessibility)",
        #     ],
        #     "tf": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations. Please retain those trnacription factor (TF) "
        #         "to gene relations that are involved in gene regulatory networks. Please remove those "
        #         "relations which correspond to protein-protein interactions (PPI's) that are involved "
        #         "in cell-signalling. "
        #         "For context, here are provided a list of relations types that are involved in gene "
        #         "regulatory networks that you might find in text and which might help you correctly "
        #         "identify TF-Gene relation pairs which you need to keep: "
        #         "i) Gene activation (when a TF promotes the transcription of a target gene, leading "
        #         "to increased expression of that gene) "
        #         "ii) Gene supression (when a TF suppresses the transcription of a target gene, leading  "
        #         "to decreased expression of that gene) "
        #         "iii) Epigenetic regulation (modifications that affect gene accessibility)",
        #         "Review one more time the transcription factor (TF) to gene relations "
        #         "and remove those relations which correspond to protein-protein interactions (PPI's) "
        #         "that are involved in cell-signalling. "
        #         "For context, here are provided a list of interactions types that are involved in "
        #         "cell-signalling that you might find in text and which might help you correctly "
        #         "identify protein-protein interaction pairs which you need to remove: "
        #         "i) Physical interactions (e.g. binding, dimerization, oligomerizationm, protein "
        #         "complexes). "
        #         "ii) Enzymatic modifications (e.g. phosphorylation, ubiquitination, acetylation, "
        #         "methylation, proteolytic Cleavage). "
        #         "iii) Regulatory interactions (e.g. activation, inhibition, interaction) "
        #         "iv) Signaling interactions (e.g. signaling cascades, signaling pathways, "
        #         "signal transduction, scaffolding) "
        #         "v) Transport and localization (e.g. chaperone interaction, anchor and localization)",
        #     ],
        # },
        "nerrel_conversational": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "Now review the extracted proteins. Please retain those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
                "Review one more time the protein-protein interactions (PPI'S) and remove "
                "those relation that are of a transcriptional or gene regulatory nature. For context, "
                "here are provided a list of relations types that are involved in gene regulatory networks"
                "that you might find in text and which might help you correctly identify transcription factor (TF) "
                "to gene relation pairs before removing them: activation or supression of a gene and epigenetic "
                "regulation.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "Now, review the extracted genes and transcription factors. Please retain those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions that are involved in cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
                "Review one more time the transcription factor (TF) to gene relations "
                "and remove those relations which correspond to protein-protein interactions that are involved in "
                "cell-signalling. For context, here are provided a list of interactions types that are involved in "
                "cell-signalling that you might find in text and which might help you correctly "
                "identify protein-protein interaction pairs which you need to remove: binding, protein"
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
        },
        "nerrel_individual": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network. ",
                "Now review the extracted relations. Please retain those relations which "
                "correspond to protein-protein interactions (PPI's) that are involved in cell-signalling.  "
                "Please remove those transcription factor (TF) to gene relations that are involved  "
                "in gene regulatory networks. "
                "For context, here are provided a list of interactions types that are involved in  "
                "cell-signalling that you might find in text and which might help you correctly  "
                "identify protein-protein interaction pairs which you need to keep: binding, protein "
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
                "Review one more time the protein-protein interactions (PPI'S) and remove "
                "those relation that are of a transcriptional or gene regulatory nature. For context, "
                "here are provided a list of relations types that are involved in gene regulatory networks"
                "that you might find in text and which might help you correctly identify transcription factor (TF) "
                "to gene relation pairs before removing them: activation or supression of a gene and epigenetic "
                "regulation.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please retain those transcription factor (TF) "
                "to gene relations that are involved in gene regulatory networks. Please remove those "
                "relations which correspond to protein-protein interactions that are involved in cell-signalling. "
                "For context, here are provided a list of relations types that are involved in gene "
                "regulatory networks that you might find in text and which might help you correctly "
                "identify TF-Gene relation pairs which you need to keep: activation or supression of "
                "a gene and epigenetic regulation.",
                "Review one more time the transcription factor (TF) to gene relations "
                "and remove those relations which correspond to protein-protein interactions that are involved in "
                "cell-signalling. For context, here are provided a list of interactions types that are involved in "
                "cell-signalling that you might find in text and which might help you correctly "
                "identify protein-protein interaction pairs which you need to remove: binding, protein"
                "complexes, phosphorylation, activation, inhibition, interaxtion.",
            ],
        },
    },
    6: {
        "simple": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted interactions. Please report those interactions "
                "whose protein members bind and interact to each other or form protein complexes.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to activate or enhance the activity ofits target protein.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to inhibit or reduce the activity of its target protein.",
                "Review the interactions a last time. Please report those interactions in "
                "which one source protein is reported to either phosphorylate or dephosphorylate its target protein.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted relations. Please report those relations in which a "
                "transcription factor (TF) orchestrates the activation, regulation or expression of a gene. In this "
                "case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene.",
                "Review the relations again. Please report those relations in which a "
                "transcription factor (TF) orchestrates the inactivation, down-regulation or supression of a gene. "
                "In this case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene. In this case, an inactivation happens when a TF suppresses the "
                "transcription of a target gene, leading to decreased expression of that gene.",
            ],
        },
        "nerrel_conversational": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "Now, review the extracted proteins. Please report those interactions "
                "whose protein members bind and interact to each other or form protein complexes.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to activate or enhance the activity ofits target protein.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to inhibit or reduce the activity of its target protein.",
                "Review the interactions a last time. Please report those interactions in "
                "which one source protein is reported to either phosphorylate or dephosphorylate its target protein.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "Now, review the extracted genes and transcription factors. Please report those relations in which a "
                "transcription factor (TF) orchestrates the activatiGon, regulation or expression of a gene. In this "
                "case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene.",
                "Review the relations again. Please report those relations in which a "
                "transcription factor (TF) orchestrates the inactivation, down-regulation or supression of a gene. "
                "In this case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene. In this case, an inactivation happens when a TF suppresses the "
                "transcription of a target gene, leading to decreased expression of that gene.",
            ],
        },
        "nerrel_individual": {
            "ppi": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named proteins that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted interactions. Please report those interactions "
                "whose protein members bind and interact to each other or form protein complexes.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to activate or enhance the activity ofits target protein.",
                "Review the interactions again. Please report those interactions in "
                "which one source protein is reported to inhibit or reduce the activity of its target protein.",
                "Review the interactions a last time. Please report those interactions in "
                "which one source protein is reported to either phosphorylate or dephosphorylate its target protein.",
            ],
            "tf": [
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                # "To start off, first extract a list of all named genes and transcription factors that are mentioned in the text.",
                "You are a top-tier molecular biologist specialized in the field of "
                "cardiology and molecular biology. Your task is to identify all protein-protein "
                "interactions (PPI's) involved in signalling as well as relations between transcription  "
                "factors (TF) and their target genes of a gene regulatory network.",
                "Now, review the extracted interactions. Please report those relations in which a "
                "transcription factor (TF) orchestrates the activation, regulation or expression of a gene. In this "
                "case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene.",
                "Review the relations again. Please report those relations in which a "
                "transcription factor (TF) orchestrates the inactivation, down-regulation or supression of a gene. "
                "In this case an activation happens when a TF promotes the transcription of a target gene, leading "
                "to increased expression of that gene. In this case, an inactivation happens when a TF suppresses the "
                "transcription of a target gene, leading to decreased expression of that gene.",
            ],
        },
        # "complex": {
        #     "ppi": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted interactions. Please report those interactions "
        #         "whose protein members bind and interact to each other or form protein complexes. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'Immunofluorescence staining and co-immunoprecipitation showed that FAPα and ITGA5  "
        #         "formed protein complexes in the inflammatory microenvironment.' "
        #         "Here a good output would be reporting that: FAPα interacts with ITGA5.",
        #         "Review the interactions again. Please report those interactions in "
        #         "which one source protein is reported to activate or enhance the activity ofits target protein. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'RAS proteins are small GTPases that act as molecular switches in various signaling  "
        #         "pathways, including MAPK.  Once active, RAS recruits and activates RAF. RAF phosphorylates  "
        #         "and activates MEK1/2, which in turn phosphorylates ERK1/2. Active ERK translocates to the  "
        #         "nucleus to regulate gene transcription involved in cell proliferation, differentiation,  "
        #         "and survival.' "
        #         "Here a good output would be reporting that: RAS activates RAF, RAF activates MEK1/2.",
        #         "Review the interactions again. Please report those interactions in "
        #         "which one source protein is reported to inhibit or reduce the activity of its target protein. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'When PDE8A binds to BRAF, it can reduce BRAF's ability to activate MEK and downstream  "
        #         "MAPK signaling.' "
        #         "Here a good output would be reporting that: PDE8A inhibits BRAF.",
        #         "Review the interactions a last time. Please report those interactions in "
        #         "which one source protein is reported to either phosphorylate or dephosphorylate its target protein. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'RAS proteins are small GTPases that act as molecular switches in various signaling  "
        #         "pathways, including MAPK.  Once active, RAS recruits and activates RAF. RAF phosphorylates  "
        #         "and activates MEK1/2, which in turn phosphorylates ERK1/2. Active ERK translocates to the  "
        #         "nucleus to regulate gene transcription involved in cell proliferation, differentiation,  "
        #         "and survival.' "
        #         "Here a good output would be reporting that: RAF phosphorylates MEK1/2, MEK1/2 phosphorylates ERK1/2.",
        #     ],
        #     "tf": [
        #         "You are a top-tier molecular biologist specialized in the field of "
        #         "cardiology and molecular biology. Your task is to identify all protein-protein "
        #         "interactions (PPI's) involved in signalling as well as relations between transcription  "
        #         "factors (TF) and their target genes of a gene regulatory network.",
        #         "Now, review the extracted relations. Please report those relations in which a "
        #         "transcription factor (TF) orchestrates the activation, regulation or expression of a gene. In this "
        #         "case an activation happens when a TF promotes the transcription of a target gene, leading "
        #         "to increased expression of that gene. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'HIF1A regulate several genes that confer stemness properties including the well-known OCT4 (POU5F1), "
        #         "as well as many genes that are involved in epithelial to mesenchymal transition (EMT) during "
        #         "development and utilized by cancer cells in metastasis and invasion such as LOX, MMP1 and TWIST' "
        #         "Here a good output would be reporting that: HIF1A regulates OCT4, HIF1A regulates POU5F1, HIF1A regulates "
        #         "LOX, HIF1A regulates MMP1, HIF1A regulates TWIST.",
        #         "Review the relations again. Please report those relations in which a "
        #         "transcription factor (TF) orchestrates the inactivation, down-regulation or supression of a gene. "
        #         "In this case an activation happens when a TF promotes the transcription of a target gene, leading "
        #         "to increased expression of that gene. In this case, an inactivation happens when a TF suppresses the "
        #         "transcription of a target gene, leading to decreased expression of that gene. "
        #         "For context, here is a good example to fulfil this request: "
        #         "'Consequently, the activation of these repressive components could ultimately result in the repression  "
        #         "of target genes. For instance, MYC has been shown to repress p53' "
        #         "Here a good output would be reporting that: MYC repress p53. ",
        #     ],
        # },
    },
}

# "You are a top-tier molecular biologist specialized in the field of  "
# "cardiology and molecular biology. Your task is to identify all protein-protein  "
# "interactions (PPI's) in the text, focusing on proteins involved in signaling pathways. "
# "To start off, extract a list of all named proteins that are mentioned in the text.",
