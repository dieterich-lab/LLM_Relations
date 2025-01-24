# LLM_Relations
This is the documentation for the **Reading papers: Extraction of molecular interaction networks with large language models** study.

Questions about the study can be addressed to [Enio Gjerga](E.Gjerga@uni-heidelberg.de), [Philipp Wiesenbach](philipp.wiesenbach@gmail.com) or [Prof. Christoph Dieterich](christoph.dieterich@uni-heidelberg.de) or feel free to open an Issue for anything related to the code.

This study makes use of the [RegulaTome](https://academic.oup.com/database/article/doi/10.1093/database/baae095/7756349) corpus of literature, so we suggest to have a look at this study first.

### License
Distributed under the GNU GPLv3 License.

## Code Organization
The code and results have been organized in the following direcotries:

### llm_files
Here we provide the structured JSON files for each case study:

+ PPI evaluations over the RegulaTome corpus (*regulatome_eval_ppi*)
+ GRN evaluations over the RegulaTome corpus (*regulatome_eval_grn*)
+ PPI evaluations over the selected Manuscript corpus (*manuscript_eval_ppi*)

The JSON files being contained in each of these directories have been named according to the type as well as the LLM model used for evaluation (Please refer to the study manuscript for the nomenclature).

### llm_evaluations
Here we provide the scripts that were used to calculate and visualize the precision-recall values for PPI and GRN relation extraction in the RegulaTome and the selected manuscript corpus.

#### PPI Evaluation over the RegulaTome corpus (regulatome_eval_ppi)
The following R-scripts can be found in the dirctory and which should be run in the order presented in this documentation.

**1.** *data_preparation.R*
Here are provided the scripts that Read through the RegulaTome resource and then generate tables of PPI and GRN/TF-Gene annotated relations as well as entities in the *src/* directory. For this the RegulaTome courpus can be read from the *devel/*, *test/* and *train/* direcotries and which can be downloaded from the Zenodo link published in [RegulaTome](https://zenodo.org/records/10808330).

**2.** *evaluate_regulatome.R*
This script is used to calculate the average weighted RE precision-recall metrics for PPI and GRN relations based on the categories of relations that were originally described in RegulaTome. Evaluation results have been stored in the *output/* directory.

**3.** *analysis_script_stas_all.R*
Here we evaluate PPI RE's without prior filtering of ground truth and LLM outputs for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
and "wikigene_description" attributes). Evaluation results have been stored in the *output/* directory.

**4.** *analysis_script_stas_ensembl.R*
Here we evaluate PPI RE's with prior filtering of ground truth and LLM outputs for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
and "wikigene_description" attributes). Evaluation results have been stored in the *output/* directory.

#### GRN Evaluation over the RegulaTome corpus (regulatome_eval_grn)
The following R-scripts can be found in the dirctory and which should be run in the order presented in this documentation.

**1.** *data_preparation.R*
Here are provided the scripts that Read through the RegulaTome resource and then generate tables of PPI and GRN/TF-Gene annotated relations as well as entities in the *src/* directory. For this the RegulaTome courpus can be read from the *devel/*, *test/* and *train/* direcotries and which can be downloaded from the Zenodo link published in [RegulaTome](https://zenodo.org/records/10808330).

**2.** *evaluate_regulatome.R*
This script is used to calculate the average weighted RE precision-recall metrics for PPI and GRN relations based on the categories of relations that were originally described in RegulaTome. Evaluation results have been stored in the *output/* directory.

**3.** *analysis_script_stas_all.R*
Here we evaluate GRN RE's without prior filtering of ground truth and LLM outputs for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
and "wikigene_description" attributes). Evaluation results have been stored in the *output/* directory.

**4.** *analysis_script_stas_ensembl.R*
Here we evaluate GRN RE's with prior filtering of ground truth and LLM outputs for relations consisting of Ensembl entities ("external_gene_name", "external_synonym", 
and "wikigene_description" attributes). Evaluation results have been stored in the *output/* directory.

#### PPI Evaluation over the Cardiac Manuscript corpus (manuscript_eval_grn)
The following R-scripts can be found in the dirctory and which should be run in the order presented in this documentation.

**1.** *analysis_script_stas.R*
Here we evaluate PPI RE's over the manually annotated corpus of the selected 5 cardiac manuscripts. Evaluation results have been stored in the *output/* directory.
