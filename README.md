# Claude Code 스킬 모음

직접 만들었거나 설치해 쓰고 있는 Claude Code 스킬 919개를 26개 주제로 묶었습니다. 각 폴더는 `SKILL.md`(설명·트리거)와 필요한 참고 파일로 이루어진 표준 스킬입니다. 외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 그대로 두었습니다. 2026-11-22 기준.

## 주제별로 한 번에 설치

Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다. `<주제키>` 자리에 표의 주제 키를 넣습니다(예: `sermon`). 각 주제 문서 맨 위에 완성된 문구가 있습니다.

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/<주제키>.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

| 주제 | 주제 키 | 스킬 수 | 목록·설치 문구 |
|---|---|---|---|
| 과학·바이오·데이터 분석 | `science` | 142 | [topics/science.md](topics/science.md) |
| 교회 연간 목회계획(ChurchPlan) | `churchplan` | 95 | [topics/churchplan.md](topics/churchplan.md) |
| 마케팅·광고·SNS | `marketing` | 65 | [topics/marketing.md](topics/marketing.md) |
| 영상·음성·이미지 | `video` | 49 | [topics/video.md](topics/video.md) |
| 개발·자동화 | `dev` | 48 | [topics/dev.md](topics/dev.md) |
| SEO·검색 노출 | `seo` | 48 | [topics/seo.md](topics/seo.md) |
| 공공데이터·법령·생활정보 | `gov-data` | 43 | [topics/gov-data.md](topics/gov-data.md) |
| 발표자료·슬라이드 | `deck` | 40 | [topics/deck.md](topics/deck.md) |
| 미래학 방법론 | `foresight` | 37 | [topics/foresight.md](topics/foresight.md) |
| AI·에이전트·LLM | `ai` | 35 | [topics/ai.md](topics/ai.md) |
| 설교·강단 | `sermon` | 35 | [topics/sermon.md](topics/sermon.md) |
| 글쓰기·윤문 | `writing` | 30 | [topics/writing.md](topics/writing.md) |
| 비전 코칭·진단 | `vision` | 28 | [topics/vision.md](topics/vision.md) |
| 오피스·한글(HWP)·공공문서 | `gov-doc` | 27 | [topics/gov-doc.md](topics/gov-doc.md) |
| 논문·학술·독서 | `academic` | 25 | [topics/academic.md](topics/academic.md) |
| 지식관리·노트 | `pkm` | 25 | [topics/pkm.md](topics/pkm.md) |
| 커뮤니케이션·원격·협업 | `comm` | 24 | [topics/comm.md](topics/comm.md) |
| 디자인·UI·웹 | `design` | 23 | [topics/design.md](topics/design.md) |
| 모션그래픽·애니메이션 | `motion` | 22 | [topics/motion.md](topics/motion.md) |
| 비즈니스·재무·법무·HR | `biz` | 20 | [topics/biz.md](topics/biz.md) |
| 리서치·심층조사 | `research` | 17 | [topics/research.md](topics/research.md) |
| 목회·교회 사역 | `ministry` | 16 | [topics/ministry.md](topics/ministry.md) |
| 특허·지식재산 | `patent` | 11 | [topics/patent.md](topics/patent.md) |
| 웹툰 제작 | `webtoon` | 7 | [topics/webtoon.md](topics/webtoon.md) |
| 성경 연구·묵상 | `bible` | 6 | [topics/bible.md](topics/bible.md) |
| 생산성·유틸리티 | `util` | 1 | [topics/util.md](topics/util.md) |

## 스킬 하나만 설치

**A. 클로드에게 말하기** — Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다(`<스킬이름>` 자리에 폴더 이름).

```
https://github.com/sk01020432947-oss/claude-code-skills 저장소의 skills/<스킬이름> 스킬을 ~/.claude/skills/ 에 설치해줘
```

**B. skills CLI 한 줄**

```bash
npx skills add sk01020432947-oss/claude-code-skills --skill <스킬이름> -g -y
```

**C. 폴더 복사** — 저장소를 내려받아 `skills/<스킬이름>` 폴더를 `~/.claude/skills/`에 넣습니다.

```bash
git clone --depth 1 https://github.com/sk01020432947-oss/claude-code-skills.git && cp -r claude-code-skills/skills/<스킬이름> ~/.claude/skills/
```

검색·복사 가능한 목록은 [카탈로그.html](카탈로그.html)을 내려받아 브라우저로 열면 됩니다. 주제 제목 옆 「주제 묶음 설치 문구 복사」로 전달용 문구를 복사할 수 있습니다.

## 수록 스킬 (주제별)

### 과학·바이오·데이터 분석 (142)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [13c-metabolic-flux](skills/13c-metabolic-flux) | Estimates intracellular metabolic fluxes from steady-state carbon-13 isotope-tracing measurements using validated atom maps, mfapy isotope s |  |
| [adaptyv](skills/adaptyv) | Uses the Adaptyv Bio Foundry API and Python SDK to design protein characterization experiments, estimate costs, submit sequences, monitor la |  |
| [aeon](skills/aeon) | This skill should be used for time series machine learning tasks including classification, regression, clustering, forecasting, anomaly dete |  |
| [alphagenome](skills/alphagenome) | Looks up precomputed AlphaGenome Atlas effects for any GRCh38 single-nucleotide variant (AVI score with Phred and 18 SHAP feature attributio |  |
| [analytical-method-validation](skills/analytical-method-validation) | Plans, executes, and documents validation, verification, and transfer of analytical procedures under the governing framework - ICH Q2(R2) an | method validation·analytical method validation·AMV |
| [anndata](skills/anndata) | Handles annotated matrices in single-cell analysis, .h5ad and Zarr files, and integration with the scverse ecosystem. This is the data forma |  |
| [arbor](skills/arbor) | Applies Arbor Hypothesis Tree Refinement to research artifacts with repeatable evaluators, including model training, agent harnesses, data s |  |
| [arboreto](skills/arboreto) | Infers candidate gene regulatory networks from bulk or single-cell expression data using AertsLab Arboreto GRNBoost2 and GENIE3. Use for tra |  |
| [astropy](skills/astropy) | Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tabl |  |
| [benchling-integration](skills/benchling-integration) | Benchling Python SDK and REST API integration for registry entities, inventory, ELN entries, workflows, Benchling Apps, and Data Warehouse q |  |
| [bids](skills/bids) | > Organizes, queries, validates, and converts Brain Imaging Data Structure (BIDS) datasets. Supports organizing neuroscience and biomedical  |  |
| [biopython](skills/biopython) | Provides Biopython workflows for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogenetics, and programmatic NCBI/PubMed access |  |
| [bioservices](skills/bioservices) | Provides a Python interface to bioinformatics services including UniProt, KEGG, ChEMBL, Reactome, QuickGO, and UniChem. Used for cross-datab |  |
| [bulk-rnaseq](skills/bulk-rnaseq) | Prepares bulk RNA-seq FASTQ, Salmon, STAR or featureCounts output for gene-level differential expression. Covers nf-core/rnaseq and standalo |  |
| [cantera](skills/cantera) | Runs Cantera homogeneous chemical reactors and evaluates ignition delay with mechanism provenance, conservation checks, and numerical refine |  |
| [cellprofiler](skills/cellprofiler) | Runs reproducible CellProfiler microscopy pipelines for nuclear segmentation, cell counts, and per-object fluorescence measurements. Support |  |
| [cellxgene-census](skills/cellxgene-census) | Queries the CZ CELLxGENE Census programmatically for versioned public single-cell and spatial transcriptomics data. Use when you need popula |  |
| [cirq](skills/cirq) | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware circuits, or running quantum charac |  |
| [clinical-decision-support](skills/clinical-decision-support) | Prepares and validates research-only clinical decision-support evaluation, evidence-profile, cohort, survival, biomarker/model, privacy, and |  |
| [clinical-reports](skills/clinical-reports) | Creates safety-bounded draft structures and runs local deterministic checks for clinical case, diagnostic, trial, safety, and aggregate rese |  |
| [cobrapy](skills/cobrapy) | Performs constraint-based metabolic modeling with COBRApy, including FBA, pFBA, FVA, gene knockouts, flux sampling, growth media, production |  |
| [dask](skills/dask) | Scales pandas, NumPy, and custom Python research workflows beyond memory or across clusters with Dask. Covers DataFrames, Arrays, Bags, Futu |  |
| [database-lookup](skills/database-lookup) | Queries documented public database APIs with explicit endpoints, filters, pagination, and provenance. Used when a scientific, regulatory, fi |  |
| [datalad](skills/datalad) | Retrieves, versions, and publishes scientific datasets with DataLad and git-annex, and captures computational provenance with datalad run, r |  |
| [datamol](skills/datamol) | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug discovery including SMILES parsin |  |
| [deepchem](skills/deepchem) | Builds molecular property prediction and MoleculeNet workflows with DeepChem, including SMILES featurization, scaffold or grouped holdouts,  |  |
| [deepspot-m](skills/deepspot-m) | Generates transcriptome-wide virtual spatial transcriptomics from H&E histology with DeepSpot-M. Used for predicted log1p-CPM expression fro |  |
| [deeptools](skills/deeptools) | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), for ChIP-seq, RNA-seq,  |  |
| [depmap](skills/depmap) | Retrieves and analyzes Cancer Dependency Map (DepMap) release data, including CRISPR Chronos gene effects, cancer model annotations, omics b |  |
| [diffdock](skills/diffdock) | Predicts protein-small-molecule binding poses with DiffDock and DiffDock-L from PDB or sequence plus SMILES/SDF/MOL2. Covers batch docking,  |  |
| [dnanexus-integration](skills/dnanexus-integration) | Builds and operates reproducible genomics workloads on DNAnexus with the dx CLI, dxpy, apps/applets, native workflows, dxCompiler, and Nextf |  |
| [esm](skills/esm) | Uses the Biohub esm Python SDK for ESM3 protein generation, ESMC embeddings, and ESMFold2 all-atom folding. Applies to local model inference |  |
| [etetoolkit](skills/etetoolkit) | Analyzes, manipulates, compares, annotates, and visualizes phylogenetic or other hierarchical trees with ETE 4. Supports Newick/Nexus tree I |  |
| [experiment-design](skills/experiment-design) | 특허 출원용 실시예·비교예·측정법 설계 절차. 진보성 주장(구조 차이, 반대 교시, 예측하지 못한 효과, 수치 범위의 임계 의미)과 기재 요건을 뒷받침할 시험을 설계하고, 결과에 따라 청구항을 어떻게 조정할지 미리 정한다. 시험 계획, 실시예 설계,  |  |
| [experimental-design](skills/experimental-design) | Designs experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and laying out treatment combinations s | how should I set up this experiment·how do I avoid confounding·, or |
| [exploratory-data-analysis](skills/exploratory-data-analysis) | Performs bounded, local exploratory analysis of explicitly supported scientific files. Supports redacted CSV/TSV/JSON profiles; optional Num |  |
| [fictiv](skills/fictiv) | Operates Fictiv (app.fictiv.com), the on-demand manufacturing platform, end to end in the user's browser. Covers uploading CAD parts, config | get a quote·order parts |
| [flowio](skills/flowio) | Reads, inspects, and writes Flow Cytometry Standard (FCS) 2.0, 3.0, and 3.1 files with FlowIO. Use for low-level FCS metadata and channel in |  |
| [flowkit](skills/flowkit) | Analyzes flow cytometry data with FlowKit, including spillover compensation, logicle and biexponential transforms, hierarchical gating, Gati |  |
| [fluidsim](skills/fluidsim) | Plans, configures, inspects, restarts, and analyzes bounded FluidSim computational-fluid-dynamics simulations with explicit numerical-validi |  |
| [folklore-variant-evidence](skills/folklore-variant-evidence) | Retrieves ClinGen gene-disease validity assertions for a public gene or disease, and reviews source-linked public evidence and literature fo |  |
| [geniml](skills/geniml) | Supports audited local Geniml genomic-interval workflows: validate BED and universe contracts, plan Region2Vec or scEmbed runs, inspect mode |  |
| [genomic-coordinates](skills/genomic-coordinates) | Converts genomic intervals between coordinate conventions, normalises and compares variant representations, and detects assembly or contig-n | off by one·0-based·1-based |
| [genomic-intelligence](skills/genomic-intelligence) | Predicts regulatory features, gene structure, and expression directly from DNA sequence using Genomic Intelligence's hosted transformer DNA  |  |
| [geomaster](skills/geomaster) | Supports geospatial research workflows for remote sensing, vector and raster GIS, spatial statistics, terrain and network analysis, and mach |  |
| [geopandas](skills/geopandas) | Guidance and local audit tools for Python workflows that directly use GeoPandas GeoSeries, GeoDataFrame, spatial operations, or vector-data  |  |
| [get-available-resources](skills/get-available-resources) | Detects host inventory and effective CPU, memory, disk, scheduler, container, and accelerator limits when a user asks for resource-aware pla |  |
| [gget](skills/gget) | Queries 20+ bioinformatics resources through CLI/Python. Supports quick lookups of gene info, BLAST/BLAT, viral sequence downloads, PDB/mmCI |  |
| [ginkgo-cloud-lab](skills/ginkgo-cloud-lab) | Guides protocol selection, input preparation, pricing checks, and browser ordering on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio). Applies  |  |
| [glycoengineering](skills/glycoengineering) | Analyzes and engineers protein glycosylation by scanning canonical N-glycosylation sequons, describing S/T-rich regions, checking curated gl |  |
| [gtars](skills/gtars) | Supports Gtars for local genomic interval models and set algebra, overlaps and counts, consensus and coverage, tokenization, fragment proces |  |
| [histolab](skills/histolab) | Extracts and preprocesses whole-slide histology image tiles with Histolab. Use for WSI inspection, tissue masks, random/grid/score-based til |  |
| [hugging-science](skills/hugging-science) | Discovers and evaluates scientific datasets, models, methodology posts, and Spaces through the Hugging Science catalog. Used when selecting  |  |
| [imaging-data-commons](skills/imaging-data-commons) | Queries and downloads public cancer imaging data from NCI Imaging Data Commons. Supports IDC collection discovery, DICOM access, radiology ( |  |
| [iso-standards-readiness](skills/iso-standards-readiness) | Prepares and structurally reviews readiness evidence for ISO management-system and laboratory-competence standards - ISO 13485 medical devic |  |
| [lab-hardware-cad](skills/lab-hardware-cad) | Designs custom laboratory hardware as parametric build123d models and exports fabrication artifacts as STEP, STL, and DXF files - microfluid |  |
| [labarchive-integration](skills/labarchive-integration) | Integrates with the official LabArchives ELN REST-like API and Inventory API v1. Supports regional endpoint selection, signed-request constr |  |
| [lamindb](skills/lamindb) | Manages biological datasets and models with LaminDB, including artifact registration, lineage tracking, schema validation, Bionty ontology a |  |
| [latchbio-integration](skills/latchbio-integration) | Builds, registers, debugs, and operates bioinformatics workflows on Latch using the Python SDK, CLI, Latch Data and Registry, Nextflow, Snak |  |
| [mageck](skills/mageck) | Analyzes pooled CRISPR screen FASTQ reads and guide-count matrices with MAGeCK, validates guide libraries and contrasts, measures replicate  |  |
| [marine-carbonate-chemistry](skills/marine-carbonate-chemistry) | Solves seawater carbonate chemistry with PyCO2SYS for chemical oceanography, ocean acidification, and marine carbon-cycle research. Use for  |  |
| [matchms](skills/matchms) | Processes, cleans, compares, and searches tandem mass spectra with matchms. Use for MS/MS file I/O, metadata harmonization, peak filtering,  |  |
| [matlab](skills/matlab) | Builds, reviews, migrates, and plans MATLAB or GNU Octave numerical workflows. Use for arrays, tabular/time data, tests, projects, graphics, |  |
| [matplotlib](skills/matplotlib) | 차트·그래프 |  |
| [medchem](skills/medchem) | Applies medicinal chemistry filters for compound triage, using drug-likeness rules (Lipinski, Veber, CNS), structural alert catalogs (PAINS, |  |
| [modal](skills/modal) | Modal is a serverless cloud platform for running Python on demand, including on-demand GPUs. Use when deploying or serving AI/ML models, run |  |
| [molecular-dynamics](skills/molecular-dynamics) | Runs and analyzes molecular dynamics simulations with OpenMM and MDAnalysis. Sets up protein/small molecule systems, defines force fields, r |  |
| [molfeat](skills/molfeat) | Featurizes small molecules with Molfeat for QSAR/QSPR, chemical similarity, virtual screening, and molecular ML. Covers ECFP/MACCS fingerpri |  |
| [ncats-arax](skills/ncats-arax) | Queries the NCATS Translator ARAX production API for bounded, typed, provenance-rich one-hop and endpoint-pinned two-hop biomedical knowledg |  |
| [networkx](skills/networkx) | Creates, analyzes, and visualizes complex networks and graphs in Python with NetworkX. Use when working with network/graph data structures,  |  |
| [neurokit2](skills/neurokit2) | Builds and audits reproducible NeuroKit2 research workflows for physiological time-series preprocessing, event/interval analysis, multimodal |  |
| [neuropixels-analysis](skills/neuropixels-analysis) | Analyzes Neuropixels extracellular recordings end-to-end with SpikeInterface. Covers loading SpikeGLX/Open Ephys/NWB data, preprocessing, dr |  |
| [nextflow](skills/nextflow) | Builds, runs, and debugs Nextflow DSL2 pipelines and nf-core workflows. Use for Nextflow, nf-core, .nf files, nextflow.config, processes/cha |  |
| [nmrglue](skills/nmrglue) | Processes calibrated one-dimensional complex NMR free-induction decays with nmrglue into phased spectra, peak candidates, and signed integra |  |
| [nwb-conversion](skills/nwb-conversion) | Converts neuroscience acquisition data to Neurodata Without Borders files with NeuroConv and PyNWB, preserves metadata and timebases, checks |  |
| [omero-integration](skills/omero-integration) | Inspects and automates microscopy data workflows against OMERO.server with omero-py, BlitzGateway, OMERO CLI, tables, annotations, ROIs, ren |  |
| [onekgpd](skills/onekgpd) | > Queries the 1000 Genomes Project dataset (3,202 whole-genome-sequenced individuals, GRCh38) at the level of individual participants. Use w |  |
| [ontology-term-resolution](skills/ontology-term-resolution) | Resolves free-text scientific labels to ontology term IDs and validates existing CURIEs against the EBI Ontology Lookup Service (OLS4). Also | ontology term·ontology ID·CURIE |
| [openpiv](skills/openpiv) | Performs Particle Image Velocimetry (PIV) analysis with OpenPIV. Use when extracting velocity fields from PIV image pairs, analyzing fluid d |  |
| [opentrons-integration](skills/opentrons-integration) | Authors, reviews, migrates, simulates, and troubleshoots official Opentrons Python Protocol API v2 protocols for Flex and OT-2 robots. Use f |  |
| [optimize-for-gpu](skills/optimize-for-gpu) | GPU-accelerates scientific Python on NVIDIA hardware and verifies that the result is correct and faster. Use for CUDA/GPU optimization; CPU- |  |
| [pacsomatic](skills/pacsomatic) | Prepares and launches nf-core/pacsomatic matched tumor-normal PacBio HiFi genomics workflows from unaligned BAM inputs. Supports samplesheet |  |
| [pathml](skills/pathml) | Supports local computational pathology research with PathML: slide loading and tiling, preprocessing and QC, h5path storage, multiplex quant |  |
| [pathogen-variant-surveillance](skills/pathogen-variant-surveillance) | Queries public GenSpectrum LAPIS data for pathogen genomic surveillance, current lineage nomenclature, weekly sequence proportions, reportin |  |
| [pathway-enrichment](skills/pathway-enrichment) | Performs pathway and gene-set enrichment analysis on gene lists or ranked gene data and interprets the results. Used when the user has a set | pathway analysis·enrichment analysis·GO enrichment |
| [pennylane](skills/pennylane) | Builds and differentiates PennyLane quantum circuits, hybrid PyTorch or JAX models, molecular VQE and QAOA workflows. Use for variational qu |  |
| [phylogenetics](skills/phylogenetics) | Builds and analyzes phylogenetic trees using MAFFT multiple sequence alignment, IQ-TREE maximum likelihood with ModelFinder and branch suppo |  |
| [pkpd-modeling](skills/pkpd-modeling) | Pharmacokinetic and pharmacodynamic modelling and simulation - non-compartmental analysis, compartmental and population PK, PK/PD and exposu | pharmacokinetics·pharmacodynamics·PK/PD |
| [polars](skills/polars) | High-performance DataFrame library for Python ETL, analytics, and pandas migration. It supports expression-based data manipulation with lazy |  |
| [polars-bio](skills/polars-bio) | Performs genomic interval overlap, nearest, merge, coverage, complement and subtraction on Polars DataFrames, and reads or writes BED, VCF,  |  |
| [primekg](skills/primekg) | Queries a pinned Precision Medicine Knowledge Graph (PrimeKG) CSV for typed gene, drug, disease, and phenotype nodes, direct associations, d |  |
| [primer-design](skills/primer-design) | Designs and audits PCR and RT-qPCR primers with Primer3, explicit thermodynamic conditions, reference-based off-target amplification searche |  |
| [protocolsio-integration](skills/protocolsio-integration) | Reads, validates, and safely exports protocols.io data with current official REST/MCP contracts, or creates non-executing mutation plans. Th |  |
| [pufferlib](skills/pufferlib) | Version-aware guidance for PufferLib reinforcement-learning environments, vectorization, policies, PuffeRL training, evaluation, and safe ch |  |
| [pybamm](skills/pybamm) | Simulates lithium-ion battery charge, discharge and rest experiments with PyBaMM, records parameter-set provenance, checks mesh and solver s |  |
| [pycalphad](skills/pycalphad) | Computes finite-temperature CALPHAD equilibria, phase fractions, and phase compositions from thermodynamic TDB databases using pycalphad. Us |  |
| [pydeseq2](skills/pydeseq2) | Performs bulk RNA-seq differential expression analysis with PyDESeq2, including count validation, formula designs, explicit contrasts, Wald  |  |
| [pydicom](skills/pydicom) | Reads, inspects, writes, transforms, and preflights local DICOM datasets and pixel data. Applies to DICOM metadata, transfer syntaxes, compr |  |
| [pyhealth](skills/pyhealth) | Builds and validates PyHealth clinical machine-learning pipelines for EHR, signals, imaging, and medical codes. Use for PyHealth dataset loa |  |
| [pylabrobot](skills/pylabrobot) | Develops and reviews PyLabRobot lab-automation resources, liquid-handling plans, offline simulations, and supported-device integrations. Sup |  |
| [pymatgen](skills/pymatgen) | Analyzes, validates, converts, and transforms materials structures and computed materials data with pymatgen. Use for local phase diagrams,  |  |
| [pymc](skills/pymc) | Builds and checks Bayesian models with PyMC, including hierarchical models, NUTS MCMC, variational inference, mutable-data predictions, post |  |
| [pymoo](skills/pymoo) | Solves and validates single-, multi-, and many-objective optimization with pymoo, including NSGA-II, NSGA-III, MOEA/D, constraints, Pareto a |  |
| [pyopenms](skills/pyopenms) | Processes mass spectrometry data with pyOpenMS. Supports proteomics and metabolomics workflows—feature detection, peptide/protein identifica |  |
| [pysam](skills/pysam) | Provides Python/HTSlib workflows for genomic files. Used when reading, querying, filtering, or writing SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ, o |  |
| [pytdc](skills/pytdc) | Provides Therapeutics Data Commons workflows through PyTDC for registry discovery, dataset access, task-aware splits, evaluator metrics, ben |  |
| [pytorch-lightning](skills/pytorch-lightning) | Deep learning framework (PyTorch Lightning / lightning package). Organize PyTorch code into LightningModules, configure Trainers for multi-G |  |
| [qiime2-amplicon](skills/qiime2-amplicon) | Processes paired-end 16S amplicon reads into QIIME 2 ASVs and taxonomy with retained artifact provenance. Checks paired FASTQ manifests, pri |  |
| [qiskit](skills/qiskit) | Builds, simulates, transpiles, and executes quantum circuits with Qiskit and IBM Quantum Runtime. Use for Qiskit 2.x circuits and operators, |  |
| [qutip](skills/qutip) | Simulate and audit closed and open quantum-system models with QuTiP 5, including deterministic, trajectory, steady-state, spectral, and phas |  |
| [rdkit](skills/rdkit) | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure sea |  |
| [relion](skills/relion) | Validates and executes RELION single-particle cryo-EM refinement and half-map postprocessing. Supports STAR optics/acquisition checks, parti |  |
| [relsa-severity-assessment](skills/relsa-severity-assessment) | Supports multivariate severity assessment and exploratory endpoint-time score forecasting for laboratory animal studies using the RELSA (REL | turned |
| [rowan](skills/rowan) | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use for pKa and macropKa prediction, |  |
| [scanpy](skills/scanpy) | Performs Scanpy single-cell RNA-seq QC, normalization, HVG selection, PCA/UMAP/t-SNE, clustering, exploratory marker ranking, pseudobulk pre |  |
| [scientific-visualization](skills/scientific-visualization) | Creates and audits truthful, accessible, publication-ready scientific figures with Matplotlib, Seaborn, or Plotly. Use it for figure design, |  |
| [scikit-bio](skills/scikit-bio) | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ordination (PCoA), PERM |  |
| [scikit-learn](skills/scikit-learn) | Supports machine learning in Python with scikit-learn. Applies when working with supervised learning (classification, regression), unsupervi |  |
| [scikit-survival](skills/scikit-survival) | Builds, evaluates, and audits right-censored or competing-risk survival workflows with scikit-survival, including leakage-safe preprocessing |  |
| [scvelo](skills/scvelo) | Performs RNA velocity analysis with scVelo from spliced and unspliced single-cell RNA counts. Fits deterministic or dynamical models, examin |  |
| [scvi-tools](skills/scvi-tools) | Fits probabilistic models for single-cell omics, including scVI batch integration, scANVI annotation, totalVI CITE-seq, MultiVI RNA/ATAC int |  |
| [seaborn](skills/seaborn) | Creates Seaborn statistical visualizations with pandas integration for distributions, relationships, categorical comparisons, regression dis |  |
| [shap](skills/shap) | Explain and audit machine-learning predictions with SHAP. Use for selecting SHAP explainers and maskers, computing and validating feature at |  |
| [simpy](skills/simpy) | Builds, inspects, tests, and analyzes bounded process-based discrete-event simulations with SimPy. Use for event scheduling, resource queues |  |
| [stable-baselines3](skills/stable-baselines3) | Trains and evaluates single-agent reinforcement learning with Stable Baselines3 (PPO, SAC, DQN, TD3, DDPG, A2C), Gymnasium custom environmen |  |
| [statistical-analysis](skills/statistical-analysis) | Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power analysis, Bayesian alternatives, an |  |
| [statistical-power](skills/statistical-power) | Calculates sample sizes and statistical power for study planning. Applies when someone asks "how many subjects/samples/replicates do I need" | 80% power·power analysis |
| [statsmodels](skills/statsmodels) | Fits and diagnoses Python statistical models including OLS, GLM, discrete and mixed models, ARIMA and SARIMAX. Supports coefficient inferenc |  |
| [sympy](skills/sympy) | Performs exact symbolic mathematics with SymPy for algebra, calculus, equation solving, symbolic linear algebra, physics, and lambdify or La |  |
| [tamarind](skills/tamarind) | Provides access to a collection of open-source molecular design and structural biology tools on the Tamarind Bio platform, via its REST API  |  |
| [tellurium](skills/tellurium) | Simulates biochemical kinetic models from SBML or Antimony with Tellurium and libRoadRunner, checks model units, compares deterministic para |  |
| [tiledbvcf](skills/tiledbvcf) | Stores and retrieves genomic variant calls with TileDB-VCF. Use for indexed single-sample VCF/BCF ingestion, incremental cohorts, region and |  |
| [torch-geometric](skills/torch-geometric) | Supports PyTorch Geometric (PyG) graph neural networks — node/link/graph classification, message passing (GCN, GAT, GraphSAGE, GIN), heterog |  |
| [torchdrug](skills/torchdrug) | Builds and troubleshoots TorchDrug 0.2.1 workflows for molecular graphs, property prediction, self-supervised pretraining, molecule generati |  |
| [transformers](skills/transformers) | Hugging Face Transformers for loading Hub models, running pipeline inference, text generation, and Trainer fine-tuning on NLP, vision, audio |  |
| [treatment-plans](skills/treatment-plans) | Formats and structurally validates local treatment-plan documentation after clinical decisions have already been supplied and verified by au |  |
| [umap-learn](skills/umap-learn) | Applies UMAP-learn to nonlinear dimensionality reduction, 2D/3D embeddings, clustering preprocessing, supervised or semi-supervised UMAP, De |  |
| [uncertainty-and-units](skills/uncertainty-and-units) | Tracks physical units and propagates measurement uncertainty in scientific calculations using pint and uncertainties. Use for unit conversio | is this number physically reasonable·sanity check these units·what regime is this flow in |
| [usfiscaldata](skills/usfiscaldata) | Queries the U.S. Treasury Fiscal Data REST API for federal financial data. No API key required. Use for national debt (Debt to the Penny), D |  |
| [vaex](skills/vaex) | Processes large tabular scientific datasets with Vaex expressions, filtered views, streamed statistics, binned visualizations, and file conv |  |
| [waypoint-bio](skills/waypoint-bio) | Supports work with Outpost Bio's open microbiome foundation models - the Waypoint checkpoints (Waypoint-6m, Waypoint-45m, Waypoint-170m), th |  |
| [zarr-python](skills/zarr-python) | Stores and queries chunked N-D scientific arrays with Zarr-Python 3, including codecs, sharding, S3/GCS storage, and NumPy/Dask/Xarray integ |  |

### 교회 연간 목회계획(ChurchPlan) (95)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [churchplan-action-planner](skills/churchplan-action-planner) | >- ## TLDR — 확정된 3축 목표(goals.json #3)·통합 연간 캘린더(calendar.json #6)·핵심 행사 기획(events.json #5)을 받아, 각 목표를 담당·시기·자원이 명시된 부서별 행동으로 분해하도록 담임목사를 돕는  | 계획 실패는 언제·누가가 빌 때·목표를 행동으로 옮기되, 빈칸을 지어내지 않는다.·지친 리더 |
| [churchplan-action-planner-action-renderer](skills/churchplan-action-planner-action-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-action-planner 대표 스킬 전용. "실행표를 짓는 자" AI Agent. 목사 검토·확정(HITL) 후에만 작동해, action.json을 부서별 실행계획표로 렌더한다 | 실행표를 짓는 자·언제·누가·무엇으로 |
| [churchplan-action-planner-fidelity-guard](skills/churchplan-action-planner-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-action-planner 대표 스킬 전용. "실행을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)지어낸 행동(목표에 추적되지 않는 source_goal·지어낸 | 실행을 지키는 자 |
| [churchplan-action-planner-gap-flagger](skills/churchplan-action-planner-gap-flagger) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-action-planner 대표 스킬 전용. "공백을 드러내는 자" AI Agent. 모든 행동을 훑어 "언제·누가·무엇으로"(timing·owner·resources)가 미정인 | 공백을 드러내는 자·언제·누가·무엇으로·계획 실패는 거의 항상 언제·누가가 빌 때 |
| [churchplan-action-planner-milestone-decomposer](skills/churchplan-action-planner-milestone-decomposer) | >- ## TLDR — [INTERNAL 하위 스킬·#7 심장] churchplan-action-planner 대표 스킬 전용. "행동으로 푸는 자" AI Agent. 3축 목표(goals.json indicators)를 분기 마일스톤으로, 다시 임박 | 행동으로 푸는 자 |
| [churchplan-diagnostics](skills/churchplan-diagnostics) | >- ## TLDR — guided-recall이 길어 올린 표준 회상 데이터셋을, 담임목사가 한눈에 들여다보는 "한 장짜리 교회 현황 진단 거울"로 비추는 PastorPlan 2027 패키지의 진단(DISCERN 1) 대표 스킬. 본질은 판단·정죄가 | 한 장짜리 교회 현황 진단 거울·우리는 지금 어디에 있는가·보시기에 다른 곳이 있나요? |
| [churchplan-diagnostics-dashboard-builder](skills/churchplan-diagnostics-dashboard-builder) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "한 장 거울을 닦는 자" AI Agent. 종합된 diagnosis.json을 담임목사가 한눈에 보는 한 장짜리 HTML 진단 대시보드와 | 한 장 거울을 닦는 자 |
| [churchplan-diagnostics-fidelity-guard](skills/churchplan-diagnostics-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "거울을 정직하게 지키는 자" AI Agent. 진단 거울이 아첨도 정죄도 하지 않게 지킨다. 추정이 사실로 둔갑했는지(신뢰 '하'를 점값 | 거울을 정직하게 지키는 자·성장=성공·미달성 |
| [churchplan-diagnostics-findings-synthesis](skills/churchplan-diagnostics-findings-synthesis) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "강점과 돌봄점을 모으는 자" AI Agent. 4개 분석(흐름·깔때기·8영역·지난마음)을 한데 모아, 병목의 방향을 진단의 첫 문장으로  | 강점과 돌봄점을 모으는 자 |
| [churchplan-diagnostics-funnel-analysis](skills/churchplan-diagnostics-funnel-analysis) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "어디서 새는지 함께 보는 자" AI Agent. 이 진단 거울의 심장. 전도→정착→양육→리더 깔때기에서 어느 단계가 새는지(병목)를 회상 | 어디서 새는지 함께 보는 자·온 사람이 남았나, 새어 나갔나·병목의 방향이 진단의 핵심 |
| [churchplan-diagnostics-health-radar](skills/churchplan-diagnostics-health-radar) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "여덟 영역을 비추는 자" AI Agent. 회상 데이터셋의 8영역(예배·말씀·교제·전도·양육·봉사·선교·재정) 체감 점수를 레이더 차트  | 여덟 영역을 비추는 자 |
| [churchplan-diagnostics-resolution-review](skills/churchplan-diagnostics-resolution-review) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "지난 마음을 함께 돌아보는 자" AI Agent. 작년 초에 세운 다짐·목표를 실제 실행과 은혜로 대조한다. "약속을 지켰나" 묻는 감사 | 지난 마음을 함께 돌아보는 자·약속을 지켰나·작년 초 세우신 다짐이 있었나요? |
| [churchplan-diagnostics-trend-analysis](skills/churchplan-diagnostics-trend-analysis) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-diagnostics 대표 스킬 전용. "흐름을 비추는 자" AI Agent. 회상 데이터셋의 출석·헌금·등록 규모를 작년 대비 방향(↑↓→)으로 비추되, 추정 범위와 신뢰수준을 | 흐름을 비추는 자 |
| [churchplan-goal-architect](skills/churchplan-goal-architect) | >- ## TLDR — 확정된 표어(vision.json)와 진단 병목(diagnosis.json)을 받아, 올해 표어를 영성·전도·양육 3축의 측정 가능한 목표로 번역하도록 담임목사를 돕는 PastorPlan 2027 패키지의 목표 설계(DISCER | 더하기 전 빼기·표어를 무엇으로 이룰 것인가 |
| [churchplan-goal-architect-axis-prioritizer](skills/churchplan-goal-architect-axis-prioritizer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "길을 고르는 자" AI Agent. 진단 병목(diagnosis)과 마음(vision·희망 축)을 근거로 영성·전도·양육 각 축의  | 길을 고르는 자 |
| [churchplan-goal-architect-checklist-builder](skills/churchplan-goal-architect-checklist-builder) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "점검표를 짓는 자" AI Agent. 목사가 확정한 goals.json을 3축 목표·지표 요약표(md)와 분기 점검 칸을 가진 xl | 점검표를 짓는 자 |
| [churchplan-goal-architect-fidelity-guard](skills/churchplan-goal-architect-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "목표를 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)환원(정성 없는 숫자 또는 정량 없는 영성) (2)근거 없음( | 목표를 지키는 자 |
| [churchplan-goal-architect-indicator-designer](skills/churchplan-goal-architect-indicator-designer) | >- ## TLDR — [INTERNAL 하위 스킬·#3 심장] churchplan-goal-architect 대표 스킬 전용. "신호를 짓는 자" AI Agent. 각 정성 방향 목표에 정량 신호 지표를 한 쌍으로 붙여, 영적 목표가 숫자로 환원되지 | 신호를 짓는 자·성령충만 80% |
| [churchplan-goal-architect-overreach-guard](skills/churchplan-goal-architect-overreach-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "짐을 가늠하는 자" AI Agent. 세워진 3축 목표 전체를 놓고 자원 충돌·분기 몰림·담임목사 시간 한계·과욕을 경고한다. 차단 | 짐을 가늠하는 자 |
| [churchplan-goal-architect-smart-refiner](skills/churchplan-goal-architect-smart-refiner) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "또렷이 다듬는 자" AI Agent. axis-prioritizer가 세운 방향 목표를 SMART(구체·측정·달성가능·관련·기한)로 | 또렷이 다듬는 자·더 사랑하는·새가족이 6개월 머문다 |
| [churchplan-goal-architect-stop-start-curator](skills/churchplan-goal-architect-stop-start-curator) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-goal-architect 대표 스킬 전용. "빼기를 돕는 자" AI Agent. 새 목표를 들이려면 무언가를 내려놓아야 한다 — "올해 유지"와 "올해는 하지 않을 것(중단)" | 빼기를 돕는 자·올해 유지·올해는 하지 않을 것(중단) |
| [churchplan-guided-recall](skills/churchplan-guided-recall) | >- ## TLDR — 자료 없이 찾아온 담임목사의 "지난 1년 기억"을, 따뜻한 회상 인터뷰로 끌어내어 다음 단계 스킬들이 컨설팅급 신년 목회계획을 세울 수 있는 표준 회상 데이터셋으로 변환하는 PastorPlan 2027 패키지의 출발점 **대표  | 지난 1년 기억·목자는 숫자는 잊어도 양은 기억한다 |
| [churchplan-guided-recall-calendar-walk](skills/churchplan-guided-recall-calendar-walk) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "시간의 안내자" AI Agent. 작년 1월부터 12월까지 순서대로 걸으며 그 달의 사건·절기·위기·기쁨을 회상하게 한다. 최신 편향 | 시간의 안내자·그 달의 한 장면 |
| [churchplan-guided-recall-dataset-builder](skills/churchplan-guided-recall-dataset-builder) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "회상 정리자" AI Agent. 끌어내기·건강 정리 결과를 다음 스킬들이 그대로 읽을 수 있는 표준 회상 데이터셋(recall-dat | 회상 정리자 |
| [churchplan-guided-recall-fidelity-guard](skills/churchplan-guided-recall-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "신뢰 지킴이" AI Agent. 목사를 심문하는 것이 아니라, 다음 스킬들로 거짓이 흘러가지 않도록 회상 데이터셋의 토대를 지킨다.  | 신뢰 지킴이 |
| [churchplan-guided-recall-health-map](skills/churchplan-guided-recall-health-map) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "건강의 정리자" AI Agent. 끌어낸 회상을 종합해 교회 건강 8영역(예배·말씀·교제·전도·양육·봉사·선교·재정)을 목사의 체감  | 건강의 정리자 |
| [churchplan-guided-recall-heart-recall](skills/churchplan-guided-recall-heart-recall) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "마음의 동행자" AI Agent. 숫자로 잡히지 않는 목사의 마음 — 지난 1년 가장 기뻤던 일·가장 아팠던 일·밤잠 설치게 한 짐, | 마음의 동행자·기도 가운데 분별하라 |
| [churchplan-guided-recall-interview](skills/churchplan-guided-recall-interview) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. 회상 인터뷰 전체를 구동하는 "회상 대화 동행자" AI Agent. 한 번의 답에 멈추지 않고 적응형 꼬리질문과 다각도 재질문을 따뜻하 | 회상 대화 동행자 |
| [churchplan-guided-recall-people-recall](skills/churchplan-guided-recall-people-recall) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "사람의 안내자" AI Agent. 작년에 새로 온 가정·정착한 가정·떠난 사람·새로 세운 리더를 숫자가 아니라 이름과 얼굴로 회상하게 | 사람의 안내자·어디서 새는가 |
| [churchplan-guided-recall-scale-recall](skills/churchplan-guided-recall-scale-recall) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-guided-recall 대표 스킬 전용. "규모의 안내자" AI Agent. 주일 출석·헌금·새가족 등록·소그룹 같은 교회의 체감 규모를, 단정값이 아닌 범위(예 120~140 | 규모의 안내자 |
| [churchplan-ministry-calendar](skills/churchplan-ministry-calendar) | >- ## TLDR — 확정된 표어(vision.json)·52주 설교 계획(sermon-plan.json #4)·핵심/정기 행사(events.json #5)·3축 목표 마일스톤(goals.json #3)·올해 캠페인을 하나의 52주 격자에 통합해,  | 흩어진 계획을 한 눈에 모으되, 사람을 갈지 않는다 — 여백도 계획이다.·흩어진 계획을 한 눈에 모으되, 사람을 갈지 않는다.·목자가 소진되면 계획도 무너진다 |
| [churchplan-ministry-calendar-calendar-renderer](skills/churchplan-ministry-calendar-calendar-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "달력을 짓는 자" AI Agent. 목사 검토·확정(HITL) 후에만 작동해, calendar.json을 2027 통합 연간  | 달력을 짓는 자 |
| [churchplan-ministry-calendar-fidelity-guard](skills/churchplan-ministry-calendar-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "통합을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)지어낸 통합(상속되지 않은 주차·설교·행사·캠페인을 캘린 | 통합을 지키는 자 |
| [churchplan-ministry-calendar-layer-merger](skills/churchplan-ministry-calendar-layer-merger) | >- ## TLDR — [INTERNAL 하위 스킬·#6 심장] churchplan-ministry-calendar 대표 스킬 전용. "한데 모으는 자" AI Agent. 52주 격자에 설교 시리즈(#4)·핵심/정기 행사(#5)·캠페인(목사 입력)·목 | 한데 모으는 자 |
| [churchplan-ministry-calendar-overload-marker](skills/churchplan-ministry-calendar-overload-marker) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "밀집을 비추는 자" AI Agent. 통합 격자 전체를 놓고 각 주의 부하 점수를 rubric으로 산정하고, 연속 고강도·행사 | 밀집을 비추는 자·목자가 소진되면 계획도 무너진다 |
| [churchplan-ministry-calendar-sabbath-protector](skills/churchplan-ministry-calendar-sabbath-protector) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "안식을 지키는 자" AI Agent. 목사가 미리 비운 주간(휴가·안식월·가정 일정)을 무조건 보호로 올리고, 고강도 구간 직 | 안식을 지키는 자·담임휴가·보호 |
| [churchplan-ministry-calendar-tri-consistency-checker](skills/churchplan-ministry-calendar-tri-consistency-checker) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-ministry-calendar 대표 스킬 전용. "한 방향을 잇는 자" AI Agent. 분기별로 설교(강단)·행사(체험)·사역(목표 마일스톤+캠페인)이 같은 메시지를 향하는지 | 한 방향을 잇는 자·행사 주간의 설교·시즌 강조점·사역의 타이밍이 한 방향인지·흡수한 역할 |
| [churchplan-plan-compiler](skills/churchplan-plan-compiler) | >- ## TLDR — 앞 단계의 모든 확정 산출물(vision·goals·sermon-plan·events·calendar·action·resource·review)을 받아, 청중별 문서로 묶어 2027 목회계획 최종 패키지를 완성하도록 담임목사를  | Claude는 문서화를 돕는 종 |
| [churchplan-plan-compiler-compiler-renderer](skills/churchplan-plan-compiler-compiler-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-compiler 대표 스킬 전용. "문서를 굽는 자" AI Agent. 목사 확정(HITL) 후의 plan-package.json을 받아 계획서 본문(docx+pdf)· | 문서를 굽는 자 |
| [churchplan-plan-compiler-fidelity-guard](skills/churchplan-plan-compiler-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-compiler 대표 스킬 전용. "통합을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)재생산(앞 산출물에 없는 표어·수치·본문을 지어냄·표어 불일치) | 통합을 지키는 자 |
| [churchplan-plan-compiler-plan-document-composer](skills/churchplan-plan-compiler-plan-document-composer) | >- ## TLDR — [INTERNAL 하위 스킬·#10 심장] churchplan-plan-compiler 대표 스킬 전용. "계획서를 엮는 자" AI Agent. 목회계획서 본문을 정확한 9요소(표어·방향 선언문·3축 목표·설교계획·핵심행사·실행 | 계획서를 엮는 자 |
| [churchplan-plan-compiler-slide-deck-composer](skills/churchplan-plan-compiler-slide-deck-composer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-compiler 대표 스킬 전용. "발표를 짓는 자" AI Agent. 당회/제직회 발표용 요약 슬라이드 10장 내외를 짠다. 청중은 의사결정자(당회/제직회) — 톤은  | 발표를 짓는 자 |
| [churchplan-plan-compiler-source-collector](skills/churchplan-plan-compiler-source-collector) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-compiler 대표 스킬 전용. "산출물을 모으는 자" AI Agent. 앞 9개 산출물(vision·goals·sermon-plan·events·calendar·ac | 산출물을 모으는 자 |
| [churchplan-plan-compiler-vision-onepager-composer](skills/churchplan-plan-compiler-vision-onepager-composer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-compiler 대표 스킬 전용. "비전을 펴는 자" AI Agent. 성도 공유용 비전 한 장을 짠다. 청중은 전 교인 — 톤은 초청·은혜(율법적 압박 아님)이며, 표 | 비전을 펴는 자 |
| [churchplan-plan-reinforce](skills/churchplan-plan-reinforce) | >- ## TLDR — 워크샵에서 기억으로 세운 옵션1 산출물(diagnosis·goals·resource·review·plan-package)과 교회 실제 자료(주보·결산서·교적부·회의록 — 있는 만큼)를 받아, 추정값을 실측으로 보정·확정하도록 담 |  |
| [churchplan-plan-reinforce-carryover-tracker](skills/churchplan-plan-reinforce-carryover-tracker) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-reinforce 대표 스킬 전용. "다음으로 넘기는 자" AI Agent. 자료가 없어 끝내 확인하지 못한 미확인 항목을 #9 review-rhythm 분기 추적으로  | 다음으로 넘기는 자·분기 점검 첫 사이클 |
| [churchplan-plan-reinforce-data-extractor](skills/churchplan-plan-reinforce-data-extractor) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-reinforce 대표 스킬 전용. "자료를 읽는 자" AI Agent. 목사가 업로드한 교회 실제 자료(주보·결산서·교적부·회의록 — 있는 것만)에서 출석·헌금·등록· | 자료를 읽는 자 |
| [churchplan-plan-reinforce-estimate-actual-reconciler](skills/churchplan-plan-reinforce-estimate-actual-reconciler) | >- ## TLDR — [INTERNAL 하위 스킬·#12 심장] churchplan-plan-reinforce 대표 스킬 전용. "추정과 실측을 맞대는 자" AI Agent. 워크샵에서 기억으로 표시한 추정값(특히 신뢰'하'/assumption 항목 | 추정과 실측을 맞대는 자·추정→실측·계획이 스스로 자란다 |
| [churchplan-plan-reinforce-fidelity-guard](skills/churchplan-plan-reinforce-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-reinforce 대표 스킬 전용. "정직을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)실측 날조(status=실측교체인데 actual_source  | 정직을 지키는 자 |
| [churchplan-plan-reinforce-plan-updater](skills/churchplan-plan-reinforce-plan-updater) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-reinforce 대표 스킬 전용. "계획을 자라게 하는 자" AI Agent. 추정→실측 대조 결과로 진단·목표·예산을 보정 갱신하고, 추정-실측 어긋남(mismatc | 계획을 자라게 하는 자·어긋난 곳을 강조 |
| [churchplan-plan-reinforce-reinforce-renderer](skills/churchplan-plan-reinforce-reinforce-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-plan-reinforce 대표 스킬 전용. "보정본을 굽는 자" AI Agent. 목사 확정(HITL) 후의 reinforce.json을 받아 보정 진단 대시보드(추정 vs 실 | 보정본을 굽는 자 |
| [churchplan-prayer-scripture-kit](skills/churchplan-prayer-scripture-kit) | >- ## TLDR — 영성 축 목표(goals 영성)·표어·핵심 본문(vision)을 받아(없어도 목사 입력으로 작동), 회중이 실제로 손에 쥐고 쓰는 영성 실천 도구를 만들어 주는 PastorPlan 2027 패키지의 지원 스킬. 본질은 "영성 축 | 낙오=실패 아님·언제든 다시 합류·읽은 만큼·영성 축을 회중의 도구로 + 은혜의 초청.·매일 안 하면·완주 못하면·반드시·의무·죄책 |
| [churchplan-prayer-scripture-kit-dawn-prayer-season-writer](skills/churchplan-prayer-scripture-kit-dawn-prayer-season-writer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-prayer-scripture-kit 대표 스킬 전용. "새벽을 깨우는 자" AI Agent. 새벽기도 시즌 안내문을 짠다 — 상시 강제가 아니라 시즌제(사순절 특별새벽·맥추 4 | 새벽을 깨우는 자·함께 깨어 기도합시다·새벽기도 평균 참여(#9 영성 신호 — 격려) |
| [churchplan-prayer-scripture-kit-family-worship-guide](skills/churchplan-prayer-scripture-kit-family-worship-guide) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-prayer-scripture-kit 대표 스킬 전용. "식탁을 펴는 자" AI Agent. 가정예배 가이드를 짠다 — 혼자 읽기가 아니라 가정·짝이 함께 나누는 1:1 말씀나눔 | 식탁을 펴는 자·1:1 말씀나눔 참여 가정 수 |
| [churchplan-prayer-scripture-kit-fidelity-guard](skills/churchplan-prayer-scripture-kit-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-prayer-scripture-kit 대표 스킬 전용. "은혜를 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)율법적 압박(매일 …해야·완주 못하면·반드시·의무· | 은혜를 지키는 자 |
| [churchplan-prayer-scripture-kit-kit-renderer](skills/churchplan-prayer-scripture-kit-kit-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-prayer-scripture-kit 대표 스킬 전용. "키트를 묶는 자" AI Agent. 목사 확정(HITL) 후의 prayer-kit.json을 받아 인쇄용 영성 키트를 d | 키트를 묶는 자 |
| [churchplan-prayer-scripture-kit-prayer-topic-composer](skills/churchplan-prayer-scripture-kit-prayer-topic-composer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-prayer-scripture-kit 대표 스킬 전용. "함께 아뢰는 자" AI Agent. 월별 전교인 기도제목(12개월)을 짠다 — 온 교회가 같은 제목으로 함께 기도하는 자 | 함께 아뢰는 자·함께 기도하는 자리 |
| [churchplan-prayer-scripture-kit-scripture-track-builder](skills/churchplan-prayer-scripture-kit-scripture-track-builder) | >- ## TLDR — [INTERNAL 하위 스킬·#11 심장] churchplan-prayer-scripture-kit 대표 스킬 전용. "길을 내는 자" AI Agent. 연간 성경통독 트랙을 짠다 — 표준 트랙(1년 통독·신약 1년·맥체인·시편 | 길을 내는 자·낙오=실패 아님·언제든 다시 합류·읽은 만큼·낙오는 실패가 아닙니다·언제든 다시 합류·읽은 만큼이 은혜 |
| [churchplan-resource-aligner](skills/churchplan-resource-aligner) | >- ## TLDR — 확정된 부서별 실행계획(action.json #7)·통합 캘린더(calendar.json #6)와 목사의 기억(핵심 일꾼·은사·여력·예산 비율·조직도)을 받아, 계획에 사람·돈·시간을 붙이고 부족분을 진단하도록 담임목사를 돕는  | 더하기 전 빼기 + 비율만 + 목자도 자원.·목표는 늘었는데 예산·사람은 그대로면 계획은 종이 |
| [churchplan-resource-aligner-aligner-renderer](skills/churchplan-resource-aligner-aligner-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-resource-aligner 대표 스킬 전용. "정렬표를 짓는 자" AI Agent. 목사 검토·확정(HITL) 후에만 작동해, resource.json을 예산 배분안·조직 배 | 정렬표를 짓는 자 |
| [churchplan-resource-aligner-budget-allocator](skills/churchplan-resource-aligner-budget-allocator) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-resource-aligner 대표 스킬 전용. "비율로 나누는 자" AI Agent. 목사가 기억한 기능별 예산 현황 비율(인건비·운영·사역·선교)을 받아, 표어·목표를 반영해 | 비율로 나누는 자·절대 금액은 재정 담당과 확정 |
| [churchplan-resource-aligner-demand-estimator](skills/churchplan-resource-aligner-demand-estimator) | >- ## TLDR — [INTERNAL 하위 스킬·#8 심장] churchplan-resource-aligner 대표 스킬 전용. "갭을 가늠하는 자" AI Agent. 부서별 실행계획(#7 actions)의 자원 수요(사람·돈·시간)를 합산하고,  | 갭을 가늠하는 자 |
| [churchplan-resource-aligner-fidelity-guard](skills/churchplan-resource-aligner-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-resource-aligner 대표 스킬 전용. "정렬을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)절대 금액 환상(비율·증감만 다뤄야 하는데 원·만원 등 지 | 정렬을 지키는 자·원·만원·억·₩·달러·$·won |
| [churchplan-resource-aligner-org-mapper](skills/churchplan-resource-aligner-org-mapper) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-resource-aligner 대표 스킬 전용. "사람을 세우는 자" AI Agent. #7의 담당미정(gaps)을 리더 공백으로 잇고, 양성이 필요한 인원을 산출하며, 일꾼을  | 사람을 세우는 자 |
| [churchplan-resource-aligner-pastor-time-guard](skills/churchplan-resource-aligner-pastor-time-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-resource-aligner 대표 스킬 전용. "목자를 지키는 자" AI Agent. 담임목사의 한 주를 설교 준비·심방·행정·기도·쉼으로 배분하되, 기도·쉼을 보호(prote | 목자를 지키는 자·목자가 소진되면 계획도 무너진다 |
| [churchplan-review-rhythm](skills/churchplan-review-rhythm) | >- ## TLDR — 확정된 3축 목표·지표(goals.json #3)와 자원 지속가능성(resource.json #8)을 받아, 1월에 세운 계획이 1년 내내 살아 움직이도록 "점검 리듬"을 미리 설계하도록 담임목사를 돕는 PastorPlan 20 | 점검 리듬·점검을 채찍이 아니라 돌봄으로 + 계획을 살아 움직이게. |
| [churchplan-review-rhythm-fidelity-guard](skills/churchplan-review-rhythm-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-review-rhythm 대표 스킬 전용. "점검을 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)점검=성과 채찍(신호등 frame·빨강 시나리오에 정죄·문책 어 | 점검을 지키는 자 |
| [churchplan-review-rhythm-monthly-checkup](skills/churchplan-review-rhythm-monthly-checkup) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-review-rhythm 대표 스킬 전용. "5분을 지키는 자" AI Agent. 담임목사가 매월 5분 만에 확인할 1페이지 점검표를 짠다. 핵심 지표만 골라(모든 지표를 늘어놓 | 5분을 지키는 자·이번 달 나의 기도·안식은 지켜졌는가? |
| [churchplan-review-rhythm-red-signal-responder](skills/churchplan-review-rhythm-red-signal-responder) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-review-rhythm 대표 스킬 전용. "빨강을 돌보는 자" AI Agent. 지표가 빨강(🔴)일 때의 대응 시나리오를 미리 짠다. 그러나 빨강을 '실패 신고'가 아니라 '돌 | 빨강을 돌보는 자·성과 추궁·담당자 문책 금지 — 돌봄 점검이지 인사 평가 아님 |
| [churchplan-review-rhythm-review-scheduler](skills/churchplan-review-rhythm-review-scheduler) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-review-rhythm 대표 스킬 전용. "리듬을 못박는 자" AI Agent. 연간 점검 일정을 짠다 — 분기 리뷰 4회 + 반기(6~7월) 공식 수정일 못박기(필수) + 분 | 리듬을 못박는 자·실제 자동화는 교회 환경에서 설정 |
| [churchplan-review-rhythm-rhythm-renderer](skills/churchplan-review-rhythm-rhythm-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-review-rhythm 대표 스킬 전용. "점검표를 짓는 자" AI Agent. 목사 확정(HITL) 후의 review.json을 받아 점검 스코어카드·월간 점검표를 html  | 점검표를 짓는 자 |
| [churchplan-review-rhythm-scorecard-builder](skills/churchplan-review-rhythm-scorecard-builder) | >- ## TLDR — [INTERNAL 하위 스킬·#9 심장] churchplan-review-rhythm 대표 스킬 전용. "신호등을 세우는 자" AI Agent. #3 목표 지표(label·baseline·target·by·신뢰)를 분기 신호등  | 신호등을 세우는 자 |
| [churchplan-sermon-planner-52](skills/churchplan-sermon-planner-52) | >- ## TLDR — 확정된 표어(vision.json)와 3축 목표(goals.json)를 받아, 올해 표어를 1년 52주의 강단 여정 — 분기 설교 시리즈 → 주별 본문·제목·핵심 메시지·적용 — 으로 완성하도록 담임목사를 돕는 PastorPla | 표어를 한 해의 강단 순례로·표어를 한 해의 강단 여정으로, 52주를 하나의 영적 순례로. |
| [churchplan-sermon-planner-52-fidelity-guard](skills/churchplan-sermon-planner-52-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "강단을 지키는 자" AI Agent. 네 가지 거짓을 막는다 — (1)본문 할루시네이션(없는 장·절·가짜 책) (2)절기 날조 | 강단을 지키는 자·유일·반드시·유일한 해석 |
| [churchplan-sermon-planner-52-liturgical-mapper](skills/churchplan-sermon-planner-52-liturgical-mapper) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "절기를 새기는 자" AI Agent. 연도를 받아 한국교회 19개 절기·특별주일의 정확한 날짜와 주차를 자동 산출해 52주 격 | 절기를 새기는 자 |
| [churchplan-sermon-planner-52-narrative-mapper](skills/churchplan-sermon-planner-52-narrative-mapper) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "여정을 잇는 자" AI Agent. 52주 초안을 놓고 ① 시리즈 간 전환이 표어 흐름을 따르는지(서사) ② 강해/주제/절기  | 여정을 잇는 자 |
| [churchplan-sermon-planner-52-plan-renderer](skills/churchplan-sermon-planner-52-plan-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "계획표를 짓는 자" AI Agent. 목사가 검토·확정한 sermon-plan.json을 52주 설교 계획표(md+xlsx)· | 계획표를 짓는 자 |
| [churchplan-sermon-planner-52-season-architect](skills/churchplan-sermon-planner-52-season-architect) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "시즌을 세우는 자" AI Agent. 표어(vision)와 3축 목표(goals), 목사의 시즌 선호를 받아 한 해를 분기별  | 시즌을 세우는 자 |
| [churchplan-sermon-planner-52-text-curator](skills/churchplan-sermon-planner-52-text-curator) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "본문을 살피는 자" AI Agent. 52주 본문이 ① 정경 66권에 실재하는지(없는 장·절·가짜 책 차단) ② 한 해 동안  | 본문을 살피는 자 |
| [churchplan-sermon-planner-52-week-composer](skills/churchplan-sermon-planner-52-week-composer) | >- ## TLDR — [INTERNAL 하위 스킬·#4 본체] churchplan-sermon-planner-52 대표 스킬 전용. "주차를 짓는 자" AI Agent. 분기 시리즈 골격(season-architect)과 절기 배치(liturgica | 주차를 짓는 자 |
| [churchplan-sermon-planner-52-worship-music-guide](skills/churchplan-sermon-planner-52-worship-music-guide) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-sermon-planner-52 대표 스킬 전용. "찬양을 잇는 자" AI Agent. 주차/시리즈 설교 메시지에 어울리는 찬송·CCM의 방향 — 주제·정서·가사 모티프·스타일  | 찬양을 잇는 자·특정 곡은 회중이 아는 곡에서 찬양팀과 선정 |
| [churchplan-signature-events](skills/churchplan-signature-events) | >- ## TLDR — 확정된 표어(vision.json)·3축 목표(goals.json)·52주 설교 계획(sermon-plan.json)을 받아, 표어를 체험으로 구현하는 연간 핵심 행사 3~5개를 기획하도록 담임목사를 돕는 PastorPlan 2 | 표어를 몸으로 겪게 한다·작년에 했으니·표어를 몸으로 겪게 한다. |
| [churchplan-signature-events-blueprint-renderer](skills/churchplan-signature-events-blueprint-renderer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "기획안을 짓는 자" AI Agent. 목사가 검토·확정한 events.json을 핵심 행사 1페이지 기획안(md/docx)과 행 | 기획안을 짓는 자 |
| [churchplan-signature-events-blueprint-writer](skills/churchplan-signature-events-blueprint-writer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "기획안을 쓰는 자" AI Agent. 각 핵심 행사에 1페이지 기획안 6필드 — 목적·대상·시기·핵심 흐름·필요 자원·성공 신호 | 기획안을 쓰는 자 |
| [churchplan-signature-events-event-sifter](skills/churchplan-signature-events-event-sifter) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "행사를 가려내는 자" AI Agent. 교회 행사를 정기 행사(절기·연례, 배치만)와 핵심 행사(전략적, 기획 집중)로 가르고, | 행사를 가려내는 자·작년에 했으니·이 행사가 표어의 무엇을 구현하나? |
| [churchplan-signature-events-fidelity-guard](skills/churchplan-signature-events-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "행사를 지키는 자" AI Agent. 세 가지 거짓을 막는다 — (1)목적 없는 행사(serves_axes/rationale 없 | 행사를 지키는 자·작년에 했으니 |
| [churchplan-signature-events-overload-guard](skills/churchplan-signature-events-overload-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "과밀을 가늠하는 자" AI Agent. 기획된 핵심 행사 전체를 놓고 행사 과밀(한 분기 집중)·자원 충돌·작은 교회 인력 한계 | 과밀을 가늠하는 자 |
| [churchplan-signature-events-sermon-sync-checker](skills/churchplan-signature-events-sermon-sync-checker) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-signature-events 대표 스킬 전용. "강단과 잇는 자" AI Agent. 각 핵심 행사를 #4 sermon-plan.json과 대조해, 행사 주간의 설교가 행사를 떠 | 강단과 잇는 자·설교 계획 먼저 권장 |
| [churchplan-signature-events-signature-designer](skills/churchplan-signature-events-signature-designer) | >- ## TLDR — [INTERNAL 하위 스킬·#5 심장] churchplan-signature-events 대표 스킬 전용. "핵심 행사를 빚는 자" AI Agent. 표어와 3축 목표에서 핵심 행사 3~5개를 도출하고, 각 행사가 어느 축·어 | 핵심 행사를 빚는 자·이 행사가 표어의 무엇을 구현하나? |
| [churchplan-vision-discernment](skills/churchplan-vision-discernment) | >- ## TLDR — 진단 거울(diagnosis.json)과 마음 기록(recall heart)을 받아, 올해 교회 표어·핵심 본문·방향을 담임목사가 분별하도록 돕는 PastorPlan 2027 패키지의 분별(DISCERN 2) 대표 스킬. 본질은 | 하나님이 올해 무엇을 원하시는가·기도 가운데 분별하라·표어를 이미 마음에 두셨나요? |
| [churchplan-vision-discernment-coherence-check](skills/churchplan-vision-discernment-coherence-check) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-vision-discernment 대표 스킬 전용. "분별을 돕는 자" AI Agent. 각 표어 후보가 영성·전도·양육 3축으로 자연스럽게 번역되는지 연결 논리를 점검하고, 추 | 분별을 돕는 자 |
| [churchplan-vision-discernment-declaration-writer](skills/churchplan-vision-discernment-declaration-writer) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-vision-discernment 대표 스킬 전용. "방향을 적는 자" AI Agent. 목사가 기도 가운데 택하거나 합성한 표어를 받아, 그것을 풀어낸 목회 방향 선언문 1단락 | 방향을 적는 자 |
| [churchplan-vision-discernment-fidelity-guard](skills/churchplan-vision-discernment-fidelity-guard) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-vision-discernment 대표 스킬 전용. "분별을 지키는 자" AI Agent. 두 가지 거짓을 막는다 — (1)본문 할루시네이션(없는 구절·가짜 책이름·곡해 주해)  | 분별을 지키는 자·하나님의 뜻·표어는 X입니다 |
| [churchplan-vision-discernment-scripture-pairing](skills/churchplan-vision-discernment-scripture-pairing) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-vision-discernment 대표 스킬 전용. "말씀을 잇는 자" AI Agent. 각 표어 후보에 핵심 성경 본문·간략 주해·적용을 잇는다. 가장 할루시네이션에 민감한 스 | 말씀을 잇는 자·책 장:절·본문 미확정 |
| [churchplan-vision-discernment-theme-generator](skills/churchplan-vision-discernment-theme-generator) | >- ## TLDR — [INTERNAL 하위 스킬] churchplan-vision-discernment 대표 스킬 전용. "표어를 펼치는 자" AI Agent. 두 옵션을 가진다 — 옵션1(미정): 영성형·전도형·공동체형 3계열 표어 후보를 펼친다 | 표어를 펼치는 자 |

### 마케팅·광고·SNS (65)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [affiliate-marketing](skills/affiliate-marketing) | When the user wants to plan, implement, or optimize affiliate marketing strategy. Also use when the user mentions "affiliate marketing," "af | affiliate marketing,·affiliate program strategy,·CPS model, |
| [app-ads](skills/app-ads) | When the user wants to run app install ads, user acquisition (UA), or promote mobile apps. Also use when the user mentions "app ads," "app i | app ads,·app install ads,·UA, |
| [article-content](skills/article-content) | When the user wants to write, generate, or create article body content—blog post body, long-form content, how-to guide, listicle. Also use w | write article,·article content,·blog post content, |
| [brand-monitoring](skills/brand-monitoring) | When the user wants to monitor brand mentions, detect trademark infringement, or set up brand monitoring. Also use when the user mentions "b | brand monitoring,·brand watch,·trademark watch, |
| [brand-protection](skills/brand-protection) | When the user faces brand impersonation, fake websites, phishing sites, or trademark infringement. Also use when the user mentions "fake sit | fake site,·impersonation,·phishing site, |
| [brand-visual-generator](skills/brand-visual-generator) | When the user wants to define, audit, or apply visual identity (typography, colors, spacing, design tokens, frontend aesthetics). Also use w | brand style guide,·visual identity,·design system, |
| [branding](skills/branding) | When the user wants to define, audit, or apply brand strategy—purpose, values, positioning, storytelling, voice, narrative (not only visuals | brand strategy,·brand story,·brand storytelling, |
| [cold-start-strategy](skills/cold-start-strategy) | When the user wants to plan cold start, get first users, or launch a new product with zero traction. Also use when the user mentions "cold s | cold start,·cold start problem,·first users, |
| [community-forum](skills/community-forum) | When the user wants to promote via forums, communities, or invite users to join a community. Also use when the user mentions "forum promotio | forum promotion,·Indie Hacker,·Hacker News, |
| [competitor-research](skills/competitor-research) | When the user wants to analyze competitors for SEO, content, backlinks, or positioning. Also use when the user mentions "competitor analysis | competitor analysis,·competitor research,·competitor keywords, |
| [content-marketing](skills/content-marketing) | When the user wants to plan content marketing across channels, define content types and formats, or create a content repurposing strategy. A | content marketing strategy,·content types,·content formats, |
| [content-strategy](skills/content-strategy) | When the user wants to plan content, or asks which topic or piece to prioritize, what to write about, or why posts bring no customers: topic |  |
| [conversion-optimization](skills/conversion-optimization) | When the user wants to improve conversion rates, run A/B tests, optimize funnels, or reduce friction. Also use when the user mentions "CRO," | CRO,·conversion rate optimization,·A/B test, |
| [creator-program](skills/creator-program) | When the user wants to plan, implement, or optimize creator program strategy. Also use when the user mentions "creator program," "creator pa | creator program,·creator partnership,·content co-creation, |
| [cro](skills/cro) | When the user wants more conversions from a page or form, or asks why a page isn't converting, what to change first, or whether to add or re |  |
| [ctv-ads](skills/ctv-ads) | When the user wants to run CTV, OTT, or streaming TV ads. Also use when the user mentions "CTV ads," "connected TV," "OTT advertising," "str | CTV ads,·connected TV,·OTT advertising, |
| [customer-research](skills/customer-research) | When the user wants to run or synthesize customer research, or asks what customer quotes, reviews, or feedback really mean, what is safe to  |  |
| [directory-listing-ads](skills/directory-listing-ads) | When the user wants to run paid ads within directories or marketplaces. Also use when the user mentions "Taaft ads," "Shopify App Store ads, | Taaft ads,·Shopify App Store ads,·G2 sponsored, |
| [discount-marketing-strategy](skills/discount-marketing-strategy) | When the user wants to plan, implement, or optimize discount and promotional pricing strategy. Also use when the user mentions "discount str | discount strategy,·promo code,·coupon, |
| [display-ads](skills/display-ads) | When the user wants to run display, banner, or ad network campaigns. Also use when the user mentions "display ads," "banner ads," "ad networ | display ads,·banner ads,·ad network, |
| [distribution-channels](skills/distribution-channels) | When the user wants to plan product distribution via marketplaces, app stores, or third-party platforms. Also use when the user mentions "di | distribution channels,·marketplace listing,·app store listing, |
| [education-program](skills/education-program) | When the user wants to plan, implement, or optimize student and education discount programs. Also use when the user mentions "student discou | student discount,·education discount,·student plan, |
| [email-marketing](skills/email-marketing) | When the user wants to plan email marketing, EDM, newsletter strategy, or email deliverability. Also use when the user mentions "email marke | email marketing,·EDM,·newsletter, |
| [employee-generated-content](skills/employee-generated-content) | When the user wants to plan, implement, or optimize employee-generated content (EGC) or employee advocacy. Also use when the user mentions " | EGC,·employee advocacy,·employee content, |
| [google-ads](skills/google-ads) | When the user wants to set up, optimize, or manage Google Ads campaigns. Also use when the user mentions "Google Ads," "Google Search Ads,"  | Google Ads,·Google Search Ads,·PPC, |
| [growth-funnel](skills/growth-funnel) | When the user wants to plan growth using the AARRR framework, diagnose growth bottlenecks, or map actions across the customer lifecycle. Als | growth funnel,·AARRR,·pirate metrics, |
| [gtm-strategy](skills/gtm-strategy) | When the user wants to plan go-to-market strategy, GTM framework, or market entry. Also use when the user mentions "GTM," "go-to-market," "m | GTM,·go-to-market,·market entry, |
| [indie-hacker-strategy](skills/indie-hacker-strategy) | When the user wants indie hacker or bootstrapping founder strategy—growth, channels, Build in Public, or solo founder tactics. Also use when | indie hacker,·indie developer,·bootstrapping, |
| [influencer-marketing](skills/influencer-marketing) | When the user wants to plan, implement, or optimize influencer marketing strategy. Also use when the user mentions "influencer marketing," " | influencer marketing,·KOL,·creator partnership, |
| [integrated-marketing](skills/integrated-marketing) | When the user wants to plan integrated marketing, coordinate channels, or clarify program vs channel vs campaign. Also use when the user men | IMC,·integrated marketing,·channel mix, |
| [lead-magnets](skills/lead-magnets) | When the user wants to plan or improve a lead magnet, or asks what to give away for emails or how much to ask in return (gating, form fields |  |
| [linkedin-ads](skills/linkedin-ads) | When the user wants to set up, optimize, or manage LinkedIn Ads. Also use when the user mentions "LinkedIn Ads," "LinkedIn Campaign Manager, | LinkedIn Ads,·LinkedIn Campaign Manager,·Sponsored Content, |
| [linkedin-posts](skills/linkedin-posts) | When the user wants to create LinkedIn post copy or optimize for LinkedIn. Also use when the user mentions "LinkedIn post," "LinkedIn articl | LinkedIn post,·LinkedIn article,·professional post, |
| [localization-strategy](skills/localization-strategy) | Plan, audit, implement, migrate, or validate localization for multilingual products and websites, including locale scope, market readiness,  |  |
| [marketing-council](skills/marketing-council) | When the user wants several expert takes on a marketing decision, or asks what a famous marketer would say about it: a simulated board (Seth |  |
| [marketing-ideas](skills/marketing-ideas) | When the user wants marketing ideas or growth tactics for a software product, or asks what to try to get attention or the next customers wit |  |
| [marketing-psychology](skills/marketing-psychology) | When the user wants to apply psychology to marketing, or asks why buyers behave or value things as they do, or whether a persuasion tactic i |  |
| [medium-posts](skills/medium-posts) | When the user wants to write, publish, republish, or optimize posts on Medium.com (canonical tags, distribution, Medium SEO). Also use when  | Medium,·Medium article,·Medium story, |
| [meta-ads](skills/meta-ads) | When the user wants to set up, optimize, or manage Meta (Facebook/Instagram) Ads. Also use when the user mentions "Meta Ads," "Facebook Ads, | Meta Ads,·Facebook Ads,·Instagram Ads, |
| [native-ads](skills/native-ads) | When the user wants to run native ads on Taboola, Outbrain, or similar platforms. Also use when the user mentions "native ads," "Taboola," " | native ads,·Taboola,·Outbrain, |
| [offers](skills/offers) | When the user wants to design or improve the offer itself, or asks why it isn't selling or how to add urgency honestly: value stacking, bonu |  |
| [open-source-strategy](skills/open-source-strategy) | When the user wants open source strategy, OSS commercialization, or open source growth. Also use when the user mentions "open source strateg | open source strategy,·OSS strategy,·open source commercialization, |
| [paid-ads-strategy](skills/paid-ads-strategy) | When the user wants to plan paid ads strategy, allocate ad budget, or choose paid channels. Also use when the user mentions "paid ads," "pai | paid ads,·paid media,·PPC, |
| [pinterest-posts](skills/pinterest-posts) | When the user wants to create Pinterest Pins, optimize Pin descriptions, or grow Pinterest presence. Also use when the user mentions "Pinter | Pinterest,·Pin,·Pinterest SEO, |
| [pmf-strategy](skills/pmf-strategy) | When the user wants to validate product-market fit, measure PMF, or plan before scaling. Also use when the user mentions "PMF," "product-mar | PMF,·product-market fit,·product market fit, |
| [podcast-marketing](skills/podcast-marketing) | When the user wants to plan, create, or market a podcast. Also use when the user mentions "podcast," "podcast strategy," "podcast SEO," "sho | podcast,·podcast strategy,·podcast SEO, |
| [pricing-strategy](skills/pricing-strategy) | When the user wants to plan, design, or optimize pricing strategy and structure. Also use when the user mentions "pricing strategy," "pricin | pricing strategy,·pricing model,·pricing tiers, |
| [product-hunt-launch](skills/product-hunt-launch) | When the user wants to launch on Product Hunt, prepare a PH submission, or plan launch day (hunter, first comment, timing, upvotes). Also us | Product Hunt,·launch on Product Hunt,·PH launch, |
| [product-launch](skills/product-launch) | When the user wants to plan a product launch, execute launch channels, or create a launch checklist. Also use when the user mentions "produc | product launch,·launch strategy,·product announcement, |
| [product-marketing](skills/product-marketing) | When the user wants to create or update the product marketing context doc (.agents/product-marketing.md), or asks what belongs in it or whet |  |
| [public-relations](skills/public-relations) | When the user wants to plan PR, write a press release, or manage media relations. Also use when the user mentions "public relations," "PR,"  | public relations,·PR,·press release, |
| [rebranding-strategy](skills/rebranding-strategy) | When the user wants to plan or execute a rebrand—domain change, 301 redirects, migration, or announcement. Also use when the user mentions " | rebranding,·rebrand,·domain change, |
| [reddit-ads](skills/reddit-ads) | When the user wants to set up, optimize, or manage Reddit Ads. Also use when the user mentions "Reddit Ads," "Promoted Posts," "subreddit ta | Reddit Ads,·Promoted Posts,·subreddit targeting, |
| [reddit-posts](skills/reddit-posts) | When the user wants to create Reddit post copy, comments, or optimize for Reddit. Also use when the user mentions "Reddit post," "subreddit, | Reddit post,·subreddit,·r/, |
| [referral-program](skills/referral-program) | When the user wants to plan, implement, or optimize referral program strategy. Also use when the user mentions "referral program," "referral | referral program,·referral marketing,·user referral, |
| [retention-strategy](skills/retention-strategy) | When the user wants to reduce churn, improve customer retention, or plan lifecycle marketing. Also use when the user mentions "retention," " | retention,·churn,·customer lifecycle, |
| [source-to-channels](skills/source-to-channels) | 하나의 원천(YouTube URL·웹 글 URL·내 원고/설교 전사본)을 받아 브리프 1장을 만들고, 채널별 산출물(블로그·뉴스레터·스레드·링크드인·카드뉴스·썸네일·쇼츠 대본·소그룹 질문)을 기존 스킬로 병렬 생성한 뒤 검수하는 오케스트레이터. "원소 | 원소스 멀티채널·이 영상/글/설교로 콘텐츠 만들어줘·한 번에 여러 채널 |
| [tiktok-ads](skills/tiktok-ads) | When the user wants to set up, optimize, or manage TikTok Ads. Also use when the user mentions "TikTok Ads," "TikTok for Business," "TikTok  | TikTok Ads,·TikTok for Business,·TikTok Pixel, |
| [tiktok-captions](skills/tiktok-captions) | When the user wants to create TikTok video captions, scripts, or optimize for TikTok. Also use when the user mentions "TikTok post," "TikTok | TikTok post,·TikTok caption,·TikTok video, |
| [translation](skills/translation) | Translate, transcreate, review, or maintain multilingual product and marketing content, including source locking, glossary decisions, langua |  |
| [twitter-x-posts](skills/twitter-x-posts) | When the user wants to create X (Twitter) post copy, threads, or optimize for X platform. Also use when the user mentions "X post," "X threa | X post,·X thread,·Twitter post, |
| [video-marketing](skills/video-marketing) | When the user wants to plan video marketing, create video scripts, or optimize for short-form or long-form video. Also use when the user men | video marketing,·video script,·short-form video, |
| [visual-content](skills/visual-content) | When the user wants to plan, create, or repurpose visual content (images, infographics, social post images) across channels. Also use when t | content images,·social media images,·infographic, |
| [weekly-content-board](skills/weekly-content-board) | 매주 "이번 주에 뭘 만들지"를 정하는 콘텐츠 의사결정 회의를 Workflow 도구(다이나믹 워크플로우)로 자동화해 승인 가능한 HTML 보고서를 뽑아낸다. "위클리보드", "AI 마케팅 본부", "콘텐츠 기획 회의 자동화", "이번 주 콘텐츠 뭐 만 | 이번 주에 뭘 만들지·위클리보드·AI 마케팅 본부 |
| [youtube-ads](skills/youtube-ads) | When the user wants to run YouTube ads, set up TrueView or Bumper campaigns, or optimize video ad creative. Also use when the user mentions  | YouTube ads,·TrueView,·Bumper ads, |

### 영상·음성·이미지 (49)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [audio-post](skills/audio-post) | 영상의 배경음악·효과음을 마련하고 나레이션 아래로 믹싱하는 대표 오디오 포스트 스킬 — 음악 베드 선택/생성과 덕킹·레벨 정규화를 하위 스킬로 오케스트레이션한다. 프로페셔널 영상 감의 핵심 레이어. "배경음악 / 음악 믹스 / 덕킹 / 오디오 포스트  | 배경음악 / 음악 믹스 / 덕킹 / 오디오 포스트 / bgm |
| [audio-post-mix](skills/audio-post-mix) | 배경음악을 나레이션 아래로 덕킹하고 라우드니스를 정규화하는 하위 스킬 — 사이드체인 덕킹·구간 페이드·유튜브 라우드니스 타깃(약 -14 LUFS)으로 최종 믹스 사양을 만든다. audio-post 믹스 관문. "오디오 믹스 / 덕킹 / 라우드니스 정규 | 오디오 믹스 / 덕킹 / 라우드니스 정규화 / 페이드 |
| [audio-post-music](skills/audio-post-music) | 영상 톤에 맞는 배경음악 베드를 저작권 안전하게 마련하는 하위 스킬 — 생성 음악(ElevenLabs Music 등)·로열티프리·보유 라이선스 중에서 확보하고 출처·라이선스를 기록한다. audio-post 음악 관문. "배경음악 선택 / 음악 생성 / | 배경음악 선택 / 음악 생성 / 로열티프리 / bgm 소스 |
| [codex-image](skills/codex-image) | ／ Generate images via Codex CLI's built-in image_gen tool (gpt-image-2). OAuth auth — no API key needed. Codex CLI의 내장 image_gen 도구로 이미지 생성. |  |
| [cost-preview-confirm](skills/cost-preview-confirm) | 종량제 외부 API(HeyGen 분당·ElevenLabs·fal.ai 초당/장당)를 실행하기 전에 예상 비용을 산출·표시하고 사용자 확인을 받는 공통 규약 스킬. 평판 리스크 옆의 비용 리스크를 막는다. "비용 미리보기 / 사전 비용 확인 / 종량제  |  |
| [explainer-video](skills/explainer-video) | 유튜브 정보성 해설 영상(바이브랩스 스타일)을 대본+내레이션에서 완성 mp4까지 자동 제작하는 스킬. 대본을 장면으로 분할하고, 내레이션 오디오(본인 녹음 또는 edge-tts)에 whisper로 자막 타이밍을 맞추고, codex-image로 장면 일 |  |
| [heygen-avatar-render](skills/heygen-avatar-render) | ElevenLabs 나레이션 오디오를 HeyGen Avatar V로 말하는 아바타 영상으로 렌더하는 대표 스킬 — 오디오 자산 업로드, v3 API의 avatar_v 엔진·audio_asset_id 구동, 적격성 확인, 폴링·다운로드·립싱크 QC. " |  |
| [heygen-avatar-render-api](skills/heygen-avatar-render-api) | HeyGen v3 API로 오디오 구동 아바타 영상을 생성하는 하위 스킬 — 오디오 자산 업로드, POST /v3/videos(engine avatar_v + audio_asset_id), 상태 폴링, 결과 다운로드의 canonical 호출 절차. h |  |
| [heygen-avatar-render-gate](skills/heygen-avatar-render-gate) | HeyGen 아바타 렌더의 적격성·완결성 게이트 하위 스킬 — 아바타 look의 supported_api_engines로 avatar_v 적격 확인, 렌더 폴링 재시도 정책, 립싱크·길이·완결 QC를 담당한다. heygen-avatar-render 품 | 아바타 적격성 / 렌더 QC / 립싱크 검수 |
| [history-shorts-mcp](skills/history-shorts-mcp) | 주제 한 줄 → 60~90초 '근거 등급' 역사·성경·지역사 해설 쇼츠를 생성형 영상 커넥터(MCP)로 한 번에 만드는 얇은 오케스트레이터. 사실 장부(A/B/C/X 등급) → 질문형 제목·장면표 → 크레딧 견적 게이트(1회 승인) → 음성 오디션(후 | 신비한 역사 사전? 영상 한번에 힉스필드로 제작! |
| [media-gen](skills/media-gen) | fal.ai 애그리게이터로 생성형 비주얼을 만드는 대표 스킬 — 텍스트→이미지·참조 편집·이미지→영상(시네마틱 B-roll)·업스케일·썸네일을 하위 스킬로 오케스트레이션한다. 모델을 경로로 지정해 새 모델도 코드 변경 없이 채택. "이미지 생성 / B |  |
| [media-gen-edit](skills/media-gen-edit) | 참조 이미지를 보존·편집하는 하위 스킬 — 입력 이미지를 URL로 전달해 정체성(얼굴 등)을 유지한 채 편집/합성한다(nano-banana-pro/edit, image_urls 배열). media-gen 편집 관문. "이미지 편집 / 참조 이미지 /  |  |
| [media-gen-image](skills/media-gen-image) | 텍스트 설명에서 이미지를 생성하는 하위 스킬 — 사용자의 거친 의도를 모델 최적 프롬프트로 재작성한 뒤 fal.ai 이미지 모델(nano-banana-pro 등)로 생성한다. media-gen 이미지 관문. "이미지 생성 / text to image  |  |
| [media-gen-thumbnail](skills/media-gen-thumbnail) | 유튜브 썸네일을 생성하는 하위 스킬 — 영상 주제·톤에서 클릭을 유도하는 이미지를 생성하고 가독성 높은 텍스트 오버레이를 얹는다(이미지 생성 + 편집 조합). media-gen 썸네일 관문. "썸네일 / 유튜브 썸네일 / thumbnail / 클릭 유 | 썸네일 / 유튜브 썸네일 / thumbnail / 클릭 유도 이미지 |
| [media-gen-upscale](skills/media-gen-upscale) | 영상·이미지를 고해상도로 업스케일하는 하위 스킬 — fal.ai Topaz 모델로 저해상 클립을 선명하게(배율 기반). 생성 B-roll뿐 아니라 임의 저화질 소스에도 적용. media-gen 업스케일 관문. "업스케일 / 화질 향상 / 해상도 올리기 | 업스케일 / 화질 향상 / 해상도 올리기 / topaz upscale |
| [media-gen-video](skills/media-gen-video) | 이미지를 시네마틱 영상 클립(B-roll)으로 애니메이트하는 하위 스킬 — fal.ai 영상 모델(Kling·Seedance 등)로 이미지→영상, 초당 종량제라 길이·비용을 정밀 제어한다. media-gen 영상 관문. "이미지를 영상으로 / B-ro |  |
| [object-separation](skills/object-separation) | Separate a person, product or hand from the background in a video, on the user's own computer with SAM 2. Scans the machine first to pick th |  |
| [photo-retouch](skills/photo-retouch) | 스튜디오급 사진 보정(리터칭) 워크플로 — 진단(색 균형·노이즈·선명도·조명·구도) → 보정 경로 선택(로컬 무료 vs 생성형) → 실행 → 개선 목록 보고. 스타일 프리셋(내추럴/시네마틱/비비드/미니멀/인물/제품). 사용자가 "사진 보정", "리터칭 | 사진 보정·리터칭·화질 개선 |
| [pumasi](skills/pumasi) | Codex /imagen으로 이미지 생성 — 모드 자동 감지 + image-studio 프롬프트 + 후처리 금지 가드 인자 없이 실행하면 어떤 이미지를 만들지 묻는다. 트리거: '/pumasi:image', 'Codex로 이미지 만들어줘', 'imag |  |
| [qwen-local-image](skills/qwen-local-image) | 이 Mac에 설치된 Qwen-Image-2.1(~/DEV/qwen-image-studio)로 이미지를 무료·오프라인 생성/편집한다. 한글 글자가 들어간 포스터·주보 표지·썸네일·슬라이드 배경, 비용 없는 초안, 개인 사진 편집(외부 전송 금지) 맥락에 | 로컬 이미지 / qwen 이미지 / 무료로 이미지 / 한글 포스터 |
| [rea-video](skills/rea-video) | 逆向拆解一条视频是怎么做出来的——逐镜头判断实拍 / 影视片段 / AI 生成 / 3D 渲染 / 2D 动画 / 定格动画 / 代码模板渲染 / 录屏截图 / 静态图推拉 / 静帧，以及实拍是否经过 AI 加工（换脸、对口型、风格化），标出后期叠加层（逐句字幕时间轴、花字、标题 |  |
| [recording-to-series](skills/recording-to-series) | 녹화 한 편(설교·강의·라이브·세미나·회의 영상이나 자막)을 받아, 따로 볼 만한 롱폼 N편과 쇼츠 M편을 Claude가 직접 판단해 편성표(제목·원본 구간·첫 문장·시청자가 얻는 것)로 만들고, 모든 구간이 실제 자막 시각과 맞는지·서로 겹치지 않는 | 녹화로 쇼츠 뽑아줘·라이브 한 편으로 몇 편 나와?·설교 영상 클립 나눠줘 |
| [script-writer](skills/script-writer) | 영상 주제 한 문장 → 사실 기반의 2~4분 유튜브 나레이션 대본을 만드는 대표 스킬. 리서치→구조 설계→사실검증→음성 청크 분절 4단계를 하위 스킬로 오케스트레이션한다. "영상 대본 / 스크립트 작성 / 나레이션 대본 / youtube script" |  |
| [script-writer-factcheck](skills/script-writer-factcheck) | 완성된 대본의 모든 단정 문장을 출처 대조로 검증하는 하위 스킬 — hallucination-guard 4문(출처 진실성·근거 적합성·논리오류·팩트체크)을 대본에 적용해 무근거 단정을 차단한다. script-writer 5단계·출고 게이트. "대본 팩 | 대본 팩트체크 / 사실 검증 / 환각 차단 |
| [script-writer-research](skills/script-writer-research) | 영상 대본의 사실 토대를 수집하는 하위 스킬 — 주제에 대해 검색·교차검증으로 검증된 사실과 출처를 모은다. 학습지식 단독 단정 금지. script-writer 1단계. "대본 리서치 / 주제 사실 수집 / 출처 조사" 맥락에서 발동. | 대본 리서치 / 주제 사실 수집 / 출처 조사 |
| [script-writer-structure](skills/script-writer-structure) | 유튜브 나레이션의 리텐션 구조를 설계하는 하위 스킬 — 훅(0~15초)·본론 세그먼트·CTA를 분량에 맞게 배치하고 각 세그먼트에 시각 큐를 단다. script-writer 2단계. "영상 구조 / 훅 설계 / 리텐션 구성 / 아웃라인" 맥락에서 발동 | 영상 구조 / 훅 설계 / 리텐션 구성 / 아웃라인 |
| [script-writer-voice-prep](skills/script-writer-voice-prep) | 검증된 대본을 음성 합성용 청크로 분절하는 하위 스킬 — 자연스러운 문장·절 경계에서 쪼개고 연속성 메타(prev/next 텍스트)와 시각 큐를 보존한다. script-writer 6단계, voice-clone-elevenlabs의 입력 생성. "대본 | 대본 청크 분절 / 음성 준비 / 나레이션 분할 |
| [shorts-series](skills/shorts-series) | Shorts를 한 편씩이 아니라 '시리즈'로 만들고, 시리즈마다 SERIES.md(형식·단계·검사·피드백·발행규칙)와 편별 수정 장부를 두어 '최근 3–4편 무수정이면 자동 발행 후보'를 기계로 판정하는 스킬. 렌더는 HyperFrames/Remoti |  |
| [slop-feedback-ledger](skills/slop-feedback-ledger) | AI가 만든 시각 결과물(코드형 모션그래픽 푸티지·덱·카드뉴스·광고 소재)을 "AI 슬롭" 기준 12개로 판정하고, 피드백을 "번호·대상·지시·이유(원칙ID)" 한 줄로 써서 프로젝트 원칙장부(원칙장부.md)에 쌓는 스킬. 이유를 함께 주면 같은 문서 | AI 슬롭·번호·대상·지시·이유(원칙ID)·클로드 코드로 감도높은 영상 만드는 법 |
| [sound-effects](skills/sound-effects) | Add a measured sound pass to a motion-graphics video made with Claude Code (HyperFrames, Remotion, GSAP, Claude Motion or the motion-broll s |  |
| [suite-runtime-keys](skills/suite-runtime-keys) | 영상 파이프라인 공통 규약 — 외부 서비스 API 키(ElevenLabs·HeyGen 등)를 하드코딩하지 않고 런타임에 받고, 없으면 deny-by-default로 멈춰 정확히 안내하는 패턴. 보급용 배포 전제. "API 키 처리 / BYOK / 런타 | API 키 처리 / BYOK / 런타임 키 / 키 누락 안내 |
| [video-stitch](skills/video-stitch) | 아바타 클립·HyperFrames 모션그래픽·생성형 B-roll·자막·배경음악을 하나의 완성 영상으로 합성하는 대표 편집 스킬 — 컴포지팅(아바타 항상 노출)·B-roll 배치·자막 번인을 하위 스킬로 오케스트레이션하고 FFmpeg로 마스터 렌더한다. | 영상 합성 / 편집 / 클립 결합 / 컴포지팅 / 자막 |
| [video-stitch-broll](skills/video-stitch-broll) | media-gen이 생성한 B-roll(이미지·영상 클립)을 편집 타임라인의 적소에 배치하는 하위 스킬 — 시각 큐에 맞춰 삽입하고 아바타 노출 규칙·길이·전환과 충돌 없게 조율한다. video-stitch B-roll 관문. "B-roll 배치 /  | B-roll 배치 / 생성 클립 삽입 / 보조영상 편집 |
| [video-stitch-captions](skills/video-stitch-captions) | 나레이션 타임스탬프 기반으로 동기 자막을 영상에 번인하는 하위 스킬 — ElevenLabs 문자 정렬(timestamps.json)로 단어 단위 동기, 가독성·세이프영역·아바타 비가림을 보장한다. video-stitch 자막 관문. "자막 번인 / 동 | 자막 번인 / 동기 캡션 / 서브타이틀 / synced captions |
| [video-stitch-compositing](skills/video-stitch-compositing) | 아바타를 모든 구간에 노출시키는 컴포지팅 하위 스킬 — 좌측 카드 슬라이드인 / 드롭섀도 둥근 크롭 모드, 전환·이징·페이싱을 사람 편집자 수준으로 적용한다. video-stitch 컴포지팅 관문. "아바타 컴포지팅 / 카드 슬라이드인 / 둥근 크롭  | 아바타 컴포지팅 / 카드 슬라이드인 / 둥근 크롭 / 전환 페이싱 |
| [video-study-pack](skills/video-study-pack) | 유튜브 영상 하나를 '연구·강의 패키지'로 만드는 오케스트레이터. 자막 확보 → 공통골격 → (병렬) 응용가이드 HTML·전문 논고·A5 소책자·강의안(슬라이드+강사노트) → 옵시디언 PKM 저장 → 스킬화 점검 → 웹페이지(아티팩트) 발행까지 한 번 |  |
| [video-to-playbook](skills/video-to-playbook) | 유튜브 영상 여러 편(또는 1편)을 받아 영상별 노트 → 교차 분석 → 응용·확장 아이디어와 "내게 쓰는 법" → 스킬·설치 점검 → HTML 정본 + 옵시디언 노트 + 자비스 학습지시문까지 한 번에 정리한다. "영상들 정리하고 분석해서 설명서 만들어 | 내게 쓰는 법·영상들 정리하고 분석해서 설명서 만들어줘·응용 아이디어와 사용 실례 |
| [video-verify](skills/video-verify) | 완성 영상을 업로드 전 시각적으로 검증·승인하는 대표 스킬 — 프레임 추출 후 비전 검수로 시각 품질·모션그래픽 타이밍·오디오 싱크·대본 사실성 4관문을 돌려 전부 GO일 때만 출고한다. "영상 검증 / 시각 검수 / 영상 QA / 업로드 전 확인 / |  |
| [video-verify-audio-sync](skills/video-verify-audio-sync) | 영상의 오디오 정합을 검증하는 하위 스킬 — 아바타 립싱크가 나레이션과 맞는지, 오디오 끊김·중복·무음 구간이 없는지, 청크 경계가 매끄러운지 판정한다. video-verify 3관문. "오디오 싱크 / 립싱크 검증 / 음성 정합 점검" 맥락에서 발동 | 오디오 싱크 / 립싱크 검증 / 음성 정합 점검 |
| [video-verify-final-gate](skills/video-verify-final-gate) | 출고 직전 최종 관문 하위 스킬 — 화면 자막·텍스트의 사실성을 대본 사실대장과 재대조하고, 앞 3관문 결과를 종합해 업로드 go/no-go를 판정한다. video-verify 4관문·출고 게이트. "최종 검증 / 사실성 재확인 / 업로드 승인 / g | 최종 검증 / 사실성 재확인 / 업로드 승인 / go no-go |
| [video-verify-timing](skills/video-verify-timing) | 모션그래픽의 진입·퇴장 타이밍이 나레이션·타임라인과 정확히 맞는지 검증하는 하위 스킬 — 그래픽이 해당 발화 지점에 맞춰 들어오고 나가는지, 너무 이르거나 늦지 않은지 판정한다. video-verify 2관문. "타이밍 검증 / 모션 싱크 / 그래픽  | 타이밍 검증 / 모션 싱크 / 그래픽 진입 점검 |
| [video-verify-visual](skills/video-verify-visual) | 완성 영상의 시각 품질을 프레임 단위 비전 검수로 판정하는 하위 스킬 — 화면 밖 이탈·요소 겹침·아바타 미노출·잘린 텍스트·미적 결함을 프레임에서 잡는다. video-verify 1관문. "시각 검수 / 프레임 QA / 화면 이탈 점검 / 레이아웃  | 시각 검수 / 프레임 QA / 화면 이탈 점검 / 레이아웃 검증 |
| [voice-clone-elevenlabs](skills/voice-clone-elevenlabs) | 검증된 대본 청크를 ElevenLabs로 일관된 나레이션 오디오로 합성하는 대표 스킬 — 음성 클론(voice_id) 확보, 글자수 한도 청킹, request stitching 연속성, 잠금된 settings·seed, 문자 타임스탬프까지. "음성 합 | 음성 합성 / 보이스 클론 / 나레이션 / elevenlabs tts |
| [voice-clone-elevenlabs-chunk](skills/voice-clone-elevenlabs-chunk) | 대본 세그먼트를 ElevenLabs 모델 글자수 한도에 맞춰 확정하고 request stitching 체인(순서·이웃 관계)을 구성하는 하위 스킬. 시간이 아니라 글자수로 자르고 문장 경계를 지킨다. voice-clone-elevenlabs 1단계.  | 음성 청킹 / stitching 체인 / 글자수 분할 |
| [voice-clone-elevenlabs-synth-qc](skills/voice-clone-elevenlabs-synth-qc) | 청크 계획을 ElevenLabs로 실제 합성하는 하위 스킬 — request stitching(previous_request_ids·prev/next_text), 잠금된 voice_settings·seed로 일관성을 강제하고, with-timestam | 음성 합성 실행 / stitching 합성 / 경계 QC |
| [voice-gate](skills/voice-gate) | 저자 voice·통찰·문장 패턴 cross-cutting 가드. 모든 단계 마스터 출력에 자동 발동. M1 VoiceScorer 결정론 호출 — LLM 추론 영구 금지. 임계 0.7+ 미달 시 1회 재작성·실패 시 저자 묶음. 저자 진북 #4 (작가성 |  |
| [voicebox-local-tts](skills/voicebox-local-tts) | 로컬 음성 스튜디오 Voicebox(jamiepine/voicebox)를 REST·MCP로 부려 한국어 TTS·내 목소리 클론 낭독·Whisper 전사·에이전트 음성 알림을 처리한다. ElevenLabs의 무료·오프라인 대안. "voicebox / 로 |  |
| [youtube-video-pipeline](skills/youtube-video-pipeline) | 주제 한 문장 → 완성된 유튜브 영상(아바타 + 모션그래픽 + 생성형 B-roll + 음악 + 썸네일)을 end-to-end로 자동 제작하는 대표 오케스트레이터 스킬. 대본→음성→아바타→생성형 비주얼→모션그래픽→음악→합성→검증의 기둥을 순서대로 굴린다 |  |
| [youtube-wiki-ingest](skills/youtube-wiki-ingest) | Ingest YouTube videos (a channel, playlist, or single URL) into an LLM Wiki / Obsidian vault as timestamped raw transcripts plus concept pag |  |

### 개발·자동화 (48)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-native-app-harness](skills/agent-native-app-harness) | Agent Native Agent(ANA) 하네스 — 대시보드를 '보면서' 코딩 에이전트와 '대화하며' 운영하는 에이전트 네이티브 앱/에이전트를 만들고 발전시키는 스킬. '에이전트 네이티브 에이전트', 'ANA', 'ANL', '보면서 대화하는 운영  |  |
| [appbuild](skills/appbuild) | 웹/앱을 기획→검증→자율빌드로 만드는 대표 오케스트레이터 스킬. 기획(plan)→화면명세(screen-spec)→작업목록(tasks)→★감독관 검증루프(supervisor)→게이트 통과까지 자율빌드(orchestrate)를 순서대로 굴린다. cysja |  |
| [appbuild-orchestrate](skills/appbuild-orchestrate) | 완료 게이트를 통과할 때까지 멀티페인으로 자율 빌드하는 대표 스킬 — master가 백/프론트 페인에 위임하고 다른 페인이 E2E 증거 검증, 메인은 절대 직접 수정 않고 문제를 해당 모듈로 라우팅하는 루프. appbuild 5단계. "자율 빌드 /  |  |
| [appbuild-orchestrate-delegate](skills/appbuild-orchestrate-delegate) | master가 빌드 작업을 백엔드·프론트엔드 페인에 위임하는 하위 스킬 — 04-tasks 슬라이스를 적합한 페인·모델에 분배하고 메인은 모니터링·조정만 한다. appbuild-orchestrate 위임 관문. "작업 위임 / 멀티페인 분배 / 백엔드 | 작업 위임 / 멀티페인 분배 / 백엔드 프론트엔드 위임 |
| [appbuild-orchestrate-route](skills/appbuild-orchestrate-route) | 검증이 보고한 문제를 프론트/백 판별해 해당 페인에 수정 위임하는 하위 스킬 — 메인 오케스트레이터가 직접 고치지 않고 원인 모듈로 라우팅하고 재검증을 시킨다. appbuild-orchestrate 라우팅 관문. "문제 라우팅 / 수정 위임 / 프론트 | 문제 라우팅 / 수정 위임 / 프론트 백 판별 / 메인은 수정 안 함 |
| [appbuild-orchestrate-verify](skills/appbuild-orchestrate-verify) | 만든 페인이 아닌 다른 페인이 완성물을 E2E로 직접 검증해 증거를 수집하는 하위 스킬 — 게이트 체크리스트를 들고 실행하고 문제는 고치지 말고 리포트만 한다(producer≠evaluator). appbuild-orchestrate 검증 관문. "E | E2E 검증 / 증거 검증 / 다른 페인 검증 / 체크리스트 실행 |
| [appbuild-plan](skills/appbuild-plan) | 웹/앱 기획 산출물(01-prd·03-architecture)을 만드는 대표 스킬 — 인터뷰/디베이트/퀵 3모드로 요구·스택·데이터모델을 도출한다. appbuild 1단계(소크라테스 기획). "앱 기획 / PRD 작성 / 요구 도출 / 기획 모드" 트 | 앱 기획 / PRD 작성 / 요구 도출 / 기획 모드 |
| [appbuild-plan-debate](skills/appbuild-plan-debate) | AI 2명(gemini·codex)이 10턴+ 스스로 토론해 웹/앱 기획을 좁히는 기획 모드 하위 스킬 — 인간 개입 없이 시장·차별점·기술 합의를 도출한다(§6 LLM 라운드 배선). appbuild-plan 모드 2. "기획 디베이트 / AI 토론 | 기획 디베이트 / AI 토론 기획 / 자동 기획 |
| [appbuild-plan-interview](skills/appbuild-plan-interview) | 소크라테스식 인터뷰로 웹/앱 요구를 캐내는 기획 모드 하위 스킬 — 분기 질문으로 가정·모서리·완료 조건을 합의에 이를 때까지 끌어낸다(grill-me 배선). appbuild-plan 모드 1. "기획 인터뷰 / 요구 캐기 / 소크라테스 기획" 맥락 | 기획 인터뷰 / 요구 캐기 / 소크라테스 기획 |
| [appbuild-plan-quick](skills/appbuild-plan-quick) | 질문을 최소로 해서 바로 기획 산출물을 작성하는 기획 모드 하위 스킬 — 명확한 아이디어·숙련 사용자를 위해 핵심 결정만 빠르게 확정하고 PRD·아키텍처를 즉시 만든다. appbuild-plan 모드 3. "빠른 기획 / 퀵 PRD / 질문 최소 기획 | 빠른 기획 / 퀵 PRD / 질문 최소 기획 |
| [appbuild-screen-spec](skills/appbuild-screen-spec) | 웹/앱 화면 명세(02-screens)를 만드는 대표 스킬 — 화면 흐름·내비게이션과 화면별 상세(레이아웃·상태·컴포넌트·데이터)를 하위 스킬로 작성한다. appbuild 2단계. "화면 명세 / 스크린 스펙 / UI 명세 / 화면 설계" 트리거, 또 | 화면 명세 / 스크린 스펙 / UI 명세 / 화면 설계 |
| [appbuild-screen-spec-detail](skills/appbuild-screen-spec-detail) | 화면별 상세(레이아웃·상태·컴포넌트·데이터)를 명세하는 하위 스킬 — 정상/빈/에러/로딩 상태를 빠짐없이, 참조 데이터를 아키텍처 모델과 일치시킨다. appbuild-screen-spec 상세 관문. "화면 상세 / 화면 상태 / 컴포넌트 명세 / 빈 | 화면 상세 / 화면 상태 / 컴포넌트 명세 / 빈 상태 에러 상태 |
| [appbuild-screen-spec-flow](skills/appbuild-screen-spec-flow) | 화면 목록과 내비게이션/사용자 흐름(정보 구조)을 설계하는 하위 스킬 — PRD 기능을 화면에 매핑하고 화면 간 이동·진입점을 정의한다. appbuild-screen-spec 흐름 관문. "화면 흐름 / 내비게이션 / 정보구조 / 사용자 플로우" 맥락 | 화면 흐름 / 내비게이션 / 정보구조 / 사용자 플로우 |
| [appbuild-supervisor](skills/appbuild-supervisor) | 이미 만든 기획 문서(01~04)를 다시 읽고 검증하는 대표 감독관 스킬 — 수집→13항목 검증→반자동 수정(승인 후·빠진 곳만·최대 3회)→완료 게이트 파생을 하위 스킬로 굴린다. 문서를 만드는 게 아니라 검증한다. appbuild 4단계·빌드 전  |  |
| [appbuild-supervisor-collect](skills/appbuild-supervisor-collect) | 감독관 검증의 입력을 수집·정규화하는 하위 스킬 — 01~04 문서와 기능↔화면↔데이터↔작업 매핑·ID를 모아 검증 가능한 형태로 만든다. appbuild-supervisor 수집 관문. "기획 문서 수집 / 매핑 정규화 / 검증 입력 준비" 맥락에서 | 기획 문서 수집 / 매핑 정규화 / 검증 입력 준비 |
| [appbuild-supervisor-fix](skills/appbuild-supervisor-fix) | 검증에서 발견된 결함을 반자동으로 교정하는 하위 스킬 — 사용자 승인을 받고, 빠진 곳만, 최대 3회 원본 스킬로 되돌려 고친 뒤 재검증한다. appbuild-supervisor 수정 관문. "반자동 수정 / 빠진 곳 교정 / 승인 후 수정 / 최대  | 반자동 수정 / 빠진 곳 교정 / 승인 후 수정 / 최대 3회 |
| [appbuild-supervisor-gate](skills/appbuild-supervisor-gate) | 검증된 스펙에서 프로젝트별 완료 게이트(05-gate.md)를 파생하는 하위 스킬 — 기능별 수용(RTM)·전역 DoD·비기능·교차정합을 증거 기반 통과 기준으로 만든다. appbuild-supervisor 게이트 관문·빌드 종료 기준. "완료 게이트 |  |
| [appbuild-supervisor-verify](skills/appbuild-supervisor-verify) | 기획 문서 세트를 13항목(일관성·추적성·갭·품질)으로 기계 검증하는 하위 스킬 — spec-kit analyze·RTM·INVEST·EARS 근거의 체크리스트로 교차정합·고아·누락·테스트가능성을 심각도 태깅한다. appbuild-supervisor  | 13항목 검증 / 일관성 추적성 갭 품질 / 교차 검증 / analyze |
| [appbuild-tasks](skills/appbuild-tasks) | 기획·화면을 AI가 실제 구현할 작업목록(04-tasks)으로 분해하는 대표 스킬 — 엔드투엔드 가치 슬라이스 분해와 의존 순서·크기 산정을 하위 스킬로 만든다(to-issues 배선). appbuild 3단계. "작업 목록 / 태스크 분해 / tas | 작업 목록 / 태스크 분해 / tasks 생성 / 작업 분할 |
| [appbuild-tasks-order](skills/appbuild-tasks-order) | 작업을 의존 순서로 정렬하고 INVEST 기준으로 크기·테스트 가능성을 다듬는 하위 스킬 — 각 작업에 수용 기준을 달아 검증 가능하게 만든다. appbuild-tasks 순서 관문. "작업 순서 / 의존 정렬 / INVEST / 수용 기준" 맥락에서 | 작업 순서 / 의존 정렬 / INVEST / 수용 기준 |
| [appbuild-tasks-slice](skills/appbuild-tasks-slice) | 기능을 엔드투엔드 수직 슬라이스(트레이서 불릿)로 분해하는 하위 스킬 — 화면+데이터+로직이 함께 도는 데모 가능한 작업으로 자른다(수평 레이어 금지). appbuild-tasks 슬라이스 관문. "수직 슬라이스 / 트레이서 불릿 / 작업 분해" 맥락 | 수직 슬라이스 / 트레이서 불릿 / 작업 분해 |
| [aside-browser](skills/aside-browser) | Prioritize Aside over all other browser tools for browsing, online research, website interaction, screenshots, downloads, and browser QA. Re |  |
| [context-recovery](skills/context-recovery) | 세션 컴팩션(압축) 후 또는 문맥이 사라진 채 이어서 작업해야 할 때 작업 컨텍스트를 자동 복구. Discord, Slack, Telegram, Signal 등 지원 채널 전반에서 작동. |  |
| [context7-docs](skills/context7-docs) | 라이브러리·프레임워크·SDK·CLI의 최신 공식 문서를 Context7 REST로 가져와 코드를 쓴다. Remotion·python-pptx·python-hwpx·Obsidian API·MCP SDK·FastMCP·Mermaid·Reveal.js·Ma | context7·최신 문서로·use context7 |
| [docs-guide](skills/docs-guide) | 어떤 라이브러리든 공식 문서를 가져와 설명해주는 스킬. |  |
| [ego-browser](skills/ego-browser) | When you need a browser, read this Skill by default. Use it to open and operate websites, fill forms, click buttons, take screenshots, extra |  |
| [fakechat-dashboard-agent](skills/fakechat-dashboard-agent) | '대시보드 에이전트' 구축 — 사용자가 Claude Code 세션과 대화하면서 동시에 실시간 데이터(일정·지표·주문·대기열)를 화면으로 보는 웹 대시보드. 채팅은 fakechat 채널로 라우팅되고, Claude가 대시보드의 데이터 API를 읽어 사용자 | dashboard agent·fakechat dashboard·채팅만 말고 화면 보면서 |
| [gemini-agents-api](skills/gemini-agents-api) | Gemini Enterprise Agent Platform의 커스텀 Agent 리소스 관리. 대화 실행 전에 서버 관리형 상태 유지 Agent 리소스를 프로그램으로 생성·설정·조회·수정·삭제(파일·스킬·도구 마운트 포함)할 때 사용. |  |
| [gemini-api](skills/gemini-api) | 기업 환경에서 Gemini를 쓰거나 Vertex AI, Google Cloud, Agent Platform이 언급될 때 사용. Google Gen AI SDK 기반 Gemini API 사용법 안내 — SDK(Python, JS/TS, Go, Java, |  |
| [gemini-interactions-api](skills/gemini-interactions-api) | Gemini Enterprise Agent Platform의 Interactions API 사용 안내. 멀티턴 대화, 백그라운드 실행, 스트리밍, 구조화 출력, 함수 호출을 서버 관리형 상태 유지 API로 쓰고 싶을 때 사용. |  |
| [git-teacher](skills/git-teacher) | 바르다 깃선생 — Git/GitHub를 쉽게 도와주는 명령어 비개발자용으로 Git 설치·GitHub 연결(시작), 상태 보기, 저장(커밋), 올리기(푸시), 검토 요청(PR), 용어 도움말을 한국어로 안내한다. 트리거: '깃선생', '/git-teac |  |
| [github](skills/github) | GitHub Desktop | GitHub,·GitHub SEO,·GitHub parasite SEO, |
| [goaljaby](skills/goaljaby) | PRD 폴더를 받아 한국어 검토 문서 5종을 자동 생성하고, 검토 요약을 대화창에 띄운 뒤 사용자 승인을 받으면 어시스턴트가 응답 마지막 줄로 /goal을 보내 다음 턴에서 골 작업을 시작한다 (Claude Code 전용). |  |
| [graphify](skills/graphify) | Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, wher |  |
| [harness](skills/harness) | 프로젝트에 맞는 하네스를 설계하고, 전문 에이전트와 각 에이전트가 사용할 스킬을 만든다. 사용자가 '하네스 구성해줘', '하네스 구축해줘', '하네스 설계', '하네스 엔지니어링', '에이전트 팀 만들어줘'라고 요청할 때 사용한다. 새로운 분야나 프로 |  |
| [harness-engineering](skills/harness-engineering) | ／ ## TLDR — 하네스(AI 에이전트를 사람 개입 없이 오래 자율주행시키는 장치)를 자비스에서 운영하는 7기법 대표 스킬. 핵심 철학은 "구체화는 사람이, 구현·검증은 자율 하네스" — 개발 4단계(요구구체화→설계→구현→검증) 중 뒤 두 단계(구 | 구체화는 사람이, 구현·검증은 자율 하네스·쓸모없는 정보는 안 주고 알아야 할 것만·하네스 엔지니어링 |
| [hycli](skills/hycli) | Prepare a website as local CLI and MCP actions, reuse its saved sign-in, and complete website tasks through Hycli. Use when a user wants to  |  |
| [hycli-recipes](skills/hycli-recipes) | 김병곤 목사·교수의 Hycli 실행 레시피 모음. "복지 보도자료 모아줘", "블로그 임시저장", "hycli 점검", "사이트 도구로 만들어줘", "교회 홈페이지 공지", "LMS 공지 확인" 등 Hycli로 웹사이트 작업을 할 때 사용. 일반 동작 | 복지 보도자료 모아줘·블로그 임시저장·hycli 점검 |
| [iam-recommendations-fetcher](skills/iam-recommendations-fetcher) | Google Cloud에서 지정한 범위(조직·폴더·프로젝트)의 원시 IAM 권한 추천과 보안 인사이트를 가져온다. 추천을 분석·적용하기 전 조회 용도 — 적용은 별도 스킬이 담당. |  |
| [qa-inspector](skills/qa-inspector) | 완성된 산출물(설교 원고·강의안·보고서·HTML·공문)을 내보내기 직전에 검수한다. 요청 항목 누락, 출처 없는 수치, 존재 확인 안 된 인용·링크, 사실/추정 혼동, 개인정보 노출, 형식 규칙 위반을 찾아 PASS/FIX/BLOCK으로 판정한다. " | @qa-inspector·검수해줘·QA |
| [replica-diff](skills/replica-diff) | >- Compares an app clone against the original: a feature parity score from the feature matrix (weighted by must, should, could) with the mis | how close is my clone·compare it to the original·what's missing |
| [replica-entrepreneur](skills/replica-entrepreneur) | >- Researches the app being cloned and reads what its real users say in public reviews (App Store, Google Play, G2, Capterra, Trustpilot, Re | what do people hate about X·read the reviews·how do I make mine better |
| [replica-recon](skills/replica-recon) | >- Reverse-engineers any app into a recon map: screen inventory, user flows, component list, inferred data model and a feature matrix, from  | clone this app·reverse engineer X·how does X work |
| [reverse-engineer-anything](skills/reverse-engineer-anything) | Reverse engineer native, managed, Electron/JavaScript, packaged, firmware, and browser targets with REA, and build agent environments (Agent |  |
| [scrapling-adaptive](skills/scrapling-adaptive) | 공개 웹페이지를 정기적으로 수집하는 스크립트에서, 사이트 개편으로 CSS 선택자가 깨져도 같은 항목을 다시 찾게 할 때 사용. "개편돼도 안 깨지는 크롤러", "공지 변경 감시", "scrapling", "적응형 선택자" 요청에 쓴다. 차단 우회용이  | 개편돼도 안 깨지는 크롤러·공지 변경 감시·scrapling |
| [security-audit](skills/security-audit) | Security guidance and vulnerability review for codebases, APIs, services, CLI tools, libraries, and daemons. Use for security questions, foc |  |
| [show-me-the-prd](skills/show-me-the-prd) | 인터뷰 기반 PRD 생성 -- 한 문장에서 4종 디자인 문서까지 아이디어 한 문장을 인터뷰(AskUserQuestion)로 구체화해 PRD 등 디자인 문서 4종으로 만든다. 트리거: '/show-me-the-prd', 'PRD 써줘', '앱 아이디어  |  |
| [work-tool-tailor](skills/work-tool-tailor) | >- 검토표(적용 함/적용 안 함)로 내 상황을 먼저 받아 적은 뒤, 로그인·DB 없는 단일 HTML 업무 도구를 맞춤 제작한다. 김지백 「업무 도구 주문 사전」(nondev-thinking.web.app/tools) 방식. 트리거: "○○ 도구 주문 | 업무 도구 주문 사전·○○ 도구 주문·업무 도구 맞춤 제작 |

### SEO·검색 노출 (48)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [ai-traffic-tracking](skills/ai-traffic-tracking) | Compatibility pointer for AI assistant referrals and generative search visibility; maintained in Open Analytics. |  |
| [analytics-tracking](skills/analytics-tracking) | Compatibility pointer for GA4 event, key-event and User-ID tracking; maintained in Open Analytics. |  |
| [backlink-analysis](skills/backlink-analysis) | When the user wants to analyze backlinks, audit link profile, or identify link issues. Also use when the user mentions "backlink analysis,"  | backlink analysis,·backlink audit,·referring domains, |
| [canonical-tag](skills/canonical-tag) | Audit and fix duplicate-page canonicalization across protocol, host, slash, default-document, extension, case, and tracking-parameter URL va |  |
| [content-optimization](skills/content-optimization) | When the user wants to optimize content for SEO—word count, H2 keywords, keyword density, multimedia, tables, lists. Also use when the user  | content length,·word count,·keyword stuffing, |
| [core-web-vitals](skills/core-web-vitals) | When the user wants to optimize Core Web Vitals, fix LCP, INP, or CLS issues. Also use when the user mentions "Core Web Vitals," "CWV," "LCP | Core Web Vitals,·CWV,·LCP, |
| [directory-submission](skills/directory-submission) | When the user wants to submit a product or app to directories, curated lists, launch platforms, or app stores—and needs ready-to-paste copy  | directory submission,·get listed,·app store listing, |
| [domain-architecture](skills/domain-architecture) | When the user wants to decide domain structure for multiple products or brands—subfolder vs subdomain vs independent domain. Also use when t | subfolder vs subdomain,·subdirectory vs subdomain,·multiple products domain, |
| [domain-selection](skills/domain-selection) | When the user wants to choose an SEO-friendly domain for a new site—brand vs keyword domain, TLD selection, or domain best practices. Also u | domain choice,·pick domain,·SEO-friendly domain, |
| [eeat-signals](skills/eeat-signals) | When the user wants to improve E-E-A-T, add trust signals, or optimize for expertise and authority. Also use when the user mentions "E-E-A-T | E-E-A-T,·E-E-A-T signals,·experience expertise authority trust, |
| [entity-seo](skills/entity-seo) | When the user wants to optimize for entity recognition, Knowledge Graph, or entity-based SEO. Also use when the user mentions "entity SEO,"  | entity SEO,·entity optimization,·Knowledge Graph, |
| [favicon-generator](skills/favicon-generator) | When the user wants to implement, optimize, or audit favicon and app icons. Also use when the user mentions "favicon," "app icon," "browser  | favicon,·app icon,·browser icon, |
| [featured-snippet](skills/featured-snippet) | When the user wants to optimize for Featured Snippets, Position Zero, or snippet extraction. Also use when the user mentions "featured snipp | featured snippet,·position zero,·snippet optimization, |
| [generative-engine-optimization](skills/generative-engine-optimization) | When the user wants to optimize for AI search visibility (ChatGPT, Claude, Perplexity, AI Overviews). Also use when the user mentions "GEO," | GEO,·AEO,·generative engine optimization, |
| [google-search-console](skills/google-search-console) | Compatibility pointer for Search Console performance and indexing analysis; maintained in Open Analytics. |  |
| [grokipedia-recommendations](skills/grokipedia-recommendations) | When the user wants to add recommendations, links, or content to Grokipedia. Also use when the user mentions "Grokipedia," "GEO wiki," "AI e | Grokipedia,·GEO wiki,·AI encyclopedia, |
| [heading-structure](skills/heading-structure) | When the user wants to write or optimize H1-H6, fix heading hierarchy, improve content structure, rewrite an H1, or align headings with page |  |
| [image-optimization](skills/image-optimization) | When the user wants to optimize images for search engines and performance. Also use when the user mentions "image SEO," "alt text," "image c | image SEO,·alt text,·image captions, |
| [indexing](skills/indexing) | When the user wants to fix indexing issues from Search Console, use noindex, or implement Google Indexing API. Also use when the user mentio | fix indexing,·not indexed,·Crawled - currently not indexed, |
| [indexnow](skills/indexnow) | When the user wants to implement IndexNow, notify search engines of new/updated URLs, or speed up Bing indexing. Also use when the user ment | IndexNow,·Bing indexing,·URL notification, |
| [internal-links](skills/internal-links) | When the user wants to optimize internal linking, fix orphan pages, or improve link structure. Also use when the user mentions "internal lin | internal links,·internal linking,·anchor text, |
| [keyword-research](skills/keyword-research) | When the user wants to research keywords, find target keywords, or analyze search intent. Also use when the user mentions "keyword research, | keyword research,·keyword tool,·target keywords, |
| [link-building](skills/link-building) | When the user wants to build backlinks, acquire links, or improve off-page SEO. Also use when the user mentions "link building," "backlinks, | link building,·backlinks,·off-page SEO, |
| [local-seo](skills/local-seo) | When the user wants to optimize for local search, set up Google Business Profile, or build local citations. Also use when the user mentions  | local SEO,·Google Business Profile,·Google Maps, |
| [meta-description](skills/meta-description) | When the user wants to write, audit, or optimize a meta description, SEO description, SERP snippet candidate, duplicate description, descrip |  |
| [mobile-friendly](skills/mobile-friendly) | When the user wants to optimize for mobile-first indexing or fix mobile usability. Also use when the user mentions "mobile-friendly," "mobil | mobile-friendly,·mobile-first indexing,·mobile SEO, |
| [multi-domain-brand-seo](skills/multi-domain-brand-seo) | When the user wants to optimize brand search for a company with multiple domains (e.g. parent company.com vs product.ai). Ensure the parent/ | brand search,·multi-domain SEO,·company domain first, |
| [open-graph](skills/open-graph) | When the user wants to add, audit, implement, or optimize Open Graph metadata for social sharing, including og:title, og:description, og:ima |  |
| [page-metadata](skills/page-metadata) | When the user wants a full-page metadata audit or implementation across discovery, search intent, title, description, canonical, robots, hre | metadata audit,·sitewide meta optimization,·metadata implementation, |
| [parasite-seo](skills/parasite-seo) | When the user wants to choose or execute third-party platform SEO (high-authority sites for rankings or backlinks). Also use when the user m | parasite SEO,·parasitic SEO,·barnacle SEO, |
| [programmatic-seo](skills/programmatic-seo) | When the user wants to create SEO pages at scale using templates and data—including AI-assisted, grounded copy for per-URL differentiation ( | programmatic SEO,·programmatic SEO pages,·template pages, |
| [rendering-strategies](skills/rendering-strategies) | When the user wants to choose or optimize rendering strategy for SEO. Also use when the user mentions "SSR," "SSG," "CSR," "ISR," "static re | SSR,·SSG,·CSR, |
| [robots-txt](skills/robots-txt) | When the user wants to configure, audit, or optimize robots.txt. Also use when the user mentions "robots.txt," "crawler rules," "block crawl | robots.txt,·crawler rules,·block crawlers, |
| [schema-markup](skills/schema-markup) | When the user wants to add or optimize structured data (Schema.org, JSON-LD). Also use when the user mentions "schema," "structured data," " | schema,·structured data,·JSON-LD, |
| [seo-audit](skills/seo-audit) | When the user wants to run an SEO audit, technical SEO audit, or site health check. Also use when the user mentions "SEO audit," "technical  | SEO audit,·technical audit,·site audit, |
| [seo-monitoring](skills/seo-monitoring) | Compatibility pointer for recurring SEO monitoring; maintained in Open Analytics. |  |
| [seo-strategy](skills/seo-strategy) | When the user wants to plan SEO strategy, prioritize SEO work, or understand the SEO workflow. Also use when the user mentions "SEO strategy | SEO strategy,·SEO plan,·SEO roadmap, |
| [serp-features](skills/serp-features) | When the user wants to understand or optimize for SERP feature types (PAA, sitelinks, rich results, AI Overviews). Also use when the user me | SERP,·SERP features,·search result features, |
| [site-crawlability](skills/site-crawlability) | When the user wants to improve crawlability, fix orphan pages, or optimize site structure for search engines. Also use when the user mention | crawlability,·crawl budget,·orphan pages, |
| [title-tag](skills/title-tag) | When the user wants to write, audit, or optimize an HTML title tag, SEO title, page title, SERP title, browser-tab title, duplicate title, o |  |
| [traffic-analysis](skills/traffic-analysis) | Compatibility pointer for source, UTM and direct-traffic analysis; maintained in Open Analytics. |  |
| [twitter-cards](skills/twitter-cards) | When the user wants to add, audit, implement, or optimize Twitter Card metadata for X link previews, including twitter:card, twitter:title,  |  |
| [url-slug-generator](skills/url-slug-generator) | When the user wants to create, optimize, or validate URL slugs for content pages. Also use when the user mentions "URL slug," "URL path," "b | URL slug,·URL path,·blog URL, |
| [url-structure](skills/url-structure) | When the user wants to optimize URL structure, fix URL issues, or plan URL hierarchy. Also use when the user mentions "URL structure," "URL  | URL structure,·URL optimization,·slug, |
| [video-optimization](skills/video-optimization) | When the user wants to optimize videos for Google Search, video sitemap, VideoObject schema, or video SEO on websites. Also use when the use | video SEO,·video sitemap,·VideoObject, |
| [website-structure](skills/website-structure) | When the user wants to plan website structure, decide which pages to build, or prioritize pages for a new or existing site. Also use when th | website structure,·site structure,·which pages do I need, |
| [xml-sitemap](skills/xml-sitemap) | When the user wants to create, audit, or optimize sitemap.xml. Also use when the user mentions "sitemap," "sitemap.xml," "sitemap index," "l | sitemap,·sitemap.xml,·sitemap index, |
| [youtube-seo](skills/youtube-seo) | When the user wants to optimize YouTube videos for search, create video descriptions, or improve channel visibility. Also use when the user  | YouTube SEO,·YouTube description,·YouTube tags, |

### 공공데이터·법령·생활정보 (43)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [alio](skills/alio) | ALIO 공공기관 경영정보 공개시스템(alio.go.kr)의 기관별 공시에서 공공기관별 공시 상세내용을 확인하고, k-dart처럼 기관 식별 → 공시 항목 선택 → 상세 공시 확인 → 출처 포함 요약으로 정리할 때 사용한다. 특정 공공기관의 일반현황, |  |
| [arch-ministry-lens](skills/arch-ministry-lens) | 목회·통합돌봄·교회 건물 실사·강의·지역 브리프에 국토교통부 건축물대장 데이터를 쓰는 레시피 스킬. 이미 설치된 korean-archhub MCP(건축HUB, mcp.gomdori.app/archhub, 도구 12종)로 ① 교회 예배당 매입·임대 전  | 건물 정보·건축물대장·예배당 매입 |
| [assembly-bill-vote-search](skills/assembly-bill-vote-search) | 열린국회정보 Open API를 k-skill-proxy 경유로 호출해 의안 검색·상세와 국회의원 본회의 표결정보를 조회한다. 조회 전용. 트리거: ''○○법 의안 검색'', ''BILL_ID 의안 상세'', ''본회의 표결 의원별 찬반''. |  |
| [bok-ecos-stats](skills/bok-ecos-stats) | 한국은행 ECOS Open API로 기준금리, 환율, 소비자물가지수, 통화량 등 중앙은행 경제통계 시계열과 100대 핵심지표를 조회한다. Use when the user asks 기준금리, 환율 추이, 물가지수, M2, 국고채 금리, 거시경제 통계.  |  |
| [building-register-search](skills/building-register-search) | Use when the user asks to look up a Korean building-register title record by address, PNU, legal-dong code, or parcel number. 예배당 매입 실사·통합돌봄 |  |
| [court-auction-notice-search](skills/court-auction-notice-search) | Browse 대법원경매정보(courtauction.go.kr) 부동산 매각공고 by 매각기일·법원·기일/기간 입찰, expand each notice into 사건번호·용도·주소·감정평가액·최저매각가, search property items by fr |  |
| [d2b-notice-search](skills/d2b-notice-search) | 국방전자조달시스템(D2B) 공개 입찰공고 검색 화면에서 공고건명·공고구분·공고/개찰일·G2B공고번호·발주기관 조건으로 공고를 조회한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [dart-ministry-lens](skills/dart-ministry-lens) | 목회·총회·사회복지 연구·강의·지역 브리프에 금융감독원 전자공시(DART)를 끼워 넣는 레시피 스킬. korean-dart MCP(chrisryugj/korean-dart-mcp, 18도구)로 ① 교회 건축 시공사·협력업체 사전 실사 ② 교단 연금·기 | 시공사 재무 확인·건설사 부도 이력·연금재단 투자처 점검 |
| [g2b-bid-search](skills/g2b-bid-search) | 나라장터(g2b.go.kr) 입찰공고 Open API로 용역·물품·공사 공고를 검색하고 공고명, 수요기관, 공고기관, 추정가격·배정예산, 입찰마감, 개찰일시, 계약방법, 낙찰방법, 첨부 규격서 URL, 상세 URL을 정리한다. Use when the  |  |
| [g2b-order-plan-search](skills/g2b-order-plan-search) | 조달청 나라장터 발주계획현황서비스로 물품·공사·용역·외자 발주계획 목록을 검색한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [g2b-sanctioned-supplier](skills/g2b-sanctioned-supplier) | 조달청 나라장터 부정당제재업체정보를 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 사업자등록번호 정확 일치로 조회시점 현재 유효한 입찰참가자격 제한(부정당제재)의 기간·제재기관·근거법률을 확인한다. |  |
| [hankookilbo-news](skills/hankookilbo-news) | 한국일보 공식 원격 MCP 서버(mcp.hankookilbo.com)를 인증 없이 직접 호출해 편집 헤드라인·많이 본·꼼꼼히 본·최신 기사·섹션별 편집 추천·주제 검색·오늘의 운세를 기사 메타데이터(제목·발행시각·원문 링크) 중심으로 조회한다. |  |
| [ip-ministry-lens](skills/ip-ministry-lens) | 목회·출판·사역·AI도구 개발·복지 강의에 특허청 KIPRIS 데이터를 쓰는 레시피 스킬. 이미 설치된 korean-patent MCP(mcp.gomdori.app/patent, 도구 7종)로 ① 사역·프로그램·책·채널 이름 상표 사전점검 ② 교회 굿 | 상표 있나·이름 써도 되나·책 제목 등록 |
| [joseon-sillok-search](skills/joseon-sillok-search) | Search Joseon Dynasty Annals records from the official sillok.history.go.kr site with keyword search plus optional king/year narrowing. |  |
| [k-dart](skills/k-dart) | 금융감독원 전자공시시스템(DART) OpenAPI로 공시검색, 기업개황, 재무제표, 주요사항보고서를 조회한다. 사용자의 API_K_DART 환경변수를 직접 사용한다. 교회 건축 시공사 실사·교단 기금 점검·기부금 공시처럼 목회 맥락 적용은 dart-m |  |
| [k-schoollunch-menu](skills/k-schoollunch-menu) | Use when the user asks for Korean school meal menus (급식 식단) by natural-language education office and school name, via k-skill-proxy NEIS sch |  |
| [kakao-map](skills/kakao-map) | Kakao Local (장소 검색·주소-좌표 변환) + Kakao Mobility (자동차 길찾기) 를 k-skill-proxy 경유로 조회한다. 사용자 키 불필요. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [korean-cinema-search](skills/korean-cinema-search) | CGV, 메가박스, 롯데시네마 영화관 검색, 상영작, 시간표, 잔여석 조회가 필요할 때 사용한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [korean-heritage-search](skills/korean-heritage-search) | Search official Korean national heritage records, details, locations, and monthly heritage events from the Korea Heritage Service Open API. |  |
| [korean-law-search](skills/korean-law-search) | 한국 법령 조회는 korean-law-mcp를 우선 사용하고, 기본 서비스가 안 될 때 법망(Beopmang)으로 폴백. | OO법 제N조·판례 찾아줘·인용 맞는지 검증 |
| [korean-scholarship-search](skills/korean-scholarship-search) | Search Korean scholarship announcements across official KOSAF, university, foundation, company, and public-sector sources, extract amount an |  |
| [korean-transit-route](skills/korean-transit-route) | Korean door-to-door public transit routing (subway + bus + walking) via ODsay LIVE API with Kakao geocoding for address-to-address queries.  |  |
| [kosis-stats](skills/kosis-stats) | 국가데이터처가 운영하는 KOSIS(국가통계포털, kosis.kr) Open API로 한국 공식 통계표를 검색하고 메타데이터·데이터·대용량 자료를 조회한다. Use when the user asks for 한국 공식 통계 수치 조회, 특히 공공기관·공무 |  |
| [kr-api-catalog](skills/kr-api-catalog) | 한국에서 쓸 수 있는 공개 API·데이터 포털 300+건(yybmion/public-apis-4Kr, 로컬 클론)과 글로벌 API 780+건을 키워드로 검색해 "이 일에는 어떤 API가 있나"를 답한다. 키 없이 즉시 조회. 사용자가 "한국 API 뭐 | 이 일에는 어떤 API가 있나·한국 API 뭐 있어·이런 데이터 주는 API |
| [kr-whois-lookup](skills/kr-whois-lookup) | 공공데이터포털 WHOIS 도메인/IP 정보 API를 k-skill-proxy 경유로 호출해 .kr/.한국 도메인, IP 주소, AS 번호의 공개 등록정보를 조회한다. 조회 전용. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [kstartup-search](skills/kstartup-search) | 공공데이터포털 창업진흥원 K-Startup Open API(15125364)로 통합 공고 사업 정보·지원사업 공고·창업 콘텐츠·통계보고서를 k-skill-proxy 경유로 조회한다. 검색 전용. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [library-book-search](skills/library-book-search) | Use when the user asks to search Korean library books, book details, library holdings, or whether a Korean public library owns a book via k- |  |
| [localdata-business-status](skills/localdata-business-status) | 지방행정 인허가데이터(LOCALDATA)로 동네 사업장(식당·카페·숙박·약국·미용실·학원 등 인허가 업종 208종)의 영업/휴업/폐업 상태, 인허가일자(업력), 폐업일자, 업태, 주소를 조회한다. 상호+시군구로 검색하며 인증키 불필요. |  |
| [mfds-drug-safety](skills/mfds-drug-safety) | 식약처 공공 OpenAPI를 k-skill-proxy 경유로 조회하기 전에 증상·복용상황을 반드시 되묻는 인터뷰형 의약품 안전 체크 스킬. e약은요 의약품개요와 안전상비의약품 정보를 조회한다. 트리거: ''이 약 효능·주의사항'', ''편의점 상비약  |  |
| [mfds-food-safety](skills/mfds-food-safety) | 식약처/식품안전나라 공개 표면을 k-skill-proxy 경유로 조회하기 전에 증상·섭취상황을 반드시 되묻는 인터뷰형 식품 안전 체크 스킬. 건강기능식품 원료 인정·개별인정·품목신고, 검사부적합·부적합 식품, 회수·판매중지 목록을 조회한다. 트리거:  |  |
| [national-assembly-tracker](skills/national-assembly-tracker) | 열린국회정보 Open API와 국회 공식 시스템으로 특정 키워드 관련 법률안·의안 진행상태를 검색하고 제안일, 소관위원회, 처리결과, 대표발의자, 공동발의자, 상세 의안정보 링크, 회의록·입법예고 확인 링크를 정리한다. Use when the user |  |
| [national-pension-workplace](skills/national-pension-workplace) | 국민연금공단 국민연금 가입 사업장 내역을 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 사업장명으로 가입자수·당월 고지금액·월별 취득/상실 추이를 확인해 그 회사의 직원 규모와 변화를 본다. |  |
| [naver-blog-research](skills/naver-blog-research) | Search Naver blogs, read full post content, and download images using only python3 stdlib — no API key required. |  |
| [naver-news-search](skills/naver-news-search) | 네이버 검색 Open API 뉴스 검색(news.json)을 k-skill-proxy 경유로 조회해 최신 뉴스 기사 제목·발행시각·링크·요약을 보수적으로 정리한다. 사용자는 별도 API 키 발급 없이 호출한다. |  |
| [naver-shopping-search](skills/naver-shopping-search) | 네이버 쇼핑 공개 BFF JSON을 k-skill-proxy로 조회해 상품 후보, 최저가, 판매처 링크를 보수적으로 가격비교한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [nhis-care-checkup-search](skills/nhis-care-checkup-search) | 국민건강보험공단 장기요양기관·건강검진기관을 조회하고, 돌쇠에서는 공식 연락·예약 가능 표면까지 이어간다. 장기요양기관과 건강검진기관 후보(주소·전화)를 조회한다. 트리거: ''○○ 장기요양기관 찾아줘'', ''요양원 후보'', ''주말 검진 가능한 검 |  |
| [nts-business-registration](skills/nts-business-registration) | 국세청 사업자등록정보 진위확인 및 사업자등록 상태조회를 공공데이터포털 API(k-skill-proxy 경유)로 수행한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [nts-tax-delinquency](skills/nts-tax-delinquency) | 국세청 고액·상습체납자 명단공개를 nts.go.kr 공개 검색으로 조회한다. 상호·법인명으로 법인 명단과 개인 명단을 대조해 공개된 체납 사실(총 체납액·세목·체납요지 등)을 나열한다. 인증키 불필요. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한 |  |
| [pax](skills/pax) | 공공AX 사례 아카이브(PAX, hollobit.github.io/PAX) 검색·인용. 사용자가 공공부문 AI 도입·AI전환(AX) 사례, 지자체·중앙부처·공공기관·교육청·복지·돌봄·상담 현장의 AI 활용 사례, 공무원이 만든 AI 도구·MCP, AX |  |
| [policy-brief](skills/policy-brief) | 정책 주제 하나를 받아 KOSIS 통계 추세 + 근거 법령 조문 + 인용 검증을 엮은 정책 브리프(마크다운·HWPX)를 만든다. "OO 정책 브리프", "OO 정책 현황 보고서", "OO 통계랑 법적 근거 정리해줘", 사회복지정책론 원고용 정책 요약이 | OO 정책 브리프·OO 정책 현황 보고서·OO 통계랑 법적 근거 정리해줘 |
| [public-data-finder](skills/public-data-finder) | 공공데이터포털(data.go.kr) 목록개방현황 API로 공공기관이 개방한 파일데이터·오픈API·표준데이터를 키워드, 제공기관, 분류체계 기준으로 검색하고 목록유형, API 유형, 갱신주기, 조회수, 목록 URL, 설명을 출처와 함께 정리한다. Use |  |
| [s2b-notice-search](skills/s2b-notice-search) | S2B 학교장터 공개 고객 공고/견적요청 목록을 브라우저 우선으로 조회하고 fixture HTML을 파싱해 공고 메타데이터를 정리한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [stats-ministry-lens](skills/stats-ministry-lens) | 목회·사회복지·강의·지역 브리프에 국가 공식 통계를 끼워 넣는 레시피 스킬. 이미 설치된 korean-stats MCP(KOSIS, mcp.gomdori.app/stats)로 ① 설교 서론·예화용 통계 한 줄+각주 ② 교회 소재지 지역 목회 현황 브리 | 설교에 넣을 통계·출산율 예화·우리 지역 현황 |

### 발표자료·슬라이드 (40)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [airbnb-deck](skills/airbnb-deck) | 원고/자료를 주면 "따뜻한 소비자 마켓플레이스형 발표자료"(HTML 덱)를 자동 생성. 순백 캔버스 + Rausch 산호빛 빨강(#ff385c) 단일 브랜드 전압 + 14px 라운딩 사진 카드 그리드 + 알약형 검색바와 원형 오브 + 부드러운 그림자  | 따뜻한 소비자 마켓플레이스형 발표자료·에어비앤비 스타일·따뜻한 소비자 덱 |
| [apple-deck](skills/apple-deck) | 원고/자료를 주면 "애플 제품 페이지형 발표자료"(HTML 덱)를 자동 생성. 밝은 타일(#fff·#f5f5f7)과 어두운 타일(#272729)을 번갈아 놓아 색 전환 자체를 구분선으로 삼고, 중앙 정렬 초대형 헤드라인(600 웨이트·음수 자간)에 액 | 애플 제품 페이지형 발표자료·애플 스타일·제품 발표 페이지 |
| [biz-infographic-deck](skills/biz-infographic-deck) | 원고를 주면 네이비·플럼·레드·앰버 팔레트의 비즈니스 인포그래픽 PPTX를 생성. SMART 스텝 체인, 불스아이 타깃, 허브 다이어그램, 피라미드, 통계 카드, 간트 액션플랜, 2×2 매트릭스, 컬러 테이블, 다크 섹션 디바이더가 특징. 사용자가 " | 인포그래픽 덱·마케팅 플랜 PPT·비즈니스 다이어그램 발표자료 |
| [blueprint-deck](skills/blueprint-deck) | 원고/자료를 주면 "모눈종이 블루프린트 인포그래픽 발표자료"(HTML 덱)를 자동 생성. 옅은 회백 종이(#F6F6F3) + 청회색 모눈 격자 + 도면 프레임과 치수선 + 디자인툴 선택 핸들 + 흰 카드·표·배지 + 테라코타/슬레이트/세이지 3악센트  | 모눈종이 블루프린트 인포그래픽 발표자료·블루프린트 발표자료·모눈종이 슬라이드 |
| [bmw-m-deck](skills/bmw-m-deck) | 원고/자료를 주면 "BMW M 모터스포츠 발표자료"(HTML 덱)를 자동 생성. 순검정(#000) 배경 + 풀블리드 자동차/제품 사진 + 대문자 초굵은(700) 헤드라인 + 초가는(300) 본문의 극단 대비 + M 트라이컬러 4px 스트라이프 + 라운 | BMW M 모터스포츠 발표자료·BMW M 스타일·모터스포츠 발표자료 |
| [boneun-deck](skills/boneun-deck) | 원고/자료를 주면 "읽지 않고 보는 PPT"(오빠두엑셀×윤춘근 직장인 PPT 디자인 강의의 원칙 전체)를 적용한 발표자료(HTML 덱→PPTX)를 자동 생성. 특정 비주얼 스타일 재현이 아니라 제작 원칙 스킬 — 문단→문장→키워드 압축, 폰트 한 가족 | 읽지 않고 보는 PPT·직장인 PPT·실무 PPT |
| [claude-ppt](skills/claude-ppt) | > Anthropic(클로드) 톤앤매너의 투자제안서·실적발표(IR) 파워포인트 슬라이드를 만드는 스킬. 베이지 배경 + 테라코타 메인 + 카드 레이아웃 + 거버닝 메시지 + 직각 차트의 5+2 타입 모듈을 제공하고, "데이터 정교화 → 레퍼런스 등록  | 의 4단계 워크플로로 진행한다. 사용자가·, |
| [darkdoc-deck](skills/darkdoc-deck) | 원고/자료를 주면 "다크 시네마틱 다큐멘터리 발표자료"(HTML 덱)를 자동 생성. 근사흑(#0D0E13) 배경 + 어둡게 깐 풀블리드 영상/사진 + 좌측 정보블록(악센트 점 키커·2줄 볼드 헤드라인·회색 보조문장) + 씬당 단일 악센트색(호박/블루/ | 다크 시네마틱 다큐멘터리 발표자료·다크 발표자료·시네마틱 덱 |
| [dell96-deck](skills/dell96-deck) | 원고/자료를 주면 "1996년 카탈로그 웹 발표자료"(HTML 덱)를 자동 생성. 순백 종이 + 8px 검정 액자 프레임 + 여덟 가지 카탈로그 색(세이지·살몬·피치·라임·스카이·스틸·페리윙클·올리브) 리본카드 + Arial Black 900 대문자  | 1996년 카탈로그 웹 발표자료·Dell 1996·90년대 웹 스타일 |
| [doodle-deck](skills/doodle-deck) | 원고/자료를 주면 "화이트보드 손그림 애니메이션 발표자료"(HTML 덱)를 자동 생성. 미색 종이 배경(#F5F3EF) + 소프트블랙 마커 선이 연필 쥔 손을 따라 그려지는 효과 + 파스텔 6색 채색 + 손글씨 글꼴(Gaegu) + 하단 알약형 자막에 | 화이트보드 손그림 애니메이션 발표자료·손그림 발표자료·화이트보드 애니메이션 |
| [editorial-mono-deck](skills/editorial-mono-deck) | 원고를 주면 흑백 편집 매거진(에디토리얼) 스타일 PPTX를 생성. 웜 오프화이트 종이+잉크 블랙, 초대형 헤비 대문자 타이틀, 그레이스케일 사진, 넘버 서클·헤어라인 룰·메타 행이 특징. 사용자가 "에디토리얼 덱", "흑백 매거진 PPT", "잡지  | 에디토리얼 덱·흑백 매거진 PPT·잡지 스타일 발표자료 |
| [figma-deck](skills/figma-deck) | 원고/자료를 주면 "흑백 에디토리얼 + 파스텔 컬러블록 발표자료"(HTML 덱)를 자동 생성. 순백·순흑의 엄격한 무채색 프레임에 라임·라일락·크림·민트·핑크·코랄·네이비 대형 색면(둥근 24px 블록)을 섹션마다 하나씩 끼워 넣고, 모든 CTA는 p | 흑백 에디토리얼 + 파스텔 컬러블록 발표자료·피그마 스타일·컬러블록 덱 |
| [genie-deck](skills/genie-deck) | 원고/자료를 주면 "딥퍼플 머티리얼 컨설팅 슬라이드"(HTML 덱)를 자동 생성. 옅은 회색 캔버스(#F2F5F7) + 흰 라운드 카드 + 딥퍼플(#562EA1) 단일 악센트 + 상단 파트 브레드크럼 + 헤드라인·거버닝 메시지 컨설팅 문법 + 카드 호 | 딥퍼플 머티리얼 컨설팅 슬라이드·제미나이 바이브 코딩 프레젠테이션·딥퍼플 발표자료 |
| [ibm-deck](skills/ibm-deck) | 원고/자료를 주면 "기업 그리드형 발표자료"(HTML 덱)를 자동 생성. IBM Carbon 디자인 시스템 재현 — 순백 캔버스 + 차콜(#161616) 타입 + IBM 블루(#0f62fe) 단일 악센트 + 모든 모서리 0px 각진 형태 + 16컬럼  | 기업 그리드형 발표자료·IBM 스타일·Carbon 디자인 |
| [kbg-발표자료](skills/kbg-발표자료) | kbg 발표자료 선택 라우터. 유튜브 혼잡스(@honjobs) 채널 발표 영상의 화면 문법을 실측해 만든 5가지 HTML 모션 발표자료(1 클린 도식, 2 라인아트 내레이션, 3 손글씨 한 장 지도, 4 데스크톱 창 타임라인, 5 보드게임 로드맵) 가 | kbg 발표자료·kbg-발표자료·/kbg-발표자료 |
| [kbg-발표자료(1)](skills/kbg-발표자료(1)) | kbg-발표자료(1). 코드팩토리 영상 「Laya 진짜 추천합니다」(youtu.be/ZktfWXfOwIY)의 발표 화면 스타일을 추출한 HTML 모션 덱. 오프화이트 캔버스(#F3F1E9) 위에 앱 아이콘형 다크/라이트 타일 노드, 헤어라인 연결선과  | Laya 진짜 추천합니다·kbg-발표자료(1)·kbg 발표자료(1) |
| [kbg-발표자료(영상)](skills/kbg-발표자료(영상)) | kbg-발표자료(영상). 바이브랩스 영상 「녹음/녹화/편집/모션 그래픽까지 클로드 코드에게 완전히 맡겨봤습니다」(youtu.be/C-rzmH3571c)의 영상 제작 방식과 화면 스타일을 추출한 발표 영상 스킬. 크림 캔버스(#F2EEE7)·네이비 터미 | 녹음/녹화/편집/모션 그래픽까지 클로드 코드에게 완전히 맡겨봤습니다·kbg-발표자료(영상)·kbg 발표 영상 |
| [kbg-발표자료-1](skills/kbg-발표자료-1) | kbg 발표자료 1 — 클린 도식형. 혼잡스(@honjobs) 개념 설명 영상의 화면 문법을 실측한 HTML 모션 덱. 순백 바탕, 검정 굵은 고딕(Pretendard 800), 검은 2.5px 테두리의 둥근 박스 도식과 화살표, 빨강·파랑 단일 강조 | kbg 발표자료 1·kbg-발표자료-1·/kbg-발표자료-1 |
| [kbg-발표자료-2](skills/kbg-발표자료-2) | kbg 발표자료 2 — 라인아트 내레이션형. 혼잡스(@honjobs) 이야기형 영상의 화면 문법을 실측한 HTML 모션 덱. 흰 바탕에 거친 손그림 선의 인물(흰 셔츠·검은 넥타이 내레이터)·로봇·노트북·책 라인아트, 화면 위쪽 큰 자막(52px)과  | kbg 발표자료 2·kbg-발표자료-2·/kbg-발표자료-2 |
| [kbg-발표자료-3](skills/kbg-발표자료-3) | kbg 발표자료 3 — 손글씨 한 장 지도형. 혼잡스(@honjobs) 요약 영상의 화면 문법을 실측한 HTML 모션 덱. 3600×2100 큰 종이 한 장에 손글씨(나눔펜·Gaegu) 제목과 구역을 배치하고 카메라가 구역마다 팬·줌하다 마지막에 전체 | kbg 발표자료 3·kbg-발표자료-3·/kbg-발표자료-3 |
| [kbg-발표자료-4](skills/kbg-발표자료-4) | kbg 발표자료 4 — 데스크톱 창 타임라인형. 혼잡스(@honjobs) 회고·작업 과정 영상의 화면 문법을 실측한 HTML 모션 덱. 모눈종이 바탕, 왼쪽 앱 독(모션그래픽·음악·Ai·Notion), 오른쪽 1~12월 레일이 장면마다 켜지고, 맥 창 | kbg 발표자료 4·kbg-발표자료-4·/kbg-발표자료-4 |
| [kbg-발표자료-5](skills/kbg-발표자료-5) | kbg 발표자료 5 — 보드게임 로드맵형. 혼잡스(@honjobs) 로드맵 영상의 화면 문법을 실측한 HTML 모션 덱. 크레용 질감 굵은 제목(Black Han Sans + 줄무늬 채움 + 7px 외곽선), 구불구불한 검정 트랙 위 색 구간·빗금·흰 | kbg 발표자료 5·kbg-발표자료-5·/kbg-발표자료-5 |
| [linear-deck](skills/linear-deck) | 원고/자료를 주면 "딥다크 SaaS 제품 발표자료"(HTML 덱)를 자동 생성. 푸른 기가 도는 근사흑 캔버스(#010102) + surface 4단 사다리(#0f1011→#191a1b) + 라벤더블루(#5e6ad2) 악센트 하나 + 초대형 헤드라인의 | 딥다크 SaaS 제품 발표자료·다크 SaaS 덱·개발자 제품 발표 |
| [monoline-deck](skills/monoline-deck) | 원고/자료를 주면 "흑백 라인아트 모션 발표자료"(HTML 덱)를 자동 생성. 순백 배경+잉크블랙, 프리텐다드 부분볼드 자막형 제목, 좌측 세로 스테퍼, 라인아트·목업·오프셋 그림자 박스, 순차 등장 모션. 영·한 토글(N키 한국어 패널) 변형, 강의 | 흑백 라인아트 모션 발표자료·흑백 발표자료·모노라인 덱 |
| [my-ppt](skills/my-ppt) | > 사용자 개인 브랜딩 규칙(Pretendard 폰트, 자기 로고, 16:9, 고정 레이아웃, 밀도 있는 본문, 영어 디자인 프롬프트)을 적용하는 PPT/슬라이드 제작 스킬. 사용자가 "/my-ppt", "내 스타일로", "내 브랜딩으로", "김병곤  | /my-ppt·내 스타일로·내 브랜딩으로 |
| [native-enhance-pptx](skills/native-enhance-pptx) | > Enhance a finished PPTX while keeping visible content and layout stable. Use for adding or replacing speaker notes, narration audio, auto- |  |
| [nike-deck](skills/nike-deck) | 원고/자료를 주면 "스포츠 캠페인형 발표자료"(HTML 덱)를 자동 생성. 풀블리드 편집 사진 위에 96px 대문자 푸투라 락업(행간 0.9)을 태우고, 그 아래는 검정 pill CTA와 회색 칩·여백 0 라운딩 0 제품 카드로 이루어진 중성 크롬이  | 스포츠 캠페인형 발표자료·나이키 스타일·캠페인 덱 |
| [nintendo01-deck](skills/nintendo01-deck) | 원고/자료를 주면 "Y2K 콘솔 하드웨어형 발표자료"(HTML 덱)를 자동 생성. 2001년 Nintendo.com 재현 — 브러시드 페리윙클 금속판(#7a8aba)을 베벨(위쪽 밝은 모서리 + 크롬인디고 그림자선)로 쌓아 올리고, 카본 상단바 + 페 | Y2K 콘솔 하드웨어형 발표자료·닌텐도 2001·Y2K 스타일 |
| [notion-deck](skills/notion-deck) | 원고/자료를 주면 "일러스트 친화형 워크스페이스 발표자료"(HTML 덱)를 자동 생성. 딥네이비(#0a1530) 히어로 밴드에 브랜드색 스티키 도트를 흩뿌리고, 흰 캔버스 위에 아홉 가지 파스텔 틴트 카드(피치·로즈·민트·라벤더·스카이·옐로)를 아낌없 | 일러스트 친화형 워크스페이스 발표자료·노션 스타일·파스텔 카드 덱 |
| [ppt-maestro](skills/ppt-maestro) | 회사·개인 서식 기반 PPT 총괄 스킬. (1) 샘플 PDF/PPTX/이미지에서 브랜드 스펙을 추출해 일관된 PPTX를 대량 생성, (2) 기존 PPTX 템플릿의 레이아웃을 유지한 채 내용만 교체(오토필), (3) 완성된 PPTX의 수정·리페어(오탈자 | 회사 양식으로 PPT·우리 폼에 맞게·템플릿 채워줘/오토필 |
| [ppt-master](skills/ppt-master) | > Post-router owner for authoring or regenerating presentation visuals through the PPT Master SVG pipeline: new decks from source material o |  |
| [ppt-master-v6](skills/ppt-master-v6) | > AI-driven presentation workflow for generating editable PPTX decks and slides, reconstructing page visuals, creating reusable Brand/Style/ |  |
| [ppt-template-fill](skills/ppt-template-fill) | Fill a raw PowerPoint (.pptx) template with new content by cloning and patching native slides — no SVG conversion, original design preserved | template·use this PPT template to generate a PPTX·fill this deck with the new content |
| [pptx-posters](skills/pptx-posters) | Creates and audits editable scientific posters in macro-free PowerPoint (.pptx) from author-approved local content and assets. Used when the |  |
| [sketch-deck](skills/sketch-deck) | Use when the user wants a "미색 종이 + 손그림 캐릭터 + 파랑 한 색 + 하단 대형 자막" explainer deck — 감자나라ai류 유튜브 설명영상(qNQ6fGB-cWA)처럼 내레이션 한 문장마다 화면 아래 자막이 바뀌고 손 | 미색 종이 + 손그림 캐릭터 + 파랑 한 색 + 하단 대형 자막·스케치 덱·손그림 캐릭터 발표 |
| [spotify-deck](skills/spotify-deck) | 원고/자료를 주면 "다크 몰입형 플레이어 발표자료"(HTML 덱)를 자동 생성. 근사흑 3단(#121212·#181818·#1f1f1f) 위에 아트 타일이 유일한 색을 담당하고, 스포티파이 그린(#1ed760)은 재생·활성·주 CTA에만 쓰는 기능색으 | 다크 몰입형 플레이어 발표자료·스포티파이 스타일·다크 몰입형 덱 |
| [starbucks-deck](skills/starbucks-deck) | 원고/자료를 주면 "따뜻한 리테일 플래그십형 발표자료"(HTML 덱)를 자동 생성. 크림 캔버스(#f2f0eb·#edebe9, 순백 아님) 위에 역할이 다른 네 가지 초록(#006241 제목 · #00754A CTA · #1E3932 밴드 · #2b5 | 따뜻한 리테일 플래그십형 발표자료·스타벅스 스타일·따뜻한 크림 덱 |
| [stepwire-deck](skills/stepwire-deck) | 원고/자료를 주면 "스텝 파이프라인 해설 발표자료"(HTML 덱)를 자동 생성. 청흑(#061017) 배경 + 상단 ①—②—③ 스텝퍼·하단 진행 점의 단계 크롬 + 재료→도구→산출 3덩어리 흐름 + 데이터 구조 다이어그램(표 크로스헤어·타일 그리드·검 | 스텝 파이프라인 해설 발표자료·스텝 발표자료·파이프라인 덱 |
| [stripe-deck](skills/stripe-deck) | 원고/자료를 주면 "밝은 핀테크 제품 발표자료"(HTML 덱)를 자동 생성. 순백 캔버스 상단 1/3에 크림·셔벗오렌지·라벤더·인디고·루비핑크 그라디언트 메시를 깔고, 그 위에 weight 300 초박 디스플레이(음수 자간 -1.4px)와 인디고(#5 | 밝은 핀테크 제품 발표자료·스트라이프 스타일·그라디언트 메시 |
| [wired-deck](skills/wired-deck) | 원고/자료를 주면 "테크 매거진 에디토리얼 발표자료"(HTML 덱)를 자동 생성. WIRED 지면 재현 — 흰 지면 + 순검정 잉크 + 고대비 좁은 세리프 디스플레이(항상 weight 400) + 세리프 본문 + 산세리프 내비/버튼의 3서체 체계, 모 | 테크 매거진 에디토리얼 발표자료·와이어드 스타일·매거진 발표자료 |

### 미래학 방법론 (37)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [vision-foresight-environmental-scanning](skills/vision-foresight-environmental-scanning) | ## TLDR — Theodore J. Gordon·Jerome C. Glenn (Millennium Project, *Futures Research Methodology V3.0* 02장) Environmental Scanning 풀 구현 **대표  |  |
| [vision-foresight-environmental-scanning-issues-management](skills/vision-foresight-environmental-scanning-issues-management) | ## TLDR — Renfro (1993) Issues Management 4단계 cycle 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: true |  |
| [vision-foresight-environmental-scanning-quest-workshop](skills/vision-foresight-environmental-scanning-quest-workshop) | ## TLDR — Burt Nanus·Slaughter (1990) QUEST 4-phase 워크숍 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation:  |  |
| [vision-foresight-environmental-scanning-report](skills/vision-foresight-environmental-scanning-report) | ## TLDR — Gordon·Glenn (2009) Appendix B 양식 (Millennium Project Environmental Security 월간 보고서) 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 |  |
| [vision-foresight-environmental-scanning-techniques](skills/vision-foresight-environmental-scanning-techniques) | ## TLDR — Gordon·Glenn (2009) Section III의 6 정보 수집 기법 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: tr |  |
| [vision-foresight-environmental-scanning-weak-signal-template](skills/vision-foresight-environmental-scanning-weak-signal-template) | ## TLDR — Gordon·Glenn (2009) 02장의 10·13-field 템플릿 + weak signal 패턴 추출 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-mod |  |
| [vision-foresight-futures-wheel](skills/vision-foresight-futures-wheel) | ／ ## TLDR — Jerome C. Glenn (Millennium Project, *Futures Research Methodology V3.0* 06장) The Futures Wheel 풀 구현 **대표 스킬**. 1971년 Glenn(Anti | 단행본·강의 자료·간단히/빠르게 |
| [vision-foresight-futures-wheel-basic-v1](skills/vision-foresight-futures-wheel-basic-v1) | ／ ## TLDR — Jerome C. Glenn (2009 [1971], V3.0 06장 §III.A) Basic Futures Wheel V1 sub-skill + 박사님 2026-05-11 6차 강화. **vision-foresight-futur |  |
| [vision-foresight-futures-wheel-categorical-binary-expansion](skills/vision-foresight-futures-wheel-categorical-binary-expansion) | ／ ## TLDR — Futures Wheel **SCBE (STEEPS Categorical Binary Expansion) 노드 생성기** sub-skill. 박사님 2026-05-11 두 번째 강화 명령 구현. **vision-foresight- | 단행본·강의 자료 |
| [vision-foresight-futures-wheel-consequence-linker](skills/vision-foresight-futures-wheel-consequence-linker) | ／ ## TLDR — Jerome C. Glenn (V3.0 06장 §III.B) Consequence Linker sub-skill + 박사님 2026-05-11 6차 강화. **vision-foresight-futures-wheel** 마스터 전용 | more control·less control |
| [vision-foresight-futures-wheel-deep-reasoning-engine](skills/vision-foresight-futures-wheel-deep-reasoning-engine) | ／ ## TLDR — Futures Wheel **추론 검증·강화 엔진** sub-skill. `vision-foresight-futures-wheel` 마스터 전용. 박사님 2026-05-11 강화 명령 3 요구사항 통합 구현: ① 6차 이상 깊이  | 간단히/빠르게 |
| [vision-foresight-futures-wheel-delphi-rounds](skills/vision-foresight-futures-wheel-delphi-rounds) | Glenn의 '인터넷 델파이 퓨처스 휠' 변형 구현 — 국제 패널이 비동기로 모여 5라운드 델파이로 퓨처스 휠을 체계적으로 구축. 빈도 가중 타원 크기, 위키 협업 지원. 마스터 스킬 전용 내부 하위 스킬. | Frontiers... Delphi via the Internet |
| [vision-foresight-futures-wheel-domain-v2](skills/vision-foresight-futures-wheel-domain-v2) | Glenn 'Version 2' 구현 — 원래 퓨처스 휠이 놓치기 쉬운 영향 범위를, 사전에 정한 도메인 세트별로 강제 검토하게 하는 변형. 마스터 전용 내부 하위 스킬. | Version 2 |
| [vision-foresight-futures-wheel-quality-control](skills/vision-foresight-futures-wheel-quality-control) | ／ ## TLDR — Jerome C. Glenn (V3.0 06장 §IV + §III.A + endnote 4) Quality Control sub-skill + 박사님 2026-05-11 강화 명령 3종 강제. **vision-foresight-f |  |
| [vision-foresight-futures-wheel-scenario-forecast](skills/vision-foresight-futures-wheel-scenario-forecast) | Glenn '대안 시나리오 내 예측 생성' 구현 — 시나리오 하나와 그 안의 항목을 골라 퓨처스 휠로 파급 영향을 전개해 시나리오 내부 예측을 만든다. 마스터 전용 내부 하위 스킬. | conscious technology |
| [vision-foresight-futures-wheel-temporal-v3](skills/vision-foresight-futures-wheel-temporal-v3) | Glenn 'Version 3' 구현 — 역사적 동인(과거)·현재 상관·미래 함의를 원뿔(cone) 형태 3차원으로 쌓는 시간축 확장 퓨처스 휠. 마스터 전용 내부 하위 스킬. | Version 3 |
| [vision-foresight-scenarios](skills/vision-foresight-scenarios) | ／ ## TLDR — Jerome C. Glenn and The Futures Group International (Millennium Project, *Futures Research Methodology V3.0* 19장) Scenarios 풀 구현 | Scenario·Futures Matrix·Good |
| [vision-foresight-scenarios-cone-of-plausibility](skills/vision-foresight-scenarios-cone-of-plausibility) | Charles W. Taylor(미 육군전쟁대학)의 'Cone of Plausibility(개연성 원뿔)' 모델러 — 시나리오 대표 스킬의 9번째 내부 하위 스킬. | Cone of Plausibility |
| [vision-foresight-scenarios-driving-forces-identification](skills/vision-foresight-scenarios-driving-forces-identification) | Schwartz 2단계 '환경의 핵심 동인·트렌드 식별' + TFG 시나리오 공간 정의 구현 — 시나리오의 빌딩블록인 추동력(driving forces)을 도출한다. 내부 하위 스킬. | * + Schwartz *·*. TFG: *·* Mandel & Wilson SRI verbatim: * |
| [vision-foresight-scenarios-focal-issue-definition](skills/vision-foresight-scenarios-focal-issue-definition) | Schwartz 1단계 '초점 이슈/결정 식별' + Bishop 워크숍 양식 구현 — '향후 [도메인]에서 가장 중요한 이슈는 무엇인가'를 확정한다. 시나리오의 1번째 내부 하위 스킬. | identify the focal issue or decision·*. Section III Key Points 강제 verbatim: *·* + * |
| [vision-foresight-scenarios-implications-synthesis](skills/vision-foresight-scenarios-implications-synthesis) | ／ ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 12번째 sub-skill (최종 종합 단계). Glenn & TFG, *Futures Research Methodology — V | Assess the implications |
| [vision-foresight-scenarios-importance-uncertainty-ranking](skills/vision-foresight-scenarios-importance-uncertainty-ranking) | Schwartz 3단계 '중요도×불확실성 순위' 구현 — 추동력·트렌드를 2×2 매트릭스로 평가해 시나리오 축 후보를 고른다. 내부 하위 스킬. |  |
| [vision-foresight-scenarios-internal-consistency-check](skills/vision-foresight-scenarios-internal-consistency-check) | '좋은 시나리오' 3기준(개연성·내적 일관성·의사결정 관련성) 검사기 — 시나리오 세트의 인과 경로와 논리 모순을 점검한다. 내부 하위 스킬. | Good scenarios |
| [vision-foresight-scenarios-key-measures-events](skills/vision-foresight-scenarios-key-measures-events) | TFG 개발 2단계 '핵심 지표 정의' 구현 — 각 시나리오 내 경제성장·입법 환경·기술 등 핵심 측정치와 사건을 설계한다. 내부 하위 스킬. | * + * |
| [vision-foresight-scenarios-leading-indicators](skills/vision-foresight-scenarios-leading-indicators) | Schwartz 7단계 '선행 지표와 이정표 선정' 구현 — 현실이 어느 시나리오로 향하는지 조기 감지할 모니터링 지표를 고른다. 내부 하위 스킬. | * Z_Punkt Section V verbatim: * |
| [vision-foresight-scenarios-narrative-writing](skills/vision-foresight-scenarios-narrative-writing) | Schwartz 5단계 '시나리오 채우기' 구현 — 현재와 미래 상태를 개연성 있는 인과로 잇는 시나리오 내러티브를 집필한다. 내부 하위 스킬. | fill out the scenarios·* + *·*. TFG Development verbatim: * |
| [vision-foresight-scenarios-policy-testing](skills/vision-foresight-scenarios-policy-testing) | TFG '정책 테스트' 구현 — 시나리오 범위 전체에 정책을 대입해 강건(robust) 요소와 조건부(contingent) 요소로 이분한다. 내부 하위 스킬. | Testing policies·* Section II 8 활용 verbatim 중: *·defined as precisely as possible |
| [vision-foresight-scenarios-projection-engine](skills/vision-foresight-scenarios-projection-engine) | TFG '핵심 지표 투영' 구현 — 트렌드 영향 분석(TIA)으로 각 시나리오의 핵심 지표를 수치로 투영한다. 내부 하위 스킬. | Project the key measures·* Section V: * |
| [vision-foresight-scenarios-scenario-logics-selection](skills/vision-foresight-scenarios-scenario-logics-selection) | Schwartz 4단계 '시나리오 로직 선택' 구현 — 2×2 사분면(MITRE 사례)·다차원 조합으로 시나리오 골격 이론을 세운다. 내부 하위 스킬. | select the scenario logics·*. PDF Section III recommendation: * |
| [vision-foresight-wild-cards](skills/vision-foresight-wild-cards) | Petersen & Steinmüller의 Wild Cards(미래연구방법론 V3.0 10장) 풀 구현 대표 스킬 — '발생 확률은 낮지만 영향은 극대'인 뜻밖의 사건을 식별·평가·모니터링·대응하는 방법론. Shell의 'rapids'(1970s) 기 | rapids·futurequakes |
| [vision-foresight-wild-cards-assessment](skills/vision-foresight-wild-cards-assessment) | '내 조직에 가장 중요한 와일드카드는?' 평가 단계 — Petersen 4요인 피라미드(존재·생존·행동·도구, 파워팩터 1~4)로 우선순위를 매긴다. 내부 하위 스킬. | relative process · biases consistent·close to home·). Pyramid 원리 PDF verbatim: |
| [vision-foresight-wild-cards-identification](skills/vision-foresight-wild-cards-identification) | '원리상 어떤 와일드카드가 발생할 수 있나' 식별 단계 — 브레인스토밍, AI 전문가 패널 인터뷰, 설문, 역사적 유추(1918 독감·닷컴버블·9/11·SARS·2008 금융위기) 등 5기법 오케스트레이션. 내부 하위 스킬. | 78-catalogue |
| [vision-foresight-wild-cards-impact-index](skills/vision-foresight-wild-cards-impact-index) | Arlington Impact Index 공식(ΔC+R+V+O+T+Op+P=I_AI) 구현 — 변화 속도·파급 범위·취약성·결과 불확실성·시점 등 7요인으로 와일드카드 영향 지수를 산출한다. 내부 하위 스킬. | faster change = more impact·wider reach = more impact·less adaptable = more vulnerable |
| [vision-foresight-wild-cards-implications-synthesis](skills/vision-foresight-wild-cards-implications-synthesis) | 최종 통합 단계 — 앞 단계 산출물을 종합해 '비범한 함의'와 강점·약점·프런티어까지 정리한 와일드카드 종합 보고를 만든다. 내부 하위 스킬. | Extraordinary Implications·Possible Implications·p.19 양식 |
| [vision-foresight-wild-cards-monitoring](skills/vision-foresight-wild-cards-monitoring) | '도래를 미리 감지할 수 있나' 모니터링 단계 — 레이더에 잡힌 와일드카드의 전조 사건(precursor)을 추적하는 감시 체계를 설계한다. 내부 하위 스킬. | 9-step institutional process |
| [vision-foresight-wild-cards-options-action](skills/vision-foresight-wild-cards-options-action) | '우리가 할 수 있는 일은 무엇인가' 대응 옵션 단계 — 시스템 사고·창의성 훈련·직관 등 비선형 사고 기법으로 비관습적 대응책을 설계한다. 내부 하위 스킬. | Three basic rules·) ② 3 Basic Rules 적용 (Rule I··Rule II |
| [vision-foresight-wild-cards-scenario-integration](skills/vision-foresight-wild-cards-scenario-integration) | 시나리오 구축과의 결합 단계 — Steinmüller의 6가지 선별 규칙을 자동 적용해 와일드카드를 시나리오에 통합한다. 내부 하위 스킬. | Use with Other Methods·barely possible·② |

### AI·에이전트·LLM (35)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agency-agents](skills/agency-agents) | 전문가 페르소나 283명(18개 분야: 개발·마케팅·디자인·보안·테스트·영업·제품·재무·학술·GIS·게임 등, msitarzewski/agency-agents, MIT) 카탈로그에서 맞는 전문가를 골라 그 역할 문서대로 일하거나 서브에이전트에 입힌다. |  |
| [agent-gap-router](skills/agent-gap-router) | 에이전트 작업의 네 빈틈(시키기·만들기·보고받기·확인하기)마다 이미 설치된 스킬을 골라 붙이는 라우터. 외부 5종(Ouroboros·img2threejs·UI Skills·Chisle·Reticle)의 핵심 장치만 빌려 와 설치 없이 쓴다. "빈틈 라 | 빈틈 라우터·다섯 스킬 흐름·시키기부터 확인까지 |
| [agent-leadership](skills/agent-leadership) | ／ ## TLDR — 비즈니스 리더가 "AI를 쓰는 사람"에서 "에이전트 조직을 경영하는 사람"으로 넘어가게 하는 방법론 스킬. 강정구(라이너 AI전략 총괄) 인터뷰(티타임즈TV, 2026-08-12) 기반. 핵심 4장치: (1) AX 3축 지도 —  | AI를 쓰는 사람·에이전트 조직을 경영하는 사람·개인의 증강 → 조직의 증폭(암묵지 증류) |
| [agents-md](skills/agents-md) | AGENTS.md 거버넌스 시스템을 분석·생성하는 마스터 프롬프트. 현재 프로젝트를 분석하여 루트 AGENTS.md와 하위 AGENTS.md를 즉시 생성하고, CLAUDE.md에 @AGENTS.md 링크를 추가한다. "AGENTS.md 만들어줘", " | AGENTS.md 만들어줘·에이전트 규칙 만들어줘·/agents-md |
| [aios-map](skills/aios-map) | 나를 아는 AI를 만드는 맥락 지도(MAP)를 점검·보강하고, 작업마다 '관련된 맥락만' 골라 컨텍스트 팩으로 묶어 준다. Meaning(나는 누구인가)·Asset(내 지식)은 PKM 볼트의 기존 문서를 재사용하고, 비어 있는 Action(AI가 쓸  |  |
| [autoresearch-loop](skills/autoresearch-loop) | Karpathy의 autoresearch를 일반화한 도메인 불문 지표 기반 개선 루프. 프로젝트/목표에 대해 무엇을 측정할지 스스로 발견한 뒤, 변경 제안→측정→개선은 유지·퇴보는 되돌리는 keep-or-revert 실험 루프를 돌리고 구현된 개선을  |  |
| [book-to-skill](skills/book-to-skill) | 책·문서(PDF, EPUB, DOCX, HTML, Markdown, 텍스트, RTF, Calibre 경유 MOBI/AZW)를 구조화된 에이전트 스킬로 변환 — 프레임워크·멘탈모델·원칙·기법·안티패턴을 추출한다. 문서를 스킬로 학습시키거나 저자의 프레임 |  |
| [compact-timing](skills/compact-timing) | 긴 세션에서 /clear, /compact, 새 세션 중 무엇을 언제 쓸지 정하고, /compact에 붙일 보존 지시문을 작업 유형별로 만들어 준다. "압축해도 돼?", "컨텍스트 정리", "세션 너무 길어", "컴팩트 타이밍", "여기서 끊을까" 요 | 압축해도 돼?·컨텍스트 정리·세션 너무 길어 |
| [config-gc](skills/config-gc) | Claude Code 설정 가비지 컬렉션. ~/.claude(스킬·메모리·훅·권한·MCP 서버·캐시)를 주기적으로 스캔해 중복·낡음·고아·저가치 항목을 찾고, 건별 확인을 거치는 정리 절차를 안내한다. "설정 정리해줘", "스킬이 너무 많아", "내  | clean up my config·config GC·too many skills |
| [context-budget](skills/context-budget) | Claude Code 컨텍스트 윈도우 소비를 에이전트·스킬·MCP 서버·규칙 단위로 감사. 비대한 항목과 중복 구성요소를 식별하고 우선순위화된 토큰 절약 권고안을 산출한다. |  |
| [dots-delegate](skills/dots-delegate) | 에이전트(OpenAI Dots, 클로드 코드, 서브에이전트 등)에게 일을 맡기기 전 위임 브리프(결과·조건·완료 증거·사람 결정·보고·실패 시)를 만들고, 결과를 받은 뒤 '준비됨/완료'를 증거로 판정한다. 생활 에이전트(피클·Muse 등)에게 어디까 |  |
| [gemini-skill-export](skills/gemini-skill-export) | 설치된 Claude 스킬(~/.claude/skills/<이름>)을 제미나이 앱 '스킬'(설정 > 스킬 > 업로드)에 올릴 수 있는 .zip으로 변환하고 규격을 점검한다. name 소문자-하이픈, description 1024자, 100MB, 미지원  | 제미나이 스킬로 옮겨·Gemini 스킬 업로드용으로·스킬을 폰에서도 쓰게 |
| [harness-evolve](skills/harness-evolve) | 하네스 진화 스킬. 사용 중인 하네스의 실행 결과에 대한 피드백을 수집·일반화하여 에이전트/스킬/오케스트레이터에 반영하고, 초기 구성 대비 델타를 포착해 변경 이력을 갱신한다. '하네스 회고', '하네스 진화', '하네스 피드백 반영', '하네스 개선 |  |
| [jev-judge](skills/jev-judge) | 클라우드 Jev(TypeSafe System One)로 많은 텍스트를 닫힌 선택지(choice·score·noul)로 빠르고 싸게 일괄 판정하고, 신뢰도 게이트로 애매한 건만 사람/Claude 검토로 넘긴다. "Jev 써서", "jev로 판정", "전 | Jev 써서·jev로 판정·전수 점검 |
| [k-skill-cleaner](skills/k-skill-cleaner) | Interview the user and inspect coding-agent skill trigger counts to recommend unused K-skills for removal. |  |
| [k-skill-setup](skills/k-skill-setup) | Install the k-skill bundle, use the unified CLI, resolve credentials, verify the runtime, and optionally configure update checks and GitHub  |  |
| [kkirikkiri](skills/kkirikkiri) | 자연어 한마디로 AI 에이전트 팀을 자동 구성하고 실행합니다. 리서치, 개발, 분석, 콘텐츠 — 목적에 맞는 팀을 만들어보세요. 흐름: 의도 파악→인터뷰→팀 생성→실행. 트리거: '끼리끼리', '/kkirikkiri', '에이전트 팀 만들어줘', '팀 |  |
| [laya-decide](skills/laya-decide) | 로컬 무료 의사결정 모델 Laya(Jev 오픈소스 대안)로 텍스트를 빠르게 분류·라우팅·점수화한다. 메일/문서/메모/댓글 대량 분류, 폴더·태그 자동 배정, 트리아지, 프롬프트 가드, "Jev", "Laya", "빠른 분류", "라우팅", "syste | Jev·Laya·빠른 분류 |
| [own-the-output](skills/own-the-output) | AI 결과물을 '내 것'으로 만드는 7단계 점검(Jay Choi 「AI 결과물 100배 좋아지는 7가지」·Addy Osmani 인지적 항복·이해 부채 정리). 맡기기 전 내 예상 적기·누구/금지/끝 정하기, 진행 중 실행 증거 먼저 보기, 끝난 뒤 " | AI 결과물 100배 좋아지는 7가지·네가 대신 정한 것·가정한 것·내가 놓친 것 |
| [parallel-task](skills/parallel-task) | 계획 파일을 조율해 막히지 않은 작업들에 병렬 서브에이전트를 여럿 띄운다. '/parallel-task' 명시 호출로 발동. | /parallel-task |
| [phone-harness](skills/phone-harness) | Control the user's phone - an iPhone through the Mac's iPhone Mirroring window, an Android over adb, a rented cloud Android, or a cloud iPho |  |
| [pi-agent](skills/pi-agent) | Builds with and operates Pi, the minimal terminal coding harness. Use for installing Pi, configuring providers/models/settings/environment v |  |
| [planner](skills/planner) | task-orchestrator 스킬이 사용할 수 있는 다중 작업 프로젝트의 구조화된 계획 수립. 복잡한 작업을 의존성 있는 병렬·순차 작업으로 분해할 때 사용. |  |
| [repeat-to-skill](skills/repeat-to-skill) | 지난 N일 Claude Code 세션 기록(~/.claude/projects/*.jsonl)에서 내가 3번 이상 비슷하게 입력한 요청을 찾아 "스킬 후보"로 뽑고, 이미 설치된 스킬과 겹치는지 함께 보여준다. "같은 말 세 번 했으면 스킬로 빼라"는  | 스킬 후보·같은 말 세 번 했으면 스킬로 빼라·반복 요청 찾아줘 |
| [rules-distill](skills/rules-distill) | Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files. Use when the same pr |  |
| [santa-method](skills/santa-method) | Multi-agent adversarial verification: two independent reviewers with the same rubric must both pass before output ships, with a fix-and-re-r |  |
| [skill-comply](skills/skill-comply) | Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs  |  |
| [skill-finder](skills/skill-finder) | 이 좌석 목록에 없는 전역 스킬 830여 개를 찾아 꺼내 쓴다. 할 일에 맞는 스킬이 목록에 없을 때 먼저 쓴다. |  |
| [skill-install](skills/skill-install) | 깃허브 URL이나 마켓플레이스로 받은 Claude Code 스킬·플러그인을 설치하기 전에 중복 판정·보안 점검·의존성 확인을 하고, 범위(user/project/local)를 정해 설치한 뒤 작동을 확인한다. "이 스킬 설치해 줘", "깃허브 스킬 깔 | 이 스킬 설치해 줘·깃허브 스킬 깔아 줘·플러그인 추가해 줘 |
| [skill-scout](skills/skill-scout) | 새 스킬을 만들기 전에 로컬·마켓플레이스·GitHub·웹의 기존 스킬을 먼저 검색. 스킬을 만들거나 포크하거나 찾고 싶을 때 사용. |  |
| [skill-stocktake](skills/skill-stocktake) | Claude 스킬·명령의 품질 감사. Quick Scan(변경된 스킬만)과 Full Stocktake 모드를 지원하며 서브에이전트 순차 배치 평가로 진행. |  |
| [skillers-suda](skills/skillers-suda) | 스킬러들의 수다 — 4명의 전문가가 수다 떨면서 바이브코더의 아이디어를 동작하는 스킬로 변환 인자 없이 실행하면 메뉴, 스킬 설명을 주면 인터뷰 후 스킬 생성, '분석 [경로]'를 주면 기존 스킬·에이전트를 분석한다. 트리거: '/skillers-su |  |
| [task-orchestrator](skills/task-orchestrator) | 의존성 분석, 병렬 tmux/Codex 실행, 자가 치유 하트비트 모니터링을 갖춘 자율 멀티에이전트 작업 오케스트레이션. 조율된 병렬 실행이 필요한 여러 이슈/작업의 대형 프로젝트에 사용. |  |
| [think](skills/think) | Apply the Fable-derived 10-stage OBSERVE, OBSERVE, LISTEN, THINK, CONNECT, CONNECT, FEEL, ACCEPT, CREATE, GROW loop to consequential or ambi |  |
| [vibe-sunsang](skills/vibe-sunsang) | 바선생 — AI 활용 성장 멘토 에이전트 인자에 따라 초기 설정(onboard)·대화 로그 변환과 회고(retro)·AI 활용 코칭(mentor)·성장 리포트(growth)·개념 학습(knowledge)으로 분기한다. 트리거: '바선생', '/vibe |  |

### 설교·강단 (35)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [canon-propagate](skills/canon-propagate) | 정본(설교 본문·성경 구절·핵심 문구)을 고치면 그 정본에서 파생된 모든 사본(발표자료·설교문·프롬프터·도식·인포그래픽·손그림·리포트·종합본·hwpx·Obsidian 노트·NotebookLM 소스·아티팩트)을 먼저 목록화하고 한 번에 교체한 뒤 "바꾼 | 바꾼 것 / 못 바꾼 것·정본 고쳤어 사본도·3-5절 개역개정으로 교체 |
| [dwelling-sermon-coach](skills/dwelling-sermon-coach) | > 한 주 동안 성경 본문과 동행하며 묵상 중심으로 설교를 준비하는 7단계 워크플로우 코치 스킬. 트리거: "머무르는 설교", "동행 설교", "한 주 묵상", "뭉근한 설교 준비", "천천히 설교", "본문에 머무르기", "살아있는 설교", "dwe | 머무르는 설교·동행 설교·한 주 묵상 |
| [kangjunmin-sermon-writing-coach](skills/kangjunmin-sermon-writing-coach) | 강준민 목사의 《목회자의 글쓰기》(두란노, 2015)에 담긴 원리를 기반으로, 설교 준비와 설교문 작성을 돕는 코칭 스킬. 사용자가 "설교 준비해줘", "설교문 써줘/다듬어줘", "강준민 목사 글쓰기 원리로", "목회자의 글쓰기 스타일로", "다독다상 | 설교 준비해줘·설교문 써줘/다듬어줘·강준민 목사 글쓰기 원리로 |
| [sermon-audience-feedback-persona](skills/sermon-audience-feedback-persona) | 설교문 초안을 가상의 회중 8명(워킹맘·미혼 청년·중년 사업가·은퇴 직전 권사·결혼 2년차 새신자 자영업·이혼 후 홀로 양육·고3 입시생·1세대 홀몸 권사)이 강단 아래에서 듣는 것처럼, 각자의 삶·신앙 연륜·신학 수준에서 솔직한 속마음(의문·반발·위 | 회중 입장에서 들어줘·워킹맘/청년/새신자/은퇴 권사 시각·여러 페르소나 비교 피드백 |
| [sermon-augustine-coaching](skills/sermon-augustine-coaching) | 히포의 어거스틴(Augustine of Hippo, 354–430)의 신학과 설교론으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 은혜의 우선성·사랑의 질서(ordo amoris)·두 도성·악의 결핍·삼위일체 같은 핵심 신학과 『기독교 | 어거스틴·Augustine·히포 |
| [sermon-bavinck-coaching](skills/sermon-bavinck-coaching) | 헤르만 바빙크(Herman Bavinck, 1854–1921)의 신학으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 『개혁교의학(Reformed Dogmatics)』을 1차 자료로 삼고, 거기 없으면 Our Reasonable Fait | 바빙크·Bavinck·개혁교의학 |
| [sermon-bible-dictionary](skills/sermon-bible-dictionary) | 성경 인물·지명·단어·신학적 개념을 성경 주석서·성경 지도·성경사전·개론서 수준의 깊이로 풀어주는 성경사전 도우미. 원어(히브리어/헬라어) 분석, 어원 추적, 성경 전체 용례 점검, 신학적 의미 해석을 한 응답에 종합하여 제공한다. 사용자가 "성경 단 | 성경 단어 뜻·원어 분석·헬라어/히브리어로 무슨 뜻 |
| [sermon-bible-history-matcher](skills/sermon-bible-history-matcher) | 성경의 특정 인물·사건·본문 내용을 입력하면 세계사 자료(고고학적 유물, 고대 문헌, 학술 연구)에서 동일하게 매칭되는 역사적 사실을 찾아 제시하는 스킬. 할루시네이션 없는 검증된 증거만 제시하며 학계 주류 의견과 물리적 증거(유물 소장 정보 포함)를 | 성경 인물을 세계사에서 찾아줘·이 성경 사건의 역사적 증거는?·성경과 역사의 교차점 |
| [sermon-bible-research-writing](skills/sermon-bible-research-writing) | 논문 연구 방법론(체계적 자료 수집·출처 등급·교차 검증·문헌 매트릭스·구조화 집필·인용 전수 점검)을 설교 준비에 적용하여, 성경 본문 연구부터 설교문 완성까지 학술적 엄밀성으로 동행하는 스킬. 트리거 — "설교를 위한 성경연구", "논문식 설교 준 | 설교를 위한 성경연구·논문식 설교 준비·학술적 설교 연구 |
| [sermon-brainstorm](skills/sermon-brainstorm) | 설교 준비를 위한 인터랙티브 브레인스토밍 파트너. 유도 질문으로 메시지를 명확히 하고 핵심 긴장을 찾아 설교 브리프를 만든다. 목회자와 '함께' 생각하며, 설교를 대신 써주지 않는다. |  |
| [sermon-calvin-institutes](skills/sermon-calvin-institutes) | 존 칼빈(John Calvin, 1509–1564)의 『기독교 강요(Institutes of the Christian Religion, 1559년 최종판)』 4권 80장 전체를 깊이 있게 분석·해설하고 학습을 지원하는 조직신학 도우미. 1559판 4권 |  |
| [sermon-calvin-style-insight](skills/sermon-calvin-style-insight) | 존 칼빈(John Calvin, 1509–1564)의 설교 스타일을 연구하고 실제 칼빈식 설교문을 작성하도록 돕는 개혁주의 설교 도우미. 칼빈의 lectio continua(연속 강해) 전통, 본문 충실성, 교리·주해·적용의 통합, 절제된 수사, 목회 | 칼빈식 설교·Calvin sermon·개혁주의 설교 |
| [sermon-christian-history-interpreter](skills/sermon-christian-history-interpreter) | 고대부터 현대까지의 역사적 사건·인물·사회 흐름을 기독교적 관점에서 해석하고 신학적 통찰을 제공하는 학술 도우미. 로마 제국의 기독교 박해, 콘스탄티누스의 회심, 동서 교회 분열, 십자군 전쟁, 르네상스, 종교개혁(루터·칼빈·츠빙글리), 30년 전쟁, | 기독교 관점에서 ○○를 어떻게 보는가·기독교적 역사 해석·○○ 사건의 신학적 의미 |
| [sermon-commentary-recommendations](skills/sermon-commentary-recommendations) | 성경 66권 각 권별로 신학적으로 신뢰할 만한 추천 주석(Ligonier Ministries·Keith Mathison 선정 목록 기반, WBC·NICOT·NICNT·TOTC·BST·NIVAC·PNTC 등 표준 시리즈 병합)을 제공하는 공용 참고 자료 | 주석 추천·이 본문 주석 뭐 볼까·성경주석추천 |
| [sermon-doctrinal-planner](skills/sermon-doctrinal-planner) | 성경 본문 또는 설교 주제의 핵심 문장을 입력받아 체계적인 교리설교(doctrinal preaching) 기획안을 자동 생성하는 스킬. 본문 분석·교리적 함의 도출·역사적 교리 정립(니케아·웨스트민스터·하이델베르크 표준 참조)·교리설교 고유의 4단계  | 교리설교·교리설교 기획안·doctrinal sermon |
| [sermon-emotive-writing-coach](skills/sermon-emotive-writing-coach) | 설득력 있고 감동적인 설교문 작성을 글쓰기 차원에서 돕는 인터랙티브 코칭 스킬. 주제·목차가 어느 정도 잡힌 설교자가 실제 설교문을 쓸 때 (1) 설교문 전체 구조 제안과 서론·본론·결론별 전개 아이디어 제시, (2) 문장·문단·전체 글의 3계층에서  | 감동적인 설교문 써줘·설득력 있는 설교문·설교 글쓰기 코칭 |
| [sermon-expository-daeji](skills/sermon-expository-daeji) | 강해설교의 3단계 작성법(주제 결정 → 대지 결정 → 대지 채우기)과 우산질문 방법론을 토대로 대지설교(3대지 설교)를 설계·작성·진단하는 스킬. 해돈 로빈슨의 10단계를 3단계로 통합한 실전 모델을 따르며, (1) 본문에서 한 문장 주제 확보(해석→ | 강해설교·대지설교·3대지 |
| [sermon-greek-grammar-machen](skills/sermon-greek-grammar-machen) | J. G. 메이첸(J. Gresham Machen, 1881–1937)의 표준 교과서 『New Testament Greek for Beginners』(1923, 33강)를 토대로 신약 헬라어 문법을 가르치는 학습 도우미. 알파벳·발음·격(주격·대격·속 |  |
| [sermon-history-culture-geo-context](skills/sermon-history-culture-geo-context) | 성경 본문의 역사적·문화적·지리적·사회적 배경을 학문적 깊이로 풀어주는 성경 배경 해설 도우미. 고대근동·이스라엘 왕국·바벨론 포로기·페르시아·헬라·로마 제국 시대의 정치 상황, 유대인의 일상 문화·사회 구조·종교 관습, 성경 무대의 지리·기후·교역로 | 성경 배경·역사적 배경·문화적 맥락 |
| [sermon-lloyd-jones-coaching](skills/sermon-lloyd-jones-coaching) | 마틴 로이드 존스(Martyn Lloyd-Jones, 1899–1981) 'The Doctor'의 명저 『설교와 설교자(Preaching and Preachers, 1971)』를 토대로 설교자를 코칭하는 스킬. MLJ 고유의 강조점인 'Logic on |  |
| [sermon-luther-coaching](skills/sermon-luther-coaching) | 마틴 루터(Martin Luther, 1483–1546)의 신학과 설교론으로 설교 주제를 잡고 메시지를 깊게 다듬도록 돕는 코칭 스킬. 이신칭의·오직 은혜·오직 성경·만인제사장·두 왕국·법과 복음·노예의지·십자가 신학·은폐된 하나님 등 핵심 신학과 평 | 루터·Luther·마틴 루터 |
| [sermon-multi-bible-version-compare](skills/sermon-multi-bible-version-compare) | 성경 한 구절을 9개 필수 번역본·종교 문헌으로 다층 비교 분석하는 다중 번역 비교 도우미. 개역개정·NIV·헬라어 원문·히브리어 원문·라틴어 Vulgata·천주교 성경(공동번역/200주년)·기타 한국어 또는 영어 추가 번역 + 코란·탈무드 대응 본문 | 번역본 비교·여러 번역으로 보고 싶다·이 구절 NIV는 어떻게 |
| [sermon-pipeline](skills/sermon-pipeline) | 설교 사역 전체를 한 구조로 돌리고 싶을 때 쓴다. 설교 이전의 기획(연간·시리즈) → 설교 준비 6단계(본문개론→개요→주해→주제선택→설교문작성→퇴고) → 설교 이후의 활용(프롬프터·발표자료·블로그·유튜브·소그룹·QT)을 서브에이전트로 단계별 실행하고 | /sermon-pipeline·설교 파이프라인·종합 파이프라인 |
| [sermon-planner-52week](skills/sermon-planner-52week) | 키워드 1개를 입력받아 52주 연간 설교 계획을 자동 생성하는 설교 기획 도우미. 각 주차별로 설교 주제, 핵심 성경구절 5개, 핵심 포인트 3개, 세부 주제 5개, 연관 찬송가 5곡을 제시하며, 절기(부활절/성탄절/맥추감사절 등)와 한국교회 트렌드( | 52주 설교 계획·연간 설교 주제·설교 시리즈 기획 |
| [sermon-prompter](skills/sermon-prompter) | > 완성된 설교 원고를 강단용 텔레프롬프터(프롬프터) HTML 파일로 출력하는 스킬. 일정한 속도로 화면이 위로 자동 스크롤되며, 스크롤 속도를 조절하는 옵션 버튼(느림·보통·빠름과 미세 ＋/−)을 제공한다. 글꼴 선택(리디바탕·애플고딕), 글자 크기 |  |
| [sermon-qt-original-text-based](skills/sermon-qt-original-text-based) | 성경 본문을 입력받아 원어 분석 기반의 완성된 큐티(QT)를 자동 생성하는 말씀묵상 도우미. '생명의 삶'·'매일성경' 스타일의 짧은 설교형 큐티를 산출하며, 핵심 구조는 (1) 예화 기반 서론 — 최신 신문기사·시·영화·도서·예화모음을 웹 검색으로  | 큐티 만들어줘·QT 작성·말씀 묵상 |
| [sermon-research](skills/sermon-research) | 주간 설교 준비용 심층 리서치 도우미. 본문·주제·질문을 주면 주석 통찰, 역사적 배경, 원어 노트, 생각거리를 돌려준다. 리서치 전용 — 개요·설교문 작성은 하지 않는다. |  |
| [sermon-series](skills/sermon-series) | 여러 주에 걸친 설교 시리즈 기획. 주제나 성경 책과 주차 수를 주면 시리즈 제목 후보, 주차별 본문·제목·핵심 아이디어를 돌려준다. |  |
| [sermon-text-analysis-multimethod](skills/sermon-text-analysis-multimethod) | 성경 본문 한 단위(절·단락·장)를 입력받아 7가지 핵심 분석법(원문 언어·구조·평행 본문·키아스무스·신학·문학·역사문화)을 자동으로 동시 산출하고, 추가 10가지 분석법(문맥적 배경·수사학·사회정치·심리·해석사·신비·묵상·페미니스트·윤리·포스트콜로니 | ○○○ 본문 분석·이 구절 다각도 분석·본문 종합 분석 |
| [sermon-textual-criticism](skills/sermon-textual-criticism) | 성경 한 구절을 신·구약 주요 고대 사본으로 비교하여 본문비평(textual criticism)적 차이를 분석하는 학술 도우미. 신약은 파피루스(P46·P52·P66·P75)·대문자(uncial) 사본(시내 사본 ℵ·바티칸 사본 B·알렉산드리아 사본  |  |
| [sermon-to-blog](skills/sermon-to-blog) | 설교 녹취록을 읽기 좋은 800~1200단어 블로그 글로 변환. 단순 녹취가 아닌 독립된 아티클. SEO 친화적 제목, 메타 설명, 웹 서식 본문. |  |
| [sermon-to-youtube](skills/sermon-to-youtube) | 설교 영상 유튜브 최적화. 제목과 녹취록을 주면 최적화된 제목, 타임스탬프 포함 설명, 태그, 썸네일 컨셉, 숏폼 클립 추천을 돌려준다. |  |
| [sermon-toego-revision](skills/sermon-toego-revision) | 채경락 교수(고려신학대학원)의 『퇴고설교학』(성서유니온선교회, 2013)을 토대로, 1차 완성된 설교문을 '바르고 힘센 설교'로 다듬는 설교 퇴고(推敲) 전문 스킬. 설교학 교수의 관점에서 4대 평가 범주 — ① 본문에 기초한 선명한 주제, ② 전략적 |  |
| [sermon-topic-message-coach](skills/sermon-topic-message-coach) | 설교 주제 설정과 핵심 전달 메시지 정립이 막힌 설교자를 6단계 대화로 코칭하는 인터랙티브 스킬. 사용자에게 단계별 질문을 던지며 (1) 주제 명확화 → (2) 설교 목적 구체화 → (3) 핵심 전달 메시지 추천 5개 → (4) 메시지 선택과 핵심 단 | 설교 주제를 못 정하겠다·어떻게 시작해야 할지 모르겠다·설교 코칭 |
| [sermon-topic-research-multidisciplinary](skills/sermon-topic-research-multidisciplinary) | 설교 주제 한 단어(예: "고난", "용서", "정의", "가난", "노동", "결혼", "환경", "AI", "전쟁", "외로움") 또는 한 문장을 입력받아, 11개 학문 분야(사회·기술·산업·경제·환경·정치·국제관계·법·제도·심리·영성)에서 학제간 | 고난·용서·정의 |

### 글쓰기·윤문 (30)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [adult-vocabulary-writing-coach](skills/adult-vocabulary-writing-coach) | 유선경 작가의 《어른의 어휘력》(앤의서재)에 담긴 어휘력·글쓰기 철학을 기반으로, 한국어 글(에세이, 칼럼, 자기소개서, 논술, 블로그, 발표문 등)을 정확한 어휘와 단단한 구성으로 다듬거나 새로 쓰도록 돕는 코칭 스킬. 사용자가 "어른의 어휘력 스타 | 어른의 어휘력 스타일로 써줘·정확한 어휘로 다듬어줘·곁가지 서술 줄여줘 |
| [blank-page-cowrite](skills/blank-page-cowrite) | 빈 문서 한 줄씩 같이 쓰기. AI가 만든 긴 보고서·리서치 결과를 사용자에게 그대로 넘기지 않고, 빈 양식에서 섹션→문단 단위로 같이 써 가며 사용자를 인터뷰해 이해시키는 스킬(커리어해커 알렉스의 '미트 프록시' 탈출법). 트리거: '한 줄씩 같이  |  |
| [classic-sentence-writing-coach](skills/classic-sentence-writing-coach) | 주인님 소장 자료(일당백 에세이집 47편·시즌1 고전·명언/첫 문장 강의·글쓰기 강의, 상세 102권·압축 72권)에서 뽑은 「고전·명언 문장사전」을 근거로, 설교·칼럼·강의 도입·축사·묵상글·카드뉴스에 들어갈 고전 문장을 골라 주고, 그 책의 문체( | 고전·명언 문장사전·고전 인용 넣어줘·명언 하나 찾아줘 |
| [copy-editing](skills/copy-editing) | When the user wants to edit, tighten, proofread, or refresh existing copy, or asks whether to keep, cut, or change a line in it, without rew |  |
| [copywriting](skills/copywriting) | When the user wants to write or rewrite page copy (homepage, landing, pricing, feature), or asks which headline, promise, or message to lead |  |
| [dhdna-profiler](skills/dhdna-profiler) | Applies the DHDNA framework as an exploratory rubric for reasoning and writing patterns in supplied text. Used for explicit requests for DHD |  |
| [final-report-lint](skills/final-report-lint) | 에이전트가 사용자에게 보내는 마지막 메시지(작업 완료 보고·결과 요약·조사 결론)를 Claude Mythos 5.1 시스템 프롬프트의 'Writing for the user'·'Delivering work' 규칙으로 린트하고 고쳐 쓴다. 검사 항목은  | 원하시면 ~할까요?·~하겠습니다·최종보고 점검 |
| [frontline-writing-coach](skills/frontline-writing-coach) | 은유 작가의 《글쓰기의 최전선》(메멘토)에 담긴 글쓰기 철학과 실제 수업 방식을 기반으로, 한국어 에세이·자기서사·후기·인터뷰 원고 등을 정직하고 구체적인 문장으로 다듬거나 새로 쓰도록 돕는 코칭 스킬. 사용자가 "은유 작가처럼", "글쓰기의 최전선  | 은유 작가처럼·글쓰기의 최전선 스타일로·관념적인 표현 좀 구체적으로 바꿔줘 |
| [godowon-writing-coach](skills/godowon-writing-coach) | 고도원의 《누구든 글쓰기 - 고도원의 인생작법》(해냄)에 담긴 글쓰기 철학과 실전 기법을 기반으로, 한국어 글(에세이, 편지, 아침편지/뉴스레터, 자기소개서, 연설문, 칼럼, 치유 글쓰기 등)을 쓰거나 다듬도록 돕는 코칭 스킬. 사용자가 "고도원 스타 | 고도원 스타일로·인생작법처럼·아침편지 스타일로 써줘 |
| [humanize](skills/humanize) | AI가 쓴 한글 텍스트를 자연스럽게 윤문하는 진입 명령. humanize-korean 파이프라인을 shim 의 route_hint 가 정한 경로(light 1콜 · standard 2콜 · heavy 3+콜)로 실행하고 `--strict`면 heavy | /humanize |
| [humanize-korean](skills/humanize-korean) | AI(ChatGPT·Claude·Gemini 등)가 쓴 한글 텍스트를 "사람이 쓴 글처럼" 윤문해주는 오케스트레이터 스킬. 번역투·영어 인용 과다·기계적 병렬·관용구·피동태 남용·접속사 남발·리듬 균일성·이모지/불릿 과다 등 10대 카테고리 85개 A | 사람이 쓴 글처럼·AI 티 없애줘·AI 같은 글 자연스럽게 |
| [humanize-redo](skills/humanize-redo) | 가장 최근 윤문 결과를 2차로 다시 다듬는다 — 특정 카테고리·문단·강도 조정도 가능. humanize-korean strict 윤문(Phase B)을 기존 run_id에 재실행해 잔존 finding을 처리한다. 트리거 — "/humanize-redo | /humanize-redo |
| [humanize-scan](skills/humanize-scan) | 한글 글에 AI 티가 얼마나 있는지 재고, 실제로 고치면 어떻게 되는지 표본으로 보여주는 정찰 스킬. 실측 판별력 상위 6개만 본다. 워크스페이스·진단·게이트·서브에이전트 없이 이 대화 안에서 끝낸다(파일 0개, 서브에이전트 0회). 손볼 게 많다고  | 이 글 AI 같아?·AI 티 있나 봐줘·스캔해줘 |
| [korean-character-count](skills/korean-character-count) | Count Korean text deterministically with exact grapheme, line, and byte contracts for self-intros and form limits. |  |
| [korean-humanizer](skills/korean-humanizer) | AI가 쓴 티가 나는 한국어 글을 자연스러운 사람 글로 고친다. 번역체, AI 상투어, 과도한 명사화·피동, 3의 법칙, 과장된 의의 부여, 마무리 상투구, 챗봇 잔재, 줄표·곡선따옴표 같은 한국어 특유의 AI 흔적을 심각도(S1/S2/S3)로 분류해 | 1000자로·AI 티 안 나게·사람이 쓴 것처럼 |
| [korean-middle-korean](skills/korean-middle-korean) | Convert incoming Korean text into a deterministic Korean Middle Korean-style rewrite with archaic particles, endings, Hanja hints, and tone- |  |
| [korean-slang-writing](skills/korean-slang-writing) | Use curated Korean trending-slang candidates plus best-effort Namu Wiki lookups to write witty Korean text with up-to-date slang, with conse |  |
| [korean-spell-check](skills/korean-spell-check) | Use Nara/PNU Korean spell-check surfaces conservatively to proofread Korean text, chunk long input, and return change-focused correction sug |  |
| [markdown-mermaid-writing](skills/markdown-mermaid-writing) | Writes scientific Markdown documentation and Mermaid diagrams for workflows, relationships, timelines, and schemas. Provides syntax referenc |  |
| [my-writing-master-prompt](skills/my-writing-master-prompt) | 우석지니의 "AI가 나처럼 글을 쓰는 마스터 프롬프트 역설계" 방법론을 기반으로, AI 초안과 사용자의 수정본을 쌍(pair)으로 비교 분석하여 사용자만의 글쓰기 규칙을 역설계하고, 이를 마스터 프롬프트로 축적·적용하는 스킬. 제안서·보고서·발표문 등 | AI가 나처럼 글을 쓰는 마스터 프롬프트 역설계·내 문체로 써줘·나처럼 써줘 |
| [parkjooyeon-lyric-writing-coach](skills/parkjooyeon-lyric-writing-coach) | 작사가 박주연(〈입영열차 안에서〉〈너에게로 또 다시〉〈오래전 그날〉〈외워두세요〉 등 KOMCA 등록 300여 곡)의 작사법을 기반으로 노래 가사·찬양 가사·설교 도입 장면·짧은 글을 쓰거나 다듬도록 돕는 코칭 스킬. 사용자가 "박주연 스타일로", "박 | 박주연 스타일로·박주연처럼·작사해줘 |
| [redteam](skills/redteam) | 기획서·글·설교문·전략을 목적별 전문 레드팀이 프레임워크로 공격하고, 요청 시 조언까지 하는 확증편향 파괴 스킬. 스쿼드 3종(business 기획·writing 글쓰기·sermon 설교) 중 자동 또는 지목 소집한다. 사용자가 "레드팀", "악마의  | 레드팀·악마의 변호인·비판해줘 |
| [seeing-writing-lens](skills/seeing-writing-lens) | 진서·버거·손택 세 렌즈로 글과 이미지를 점검하는 코치. (1) 진서 렌즈 — 『글쓰기 생각쓰기』의 군더더기 4종(일 안 하는 단어·긴 단어·동사와 겹치는 부사·행위자 숨긴 피동)을 표시하고 "무엇을 말하려는가/제대로 말했나/처음 읽는 사람에게 명료한 | 무엇을 말하려는가/제대로 말했나/처음 읽는 사람에게 명료한가·군더더기 빼줘·진서처럼 퇴고 |
| [soul-distill](skills/soul-distill) | 사용자 본인이 직접 쓴 글·메시지·설교·메일 묶음에서 "분신 에이전트용 soul.md 초안"을 증류한다 — ①말투 ②개입 시점(언제 답하고 언제 침묵) ③판단 기준·거절 방식 ④금지선(자기 이름으로 하지 않는 일)을 근거 문장과 함께 뽑는다. "내 분 | 분신 에이전트용 soul.md 초안·내 분신 만들어줘·soul.md 증류 |
| [ste-korean](skills/ste-korean) | 한국어 통제어(STE100식) 글쓰기. ASD-STE100(항공 정비 문서용 통제어) 규칙을 한국어에 맞게 옮긴 12개 규칙으로 설명·요약·절차서·공문·AI 지시서를 짧고 오해 없는 문장으로 쓰거나 고친다. 모드: 엄격 / 80%(기본) / 절차 /  | STE로 써 줘·통제어로·STE100 80%로 |
| [technique-transfer](skills/technique-transfer) | 남이 쓴 글이나 책을 넣으면 그 안에 쓰인 글쓰기 기법을 10개 영역 97개 항목의 분류 체계로 체계적으로 분석해 ''기법 프로파일''로 뽑아내고, 그 프로파일을 사용자 자신의 글에 이식해 같은 기법으로 다시 쓰게 해 주는 기법 채굴·이식 스킬. 세  | 이 글 기법 분석해줘·이 작가처럼 쓰고 싶어·이 책 문체 분석 |
| [toego-korean](skills/toego-korean) | 사람이 직접 쓴 한국어 글(에세이·블로그·보고서·자기소개서·편지·일기·칼럼·아이의 글)을 구조 → 문단 → 문장 → 처음과 끝의 순서로 고쳐 주는 퇴고 전담 스킬. 유시민의 '나쁜 글 고치는 여섯 가지'(소리 내어 읽기·짧게 쓰기·군더더기 빼기·흐린  | 이 글 좀 고쳐줘·퇴고해줘·다듬어줘 |
| [token-diet](skills/token-diet) | 지침 파일(SKILL.md·CLAUDE.md·AGENTS.md·시스템 프롬프트)에서 토큰을 태우는 문구를 린트하고 고쳐 쓴다. 검사 항목은 '매번·항상 읽어'식 상시 읽기, 부정 트리거가 없는 스킬 description, 종료 조건 누락, 우선순위 없 | 토큰 다이어트·지침 린트·스킬 설명 점검 |
| [writing-analytical-essay](skills/writing-analytical-essay) | Use when the user gives a one-line topic (책·논문·행사·제품·정책·기술·시사·개인 경험) and wants a finished Korean SNS·블로그용 분석형 글, 서평, 행사 후기, 기술 분석, 시사 논평, 칼럼 | 이 주제로 글 써줘·블로그 글·SNS 글 |
| [yuhongjun-writing-coach](skills/yuhongjun-writing-coach) | 유홍준 교수(『나의 문화유산답사기』, 『나의 인생만사 답사기』 부록 '좋은 글쓰기를 위한 15가지 조언')의 글쓰기 원리로 한국어 산문·칼럼·답사기·설교 예화·주보 글·강의 원고를 쓰거나 퇴고하는 코칭 스킬. "유홍준처럼", "답사기 스타일로", "쉽 | 유홍준처럼·답사기 스타일로·쉽게 읽히게 |

### 비전 코칭·진단 (28)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [vision-career-recommendation](skills/vision-career-recommendation) | 사용자의 *가치 단어·관심사·심리검사 결과(에니어그램·MBTI·다중지능·STRONG/RIASEC) + 나이·학력*을 종합하여 적합한 직업을 4가지 유형으로 각 5개씩 총 20개 추천하는 진로 매칭 스킬. 4유형 분류는 원본 지침 그대로 — ① 미래 직 | 직업 추천·진로 추천·어떤 직업이 좋을까 |
| [vision-clarity-coaching](skills/vision-clarity-coaching) | 비전이 *막연하거나 막힌* 사용자가 *비전의 핵심*을 한 문장으로 끄집어내도록 돕는 1:1 깊이 코칭 스킬. 소크라테스 산파술(maieutics) 방식으로 답을 가르치지 않고 *질문으로* 사용자가 스스로 비전 핵심에 도달하게 한다. 5단계 깊이 코칭  | 비전이 모르겠어요·내가 뭘 하고 싶은지·비전 명료화 |
| [vision-cys-competence-visioncoding](skills/vision-cys-competence-visioncoding) | 최윤식 박사가 직접 개발한 *CYS 비전 역량 진단 검사*(『미래준비학교』)를 그대로 구현한 비전 역량 진단 스킬. 박사님의 200여 개 질문 평가지를 토대로 한 *10개 비전 코드 진단* — ① **비전 방향성** ② **비전 가치 방향**(가치 성 | CYS 비전 역량 검사·비전 역량 진단·비전 코드 |
| [vision-eight-training-areas](skills/vision-eight-training-areas) | 최윤식 박사 『미래준비학교』(2016)의 *비전 훈련 8대 영역*을 그대로 구현한 미래인재 습관 훈련 코칭 스킬. 박사님 인용 *"비전 훈련을 평가하는 기준은 무엇일까? 비전 훈련의 최종 결과물은 무엇일까? 바로 기술의 향상과 습관의 형성이다. 미래준 | 비전 훈련 8대 영역·박사님 SMART Habit·미래인재 습관 |
| [vision-enneagram-visioncoding](skills/vision-enneagram-visioncoding) | 에니어그램(Enneagram) 9유형의 *핵심 동기(Core Desire)와 핵심 두려움(Core Fear)*을 검사 문항의 중심으로 삼는 자가 진단 스킬. 27문항 카탈로그(각 유형 3문항)를 *층화 무작위 셔플*(블록 A 각 유형 2문항×9=18, | 에니어그램 검사·Enneagram type test·내 에니어그램 유형 |
| [vision-financial-3shields-3windows](skills/vision-financial-3shields-3windows) | 최윤식 박사 『미래준비학교』(2016) + 『부의 정석』(2011)의 *3개의 방패와 3개의 창* 재정 전략 모델을 그대로 구현한 비전 재정 코칭 스킬. 박사님 고유 모델 — **3개의 방패(자산 보존)**: ① 보험·연금·빚 등 *금융 관련 자산 리 | 박사님 재정 전략·3개 방패 3개 창·자산 리모델링 |
| [vision-financial-coach](skills/vision-financial-coach) | Dave Ramsey(『The Total Money Makeover』·7 Baby Steps·스노우볼 방식)와 Suze Orman(『The Money Book for the Young, Fabulous & Broke』·"People First, the | People First, then Money, then Things·재정 분석 시작해줘·재정 코칭 |
| [vision-five-stages](skills/vision-five-stages) | 최윤식 박사 『미래준비학교』(2016)의 *미래준비학교 비전 5단계*를 그대로 구현한 통합 비전 코칭 스킬. 박사님 고유 5단계 — ① **비전 스케치(자기 인식)** — 비전 역량 검사·미래 변화 통찰·가치 정립으로 비전의 *밑그림*을 그림 ② ** | 박사님 5단계·비전 스케치 디자인 훈련 재인식 재생산·미래준비학교 5단계 |
| [vision-follow-through-habits](skills/vision-follow-through-habits) | 결심·계획이 *습관·일상 시스템*으로 정착하도록 설계하는 실행 지속력 코칭 스킬. BJ Fogg(Tiny Habits, 2019) + James Clear(Atomic Habits, 2018) + Charles Duhigg(The Power of Ha | 습관 설계·작심삼일·실행이 안 돼요 |
| [vision-four-futures](skills/vision-four-futures) | 최윤식 박사 『미래준비학교』(2016, 지식노마드, ISBN 9788993322972)의 *4가지 미래 가능성*을 그대로 구현한 비전 미래학 코칭 스킬. 박사님 미래학자 본업의 핵심 분류 — ① **Plausible Future (기본미래)** — 발 | 하나의 미래(a Future)·그 미래(the Future)·대안적 미래들(Alternative Futures) |
| [vision-future-needs-prediction](skills/vision-future-needs-prediction) | 미래 사회 변화로부터 발생할 *잠재적 기회·위기·문제·필요·결핍*을 현실적이고 분석적으로 예측·분해하는 미래필요 예측 전문가 스킬. 사용자가 던진 변화 주제(AGI 도래·인구절벽·기후위기·디지털화폐·통일·고령화·플랫폼 경제 등)를 받아 **3축 분석  | 미래 필요 예측·사회 변화 분석·기회와 위기 |
| [vision-future-promise-five-criteria](skills/vision-future-promise-five-criteria) | 최윤식 박사 『미래준비학교』(2016)의 *미래 유망성 판단 5가지 기준*을 그대로 구현한 비전 영역 평가 스킬. 박사님이 미래준비학교에서 *비전 영역을 선택*할 때 사용하는 판단 도구로, 사용자가 자신의 관심사·재능 중 *미래에 유망한 것*을 객관적 | * 사용자가·, |
| [vision-futures-timeline-map](skills/vision-futures-timeline-map) | 최윤식 박사 『미래준비학교』(2016)의 *미래지도(Futures Timeline Map)* 작성 도구를 그대로 구현한 비전 코칭 스킬. 박사님 미래학자 본업의 시그니처 도구로, 사용자가 자신의 비전 영역에 대한 *맞춤 미래지도*를 작성하도록 코칭한다 | * 사용자가·, |
| [vision-goal-reframing](skills/vision-goal-reframing) | 사용자의 *영감·꿈·소망*을 측정 가능한 *현실 목표*로 변환하는 워크북 스킬. 명료해진 비전 한 문장(vision-clarity-coaching 산출물 또는 사용자 입력)을 받아 SMART 원칙 + Backcasting + OKR 3가지 검증된 프레 | 꿈을 목표로·영감 변환·SMART 목표 |
| [vision-grill-with-docs](skills/vision-grill-with-docs) | **vision 시리즈 *마스터 진입 스킬*** + 미래비전코칭의 모든 단계에서 사용자가 난관에 부딪히거나 생각이 정리되지 않을 때 호출하는 *다목적 인터뷰 엔진* 스킬. 박사님 28개 vision 스킬의 *cross-stage 진입로* — 사용자가  | 비전 grill·비전 인터뷰·내 비전 무너뜨려봐 |
| [vision-mbti-visioncoding](skills/vision-mbti-visioncoding) | MBTI 전문가·심리측정학자 페르소나로 사용자가 자신의 MBTI 16유형을 발견하도록 돕는 자가 진단 스킬. 4축(E/I 외향-내향, S/N 감각-직관, T/F 사고-감정, J/P 판단-인식) 각 5문항씩 총 20문항을 *순차 제시*하고 사용자 응답을 | MBTI 검사·MBTI 진단·내 MBTI 찾기 |
| [vision-mission-frame](skills/vision-mission-frame) | 최윤식 박사 『미래준비학교』(2016)의 핵심 도식 *비전 프레임(Mission Frame)*을 단독 도구로 구현한 비전 코칭 스킬. 비전이 자라기 위해 필요한 2개의 중심축 — ① **영적 직관력(Spiritual Intuition)** = 영감(D | 가치 있는·시대적·소명 |
| [vision-multipleintel-visioncoding](skills/vision-multipleintel-visioncoding) | Howard Gardner의 다중지능 이론(Theory of Multiple Intelligences, 1983 『Frames of Mind』 + 1995 자연친화 추가 + Existential 잠정)을 토대로 9가지 지능 — ① Linguistic( | 다중지능 검사·Multiple Intelligences test·Howard Gardner 검사 |
| [vision-personal-future-research](skills/vision-personal-future-research) | 사용자의 *Vision Coding 진단 7종 결과*(CYS 비전 역량·MBTI·에니어그램·STRONG/RIASEC·다중지능·가치·준비도)를 입력받아, 그 사용자에게 *직접 연관된 미래 변화*를 최윤식 박사 미래학 프레임의 STEEPS 6영역(Soci | 내 진단 결과를 가지고 미래 변화 정리해줘·나와 연관된 미래 변화 수집·맞춤 미래 자극 |
| [vision-progress-review](skills/vision-progress-review) | 사용자의 비전·목표·행동 계획 진척을 *주간·월간·분기·연간* 4단위 정기 점검으로 추적·평가·재조정하는 진척 추적 스킬. **결정론 환원** — 날짜 계산·다음 점검 일정 산출·달성률 분류(✓/△/✗)·OKR 점수 분류(0.0-0.3/0.4-0.6/ | 정기 점검·주간/월간/분기 회고·progress review |
| [vision-readiness-visioncoding](skills/vision-readiness-visioncoding) | 사용자의 *꿈 달성 준비도(Dream Readiness)*를 20문항 자가 진단으로 평가하고 영어 축 막대 그래프로 시각화하는 비전 코칭 스킬. **결정론 환원** — 점수 파싱·범위/누락 검증·능력별 평균·Composite·레벨 매핑·강점/성장 분류 | I am good at [skill]·비전 준비도·꿈 달성 능력 |
| [vision-school-major-info](skills/vision-school-major-info) | 한국 대학·학과·진로 정보(공공데이터포털 7개 API 통합)와 미국 직업 정보(O*NET)를 *결정론적*으로 조회·매핑·진로 추천에 활용하는 미래비전코칭 데이터 스킬. 박사님 vision-career-recommendation·vision-strong | 한국 대학 검색·전공 정보·이 학과의 관련 직업 |
| [vision-smart-five-competence](skills/vision-smart-five-competence) | 최윤식 박사 『미래준비학교』(2016)의 *SMART 미래인재 5역량 훈련*을 그대로 구현한 비전 훈련 코칭 스킬. 박사님 고유 5역량 — ① **S**ense(사물·현상에 대한 감각·판단력·통찰을 기르라) — 직관적 통찰력·훈련된 통찰력 ② **M* | SMART 5역량·Sense Method Art Relationship Technology·박사님 SMART 훈련 |
| [vision-statement-writer](skills/vision-statement-writer) | 최윤식 박사 『최윤식의 미래준비학교』(2016, 지식노마드, ISBN 9788993322972)의 *Vision Statement 비전 선언문* 양식을 그대로 구현한 비전 선언문 작성 코칭 스킬. 박사님 책 양식 빈칸 그대로 채워가는 1:1 코칭 —  | 비전 선언문·Vision Statement·비전 임무 선언 |
| [vision-strategy-coach](skills/vision-strategy-coach) | 사용자의 *비전(Vision)을 구체적·단계별 행동(Action)*으로 변환하는 통합 전략 코칭 스킬. 전략 계획·코칭 실무에서 널리 통용되는 5단계 흐름을 따른다 — ① **비전의 핵심(Core) 식별** — 표면 욕망과 본질 가치를 분리해 비전을  | 전략 코치·비전을 행동으로·5단계 메소드 |
| [vision-strong-visioncoding](skills/vision-strong-visioncoding) | STRONG 직업흥미도 검사(Strong Interest Inventory®) 간이 시뮬레이션 스킬. Holland(1959, 1997)의 RIASEC 6유형 모델 기반 — Realistic(현실형 R)·Investigative(탐구형 I)·Artis | STRONG 직업흥미도 검사·직업 흥미 검사·RIASEC 검사 |
| [vision-three-realm-balance](skills/vision-three-realm-balance) | 최윤식 박사 『미래준비학교』(2016)의 *비전 영역 3겹 다이어그램*을 그대로 구현한 비전 건강도 점검 스킬. 박사님 책 다이어그램의 3개 원이 교집합을 이루는 핵심 — ① **나만 기쁘게 함 = 개인 욕망** (한 영역만 극대화 시 자기중심·이기적 | 비전 영역 3겹·3영역 교집합·박사님 비전 다이어그램 |
| [vision-values-visioncoding](skills/vision-values-visioncoding) | 사용자의 MBTI 16유형·에니어그램 9유형·다중지능(Multiple Intelligences) 8지능 결과를 *가치 단어(value words)*에 매핑하여 사용자가 본능적으로 추구하는 *비전 가치 프로파일*을 도출하는 통합 가치 검사 스킬. 가치  | 비전 가치 검사·내 핵심 가치·MBTI·에니어그램·다중지능 통합 |

### 오피스·한글(HWP)·공공문서 (27)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [elegant-reports](skills/elegant-reports) | 북유럽 감성의 아름다운 PDF 보고서 생성. 마크다운·HTML로부터 Nutrient DWS를 거쳐 세련된 경영진 브리핑, 분석 보고서, 프레젠테이션형 PDF를 만들 때 사용. |  |
| [genie-report](skills/genie-report) | 원고/자료를 주면 "그레이스케일 A4 세로 보고서"를 HTML과 편집 가능한 PPTX 두 형식으로 생성. 텍스트가 많고 복잡한 보고서·제안서 전용 — A4 210×297mm 페이지 구분 + 헤더(제목·쪽번호)/푸터 + 프리텐다드 + 무채색 그레이스케일 | 그레이스케일 A4 세로 보고서·AI 보고서·제안서 PPTX 작성 워크플로우·A4 보고서 |
| [gongik-seosik](skills/gongik-seosik) | 서울특별시교육청 「2026 공익법인 실무지침서」 기반 공익법인 행정서식 작성 스킬. 사용자가 제공한 법인 정보·메모·회의 내용을 지침서의 공식 서식에 맞게 정리해 완성본을 만든다. 법인설립허가, 해산·청산, 기본재산 처분/담보·장기차입/기부금사용승인/ | 2026 공익법인 실무지침서·공익법인 서식·설립허가 신청서 |
| [gov-meeting-minutes](skills/gov-meeting-minutes) | 공공기관 회의 메모, 녹취록, ClovaNote 전사, 참석자 발언 기록을 바탕으로 담백한 공문서형 회의록 PDF를 만들 때 사용한다. 1쪽에는 회의록 요약본을, 2쪽 이후에는 시간순 상세 발언록을 배치하며, 익명 발언자는 사용자에게 이름·직함을 확인 |  |
| [gov-overseas-trip-report](skills/gov-overseas-trip-report) | 선관위·권익위·정보공개포털·주요 지방의회 등 검증된 공개 표면에서 공무국외출장/국외훈련 보고서·현황을 조회하고, 첨부 원문이 있으면 kordoc으로 사실·공개성·검토 신호만 구조화한다. 부정부패 판정 도구가 아니다. |  |
| [haengbok-case-record](skills/haengbok-case-record) | 공공 통합사례관리(행복이음·사회보장정보시스템) 상담일지·사례기록을 복지부 업무안내 기준으로 작성·검토·분석한다. 상담 녹취·메모를 행복이음 입력용 상담일지로 정리할 때, 초기상담지·욕구조사표·위기도 조사지·서비스 제공계획·모니터 상담지 항목을 채우거나 |  |
| [hop-desktop](skills/hop-desktop) | HOP(golbin/hop, 오픈소스 HWP/HWPX 데스크톱 앱)로 한글 문서를 사람 눈으로 열람·확인·PDF 내보내기 할 때 사용. "HOP로 열어줘", "hwp 미리보기", "만든 hwpx 화면으로 확인", "Finder에서 hwp 썸네일", " | HOP로 열어줘·hwp 미리보기·만든 hwpx 화면으로 확인 |
| [hwpx](skills/hwpx) | 한글 HWP/HWPX 파일의 변환·읽기·편집과 편집 가능한 .hwpx 문서 생성. 한글 파일, HWP 변환, HWPX 공문·보고서·계획서·활동지, 기존 한글 양식 채우기 요청에 사용한다. |  |
| [hwpx-gongmun-standardizer](skills/hwpx-gongmun-standardizer) | 우석진 「클로드.ai 공공기관 아래한글 .hwpx 공문서 표준화 생성 반자동화 워크플로우」 방법론. 기관의 기존 공문·보고서 2~3건(PDF)을 역추출해 "글쓰기 마스터 프롬프트.md"(무엇을 어떤 순서·문체로 쓸지)를 만들고, HWPX+PDF 쌍을  | 글쓰기 마스터 프롬프트.md·HWPX 템플릿 스킬·공문 표준화 |
| [hwpx-mouseco](skills/hwpx-mouseco) | 한국 공공문서용 HWPX(.hwpx) 보고서 양식을 분석·작성·검증할 때 사용한다. 공개 배포용 원페이퍼, 다중페이퍼, 장문 보고서 프로파일과 템플릿을 기준으로 report JSON을 만들고, HWPX 내부 XML을 보존하면서 문서를 생성한다. 레거시 |  |
| [hwpxskill](skills/hwpxskill) | 한글 HWPX 문서 생성/읽기/편집 스킬. .hwpx 파일, Hancom, OWPML 관련 요청 시 사용. .hwp 바이너리 파일 작성/생성/직접 편집 요청은 거부한다. |  |
| [ieumoffice](skills/ieumoffice) | Create, convert, read and edit Office documents locally with IeumOffice's command line: build pptx decks (checked outline, per-page spec, re |  |
| [kbg-문서양식(1)](skills/kbg-문서양식(1)) | kbg-문서양식(1). 「한 장으로 읽는 가톨릭 성경 73권」 판매 페이지(gatollik-seonggyeong73.impultienda.ar, 2026-11-18 열람)에 실린 견본 PDF의 문서 양식을 추출한 A4 한 장 정리 시트. 둥근 테마색  | 한 장으로 읽는 가톨릭 성경 73권·kbg-문서양식(1)·kbg 문서양식(1) |
| [korean-doc-corpus](skills/korean-doc-corpus) | > 한국 공공문서(PDF·HWP·HWPX·DOCX)를 AI가 읽을 수 있는 **하나의 구조화 마크다운 코퍼스**로 수렴시킬 때 사용한다. 핵심 3가지 — ①포맷 판별 후 적절한 도구로 라우팅 ②**스캔 PDF의 OCR 깨짐 글자 보정**(사전+정규식+ |  |
| [liteparse](skills/liteparse) | Local document and PDF parsing that returns spatial text with bounding boxes. Use for extracting text from PDFs, DOCX, Office files, and ima |  |
| [markitdown](skills/markitdown) | Converts heterogeneous documents and selected URIs to Markdown with Microsoft MarkItDown for text analysis, search, and LLM/RAG ingestion. C |  |
| [new-hwpx-master-v5-1-20260720](skills/new-hwpx-master-v5-1-20260720) | hwpx 공문/기안문 양식을 첨부하면 주제에 맞춰 공문 내용을 자동 작성. 작성 전 반드시 사용자에게 ①목표 분량(페이지 수) ②문체(개조식/서술식) ③내용 중점 방향을 3단계로 질문·확정한 뒤, 확정값에 근사하게 본문을 설계·검증한다 (v5.1, 2 |  |
| [nudocs](skills/nudocs) | Nudocs.ai로 문서 업로드·편집·내보내기. 협업 편집용 공유 문서 링크 생성, 마크다운 업로드, 편집된 내용 회수 시 사용. | send to nudocs·upload to nudocs·edit in nudocs |
| [nutrient-openclaw](skills/nutrient-openclaw) | Nutrient DWS용 OpenClaw 네이티브 문서 처리 스킬. 파일 변환, 텍스트·표 추출, 스캔 OCR, 개인정보 마스킹, PDF 워터마크, 전자서명, 크레딧 사용량 확인. | OpenClaw plugin·Nutrient OpenClaw |
| [officecli](skills/officecli) | officecli CLI 도구로 Office 문서(.docx, .xlsx, .pptx)를 생성·분석·교정·수정. 문서 생성, 검사, 서식 확인, 문제 찾기, 차트 추가, 수정 요청 시 사용. |  |
| [official-report-skillset](skills/official-report-skillset) | 공공기관 보고서, 결과보고, 계획보고, 검토보고, 회의결과 보고, 공문서 초안 작성에 사용하는 스킬. 사용자가 메모, 개요, 추진 경과, 계약 내용, 수요조사, 운영계획, 배분안, 붙임 자료 등을 주고 공공기관 결재문서 형태로 정리해 달라고 할 때 사 |  |
| [read-hwp](skills/read-hwp) | HWP/HWPX 문서의 에이전트 네이티브 파싱은 kordoc 사용 — JSON 추출, 문서 비교(diff), 서식 필드 추출, 마크다운→HWPX 역변환. 읽기/변환 전용 — 바이너리 편집은 rhwp-edit 사용. |  |
| [reporting-guideline-router](skills/reporting-guideline-router) | 논문 투고 직전, reporting guideline(CONSORT·STROBE·PRISMA·SRQR·COREQ·TRIPOD+AI 등)을 '유명한 checklist 고르기'가 아니라 '연구 설계와 보고 항목의 대응 증명'으로 선택하게 하는 라우팅 스킬 | reporting guideline 골라줘\·어떤 체크리스트 써야 해\·CONSORT/STROBE/PRISMA 맞나\ |
| [rhwp-advanced](skills/rhwp-advanced) | Debug HWP layout, dump document IR, compare versions, extract thumbnails, and unlock read-only HWPs with the upstream rhwp Rust CLI (export- |  |
| [rhwp-edit](skills/rhwp-edit) | Edit HWP documents — insert/delete text, replace-all, create tables, set cell text — with the k-skill-rhwp CLI that wraps the @rhwp/core WAS |  |
| [sungahna-foundation](skills/sungahna-foundation) | (재)성안나장학재단(재단법인, 서울특별시교육청 평생교육과 관할 공익법인) 실무 문서를 작성할 때 사용한다. 이사회 회의록, 사업계획서·예산서, 사업실적·결산서, 정관변경, 예결산보고, 재산목록, 감사서, 임원현황 등 서울특별시교육청 소관 비영리법인이  | 2026 공익법인 실무지침서·장학재단·성안나 |
| [transport-receipt-collector](skills/transport-receipt-collector) | 공공기관 출장·여비·교통비 정산에 필요한 하이패스, 코레일, SRT 영수증을 공식 사이트 또는 승인된 제공자 경로에서 수집하고 PDF와 PNG 증빙 파일로 정리할 때 사용한다. |  |

### 논문·학술·독서 (25)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [bgpt-paper-search](skills/bgpt-paper-search) | Searches BGPT scientific papers by topic or DOI and retrieves claim-level evidence extracted from full text, including experiments, reported |  |
| [citation-gate](skills/citation-gate) | 저자 책 학술 신뢰성 cross-cutting 가드. M2 HallucinationDetector + M3 AuthorityGrader + M4 QuantitativeAnchorExtractor 결정론 호출. 5 신호 자동 감지 — Critical 시 |  |
| [hypogenic](skills/hypogenic) | Plans and audits use of ChicagoHAI HypoGeniC/HypoRefine for LLM-assisted hypothesis generation from labeled text datasets. Use for the `hypo |  |
| [hypothesis-generation](skills/hypothesis-generation) | Formulates evidence-bounded scientific questions, candidate hypotheses, rival explanations, causal or associational claims, discriminating p |  |
| [kci-journal-finder](skills/kci-journal-finder) | KCI 등재지·등재후보지 2,888종에서 투고할 학술지를 고르는 스킬. 분야·등급(우수등재/등재/등재후보)·연 발행 횟수·발행 주체·언어로 거르고, 게재료·심사료·투고 마감·투고 시스템(JAMS 등)·대학원생 감면 정보(215종 채움)를 함께 보여 준 | 어디에 투고\·학술지 추천\·등재지 목록\ |
| [keris-academic-search](skills/keris-academic-search) | Use when the user asks to search Korean theses, academic articles, research reports, journals, or university-library catalog metadata throug |  |
| [paper-critical-review](skills/paper-critical-review) | 학술 논문을 까다로운 Reviewer 2 관점에서 적대적으로 심사하거나, 저자·학생을 지도하기 위해 논문의 약점을 사전 진단하는 전문 논문점검 스킬. 초록·본문·결론을 읽고 contribution 요약 → 주장-근거 매핑 → 실험설계 공격 → 재현성  | 논문 심사·논문 리뷰·reviewer 2 |
| [paper-lookup](skills/paper-lookup) | Searches 18 scholarly APIs for papers, preprints, citations, open-access full text, repository records, and journal OA status, and returns r | find papers on X·look up this DOI·who cites this paper |
| [paper-study](skills/paper-study) | 논문을 "능동적으로" 학습하고 마크다운 위키에 축적하는 스킬. 로컬 PDF 논문을 읽고 능동 회상 질문·파인만식 재설명·기존 위키와의 연결을 통해 기억에 정착시킨 뒤, 사용자의 재설명과 연구 적용 아이디어를 포함한 .md 노트로 저장하고 논문/개념 간 | 능동적으로 |
| [paper-writing-master](skills/paper-writing-master) | 논문작성 전 과정(준비·주제·선행연구·연구문제·설계·뼈대·서론·이론적 배경·방법·분석·결론·초록·윤리·심사·투고)을 한국 대학원 학위논문·학술지 논문 기준으로 코칭하고 산출물을 함께 만드는 총괄 스킬. 논준모연구소(김성하) 공개 영상 1,080편 종합 | 논문 써야 해\·논문 처음부터 끝까지\·학위논문 지도\ |
| [paper-writing-order](skills/paper-writing-order) | 논문 13편을 쓴 저자의 '논문 쓰기 순서' 방법론을 기반으로, 논문이 안 써지는 원인을 '쓰는 순서의 오류'로 진단하고 5단계 기획 순서(넓은 주제 → 발췌독 → 인용문 3분류 → 뼈대 세우기 → 서론·결론 쌍)로 논문 작성을 코칭하는 스킬. 사용자 | 논문이 안 써져요\·논문 어디서부터 시작\·주제를 못 잡겠어요\ |
| [paperclip](skills/paperclip) | Searches and reads biomedical papers, FDA/PMDA/EMA documents, clinical trials, and protein records with the GXL Paperclip CLI and Python SDK |  |
| [paperzilla](skills/paperzilla) | Reads projects, searches project feeds, and retrieves recommendations and canonical papers in Paperzilla through the pz CLI. Supports recent |  |
| [peer-review](skills/peer-review) | Prepares evidence-bounded, constructive peer-review drafts and structured manuscript assessments. Supports authorized review of scientific m |  |
| [pyzotero](skills/pyzotero) | >- Manages Zotero reference libraries using the pyzotero Python client: retrieves, creates, updates, and deletes items, collections, tags, a |  |
| [reading-craft](skills/reading-craft) | 책과 긴 글을 "읽고 나서 남게" 읽는 법을 코칭하는 독서 훈련 스킬. 책의 성격을 먼저 판정(지나가는 책·써먹을 책·바꿀 책)하고, 존 스튜어트 밀의 7단계 독서법(해설서→통독→정독→필사→주제 확장→가르치기→쓰기)과 문해력 4단계(낱말 세우기→문장  | 읽고 나서 남게·책을 읽어도 남는 게 없어·독서법 알려줘 |
| [ref-toolkit](skills/ref-toolkit) | 박사논문 레퍼런스 수집 도구 안내·라우팅 스킬. 사용자가 "레퍼런스 수집", "문헌 검색 도구", "Consensus/Elicit/SciSpace 뭐 쓸까", "논문 자료 조사 도구", "레퍼런스 대시보드", "/ref-toolkit"을 요청하면 발동 | 레퍼런스 수집·문헌 검색 도구·Consensus/Elicit/SciSpace 뭐 쓸까 |
| [research-grants](skills/research-grants) | Supports research proposal preparation and review for NSF, NIH, DOE, DARPA, and Taiwan NSTC, including opportunity-specific requirements, ai |  |
| [scholar-evaluation](skills/scholar-evaluation) | Provides qualitative-first, evidence-traceable developmental review of scholarly works and audit low-stakes research-assessment rubrics with |  |
| [scientific-brainstorming](skills/scientific-brainstorming) | Facilitates evidence-aware scientific ideation with independent generation, structured discussion, explicit assumptions, transparent evaluat |  |
| [scientific-critical-thinking](skills/scientific-critical-thinking) | Evaluates scientific claims and evidence quality. Applies to experimental design validity, biases and confounders, statistical interpretatio |  |
| [scientific-writing](skills/scientific-writing) | Drafts, revises, and audits scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship ac |  |
| [talk-to-my-books](skills/talk-to-my-books) | 사용자의 자료(책·설교·주석·강의안 등)를 talk-to-algorithms.vercel.app 방식의 "책과 대화" 형식으로 변환·등록하고, 등록된 자료와 본문 근거 기반 대화를 수행하는 스킬. 두 가지 모드로 작동한다. (1) 등록 모드 — 사용자 | 책과 대화·이 책 등록해줘·이 자료 학습시켜줘 |
| [venue-templates](skills/venue-templates) | Prepares journal manuscripts, conference papers, research posters, and grant documents using venue-specific formatting guidance and bundled  |  |
| [zotero](skills/zotero) | 문헌 관리·인용 | 내 조테로에서 찾아줘·참고문헌 몇 편이야·서지정보 진단 |

### 지식관리·노트 (25)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [alda-report](skills/alda-report) | 알다 로컬 위키(옵시디언 메인 볼트의 내 노트·설교·문헌을 로컬 qwen3:8b·bge-m3로 색인한 것)를 먼저 조회하고 웹검색으로 보강해, 빈틈 분석과 mermaid 개념 지도를 담은 보고서 초안을 PKM/30 output/에 status draf | 알다로 보고서·내 노트 기반 리서치 보고서·알다 리포트 |
| [analog-diary](skills/analog-diary) | 어떤 자료든(사진·그림·유튜브·영상·짧은 글·아이디어) 낡은 종이 위 손판화 스탬프 카드로 변환해 일기장 "스쳐가는 일상"에 발행하는 스킬. 카드 하단에 Location/No./Keywords/Year 타자기 메타를 찍고, Documents\analo | 스쳐가는 일상·그림일기·아날로그 일기 |
| [canvas](skills/canvas) | Create, inspect, and update Obsidian JSON Canvas boards with text, file, link, group, and edge nodes. Use for canvas status, canvas lists, v |  |
| [km-archive-reorganization](skills/km-archive-reorganization) | Use when needing Archive Reorganization Mode (Mode R) - 대규모 vault 폴더 재편을 위한 6-Phase 반복 적용 워크플로우. 얼룩소 프로젝트 4단계를 일반화. |  |
| [km-link-audit](skills/km-link-audit) | Use when needing Knowledge Manager 링크 감사 스킬. Obsidian vault의 broken links, orphan notes, 미해결 참조 감지 및 수정. |  |
| [km-link-strengthening](skills/km-link-strengthening) | Use when needing Knowledge Manager 링크 강화 스킬. Obsidian vault 노트 간 의미적 wikilink 연결 생성 및 백링크 보강. |  |
| [kordoc-obsidian-bridge](skills/kordoc-obsidian-bridge) | 옵시디언 노트와 한글(HWP/HWPX)·PDF 문서를 kordoc으로 왕복시킨다. "hwp를 옵시디언 노트로", "이 공문 노트로 저장", "노트를 hwpx 공문으로", "옵시디언 노트로 보고서 만들어줘" 요청 시 사용. 일반 파싱·생성 자체는 kor | hwp를 옵시디언 노트로·이 공문 노트로 저장·노트를 hwpx 공문으로 |
| [memory-four-cells](skills/memory-four-cells) | 작업 피드백·회의 메모·세션 기록을 교훈·상태·결정·선호 네 칸으로 나눠 ~/Desktop/cysjavis/기억장치/에 쌓고, 거기서 "최근 결정"·"다음 할 일"을 근거 인용과 함께 꺼낸다. "피드백 기록해", "네 칸으로 정리", "최근 결정 정리 | 최근 결정·다음 할 일·피드백 기록해 |
| [nlm-skill](skills/nlm-skill) | Expert guide for the NotebookLM CLI (`nlm`) and MCP server - interfaces for Google NotebookLM. Use this skill when users want to interact wi | nlm\·notebooklm\·notebook lm\ |
| [notebooklm](skills/notebooklm) | Google NotebookLM 완전 API — 웹 UI에 없는 기능까지 프로그래밍 방식으로 접근. 노트북 생성, 소스 추가, 모든 아티팩트 유형 생성, 다양한 형식 다운로드. /notebooklm 명시 호출 또는 "X에 대해 팟캐스트 만들어줘" 같은 |  |
| [pkm-os](skills/pkm-os) | 김병곤의 옵시디언 지식 OS(PKM 폴더: raw→wiki→output 3층 + MOC) 운영 스킬. 유튜브·논문·도서·클리핑·설교자료를 raw에 넣고(ingest), wiki를 근거로 답하고(query), 건강 검진(lint), 세이브 포인트(log |  |
| [save](skills/save) | Save a user-selected answer, decision, insight, or session summary into an Obsidian vault as one reviewed transaction. Use only when the use |  |
| [url-manual-forge](skills/url-manual-forge) | URL 한 줄(YouTube·GitHub·X·웹 글)을 받아 따라 하는 매뉴얼 HTML → 응용·확장 아이디어와 사례 → 나에게 적용하는 법과 사용 실례 → 스킬·설치 가치 판정표 → 옵시디언 노트 → 비공개 아티팩트 발행까지 한 번에 끝낸다. 트리거 | 이 URL로 메뉴얼 만들어줘·메뉴얼 html+응용+나의 적용·스킬 점검하고 옵시디언에 저장 |
| [weekly-review](skills/weekly-review) | 한 주를 데이터 기반으로 회고한다. LLM 위키의 세션 로그·질의 결과·새 자료와 옵시디언 모선 볼트의 이번 주 노트를 모아, 7 재활용 축(설교·목회·논문·강의·저술·AI시스템·인문교양)별 진척과 이번 주의 원싱, 다음 주 우선순위를 정리한다. "주 | 주간 회고·이번 주 회고·한 주 정리 |
| [wiki](skills/wiki) | Initialize, adopt, and route work for a separate Obsidian knowledge vault through the portable claude-obsidian core. Use for vault setup, sc |  |
| [wiki-cli](skills/wiki-cli) | Detect and use the official Obsidian command-line interface for read-only vault access; use for wiki-cli, Obsidian CLI, Obsidian read, Obsid |  |
| [wiki-fold](skills/wiki-fold) | Create a bounded, extractive, structurally idempotent rollup of recent Obsidian wiki log entries, with dry-run preview by default and one op |  |
| [wiki-ingest](skills/wiki-ingest) | Ingest supplied source material into an Obsidian vault with provenance and claim tracking: pasted text, files staged in the selected vault's |  |
| [wiki-lint](skills/wiki-lint) | Run a deterministic, read-only health check on an Obsidian wiki. Use for lint, vault health check, audit wiki health, find orphans, find dea |  |
| [wiki-mode](skills/wiki-mode) | Read or configure the vault filing methodology and suggest destinations for planned knowledge creation under Generic, LYT, PARA, or Zettelka |  |
| [wiki-query](skills/wiki-query) | Answer an explicitly vault-scoped question from an Obsidian wiki without changing it. Use when the user selects the vault as the evidence so |  |
| [wiki-recall](skills/wiki-recall) | 설교·논문·강의·저술 준비를 시작할 때, 백지에서 시작하지 않도록 내 LLM 위키와 옵시디언 모선 볼트에 이미 축적된 지식을 먼저 조회한다. 본문·주제·개념을 받아 관련 위키 페이지·원본 자료·과거 설교/강의 노트를 찾아 요약해 준다. "설교 준비", | 설교 준비·본문 연구·논문 쓰자 |
| [wiki-retrieve](skills/wiki-retrieve) | Build and query a vault-local contextual BM25 retrieval index with optional multilingual Nomic cosine reranking; use for retrieve, hybrid re |  |
| [zettelkasten-note](skills/zettelkasten-note) | Obsidian/Markdown 노트를 제텔카스텐 원칙(원자적 노트·permanent/literature/MOC 구분·wikilink 연결)으로 작성하는 표준 템플릿과 규칙. 자료를 노트로 정리하거나, 노트 형식·frontmatter·태그 체계를 잡거 | 제텔카스텐으로 정리해줘 |
| [통합-data-수집기](skills/통합-data-수집기) | 여러 곳에 흩어진 개인 자료(쓰레드·X·인스타·페이스북·유튜브·블로그·카톡·브라우저 북마크·옵시디언 노트·Claude 아티팩트·폰 자료·외장하드/USB/NAS 파일)를 한 파일로 모으고, 검색·메모·태그·별표·삭제·내보내기가 되는 단일 HTML 보기  | 통합 DATA 수집기·통합 DATA 수집기 만들어줘·통합자료수집기 만들어줘 |

### 커뮤니케이션·원격·협업 (24)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [gws-calendar](skills/gws-calendar) | Google Calendar: Manage calendars and events. |  |
| [gws-calendar-agenda](skills/gws-calendar-agenda) | Google Calendar: Show upcoming events across all calendars. |  |
| [gws-calendar-insert](skills/gws-calendar-insert) | Google Calendar: Create a new event. |  |
| [gws-classroom](skills/gws-classroom) | Google Classroom: Manage classes, rosters, and coursework. |  |
| [gws-docs](skills/gws-docs) | Read and write Google Docs. |  |
| [gws-docs-write](skills/gws-docs-write) | Google Docs: Append text to a document. |  |
| [gws-drive](skills/gws-drive) | Google Drive: Manage files, folders, and shared drives. |  |
| [gws-drive-upload](skills/gws-drive-upload) | Google Drive: Upload a file with automatic metadata. |  |
| [gws-forms](skills/gws-forms) | Read and write Google Forms. |  |
| [gws-gmail](skills/gws-gmail) | Gmail: Send, read, and manage email. |  |
| [gws-gmail-read](skills/gws-gmail-read) | Gmail: Read a message and extract its body or headers. |  |
| [gws-gmail-reply](skills/gws-gmail-reply) | Gmail: Reply to a message (handles threading automatically). |  |
| [gws-gmail-send](skills/gws-gmail-send) | Gmail: Send an email. |  |
| [gws-gmail-triage](skills/gws-gmail-triage) | Gmail: Show unread inbox summary (sender, subject, date). |  |
| [gws-shared](skills/gws-shared) | gws CLI: Shared patterns for authentication, global flags, and output formatting. |  |
| [gws-sheets](skills/gws-sheets) | Google Sheets: Read and write spreadsheets. |  |
| [gws-sheets-append](skills/gws-sheets-append) | Google Sheets: Append a row to a spreadsheet. |  |
| [gws-sheets-read](skills/gws-sheets-read) | Google Sheets: Read values from a spreadsheet. |  |
| [gws-slides](skills/gws-slides) | Google Slides: Read and write presentations. |  |
| [gws-tasks](skills/gws-tasks) | Google Tasks: Manage task lists and tasks. |  |
| [gws-workflow](skills/gws-workflow) | Google Workflow: Cross-service productivity workflows. |  |
| [gws-workflow-meeting-prep](skills/gws-workflow-meeting-prep) | Google Workflow: Prepare for your next meeting: agenda, attendees, and linked docs. |  |
| [gws-workflow-weekly-digest](skills/gws-workflow-weekly-digest) | Google Workflow: Weekly summary: this week's meetings + unread email count. |  |
| [nopal](skills/nopal) | Google Workspace 오케스트레이션 — 자연어로 9개 서비스를 자동 조합 Gmail·Calendar·Drive·Sheets·Docs·Slides·Chat·Tasks·Meet을 gws CLI로 조합한다. 읽기 조회는 바로 실행하고 쓰기·변경은  |  |

### 디자인·UI·웹 (23)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [10k-websites](skills/10k-websites) | Guide a beginner from a brief and simple creative choices to a cinematic scroll-driven website, original OpenArt imagery and video, and a li |  |
| [astryx](skills/astryx) | Astryx, a design system and UI library, is available on this computer through the astryx command; use it when building or changing UI, choos |  |
| [better-accessibility](skills/better-accessibility) | Helps your project comply with accessibility standards and best practices. Covers native elements first, visible focus rings, full keyboard  |  |
| [better-colors](skills/better-colors) | Helps you build a color system and answer anything about color in your project. You can generate palettes, use semantic tokens, convert betw |  |
| [better-typography](skills/better-typography) | Focuses on type scale, spacing, sizing, variable fonts, OpenType features, wrapping, truncation and other details that make typography feel  |  |
| [character-style-prompts](skills/character-style-prompts) | 사진 한 장을 손그림·공작물·인쇄물·기계 출력·게임 화면 캐릭터로 바꾸는 한국어 프롬프트 110개(11시리즈×10) 아카이브. 원본 revfactory/character-comic. "사진을 ~스타일로", "캐릭터 프롬프트", "낙서/질감/변주/유행/ | 사진을 ~스타일로·캐릭터 프롬프트·낙서/질감/변주/유행/시대/기호/도해/기계/거리/무대/게임 스타일 |
| [clone-website](skills/clone-website) | Rebuild existing web pages as working local code, matching their real content, assets, responsive layout, and interactions. Use for website  |  |
| [concept-doodle](skills/concept-doodle) | Use when the user wants a single black-ink doodle / stick-figure concept illustration that explains one topic at a glance — 흰 배경·검은 펜 손그림·졸라 | 개념 일러스트·졸라맨 그림·화이트보드 낙서 |
| [concept-first-web](skills/concept-first-web) | 코드를 쓰기 전에 이미지 모델로 페이지 전체 시안과 움직임 참고를 먼저 만들고, 그것을 HTML/CSS로 다시 지은 뒤 스크립트로 "붙여넣지 않았는지" 검사하는 웹페이지 제작 절차. "시안 먼저", "이미지 먼저 그리고 코드로", "뻔하지 않은 랜딩페 | 붙여넣지 않았는지·시안 먼저·이미지 먼저 그리고 코드로 |
| [design-audit](skills/design-audit) | Jobs/Ive 철학의 프리미엄 UI/UX 디자인 감사관. 기존 UI를 검토·평가·격상할 때 사용 — '디자인 검토해줘', 'UI 리뷰', '프리미엄 느낌으로', 'UX 감사', '기능은 그대로 두고 시각 품질만 올려줘' 요청 시 발동. | audit my design·review UI·make it feel premium |
| [design-dna](skills/design-dna) | >- 레퍼런스 디자인(포스터·스크린샷·이미지·영상 스타일 등 CSS가 없는 시각물)을 "측정 → 논쟁 → 규칙화 → 불량복제 테스트 → 규칙만으로 재현 → 누락 규칙 보강" 루프로 역설계해, 언제든 같은 스타일을 재현할 수 있는 재사용 스킬(~/.cl | 이 디자인 DNA 뽑아줘·이 포스터 스타일 스킬로 만들어줘·이 스타일 복제/재현 가능하게 |
| [design-pick](skills/design-pick) | >- Claude로 PPT·발표자료나 웹사이트를 만들 때, AI 기본 미감(보라 그라디언트·둥근 카드·천편일률)으로 수렴하지 않도록 80가지 검증된 디자인 스타일 팩 중 하나를 골라 그 명세대로 생성하게 하는 스킬. 사용자가 "PPT/슬라이드/덱/발표 | PPT/슬라이드/덱/발표자료·웹사이트/랜딩페이지/UI·디자인 팩 |
| [design-taste-frontend](skills/design-taste-frontend) | tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of 247 curated gallery sites (One Page Love, | AI-made |
| [diagram-design](skills/diagram-design) | > Diagram design reference library (14 types — architecture, flowchart, sequence, state, ER, timeline, swimlane, quadrant, nested, tree, org |  |
| [frontend-design](skills/frontend-design) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typog |  |
| [insane-design](skills/insane-design) | URL 하나로 실제 CSS 기반 디자인 시스템 분석 — design.md + HTML 리포트 생성 인자 없이 실행하면 URL을 묻고, URL을 받으면 실제 CSS를 분석해 design.md와 report.ko.html을 만든다. 트리거: '/insan |  |
| [kbg-infographic](skills/kbg-infographic) | kbg-인포그래픽. 설교 원고·강의 자료·논문을 학회 포스터(EMNLP식 1장 인포그래픽)로 만든다 — 질문형 큰 제목, 다크 히어로 밴드(핵심 숫자 1개+비교 막대+지표 3개+TL;DR), 번호 섹션 2단 그리드, 큰 숫자 콜아웃, 기대 vs 실제  | kbg-인포그래픽·인포그래픽 포스터로·학회 포스터처럼 |
| [layout-design-coach](skills/layout-design-coach) | 디자이너를 위한 레이아웃·구성 가이드(시각적 움직임과 흐름 6단계, 그리드 시스템 13종, LIFT 시스템)를 기반으로 포스터·웹페이지·PPT·배너·인쇄물 등 모든 시각물의 레이아웃을 설계·진단·개선하는 코칭 스킬. 사용자가 "레이아웃 잡아줘", "구 | 레이아웃 잡아줘·구도/구성 봐줘·시선 흐름 |
| [palette-forge](skills/palette-forge) | > 이미지·제품 사진·와디즈 등 커머스 페이지에서 브랜드/제품별 고유 컬러를 추출해 ① 팔레트 HTML 보고서(변형 4단계·대비율·CMYK·PPTX 활용 분석)와 ② 테마 색이 패치된 7슬라이드 PPTX 테마 덱을 만드는 스킬. 사용자가 "팔레트 추출 | 팔레트 추출·컬러 추출해서 정리·이 이미지 색 뽑아줘 |
| [scandinavian-design](skills/scandinavian-design) | Apply a refined Scandinavian visual system with a neutral black-and-white foundation, restrained sans-serif typography, purposeful product i |  |
| [scribble-cityscape](skills/scribble-cityscape) | Use when the user wants a cityscape / street image drawn in dense chaotic scribble line art — 수천 개의 가는 선을 겹쳐 형태·명암·빛·속도를 만드는 도시 풍경(볼펜 낙서풍, 크 | 스크리블 도시·낙서풍 도시·선으로 그린 도시 |
| [ui-ux-pro-max](skills/ui-ux-pro-max) | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, |  |
| [uxui-design-system](skills/uxui-design-system) | UI 의존성 제로로 토스 스타일(클린 핀테크) UX/UI 디자인 시스템을 설계·구현 — 토큰 체계(색·타이포·형태·엘리베이션), 컴포넌트 패턴, 반응형/다크모드/접근성 규칙, 빌드 워크플로우. 새 웹 UI 시작, 일관성 없는 UI 통일, '디자인 시스 | design system·디자인 시스템 |

### 모션그래픽·애니메이션 (22)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [aimotion](skills/aimotion) | 웹 그래픽 표현 기법 참고서 aimotion — 기법 하나당 데모 하나, 데모 166편의 구현 노트와 소스와 그림이 이 스킬 안에 모두 들어 있다. 장면에 맞는 기법을 찾아 원리와 소스를 읽고 지금 만드는 영상에 옮긴다. Use when buildin |  |
| [animate](skills/animate) | UI에 자연스러운 애니메이션·마이크로 인터랙션을 붙이는 스킬. 사용자가 "애니메이션 넣어줘", "호버 효과", "부드럽게 움직이게", "마이크로 인터랙션", "페이지 전환", "스크롤 등장", "Framer Motion", "GSAP", "이징", " | 애니메이션 넣어줘·호버 효과·부드럽게 움직이게 |
| [claude-animation-base](skills/claude-animation-base) | ClaudeAnimationBase 키트로 p5.js와 p5.brush를 써서 손으로 칠한 듯한 수채화풍 캐릭터 단편 영상을 만든다. 기본 캐릭터는 Clawd이고 다른 캐릭터로 바꿀 수 있다. 사용자가 "/claude-animation-base", " | /claude-animation-base·Clawd 애니메이션·p5.brush 영상 |
| [claude-motion-studio](skills/claude-motion-studio) | 편집 프로그램 없이 Claude가 코드(HTML+GSAP)로 모션그래픽 영상을 만드는 작업대. 입력 5종(대사+초 / 참고 영상 / 음악 / 나레이션+이미지 / 광고 브리프·웹사이트)과 프롬프트 사다리(한 문장 → 4블록 구조 프롬프트 → 스타일 팩  | 모션그래픽 만들어줘·대사에 맞춰 모션·음악에 맞춰 모션 |
| [design-to-motion](skills/design-to-motion) | Turns a static design (a Figma frame, dashboard, card set, app screen, or a UI on a photo background) into a pixel exact HTML replica that l | animate this\ |
| [explainer-default](skills/explainer-default) | Make a clean 45–90 second product demo video for any software product, rendered from code to MP4 with music. Airy light canvas, short centre | how it works |
| [explainer-engaging](skills/explainer-engaging) | Make a 10–30 second continuous-shot explainer for any product, rendered from code to MP4 with sound. One hero element (a ball, a cursor, a f |  |
| [explainer-high-energy](skills/explainer-high-energy) | Make a 12–20 second high-energy motion-graphics promo for any product, rendered from code to MP4 with synthesised music. Fast beat-locked sc |  |
| [manim-video](skills/manim-video) | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style explainer videos, alg |  |
| [mg-styles-15](skills/mg-styles-15) | mg-styles-15 저장소의 15가지 스타일 프롬프트로 코드만 써서 약 10초 모션 디자인 영상을 만든다. 플랫 벡터, 라인 아트, 아이소메트릭, 3D, 셀 애니메이션, 콜라주, 리퀴드, 모프, 바우하우스, 신스웨이브, 오로라 글래스, 예능 자막, | /mg-styles-15·mg-styles |
| [motion-broll](skills/motion-broll) | Turn a talking-head video and its transcript into motion-graphic B-roll timed to the speaker's words, in a continuous one-shape style (one e |  |
| [motion-design](skills/motion-design) | Code-only motion design pipeline (no After Effects) for Raphaël / Howseen: launch films, showreels, product promos, LinkedIn/X videos, meme  | remake this video\·make a 15s motion graphics video…\ |
| [motion-order-sheet](skills/motion-order-sheet) | 모션그래픽 "주문서"(촬영대본식 영상 생성 프롬프트)를 쓰는 스킬. 내 내용을 넣어 장면 순서·초 단위 타이밍·움직임·모양·색·금지 조건까지 적은 '자세히' 프롬프트를 만들고, 참고 영상(URL·파일)을 역분석해 같은 스타일의 프롬프트로 바꾼다. 결과 | 주문서·모션 주문서·키네틱 타이포 프롬프트 |
| [motion-tone-qa](skills/motion-tone-qa) | 코드로 만든 모션 영상을 "톤 카드 + 숫자 검수"로 출고 전에 재는 스킬. 참고 영상 몇 편을 재서 톤 카드(밝기·컷 간격·움직임·정지 허용·음량 목표)를 저장하고, 결과물을 같은 자로 재서 PASS/FIX를 낸다. 1초 넘는 정지, 대본에 없는 숫 | 톤 카드 + 숫자 검수·톤 카드 / 숫자 검수 / 톤 측정 / 영상 수치 검사 / 컷 속도 확인 |
| [motion-video-production](skills/motion-video-production) | Plan and assemble 30–90 second motion graphics and character videos with six production stages, media gates, and visual review. Use for vide |  |
| [opus-motion-playbook](skills/opus-motion-playbook) | Claude Opus 5.5로 모션그래픽을 만드는 원리 74개 플레이북. 프로젝트 지침 8섹션(고정 규칙/변수 분리·제작 전 검증 관문), 박자 계층(128BPM 8마디=15초, 강박·박·8분·16분·히트), seek(t) 렌더 공학(순수함수·닫힌형  | 모션그래픽 원리·오퍼스 모션·박자에 맞춰 |
| [raea](skills/raea) | Make video, motion graphics, games and 3D scenes with raea, the Render Anything Engine, by writing React/TypeScript compositions with raea a |  |
| [raea-bevy](skills/raea-bevy) | Writing 3D scenes and 3D games in raea's TypeScript SDK (raea/3d), which Bevy 0.20 draws, and extending that SDK. Use when writing or fixing |  |
| [remotion](skills/remotion) | React 기반 Remotion 영상 제작 모범 사례 — 컴포지션, 시퀀스, 애니메이션, 타이밍, 렌더링. Remotion 영상을 만들거나 리뷰·디버깅할 때 사용. |  |
| [remotion-kr](skills/remotion-kr) | 공식 Remotion 스킬(remotion-best-practices 등 12종)을 보완하는 한국어 로컬 보강. 한국어 예제 갤러리 44개 지도·Pretendard 고정·"참고 코드 + :: 정확 명령" 요청 틀, 그리고 공식 스킬에 없는 차트·텍스트 | 참고 코드 + :: 정확 명령 |
| [stick-scene](skills/stick-scene) | Make small hand-drawn stick-figure scenes for landing pages and sites, where a stick figure works a machine or prop that shows what a produc | worker·crew·like the stick figures on my story page |
| [vox-paper-motion](skills/vox-paper-motion) | Vox식 종이 콜라주 모션그래픽(찢어진 종이·4색 팔레트·주인공 강조·신문 조각·2.5D 패럴랙스·점선 항로·지도 기울이기·망점 마감)을 "이미지는 AI로 몇 장, 영상은 코드로 조립"하는 방식으로 만든다. 원리 60여 개(영상 출처+확장)와 도감 2 | 이미지는 AI로 몇 장, 영상은 코드로 조립·Vox 스타일·복스 스타일 |

### 비즈니스·재무·법무·HR (20)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-visa-lens](skills/agent-visa-lens) | 에이전트 커머스(대신 사고·예약하고·송금하는 AI 에이전트) 아이디어, 제품, 뉴스, 투자 건을 "신원·위임·보증" 세 축과 "마지막 클릭은 누구의 권한인가" 질문으로 진단한다. 사용자가 에이전트 결제/예약/송금/구매 대행, 플랫폼의 에이전트 차단,  | 신원·위임·보증·마지막 클릭은 누구의 권한인가·비자 렌즈로 봐줘 |
| [biz-health-check](skills/biz-health-check) | 사업자등록번호 하나로 "이 사업자, 실제 문제 없나"를 확인한다 — 국세청 사업자등록 상태·국민연금 가입 사업장·국세 체납 명단·금융위 법인개요·조달청 부정당제재·지방행정 인허가 영업상태를 무료 공공 데이터로 교차 조회해 사실만 병렬하는 실사 리포트( | 이 사업자, 실제 문제 없나 |
| [contract-review-kr](skills/contract-review-kr) | 한국 계약서(용역·강의 위촉·출판·임대차·협약서·MOU)를 조항별로 검토해 위험도(높음·중간·낮음) 보고서와 원본 보존형 수정 제안본을 만든다. 근거 조문은 korean-law MCP로 조회·검증한다. "계약서 검토해줘", "이 계약 괜찮아?", "불 | 계약서 검토해줘·이 계약 괜찮아?·불리한 조항 |
| [corporate-registration-consulting](skills/corporate-registration-consulting) | 법인등기소/인터넷등기소 상업등기 신청을 처음 하는 사용자를 위해 일반 영리 주식회사 발기설립 절차, 정관·첨부서류 실제 HWP 양식 작성, 등록면허세·과밀억제권역 중과 체크, rhwp 기반 순차 검토 흐름을 참고용으로 안내한다. 돌쇠에서는 가능한 가장 |  |
| [court-payment-order-assistant](skills/court-payment-order-assistant) | 법원 전자소송 지급명령 신청을 위해 채권자·채무자·청구금액·청구원인·증빙 정보를 인터뷰하고, 신청서 초안과 공식 전자소송 브라우저 입력 handoff를 준비한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [expense-receipts](skills/expense-receipts) | 영수증 사진을 읽어 경비 정리표(엑셀, 분류별 원그래프 포함)를 만든다. "영수증 정리", "경비 정리표", "경비 청구", "교회 지출 정리", "부서 회계 정리" 요청이나 영수증 사진 여러 장이 올라왔을 때 사용. 원본: 혼잡스 「모조리 자동화 # | 영수증 정리·경비 정리표·경비 청구 |
| [fsc-corporate-info](skills/fsc-corporate-info) | 금융위원회 기업기본정보(법인 개요)를 공공데이터포털 API(k-skill-proxy 경유)로 조회한다. 법인명으로 대표자·설립일·업종 등 법인 개요를 확인하고, 응답에 사업자번호가 있으면 입력 번호와 교차검증한다. |  |
| [iros-registry-automation](skills/iros-registry-automation) | 인터넷등기소(IROS)에서 법인/부동산 등기부등본(등기사항증명서) 발급을 준비하고, 사용자가 직접 로그인·결제한 브라우저 흐름 안에서 장바구니·열람·저장을 안전하게 보조한다. 돌쇠에서는 가능한 가장 가까운 합법적 공식 단계까지 준비한다. |  |
| [jangbu-connect](skills/jangbu-connect) | 홈택스·은행·카드사 데이터를 자동 수집하기 위한 CODEF API 자격증명 발급·설정 가이드 스킬. 사용자가 직접 CODEF(developer.codef.io)에 무료 가입해 받은 Client ID/Secret을 로컬(macOS Keychain 또는  |  |
| [jangbu-dash](skills/jangbu-dash) | 스타트업·1인 법인 대표용 경영 리포트 자동 생성 스킬. 월별 손익 추이, 현금흐름(일별 net), cash burn rate(최근 N개월 평균 순지출), 비용 구조 분석. 공식 재무제표와 별개로 의사결정용 가공 리포트 제공. |  |
| [jangbu-import](skills/jangbu-import) | 원본 재무 데이터(엑셀·은행 CSV·카드 내역 CSV·영수증 이미지·세금계산서 PDF·카드명세서 PDF)를 표준 거래내역 13개 필드로 변환하는 스킬. PaddleOCR 로컬 처리로 영수증·세금계산서·카드명세서에서 거래 자동 추출, Level 2 민감 |  |
| [jangbu-jongso](skills/jangbu-jongso) | 한국 종합소득세·법인세 신고 준비를 위한 서류 체크리스트 자동 생성 스킬. 개인사업자(일반·간이·면세)·프리랜서·1인 법인·겸업·성실신고확인대상 5가지 유형별로 필요 서류 목록을 제공하고, korean-jangbu-for에서 자동 생성 가능한 항목을  |  |
| [jangbu-tag](skills/jangbu-tag) | 표준 거래내역에 계정과목을 매핑하는 스킬. 룰 기반 분류 우선(80%+), 실패 건만 LLM fallback(마스킹 뷰), 사용자 확인 루프. 한국 거래처 100개 시드 룰 포함, 내부 계정 ↔ 국세청 표준계정 이중 구조. |  |
| [jangbu-tax](skills/jangbu-tax) | 세무용 재무제표(재무상태표·손익계산서) 자동 생성 스킬. 국세청 표준계정과목 매핑, 일반기업회계기준(K-GAAP) 간소화 버전. 분류 완료된 거래내역을 기간 지정해 BS·PL로 집계하고 JSON·CSV 파일로 출력. |  |
| [korean-jangbu-for](skills/korean-jangbu-for) | kimlawtech/korean-jangbu-for (Apache-2.0) 업스트림을 중심으로 한국 스타트업·1인 법인·프리랜서·개인사업자 장부 자동화와 사업자 세무 자료 정리, 원본 데이터 가져오기, 계정과목 태깅, 세무사 전달 CSV, 경영 리포트 |  |
| [korean-privacy-terms](skills/korean-privacy-terms) | kimlawtech/korean-privacy-terms (Apache-2.0) 업스트림을 경유해 Next.js 프로젝트에 한국 법령(개인정보보호법·약관규제법·전자상거래법) 기반 개인정보처리방침·이용약관·쿠키 배너·동의 모달을 생성하는 thin wra |  |
| [notice-letter-kr](skills/notice-letter-kr) | 대금 미지급·계약 불이행·반환 요구 거부 등에서 사실 기반 내용증명 초안, 사실확인표, 발송 전 점검표 3종을 만든다. 근거 조문은 korean-law MCP로 검증한다. "내용증명 써줘", "돈을 못 받았어", "최고서", "이행 촉구" 요청 시 발 | 내용증명 써줘·돈을 못 받았어·최고서 |
| [popbill](skills/popbill) | 팝빌 전자세금계산서·전자명세서·현금영수증·문자·카카오톡·팩스·휴폐업/기업정보·계좌조회·홈택스 수집을 테스트/운영 환경에서 안전하게 호출한다. 돌쇠에서는 공식 표면을 통한 후속 액션까지 진행한다. |  |
| [reversebusiness](skills/reversebusiness) | 사업 웹사이트 주소 하나를 받아 그 사업을 해부한다(reversebusiness, rebiz). 사용자가 "이 사업 해부해 줘", "이 서비스 분석해 줘", "이 사업 어떻게 돈 버는지 읽어 줘", "역공학으로 비즈니스 읽기", "똑같이 만들어 줘", | 이 사업 해부해 줘·이 서비스 분석해 줘·이 사업 어떻게 돈 버는지 읽어 줘 |
| [subscription-arrears-audit](skills/subscription-arrears-audit) | Gmail 최근 N개월(기본 3개월) 영수증·구독·결제실패 메일을 읽기 전용으로 훑어 ①새는 구독료 ②결제 실패·연체·독촉 ③무료체험 종료·갱신 예정을 표로 정리한다. "구독료 점검", "안 쓰는 구독 찾아줘", "미납·연체 확인", "결제 실패 메일 | 구독료 점검·안 쓰는 구독 찾아줘·미납·연체 확인 |

### 리서치·심층조사 (17)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [agent-reach](skills/agent-reach) | 인터넷에서 무언가를 조사·검색해야 할 때 사용하는 스킬. 특정 플랫폼(샤오홍슈, 트위터/X, 빌리빌리, Reddit, Facebook, Instagram, V2EX, LinkedIn, YouTube, GitHub 코드검색, 팟캐스트, 주식 시세, RS |  |
| [autoresearch](skills/autoresearch) | Run a bounded, source-grounded research loop, draft a cited dossier, and optionally propose a separately reviewed canonical vault merge. Use |  |
| [consciousness-council](skills/consciousness-council) | Structures a multi-perspective council exercise for decisions, research trade-offs, and creative challenges. Simulates thinking archetypes,  | mind council |
| [council](skills/council) | 지성 위원회 소집 — 역사적 사상가들의 다중 페르소나 숙의로 복잡한 문제를 더 깊이 분석. |  |
| [daily-radar-magazine](skills/daily-radar-magazine) | 관심 대상(브랜드·조례/입법예고·정책·교계 소식·학술지·시세)을 매일 정해진 시각에 자동 조사하고, 공식 출처로 교차 확인한 뒤 '오늘의 매거진' HTML 한 장으로 묶어 같은 아티팩트 URL에 갱신 발행하는 레시피. "매일 아침 9시에 ~ 모아서 알 | 매일 아침 9시에 ~ 모아서 알려줘·신제품/새 조례/입법예고 레이더·모니터링 결과를 매거진 웹으로 |
| [deep-interview](skills/deep-interview) | ／ 모호한 요청을 소크라테스식 질문으로 인터뷰해 실행 가능한 요구사항으로 정리한다. 사용자가 deep-interview, 심층 인터뷰, 요구사항 명확화, 생각 정리를 요청하거나 목표, 범위, 제약, 완료 기준이 흐릿할 때 사용한다. 요청이 이미 구체적 |  |
| [deep-research](skills/deep-research) | AI 딥리서치 -- 멀티에이전트 기반 종합 리서치 시스템 주제를 받아 범위 설정→멀티에이전트 검색→출처 검증→종합 보고서로 진행하고, resume·status로 이전 리서치 세션을 이어 간다. 트리거: '딥리서치', '깊게 조사해줘', '종합 리서치' |  |
| [deep-research-pro](skills/deep-research-pro) | 출처 있는 심층조사와 판단 브리프가 필요할 때 사용하는 OpenClaw 맞춤 리서치 스킬. 단순 검색 답변이 아니라 정책·시장·기업·기술·제도·문헌·공공기관 보고서 근거를 여러 출처로 교차확인하고, 출처 등급·첨부 PDF 확인·반대검토·합의점/쟁점·의 |  |
| [exa-search](skills/exa-search) | Searches scientific and technical web content with Exa and extracts page or PDF text from URLs in batches. Supports scholarly discovery with |  |
| [geeknews-search](skills/geeknews-search) | GeekNews public RSS/Atom feed로 긱뉴스 게시물을 조회, 검색, 상세 확인하는 읽기 전용 스킬. 공개 RSS 피드로 최신 글 목록·키워드 검색·항목 상세를 읽기 전용으로 조회한다. 트리거: ''긱뉴스 오늘 뭐 올라왔어'', ''긱 |  |
| [grill-me](skills/grill-me) | 지시·계획의 의도 파악이 불충분할 때 합의에 이를 때까지 구조화 질문을 반복하는 의도 합의 스킬(work management 앵커 c). "의도 확인 / 의도 합의 / grill me / 계획 검증 질문 / 뭘 원하는지 모르겠다" 트리거로 발동 |  |
| [insane-search](skills/insane-search) | 차단된 웹사이트 적응형 접근 — 되는 방법이 나올 때까지 모든 수단을 시도. WebFetch가 402/403/차단될 때, X/Twitter·Reddit·YouTube·GitHub·Medium·Substack·네이버·쿠팡·LinkedIn 등 WAF/봇  |  |
| [last30days](skills/last30days) | 최근 30일의 Reddit + X + 웹에서 어떤 주제든 조사해 종합하고, 복붙 가능한 프롬프트로 정리. '요즘 사람들이 X에 대해 뭐라고 해?', 최신 모범 사례 학습 요청 시 사용. 전체 기능엔 OPENAI_API_KEY/XAI_API_KEY 필요 | what are people saying about X |
| [market-research-reports](skills/market-research-reports) | Builds evidence-traceable market research reports and assumption-driven market sizing or forecast scenarios. Use for market definition, indu |  |
| [parallel-web](skills/parallel-web) | Uses Parallel CLI for web search, URL extraction, deep research, structured data enrichment, entity discovery, and recurring web monitoring. |  |
| [research-sources](skills/research-sources) | When the user wants to find information sources for content ideation, competitor monitoring, or industry tracking. Also use when the user me | research sources,·information sources,·content ideation, |
| [what-if-oracle](skills/what-if-oracle) | Supports structured what-if scenario analysis for research planning, experimental contingencies, and scientific project decisions. Explores  |  |

### 목회·교회 사역 (16)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [ai-license-3day](skills/ai-license-3day) | AI 입문자에게 '3일 AI 면허' 코스(정거장 9개 + 보너스 커넥터)를 대상 맞춤으로 만들어 주는 교육 설계 스킬. 청중(교사·목회자·교인 시니어·사회복지사·청년·소상공인 등)과 시간(90분 특강/3일 과정/소그룹 3회)을 받아 정거장별 미션 카드 |  |
| [announcement-script](skills/announcement-script) | 주일 아침 광고용 60~90초 구두 안내 대본 작성. 대화체, 우선순위 정리, 최대 3~4개 항목. 아무도 졸지 않는 광고. |  |
| [church-admin-assistant](skills/church-admin-assistant) | 교회행정 비서. 첨부된 연간계획(CSV)·교회요람·문체가이드를 근거로 주보 광고, 교회소식, 카톡·문자 공지, 행사 안내문, 월간 일정표, 일정·장소 문의 답변을 쓴다. 파일에 없는 날짜·시간·장소는 지어내지 않고 [확인 필요]로 표시한다. "주보 광 | 주보 광고 써줘·이번 주 교회소식·11월 일정 정리 |
| [church-comment-reply](skills/church-comment-reply) | 교회에 달린 댓글·후기·문의(유튜브 설교 영상 댓글, 인스타·페이스북 댓글, 카카오 채널 문의, 구글 지도 리뷰)에 답글 초안을 3가지 버전으로 쓴다. "댓글 답글 써 줘", "이 문의에 답장", "리뷰 답글" 요청이나 댓글 캡처를 받았을 때 쓴다. | 댓글 답글 써 줘·이 문의에 답장·리뷰 답글 |
| [church-email](skills/church-email) | 주간 교회 이메일 완성본 작성. 제목·미리보기 텍스트·본문까지. 따뜻하고 훑어보기 좋고 모바일 친화적. 광고와 행사 내용을 붙여넣으면 바로 보낼 수 있는 이메일이 나온다. |  |
| [church-letter](skills/church-letter) | 모든 상황에 맞는 교회 서신 작성. 리더십 교체, 시설 안내, 정책 변경, 환영 편지, 민감한 소통까지. 상황에 맞는 무게감을 갖춘 목회적 어조. |  |
| [church-social-post](skills/church-social-post) | 교회용 플랫폼별 SNS 게시물 작성. 주제·행사·성경구절을 주면 Facebook·Instagram·Twitter용 캡션과 이미지 제안을 플랫폼별로 최적화해 돌려준다. |  |
| [meeting-agenda](skills/meeting-agenda) | 시간 블록·토론 질문·액션아이템 프롬프트가 있는 구조화된 회의 안건 작성. 교역자 회의, 장로회, 제직회, 봉사자 모임에 사용. |  |
| [midweek-devotional](skills/midweek-devotional) | 이메일이나 앱으로 보내는 짧은 주중 묵상글(200~300단어) 작성. 성경 기반, 개인적, 따뜻한 톤. 주일과 주일 사이 성도들과의 연결을 유지. |  |
| [next-gen-ministry-bible](skills/next-gen-ministry-bible) | 『다음세대 목회 바이블 — 일곱개의 사랑이 만드는 한 해의 기적』(안세주 저, 총회 교육훈련처, 7 LOVE Project) 전체를 기반으로 교회학교·다음세대 사역을 설계하는 스킬. 12개월 상세 로드맵(1월 RESET~12월 LOVE CELEBRAT | 다음세대·교회학교 프로그램·주일학교 |
| [pastor-ai-safety-guide](skills/pastor-ai-safety-guide) | 목회자를 위한 인공지능 안전 활용 가이드 스킬. 『인공지능 안전 활용 가이드북 50선』을 기반으로 (1) 목회 업무에 맞는 안전 프롬프트 처방(50선 라이브러리 + 안전 강화판), (2) AI 산출물의 환각·이단성·비성경적 요소 검증, (3) AI 입 | AI 안전 가이드·인공지능 안전 활용·안전 프롬프트 |
| [pastor-foundation](skills/pastor-foundation) | 모든 목회자 AI 스킬의 공유 컨텍스트 레이어. 신학적 가드레일, 목회적 어조, 교회 컨텍스트 변수, 산출물 표준을 설정한다. 다른 작업 스킬과 함께 설치. |  |
| [pastoral-prompt-engineering](skills/pastoral-prompt-engineering) | 이경석 저 『목회 프롬프트 엔지니어링』(2026) 기반의 목회·사역용 프롬프트 설계 스킬. 목회 현장의 문서·기획·교육·연구·미디어·로컬비즈니스 과업을 CRIT/BAB/CARE/RISE/RTF 프레임워크와 골든 프롬프트 50선 템플릿으로 처리한다. 트 | 목회 프롬프트·골든 프롬프트·프롬프트 짜줘/설계해줘 |
| [school-ministry-radar](skills/school-ministry-radar) | 교회학교·청소년부·청년부 사역을 지역 학교 데이터와 맞물리게 하는 레시피 스킬. 이미 설치된 korean-school MCP(우리학교 알리미, mcp.gomdori.app/school)로 출석 학생들 학교의 시험기간·학사일정·학교 규모를 모아 ① 수련 | 시험기간 피해서 수련회·우리 아이들 학교 시험 언제·교회학교 학사일정 |
| [small-group-questions](skills/small-group-questions) | 주일 설교 기반 주간 소그룹 토론 질문 생성. 관찰→해석→적용 흐름. 아이스브레이커와 마무리 기도 제목 포함. 소그룹 리더에게 바로 전달 가능. |  |
| [social-media-calendar](skills/social-media-calendar) | 1주 또는 1개월치 SNS 콘텐츠를 날짜별로 생성. 다가오는 설교·행사·강조점을 주면 게시물 아이디어·유형·플랫폼 배정이 있는 구조화된 캘린더를 돌려준다. |  |

### 특허·지식재산 (11)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [claim-drafting](skills/claim-drafting) | 한국 특허 청구범위 작성·보정 절차. 독립항에 넣을 필수 구성 선정, 종속항 단계 배치, 물건·방법·용도 범주 설계, 한국 청구항 문체('~를 포함하고, ~를 특징으로 하는'), 선행 근거('상기'), 수치 한정과 측정법 연결, 거절 이유에 맞춘 보정 |  |
| [filing-strategy](skills/filing-strategy) | 특허 출원 전략과 일정 수립 절차. 권리 형태(특허·실용신안·디자인) 선택, 국내·PCT·파리조약 경로와 국가 선택, 우선권·공지예외·심사청구·국내단계 기한 계산, 우선심사 검토, 출원 전 공개 통제와 실시권자 접촉 순서를 날짜가 들어간 일정표와 체크 |  |
| [fto-analysis](skills/fto-analysis) | 자유실시(FTO)·침해 위험 분석 절차. 존속 중인 특허·실용신안·디자인을 국가별로 추리고, 청구항 구성과 실시 예정 제품을 구성요소 완비 원칙과 균등 요건으로 대비해 위험 등급, 회피 설계, 자유롭게 쓸 수 있는 소멸 기술을 정리한다. FTO 분석, |  |
| [invention-disclosure](skills/invention-disclosure) | 발명 발굴과 발명신고서(직무발명 신고서) 작성 절차. 아이디어 메모·회의록·기술 문서·기존 조사 보고서에서 기술 과제, 해결 구성, 작동 원리, 효과, 변형 실시 형태를 뽑고, 발명 단위를 나누며, 발명 후보를 재료·구조·공정·용도 축으로 넓힌다. 발 |  |
| [korean-patent-search](skills/korean-patent-search) | Search Korean patent and utility-model publications through the official KIPRIS Plus Open API with keyword search plus application-number de |  |
| [patent-orchestrator](skills/patent-orchestrator) | 특허 발굴과 특허 출원 준비를 15개 전문 에이전트로 조율한다. 기존 선행기술 조사 보고서(PDF·Markdown) 검토·정리, 아이디어·기술 문서에서 발명 발굴, 선행기술 조사와 인용 문헌 검증, 신규성·진보성 판단, 자유실시 위험 분석, 발명신고서 |  |
| [patent-qa](skills/patent-qa) | 특허 출원 서류 형식·일관성 검사 절차. 청구항 번호·종속 관계·다중 종속·선행 근거('상기')·불명확 표현·수치 한정을 스크립트로 검사하고, 명세서의 필수 항목·문단 번호·도면 부호·도면 언급·청구항 용어 뒷받침을 대조하며, 청구항-명세서-도면 대응 |  |
| [patent-report](skills/patent-report) | 특허 발굴·출원 결과 보고서 편집 절차. 검증 원장, 특허성 판단, 자유실시 분석, 청구항, 모의 심사, 시험 계획, 출원 일정을 모아 의사결정자와 변리사가 읽을 한국어 보고서(기존 보고서 검토 결과, 발굴 결과 요약, 출원 준비 패키지 안내)를 만든 |  |
| [patentability-analysis](skills/patentability-analysis) | 특허 신규성·진보성 판단 절차와 기준. 발명을 구성 요소로 나누고 선행문헌 대비표(클레임 차트)를 만들어 한국 심사기준(특허법 제29조)으로 신규성·진보성을 판단하고, 심사관 결합 논리와 출원인 반론, 필요한 증거, 후보 간 비교 등급을 정리한다. 특 |  |
| [prior-art-search](skills/prior-art-search) | 특허 선행기술 검색과 인용 문헌 서지 검증 절차. 키워드·분류코드(IPC/CPC/F-term)·출원인·인용 추적으로 KR·JP·US·CN·EP·WO 문헌을 찾고, Google Patents 원문에서 번호·출원인·날짜·법적 상태·청구항을 스크립트로 가져 |  |
| [spec-drafting](skills/spec-drafting) | 한국 특허 출원 명세서와 도면 작성 절차. 발명의 명칭, 기술분야, 배경기술, 선행기술문헌, 해결하려는 과제, 과제의 해결 수단, 발명의 효과, 도면의 간단한 설명, 발명을 실시하기 위한 구체적인 내용(실시예·비교예), 부호의 설명, 요약서를 서식 순 |  |

### 웹툰 제작 (7)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [insta-toon](skills/insta-toon) | 어떤 글이든(설교·묵상·강의·아이디어·기록) 1~4컷 인스타툰(4:5)으로 변환하는 스킬. 말풍선과 한글 대사를 이미지에 함께 굽고(in-image 베이크), 렌더 후 스스로 눈으로 검수해 오탈자·일관성 미달이면 재생성한다. 스타일 앵커 이미지를 주면 | 인스타툰·네컷 만화·카드툰 |
| [webtoon-assembly](skills/webtoon-assembly) | 웹툰 조립·레터링·검수·패키징 방법론. 렌더된 패널 PNG(말풍선·한글 대사가 이미지에 베이크됨)를 세로 스크롤 뷰어(index.html)로 오버레이 없이 조립하고, letterer의 말풍선/레터링 베이크 명세(대사·생각·외침·나레이션)를 설계하며,  |  |
| [webtoon-orchestrator](skills/webtoon-orchestrator) | 웹툰 제작 에이전트 팀(27명)을 조율하는 메인 오케스트레이터. 인기 웹툰 트렌드 조사 → 대사 위주·고긴장·매 회차 반전 시나리오 작성 → 캐릭터 다각도 레퍼런스 시트를 먼저 렌더 → 회차당 50+ 패널을 말풍선·한글 대사 in-image 베이크로  |  |
| [webtoon-panel-breakdown](skills/webtoon-panel-breakdown) | 웹툰 대본을 50+ 패널 샷리스트로 분해하고, 작화 스타일 가이드와 캐릭터 일관성 토큰을 정제하는 비주얼 프로덕션 방법론. 패널 분해, 샷리스트, 웹툰 콘티/연출, 세로 스크롤 구성, 카메라 앵글/구도 어휘, 스타일 가이드(스타일 바이블), 캐릭터 시 |  |
| [webtoon-panel-render](skills/webtoon-panel-render) | 웹툰 패널 이미지를 codex-image(codex exec image_generation)로 동시 5장씩 병렬 렌더링하는 스킬. 패널 렌더 전 캐릭터 다각도 레퍼런스 시트를 먼저 렌더해 일관성 기준을 만들고, 패널 프롬프트 목록(ep{NN}_prom |  |
| [webtoon-scenario](skills/webtoon-scenario) | 웹툰 시나리오·스토리·대본을 설계/집필할 때 반드시 사용한다. 하이콘셉트/로그라인, 세계관, 캐릭터, 시리즈 아크와 회차 맵, 매 회차 반전 설계와 복선, 긴장 곡선과 클리프행어, 대사 위주 회차 대본, 50+ 패널 비트 분할, 캐릭터 외형 토큰화를  |  |
| [webtoon-trend-research](skills/webtoon-trend-research) | 웹툰 트렌드 리서치 방법론. 웹툰 트렌드 조사, 인기 웹툰 분석, 장르 동향 파악, 플랫폼 랭킹·연재 구조 조사, 독자층·댓글 반응 분석, 후킹·클리프행어·반전 메커니즘 역설계, 기획 인사이트 브리프 종합을 수행할 때 반드시 사용한다. '웹툰 트렌드  |  |

### 성경 연구·묵상 (6)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [bible-study-lesson-plan](skills/bible-study-lesson-plan) | 활동이 아니라 본문이 먼저인 60분 성경공부 교안(도입5-관찰15-해석15-적용15-기도10)을 설계하는 보조 스킬. 교사가 확정한 8개 입력(본문 범위·번역본, 앞뒤 문맥 2문장, 교사가 직접 관찰한 3가지, 본문 핵심 주장 1문장, 하나님이 하신  | 성경공부 교안·성경공부 교재/커리큘럼·60분 성경공부 |
| [pauline-law-hermeneutics](skills/pauline-law-hermeneutics) | 이진섭 교수의 「바울과 율법」(Canon & Culture 5/2, 2011)·「'새 관점'과 '옛 관점'」(성경과 교회 9/1, 2011)과 박사논문("The Law of Faith in Romans", Brunel 2006)에 기반한 율법 해석·적 | 바울과 율법·'새 관점'과 '옛 관점'·The Law of Faith in Romans |
| [pbs-easy-study](skills/pbs-easy-study) | 이재천 저 『개인성경연구핸드북』(IVP)의 PBS(Personal Bible Study) 방법론을 짧은 시간 안에 부담 없이 실천하도록 돕는 간편 코칭 스킬. 관찰(개관→탐색→흐름정리) → 해석(배경→내용전개→핵심메시지) → 적용(적용상황분석→적용점정 | 개인성경연구·PBS·관찰 해석 적용 |
| [pbs-graduate-study](skills/pbs-graduate-study) | 이재천 저 『개인성경연구핸드북』(IVP)의 PBS(Personal Bible Study) 방법론을 신대원 주해 세미나 수준으로 전체 구현한 심화 코칭 스킬. 문예적-역사적-신학적 해석 원리, 귀납법/연역법을 절충한 "관찰-해석-적용" 해석학적 틀, 성 | 관찰-해석-적용·대학원 수준 성경연구·정식으로 제대로 |
| [pbs-personal-bible-study](skills/pbs-personal-bible-study) | 이용세 『개인성경연구』(PBS, 성서유니온)의 귀납적 방법으로 성경 본문을 5단계(외부관찰→내부관찰→객관적 해석→적용적 해석→적용)로 직접 연구해 연구노트를 완성하도록 돕는 코칭 스킬. 단계별 관찰·해석·적용 방법(해석 원리, 적용 원리와 잘못된 적용 | 개인성경연구·PBS·귀납적 성경연구 |
| [romans-meditation-study](skills/romans-meditation-study) | 라종렬 편저 《묵상을 위한 로마서 주해》(대구부광교회)와 이진섭 교수(에스라성경대학원대학교 신약학)의 ''믿음의 법''(νόμος πίστεως) 신학 체계를 기반으로, 로마서(및 갈라디아서) 본문의 묵상 주해·설교 준비·본문 분석을 수행하는 전문 스 | 로마서 묵상·로마서 주해·로마서 ○장 분석/설교 |

### 생산성·유틸리티 (1)

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [folder-tidy-recipes](skills/folder-tidy-recipes) | 폴더 하나를 대상으로 하는 사무 정리 레시피 3종 — (1) 다운로드·스캔 폴더를 삭제후보/보관추천/확인필요로 분류만 하고 승인받기, (2) 영수증·증빙 사진을 엑셀로(확인필요·중복의심 표시), (3) 파일명 일괄 규칙 변경(전후 대조표). "다운로드 | 다운로드 폴더 정리·영수증 엑셀로·파일명 바꿔줘 |

## 별도 저장소

- [awesome-ai-motion](https://github.com/sk01020432947-oss/awesome-ai-motion)
- [motion-web](https://github.com/sk01020432947-oss/motion-web)

## 수록하지 않은 것

원 저장소가 따로 있는 스킬 14개는 원 저장소에서 받으세요(목록은 아래). 영상·5MB 초과 파일·환경변수 파일은 제외했습니다.

- chatdaeri-2d-3d → https://github.com/chatdaeri/chatdaeri-2d-3d
- gc-minimal-zine-poster-v0-3 → https://github.com/LiamGvchi/gc-minimal-zine-poster
- handdrawn-longform-html → https://github.com/mitmirsein/handdrawn-longform-html
- html-diagram → https://github.com/tonywjs/html-diagram
- html-ppt → https://github.com/aiden-44/html-ppt-skill
- img2threejs → https://github.com/img2threejs/img2threejs
- ir-search → https://github.com/djfksjd/ir-search
- lanshu-create-ai-presenter-video → https://github.com/cclank/lanshu-create-ai-presenter-video
- line-art-animation → https://github.com/JDhruv14/line-art-animation
- llm-wiki → https://github.com/nashsu/llm_wiki_skill
- pptx-design-styles → https://github.com/corazzon/pptx-design-styles
- script-to-motion → https://github.com/kstost/script-to-motion
- showreel → https://github.com/revfactory/showreel
- video-use → https://github.com/browser-use/video-use

## 라이선스

MIT. 스킬 안에 인용된 외부 자료와 외부 오픈소스 스킬은 각 출처의 조건을 따릅니다.
