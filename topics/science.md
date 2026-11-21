# 과학·바이오·데이터 분석 (142개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/science.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-science && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-science && cd /tmp/ccs-science && git sparse-checkout set skills/13c-metabolic-flux skills/adaptyv skills/aeon skills/alphagenome skills/analytical-method-validation skills/anndata skills/arbor skills/arboreto skills/astropy skills/benchling-integration skills/bids skills/biopython skills/bioservices skills/bulk-rnaseq skills/cantera skills/cellprofiler skills/cellxgene-census skills/cirq skills/clinical-decision-support skills/clinical-reports skills/cobrapy skills/dask skills/database-lookup skills/datalad skills/datamol skills/deepchem skills/deepspot-m skills/deeptools skills/depmap skills/diffdock skills/dnanexus-integration skills/esm skills/etetoolkit skills/experiment-design skills/experimental-design skills/exploratory-data-analysis skills/fictiv skills/flowio skills/flowkit skills/fluidsim skills/folklore-variant-evidence skills/geniml skills/genomic-coordinates skills/genomic-intelligence skills/geomaster skills/geopandas skills/get-available-resources skills/gget skills/ginkgo-cloud-lab skills/glycoengineering skills/gtars skills/histolab skills/hugging-science skills/imaging-data-commons skills/iso-standards-readiness skills/lab-hardware-cad skills/labarchive-integration skills/lamindb skills/latchbio-integration skills/mageck skills/marine-carbonate-chemistry skills/matchms skills/matlab skills/matplotlib skills/medchem skills/modal skills/molecular-dynamics skills/molfeat skills/ncats-arax skills/networkx skills/neurokit2 skills/neuropixels-analysis skills/nextflow skills/nmrglue skills/nwb-conversion skills/omero-integration skills/onekgpd skills/ontology-term-resolution skills/openpiv skills/opentrons-integration skills/optimize-for-gpu skills/pacsomatic skills/pathml skills/pathogen-variant-surveillance skills/pathway-enrichment skills/pennylane skills/phylogenetics skills/pkpd-modeling skills/polars skills/polars-bio skills/primekg skills/primer-design skills/protocolsio-integration skills/pufferlib skills/pybamm skills/pycalphad skills/pydeseq2 skills/pydicom skills/pyhealth skills/pylabrobot skills/pymatgen skills/pymc skills/pymoo skills/pyopenms skills/pysam skills/pytdc skills/pytorch-lightning skills/qiime2-amplicon skills/qiskit skills/qutip skills/rdkit skills/relion skills/relsa-severity-assessment skills/rowan skills/scanpy skills/scientific-visualization skills/scikit-bio skills/scikit-learn skills/scikit-survival skills/scvelo skills/scvi-tools skills/seaborn skills/shap skills/simpy skills/stable-baselines3 skills/statistical-analysis skills/statistical-power skills/statsmodels skills/sympy skills/tamarind skills/tellurium skills/tiledbvcf skills/torch-geometric skills/torchdrug skills/transformers skills/treatment-plans skills/umap-learn skills/uncertainty-and-units skills/usfiscaldata skills/vaex skills/waypoint-bio skills/zarr-python && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [13c-metabolic-flux](../skills/13c-metabolic-flux) | Estimates intracellular metabolic fluxes from steady-state carbon-13 isotope-tracing measurements using validated atom maps, mfapy isotope s |  |
| [adaptyv](../skills/adaptyv) | Uses the Adaptyv Bio Foundry API and Python SDK to design protein characterization experiments, estimate costs, submit sequences, monitor la |  |
| [aeon](../skills/aeon) | This skill should be used for time series machine learning tasks including classification, regression, clustering, forecasting, anomaly dete |  |
| [alphagenome](../skills/alphagenome) | Looks up precomputed AlphaGenome Atlas effects for any GRCh38 single-nucleotide variant (AVI score with Phred and 18 SHAP feature attributio |  |
| [analytical-method-validation](../skills/analytical-method-validation) | Plans, executes, and documents validation, verification, and transfer of analytical procedures under the governing framework - ICH Q2(R2) an | method validation·analytical method validation·AMV |
| [anndata](../skills/anndata) | Handles annotated matrices in single-cell analysis, .h5ad and Zarr files, and integration with the scverse ecosystem. This is the data forma |  |
| [arbor](../skills/arbor) | Applies Arbor Hypothesis Tree Refinement to research artifacts with repeatable evaluators, including model training, agent harnesses, data s |  |
| [arboreto](../skills/arboreto) | Infers candidate gene regulatory networks from bulk or single-cell expression data using AertsLab Arboreto GRNBoost2 and GENIE3. Use for tra |  |
| [astropy](../skills/astropy) | Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tabl |  |
| [benchling-integration](../skills/benchling-integration) | Benchling Python SDK and REST API integration for registry entities, inventory, ELN entries, workflows, Benchling Apps, and Data Warehouse q |  |
| [bids](../skills/bids) | > Organizes, queries, validates, and converts Brain Imaging Data Structure (BIDS) datasets. Supports organizing neuroscience and biomedical  |  |
| [biopython](../skills/biopython) | Provides Biopython workflows for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogenetics, and programmatic NCBI/PubMed access |  |
| [bioservices](../skills/bioservices) | Provides a Python interface to bioinformatics services including UniProt, KEGG, ChEMBL, Reactome, QuickGO, and UniChem. Used for cross-datab |  |
| [bulk-rnaseq](../skills/bulk-rnaseq) | Prepares bulk RNA-seq FASTQ, Salmon, STAR or featureCounts output for gene-level differential expression. Covers nf-core/rnaseq and standalo |  |
| [cantera](../skills/cantera) | Runs Cantera homogeneous chemical reactors and evaluates ignition delay with mechanism provenance, conservation checks, and numerical refine |  |
| [cellprofiler](../skills/cellprofiler) | Runs reproducible CellProfiler microscopy pipelines for nuclear segmentation, cell counts, and per-object fluorescence measurements. Support |  |
| [cellxgene-census](../skills/cellxgene-census) | Queries the CZ CELLxGENE Census programmatically for versioned public single-cell and spatial transcriptomics data. Use when you need popula |  |
| [cirq](../skills/cirq) | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware circuits, or running quantum charac |  |
| [clinical-decision-support](../skills/clinical-decision-support) | Prepares and validates research-only clinical decision-support evaluation, evidence-profile, cohort, survival, biomarker/model, privacy, and |  |
| [clinical-reports](../skills/clinical-reports) | Creates safety-bounded draft structures and runs local deterministic checks for clinical case, diagnostic, trial, safety, and aggregate rese |  |
| [cobrapy](../skills/cobrapy) | Performs constraint-based metabolic modeling with COBRApy, including FBA, pFBA, FVA, gene knockouts, flux sampling, growth media, production |  |
| [dask](../skills/dask) | Scales pandas, NumPy, and custom Python research workflows beyond memory or across clusters with Dask. Covers DataFrames, Arrays, Bags, Futu |  |
| [database-lookup](../skills/database-lookup) | Queries documented public database APIs with explicit endpoints, filters, pagination, and provenance. Used when a scientific, regulatory, fi |  |
| [datalad](../skills/datalad) | Retrieves, versions, and publishes scientific datasets with DataLad and git-annex, and captures computational provenance with datalad run, r |  |
| [datamol](../skills/datamol) | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug discovery including SMILES parsin |  |
| [deepchem](../skills/deepchem) | Builds molecular property prediction and MoleculeNet workflows with DeepChem, including SMILES featurization, scaffold or grouped holdouts,  |  |
| [deepspot-m](../skills/deepspot-m) | Generates transcriptome-wide virtual spatial transcriptomics from H&E histology with DeepSpot-M. Used for predicted log1p-CPM expression fro |  |
| [deeptools](../skills/deeptools) | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), for ChIP-seq, RNA-seq,  |  |
| [depmap](../skills/depmap) | Retrieves and analyzes Cancer Dependency Map (DepMap) release data, including CRISPR Chronos gene effects, cancer model annotations, omics b |  |
| [diffdock](../skills/diffdock) | Predicts protein-small-molecule binding poses with DiffDock and DiffDock-L from PDB or sequence plus SMILES/SDF/MOL2. Covers batch docking,  |  |
| [dnanexus-integration](../skills/dnanexus-integration) | Builds and operates reproducible genomics workloads on DNAnexus with the dx CLI, dxpy, apps/applets, native workflows, dxCompiler, and Nextf |  |
| [esm](../skills/esm) | Uses the Biohub esm Python SDK for ESM3 protein generation, ESMC embeddings, and ESMFold2 all-atom folding. Applies to local model inference |  |
| [etetoolkit](../skills/etetoolkit) | Analyzes, manipulates, compares, annotates, and visualizes phylogenetic or other hierarchical trees with ETE 4. Supports Newick/Nexus tree I |  |
| [experiment-design](../skills/experiment-design) | 특허 출원용 실시예·비교예·측정법 설계 절차. 진보성 주장(구조 차이, 반대 교시, 예측하지 못한 효과, 수치 범위의 임계 의미)과 기재 요건을 뒷받침할 시험을 설계하고, 결과에 따라 청구항을 어떻게 조정할지 미리 정한다. 시험 계획, 실시예 설계,  |  |
| [experimental-design](../skills/experimental-design) | Designs experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and laying out treatment combinations s | how should I set up this experiment·how do I avoid confounding·, or |
| [exploratory-data-analysis](../skills/exploratory-data-analysis) | Performs bounded, local exploratory analysis of explicitly supported scientific files. Supports redacted CSV/TSV/JSON profiles; optional Num |  |
| [fictiv](../skills/fictiv) | Operates Fictiv (app.fictiv.com), the on-demand manufacturing platform, end to end in the user's browser. Covers uploading CAD parts, config | get a quote·order parts |
| [flowio](../skills/flowio) | Reads, inspects, and writes Flow Cytometry Standard (FCS) 2.0, 3.0, and 3.1 files with FlowIO. Use for low-level FCS metadata and channel in |  |
| [flowkit](../skills/flowkit) | Analyzes flow cytometry data with FlowKit, including spillover compensation, logicle and biexponential transforms, hierarchical gating, Gati |  |
| [fluidsim](../skills/fluidsim) | Plans, configures, inspects, restarts, and analyzes bounded FluidSim computational-fluid-dynamics simulations with explicit numerical-validi |  |
| [folklore-variant-evidence](../skills/folklore-variant-evidence) | Retrieves ClinGen gene-disease validity assertions for a public gene or disease, and reviews source-linked public evidence and literature fo |  |
| [geniml](../skills/geniml) | Supports audited local Geniml genomic-interval workflows: validate BED and universe contracts, plan Region2Vec or scEmbed runs, inspect mode |  |
| [genomic-coordinates](../skills/genomic-coordinates) | Converts genomic intervals between coordinate conventions, normalises and compares variant representations, and detects assembly or contig-n | off by one·0-based·1-based |
| [genomic-intelligence](../skills/genomic-intelligence) | Predicts regulatory features, gene structure, and expression directly from DNA sequence using Genomic Intelligence's hosted transformer DNA  |  |
| [geomaster](../skills/geomaster) | Supports geospatial research workflows for remote sensing, vector and raster GIS, spatial statistics, terrain and network analysis, and mach |  |
| [geopandas](../skills/geopandas) | Guidance and local audit tools for Python workflows that directly use GeoPandas GeoSeries, GeoDataFrame, spatial operations, or vector-data  |  |
| [get-available-resources](../skills/get-available-resources) | Detects host inventory and effective CPU, memory, disk, scheduler, container, and accelerator limits when a user asks for resource-aware pla |  |
| [gget](../skills/gget) | Queries 20+ bioinformatics resources through CLI/Python. Supports quick lookups of gene info, BLAST/BLAT, viral sequence downloads, PDB/mmCI |  |
| [ginkgo-cloud-lab](../skills/ginkgo-cloud-lab) | Guides protocol selection, input preparation, pricing checks, and browser ordering on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio). Applies  |  |
| [glycoengineering](../skills/glycoengineering) | Analyzes and engineers protein glycosylation by scanning canonical N-glycosylation sequons, describing S/T-rich regions, checking curated gl |  |
| [gtars](../skills/gtars) | Supports Gtars for local genomic interval models and set algebra, overlaps and counts, consensus and coverage, tokenization, fragment proces |  |
| [histolab](../skills/histolab) | Extracts and preprocesses whole-slide histology image tiles with Histolab. Use for WSI inspection, tissue masks, random/grid/score-based til |  |
| [hugging-science](../skills/hugging-science) | Discovers and evaluates scientific datasets, models, methodology posts, and Spaces through the Hugging Science catalog. Used when selecting  |  |
| [imaging-data-commons](../skills/imaging-data-commons) | Queries and downloads public cancer imaging data from NCI Imaging Data Commons. Supports IDC collection discovery, DICOM access, radiology ( |  |
| [iso-standards-readiness](../skills/iso-standards-readiness) | Prepares and structurally reviews readiness evidence for ISO management-system and laboratory-competence standards - ISO 13485 medical devic |  |
| [lab-hardware-cad](../skills/lab-hardware-cad) | Designs custom laboratory hardware as parametric build123d models and exports fabrication artifacts as STEP, STL, and DXF files - microfluid |  |
| [labarchive-integration](../skills/labarchive-integration) | Integrates with the official LabArchives ELN REST-like API and Inventory API v1. Supports regional endpoint selection, signed-request constr |  |
| [lamindb](../skills/lamindb) | Manages biological datasets and models with LaminDB, including artifact registration, lineage tracking, schema validation, Bionty ontology a |  |
| [latchbio-integration](../skills/latchbio-integration) | Builds, registers, debugs, and operates bioinformatics workflows on Latch using the Python SDK, CLI, Latch Data and Registry, Nextflow, Snak |  |
| [mageck](../skills/mageck) | Analyzes pooled CRISPR screen FASTQ reads and guide-count matrices with MAGeCK, validates guide libraries and contrasts, measures replicate  |  |
| [marine-carbonate-chemistry](../skills/marine-carbonate-chemistry) | Solves seawater carbonate chemistry with PyCO2SYS for chemical oceanography, ocean acidification, and marine carbon-cycle research. Use for  |  |
| [matchms](../skills/matchms) | Processes, cleans, compares, and searches tandem mass spectra with matchms. Use for MS/MS file I/O, metadata harmonization, peak filtering,  |  |
| [matlab](../skills/matlab) | Builds, reviews, migrates, and plans MATLAB or GNU Octave numerical workflows. Use for arrays, tabular/time data, tests, projects, graphics, |  |
| [matplotlib](../skills/matplotlib) | 차트·그래프 |  |
| [medchem](../skills/medchem) | Applies medicinal chemistry filters for compound triage, using drug-likeness rules (Lipinski, Veber, CNS), structural alert catalogs (PAINS, |  |
| [modal](../skills/modal) | Modal is a serverless cloud platform for running Python on demand, including on-demand GPUs. Use when deploying or serving AI/ML models, run |  |
| [molecular-dynamics](../skills/molecular-dynamics) | Runs and analyzes molecular dynamics simulations with OpenMM and MDAnalysis. Sets up protein/small molecule systems, defines force fields, r |  |
| [molfeat](../skills/molfeat) | Featurizes small molecules with Molfeat for QSAR/QSPR, chemical similarity, virtual screening, and molecular ML. Covers ECFP/MACCS fingerpri |  |
| [ncats-arax](../skills/ncats-arax) | Queries the NCATS Translator ARAX production API for bounded, typed, provenance-rich one-hop and endpoint-pinned two-hop biomedical knowledg |  |
| [networkx](../skills/networkx) | Creates, analyzes, and visualizes complex networks and graphs in Python with NetworkX. Use when working with network/graph data structures,  |  |
| [neurokit2](../skills/neurokit2) | Builds and audits reproducible NeuroKit2 research workflows for physiological time-series preprocessing, event/interval analysis, multimodal |  |
| [neuropixels-analysis](../skills/neuropixels-analysis) | Analyzes Neuropixels extracellular recordings end-to-end with SpikeInterface. Covers loading SpikeGLX/Open Ephys/NWB data, preprocessing, dr |  |
| [nextflow](../skills/nextflow) | Builds, runs, and debugs Nextflow DSL2 pipelines and nf-core workflows. Use for Nextflow, nf-core, .nf files, nextflow.config, processes/cha |  |
| [nmrglue](../skills/nmrglue) | Processes calibrated one-dimensional complex NMR free-induction decays with nmrglue into phased spectra, peak candidates, and signed integra |  |
| [nwb-conversion](../skills/nwb-conversion) | Converts neuroscience acquisition data to Neurodata Without Borders files with NeuroConv and PyNWB, preserves metadata and timebases, checks |  |
| [omero-integration](../skills/omero-integration) | Inspects and automates microscopy data workflows against OMERO.server with omero-py, BlitzGateway, OMERO CLI, tables, annotations, ROIs, ren |  |
| [onekgpd](../skills/onekgpd) | > Queries the 1000 Genomes Project dataset (3,202 whole-genome-sequenced individuals, GRCh38) at the level of individual participants. Use w |  |
| [ontology-term-resolution](../skills/ontology-term-resolution) | Resolves free-text scientific labels to ontology term IDs and validates existing CURIEs against the EBI Ontology Lookup Service (OLS4). Also | ontology term·ontology ID·CURIE |
| [openpiv](../skills/openpiv) | Performs Particle Image Velocimetry (PIV) analysis with OpenPIV. Use when extracting velocity fields from PIV image pairs, analyzing fluid d |  |
| [opentrons-integration](../skills/opentrons-integration) | Authors, reviews, migrates, simulates, and troubleshoots official Opentrons Python Protocol API v2 protocols for Flex and OT-2 robots. Use f |  |
| [optimize-for-gpu](../skills/optimize-for-gpu) | GPU-accelerates scientific Python on NVIDIA hardware and verifies that the result is correct and faster. Use for CUDA/GPU optimization; CPU- |  |
| [pacsomatic](../skills/pacsomatic) | Prepares and launches nf-core/pacsomatic matched tumor-normal PacBio HiFi genomics workflows from unaligned BAM inputs. Supports samplesheet |  |
| [pathml](../skills/pathml) | Supports local computational pathology research with PathML: slide loading and tiling, preprocessing and QC, h5path storage, multiplex quant |  |
| [pathogen-variant-surveillance](../skills/pathogen-variant-surveillance) | Queries public GenSpectrum LAPIS data for pathogen genomic surveillance, current lineage nomenclature, weekly sequence proportions, reportin |  |
| [pathway-enrichment](../skills/pathway-enrichment) | Performs pathway and gene-set enrichment analysis on gene lists or ranked gene data and interprets the results. Used when the user has a set | pathway analysis·enrichment analysis·GO enrichment |
| [pennylane](../skills/pennylane) | Builds and differentiates PennyLane quantum circuits, hybrid PyTorch or JAX models, molecular VQE and QAOA workflows. Use for variational qu |  |
| [phylogenetics](../skills/phylogenetics) | Builds and analyzes phylogenetic trees using MAFFT multiple sequence alignment, IQ-TREE maximum likelihood with ModelFinder and branch suppo |  |
| [pkpd-modeling](../skills/pkpd-modeling) | Pharmacokinetic and pharmacodynamic modelling and simulation - non-compartmental analysis, compartmental and population PK, PK/PD and exposu | pharmacokinetics·pharmacodynamics·PK/PD |
| [polars](../skills/polars) | High-performance DataFrame library for Python ETL, analytics, and pandas migration. It supports expression-based data manipulation with lazy |  |
| [polars-bio](../skills/polars-bio) | Performs genomic interval overlap, nearest, merge, coverage, complement and subtraction on Polars DataFrames, and reads or writes BED, VCF,  |  |
| [primekg](../skills/primekg) | Queries a pinned Precision Medicine Knowledge Graph (PrimeKG) CSV for typed gene, drug, disease, and phenotype nodes, direct associations, d |  |
| [primer-design](../skills/primer-design) | Designs and audits PCR and RT-qPCR primers with Primer3, explicit thermodynamic conditions, reference-based off-target amplification searche |  |
| [protocolsio-integration](../skills/protocolsio-integration) | Reads, validates, and safely exports protocols.io data with current official REST/MCP contracts, or creates non-executing mutation plans. Th |  |
| [pufferlib](../skills/pufferlib) | Version-aware guidance for PufferLib reinforcement-learning environments, vectorization, policies, PuffeRL training, evaluation, and safe ch |  |
| [pybamm](../skills/pybamm) | Simulates lithium-ion battery charge, discharge and rest experiments with PyBaMM, records parameter-set provenance, checks mesh and solver s |  |
| [pycalphad](../skills/pycalphad) | Computes finite-temperature CALPHAD equilibria, phase fractions, and phase compositions from thermodynamic TDB databases using pycalphad. Us |  |
| [pydeseq2](../skills/pydeseq2) | Performs bulk RNA-seq differential expression analysis with PyDESeq2, including count validation, formula designs, explicit contrasts, Wald  |  |
| [pydicom](../skills/pydicom) | Reads, inspects, writes, transforms, and preflights local DICOM datasets and pixel data. Applies to DICOM metadata, transfer syntaxes, compr |  |
| [pyhealth](../skills/pyhealth) | Builds and validates PyHealth clinical machine-learning pipelines for EHR, signals, imaging, and medical codes. Use for PyHealth dataset loa |  |
| [pylabrobot](../skills/pylabrobot) | Develops and reviews PyLabRobot lab-automation resources, liquid-handling plans, offline simulations, and supported-device integrations. Sup |  |
| [pymatgen](../skills/pymatgen) | Analyzes, validates, converts, and transforms materials structures and computed materials data with pymatgen. Use for local phase diagrams,  |  |
| [pymc](../skills/pymc) | Builds and checks Bayesian models with PyMC, including hierarchical models, NUTS MCMC, variational inference, mutable-data predictions, post |  |
| [pymoo](../skills/pymoo) | Solves and validates single-, multi-, and many-objective optimization with pymoo, including NSGA-II, NSGA-III, MOEA/D, constraints, Pareto a |  |
| [pyopenms](../skills/pyopenms) | Processes mass spectrometry data with pyOpenMS. Supports proteomics and metabolomics workflows—feature detection, peptide/protein identifica |  |
| [pysam](../skills/pysam) | Provides Python/HTSlib workflows for genomic files. Used when reading, querying, filtering, or writing SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ, o |  |
| [pytdc](../skills/pytdc) | Provides Therapeutics Data Commons workflows through PyTDC for registry discovery, dataset access, task-aware splits, evaluator metrics, ben |  |
| [pytorch-lightning](../skills/pytorch-lightning) | Deep learning framework (PyTorch Lightning / lightning package). Organize PyTorch code into LightningModules, configure Trainers for multi-G |  |
| [qiime2-amplicon](../skills/qiime2-amplicon) | Processes paired-end 16S amplicon reads into QIIME 2 ASVs and taxonomy with retained artifact provenance. Checks paired FASTQ manifests, pri |  |
| [qiskit](../skills/qiskit) | Builds, simulates, transpiles, and executes quantum circuits with Qiskit and IBM Quantum Runtime. Use for Qiskit 2.x circuits and operators, |  |
| [qutip](../skills/qutip) | Simulate and audit closed and open quantum-system models with QuTiP 5, including deterministic, trajectory, steady-state, spectral, and phas |  |
| [rdkit](../skills/rdkit) | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure sea |  |
| [relion](../skills/relion) | Validates and executes RELION single-particle cryo-EM refinement and half-map postprocessing. Supports STAR optics/acquisition checks, parti |  |
| [relsa-severity-assessment](../skills/relsa-severity-assessment) | Supports multivariate severity assessment and exploratory endpoint-time score forecasting for laboratory animal studies using the RELSA (REL | turned |
| [rowan](../skills/rowan) | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use for pKa and macropKa prediction, |  |
| [scanpy](../skills/scanpy) | Performs Scanpy single-cell RNA-seq QC, normalization, HVG selection, PCA/UMAP/t-SNE, clustering, exploratory marker ranking, pseudobulk pre |  |
| [scientific-visualization](../skills/scientific-visualization) | Creates and audits truthful, accessible, publication-ready scientific figures with Matplotlib, Seaborn, or Plotly. Use it for figure design, |  |
| [scikit-bio](../skills/scikit-bio) | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ordination (PCoA), PERM |  |
| [scikit-learn](../skills/scikit-learn) | Supports machine learning in Python with scikit-learn. Applies when working with supervised learning (classification, regression), unsupervi |  |
| [scikit-survival](../skills/scikit-survival) | Builds, evaluates, and audits right-censored or competing-risk survival workflows with scikit-survival, including leakage-safe preprocessing |  |
| [scvelo](../skills/scvelo) | Performs RNA velocity analysis with scVelo from spliced and unspliced single-cell RNA counts. Fits deterministic or dynamical models, examin |  |
| [scvi-tools](../skills/scvi-tools) | Fits probabilistic models for single-cell omics, including scVI batch integration, scANVI annotation, totalVI CITE-seq, MultiVI RNA/ATAC int |  |
| [seaborn](../skills/seaborn) | Creates Seaborn statistical visualizations with pandas integration for distributions, relationships, categorical comparisons, regression dis |  |
| [shap](../skills/shap) | Explain and audit machine-learning predictions with SHAP. Use for selecting SHAP explainers and maskers, computing and validating feature at |  |
| [simpy](../skills/simpy) | Builds, inspects, tests, and analyzes bounded process-based discrete-event simulations with SimPy. Use for event scheduling, resource queues |  |
| [stable-baselines3](../skills/stable-baselines3) | Trains and evaluates single-agent reinforcement learning with Stable Baselines3 (PPO, SAC, DQN, TD3, DDPG, A2C), Gymnasium custom environmen |  |
| [statistical-analysis](../skills/statistical-analysis) | Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power analysis, Bayesian alternatives, an |  |
| [statistical-power](../skills/statistical-power) | Calculates sample sizes and statistical power for study planning. Applies when someone asks "how many subjects/samples/replicates do I need" | 80% power·power analysis |
| [statsmodels](../skills/statsmodels) | Fits and diagnoses Python statistical models including OLS, GLM, discrete and mixed models, ARIMA and SARIMAX. Supports coefficient inferenc |  |
| [sympy](../skills/sympy) | Performs exact symbolic mathematics with SymPy for algebra, calculus, equation solving, symbolic linear algebra, physics, and lambdify or La |  |
| [tamarind](../skills/tamarind) | Provides access to a collection of open-source molecular design and structural biology tools on the Tamarind Bio platform, via its REST API  |  |
| [tellurium](../skills/tellurium) | Simulates biochemical kinetic models from SBML or Antimony with Tellurium and libRoadRunner, checks model units, compares deterministic para |  |
| [tiledbvcf](../skills/tiledbvcf) | Stores and retrieves genomic variant calls with TileDB-VCF. Use for indexed single-sample VCF/BCF ingestion, incremental cohorts, region and |  |
| [torch-geometric](../skills/torch-geometric) | Supports PyTorch Geometric (PyG) graph neural networks — node/link/graph classification, message passing (GCN, GAT, GraphSAGE, GIN), heterog |  |
| [torchdrug](../skills/torchdrug) | Builds and troubleshoots TorchDrug 0.2.1 workflows for molecular graphs, property prediction, self-supervised pretraining, molecule generati |  |
| [transformers](../skills/transformers) | Hugging Face Transformers for loading Hub models, running pipeline inference, text generation, and Trainer fine-tuning on NLP, vision, audio |  |
| [treatment-plans](../skills/treatment-plans) | Formats and structurally validates local treatment-plan documentation after clinical decisions have already been supplied and verified by au |  |
| [umap-learn](../skills/umap-learn) | Applies UMAP-learn to nonlinear dimensionality reduction, 2D/3D embeddings, clustering preprocessing, supervised or semi-supervised UMAP, De |  |
| [uncertainty-and-units](../skills/uncertainty-and-units) | Tracks physical units and propagates measurement uncertainty in scientific calculations using pint and uncertainties. Use for unit conversio | is this number physically reasonable·sanity check these units·what regime is this flow in |
| [usfiscaldata](../skills/usfiscaldata) | Queries the U.S. Treasury Fiscal Data REST API for federal financial data. No API key required. Use for national debt (Debt to the Penny), D |  |
| [vaex](../skills/vaex) | Processes large tabular scientific datasets with Vaex expressions, filtered views, streamed statistics, binned visualizations, and file conv |  |
| [waypoint-bio](../skills/waypoint-bio) | Supports work with Outpost Bio's open microbiome foundation models - the Waypoint checkpoints (Waypoint-6m, Waypoint-45m, Waypoint-170m), th |  |
| [zarr-python](../skills/zarr-python) | Stores and queries chunked N-D scientific arrays with Zarr-Python 3, including codecs, sharding, S3/GCS storage, and NumPy/Dask/Xarray integ |  |
