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
+ Synonyms of entities participating in PPI interactions from the RegulaTome corpus (*regulatome_synonyms*)
+ PPI evaluations over the selected Manuscript corpus (*manuscript_eval_ppi*)

The JSON files being contained in each of these directories have been named according to the type as well as the LLM model used for evaluation (Please refer to the study manuscript for the nomenclature).

### llm_evaluations
Here we provide the scripts that were used to calculate and visualize the precision-recall values for PPI relation extraction in the RegulaTome and the selected manuscript corpus.
