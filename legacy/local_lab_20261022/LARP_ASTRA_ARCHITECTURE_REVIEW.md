# LARP / MHU — Architecture Review Brief for GPT-6 Astra
Version: pre-experiment design review
Date: 2026-10-07
Intended reader: GPT-6 Astra (or another high-capability reasoning model)
Purpose: produce a technically concrete, falsifiable, implementation-ready v0.1 specification for LARP without optimizing for a positive result.

---

## 0. Executive task

You are acting as a senior research architect and adversarial scientific reviewer.

Design the first serious experimental specification for:

**LARP = Large Avian Retina Pattern**

Core architectural idea:

**MHU = multihyperuniform neural architecture inspired by the multihyperuniform organization of the avian retina.**

The goal is NOT to advocate MHU. The goal is to determine whether a multihyperuniform spatial organization can provide a useful inductive bias for neural computation, compared against deliberately strong and relevant alternative graph/topology designs.

The project methodology is:

1. **Abductive before the first experiment**
2. **Abductive-Bayesian (AB) after evidence begins arriving**

This means:
- generate competing explanatory hypotheses before experiments;
- identify mechanisms, not just outcome predictions;
- assign explicit subjective priors when useful;
- define discriminating observations before looking at results;
- update beliefs after each experiment;
- distinguish evidence that an architecture works from evidence that the proposed mechanism explaining why it works is correct.

Your output will be reviewed by another model before implementation. Do not defer key design choices to the coding model unless uncertainty is itself scientifically essential.

---

## 1. Scientific motivation

The biological inspiration is the avian retina, especially chicken photoreceptor mosaics.

Relevant conceptual property to verify from literature before relying on it:

- several photoreceptor subtypes form interpenetrating spatial mosaics;
- each subtype is reported as hyperuniform or near-hyperuniform at large scales;
- the union of the photoreceptor populations is also hyperuniform;
- this motivates the term **multihyperuniformity**.

The computational hypothesis is not:

> "The retina is efficient, therefore copying it should improve AI."

That is explicitly rejected as insufficient reasoning.

The stronger hypothesis is:

> If a distributed computation benefits from several distinct functional resources being available throughout space with suppressed large-scale density fluctuations, then a multihyperuniform arrangement of functional node classes may provide a useful inductive bias by reducing large spatial deficits of any one class while retaining disorder and isotropy.

This mechanism must be tested independently of generic sparsity, locality, low degree, regular spacing, or total hyperuniformity.

---

## 2. Nomenclature

Use the following names consistently:

- **LARP**: overall project / architecture family
- **MHU**: multihyperuniform architecture or geometry
- **RAMHU**: descriptive phrase "retina aviar multihiperuniforme" / avian-retina multihyperuniform inspiration; optional, not required as an architecture name
- Do NOT use the old provisional name "Chicken Drive"

---

## 3. Long-term ambition vs immediate scope

### Immediate scientific goal
Determine whether MHU contributes measurable computational value relative to strong topology baselines.

### Intermediate goal
Develop an architecture that is a strong **problem solver**, especially on tasks requiring:
- distributed integration,
- routing,
- iterative computation,
- local-to-global information processing,
- robustness,
- generalization to larger spatial domains.

### Long-term optional goal
If earlier evidence justifies it:
- sequential modeling,
- small language model (SLM),
- eventually language modeling / LLM-style scaling experiments.

Do NOT design v0.1 around language modeling. Do NOT assume LARP deserves to become an LM architecture.

---

## 4. Dimensionality

Default proposal under review:

- v0.1 should be **2D**
- rationale:
  - closest to the observed photoreceptor mosaic organization;
  - simpler to visualize;
  - lower compute;
  - easier to verify hyperuniformity;
  - easier to compare geometries cleanly.
- 3D should be treated as a later extension if v0.1 provides reason to continue.

Evaluate this proposal critically.

Clarify:
- whether a 2D MHU architecture is scientifically faithful enough to the biological inspiration;
- what would be gained or lost by 3D;
- whether 3D should appear in v0.2 or later.

---

## 5. Photoreceptor subtype proportions

Preferred default:

Use empirical chicken-retina proportions if sufficiently well established and relevant to the dataset/source being cited.

Current remembered approximate global proportions:
- double cones: ~40.7%
- green: ~21.1%
- red: ~17.1%
- blue: ~12.6%
- violet: ~8.5%

You MUST verify these values from primary or high-quality sources before adopting them.

Also require an ablation with equal subtype proportions:

\[
20\%,20\%,20\%,20\%,20\%
\]

Reason:
separate the effect of multihyperuniform organization from the effect of biological subtype frequencies.

If there is a better empirical mapping or if "five computational types" should not map one-to-one to these exact biological classes, explain why.

---

## 6. Core architecture families that must be distinguished

### 6.1 MHU-G
Multihyperuniform geometry only.

- five subtype labels exist to construct/verify multihyperuniformity;
- computationally, all nodes use the same update function and same parameterization;
- subtype identity should NOT provide extra computational information unless needed only for geometry construction.

Purpose:
test whether MHU geometry alone matters.

### 6.2 MHU-T
Multihyperuniform geometry + learnable type identity.

- same general update function shared across all nodes;
- each subtype A/B/C/D/E has an embedding or analogous identity signal;
- the model may learn different behavior conditional on subtype.

Purpose:
test whether well-distributed functional identity helps.

### 6.3 MHU-F
Multihyperuniform geometry + functionally distinct subtype parameterizations.

Possible designs:
- different MLP/message functions per subtype;
- low-rank adapters per subtype;
- hypernetwork-conditioned update functions;
- mixture-of-experts style subtype specialization.

Constraint:
parameter count must be controlled so MHU-F is not allowed to win merely by having more trainable parameters.

Purpose:
test whether explicit heterogeneous processing combined with MHU is beneficial.

You may propose a better decomposition, but preserve the scientific distinction:

\[
\text{geometry-only}
\quad vs \quad
\text{type-conditioned}
\quad vs \quad
\text{functionally heterogeneous}
\]

---

## 7. Competing hypotheses to refine

Start from these, but improve or merge them if a better hypothesis set exists.

### H1 — Null / generic sparsity hypothesis
MHU provides little or no advantage beyond:
- sparsity,
- locality,
- degree control,
- generic hyperuniformity,
- or regular coverage.

Expected implication:
MHU-G ≈ strong HU baseline when parameter count and graph statistics are controlled.

### H2 — Coverage/robustness hypothesis
MHU primarily improves:
- spatial coverage,
- robustness to local damage,
- positional invariance,
- graceful degradation,
rather than clean-task accuracy.

### H3 — Heterogeneous distributed-computation hypothesis
MHU becomes valuable specifically when:
- different node classes have different learned functions,
- those functions need to be available across the domain,
- local computation repeatedly combines heterogeneous resources.

Expected implication:
MHU-T or MHU-F > HU baseline especially on spatially distributed heterogeneous tasks.

### H4 — Global-routing dominance hypothesis
The main bottleneck is long-distance communication, not local coverage.

Expected implication:
small-world, attention-like, or globally routed networks outperform local MHU unless MHU is augmented with shortcuts/gating.

### H5 — Initialization-not-final-topology hypothesis
MHU may be useful as:
- an initialization,
- regularizer,
- or early-training topology,
while the best learned connectivity later drifts away from MHU.

### H6 — Overconstraint hypothesis
MHU hurts because it suppresses useful:
- modular clustering,
- hub formation,
- localized specialization,
- asymmetry.

Please assign reasoned subjective priors to a refined hypothesis set.

Priors are epistemic bookkeeping, NOT objective probabilities.

---

## 8. Pre-study expectations already held by the project

These are prior intuitions, not findings:

- MHU-G is not strongly expected to beat a well-designed HU network on most clean tasks.
- MHU-T is considered more promising than MHU-G for tasks requiring distributed heterogeneous computation.
- Any advantage may appear more clearly under perturbation, domain scaling, or relocation of inputs than on raw accuracy.
- Purely local MHU is not expected to beat well-designed small-world/global-routing topologies on tasks dominated by long-range communication.
- A future hybrid:
  - local MHU substrate
  - sparse global links
  - dynamic routing/gating
  may be more promising than pure MHU.

Challenge these priors if needed.

---

## 9. Strong baselines

The benchmark set must NOT be designed to make MHU win.

At minimum consider:

### B1 — Regular grid
A deliberately structured spatial baseline.

### B2 — IBM-inspired HU/NHU neural topology
There is an IBM patent/public disclosure concerning:
- hyperuniform or nearly hyperuniform neural networks,
- sparse topology,
- material-inspired graph structures,
- Delaunay-related connectivity,
- possibly rings/surfaces and bidirectionality.

You MUST:
- search and verify the closest public IBM work;
- state what can be faithfully reproduced;
- label the implementation **IBM-inspired** unless exact reproduction is possible;
- separate geometry effects from other IBM-specific design choices.

### B3 — Random-regular or degree-matched graph
Purpose:
control for average degree while removing spatial MHU structure.

### B4 — Small-world
Purpose:
strong baseline for efficient local + global communication.

### B5 — Poisson spatial random graph
Optional cheap negative/control baseline.
Not a primary "opponent", but scientifically useful.

You may add:
- expander-like sparse graphs,
- Watts-Strogatz,
- learned sparse graphs,
- graph transformers,
if they materially improve causal interpretation.

Do not add baselines merely to make the benchmark suite look large.

---

## 10. Two distinct comparison regimes

### 10.1 Causal comparison
Hold as much as possible constant:
- node count
- hidden dimension
- trainable parameter count
- degree or edge count
- optimizer
- training budget
- update rule
- number of recurrent steps
- input/output interface

Change only topology/geometry.

Purpose:
estimate causal contribution of geometry.

### 10.2 Ecological / best-form comparison
Each architecture is allowed to use a connectivity scheme natural to it.

Examples:
- MHU + Delaunay
- grid + grid neighborhood
- small-world + native rewiring
- IBM-inspired + its natural graph construction

Purpose:
ask which complete architecture works best under reasonable design.

Both regimes are required because they answer different questions.

---

## 11. Open design question: what is a "neighbor"?

Current candidate rules:

### Option A — k-nearest neighbors (kNN)
Pros:
- degree approximately controlled;
- clean causal comparisons;
- simple.

Cons:
- physical radius varies;
- can generate longer edges in sparse regions.

### Option B — fixed-radius graph
Pros:
- true geometric locality;
- interpretable spatial radius.

Cons:
- degree differs by local density/topology;
- confounds topology and edge count.

### Option C — Delaunay triangulation
Pros:
- natural geometric neighborhood;
- dual to Voronoi;
- biologically/geometrically motivated;
- relevant to previous hyperuniform graph work.

Cons:
- variable degree;
- geometry can affect degree statistics;
- harder to isolate topology from connectivity rule.

Current provisional plan:
- use **Delaunay** as a natural LARP/MHU connectivity;
- use **kNN** as the main controlled connectivity for causal comparisons.

Evaluate whether this is optimal.

Also consider whether:
- mutual-kNN,
- Gabriel graphs,
- relative-neighborhood graphs,
- radius + degree cap,
- learned local gating
would be better.

---

## 12. Node state and update rule — major unresolved issue

You must choose concrete v0.1 defaults.

For node \(i\), define:

\[
h_i(t)\in\mathbb R^d
\]

Potential values under consideration:
- d = 16
- d = 32
- d = 64

You must recommend one.

Define message passing precisely.

Candidate template:

\[
m_i(t)=\operatorname{AGG}_{j\in N(i)}
\phi(h_i(t),h_j(t),e_{ij},c_i,c_j)
\]

\[
h_i(t+1)=\psi(h_i(t),m_i(t),c_i)
\]

Decide:
- aggregation: sum / mean / normalized sum / attention / gated sum;
- edge features: distance, angle, subtype pair, learned gate, none;
- residual update or replacement;
- normalization;
- activation;
- whether update weights are shared over time;
- whether MHU-G/T/F share the same high-level update design.

Strong preference:
v0.1 should remain interpretable and computationally cheap.

Do not select local attention simply because attention is fashionable.
Select it only if the mechanism is justified.

---

## 13. Recurrent block vs stacked layers

Two broad designs:

### Recurrent substrate
Same graph and same update function reused for T steps:

\[
H_{t+1}=F_\theta(H_t,G)
\]

Advantages:
- close to a dynamical system;
- parameter efficient;
- tests emergence from repeated local interactions;
- clean scalability.

Risks:
- optimization difficulty;
- oversmoothing;
- limited expressivity if F is too simple.

### Stacked MHU blocks
Different parameters by depth:

\[
H_{l+1}=F_{\theta_l}(H_l,G_l)
\]

Advantages:
- more expressive;
- closer to mainstream deep learning.

Risks:
- harder to isolate geometry;
- more parameters;
- less direct dynamical interpretation.

Current project instinct:
start with one recurrent MHU substrate, later test stacked/hybrid forms.

Evaluate and choose v0.1.

Specify:
- number of recurrent steps;
- whether weights are tied;
- whether recurrent depth varies at test time;
- whether we should test generalization to more steps than seen in training.

---

## 14. Geometry generation

Critical requirement:

Do NOT generate something that merely looks irregular-and-evenly-spaced.

We need a quantitatively verified MHU configuration.

You must propose:
- a reproducible algorithm to generate the full point pattern;
- a way to assign 5 subtypes while preserving subtype-level hyperuniformity;
- how to match target biological proportions;
- how to seed/reproduce geometries;
- whether to use periodic boundary conditions for generation/measurement;
- whether training domain should be toroidal, bounded, or both in separate experiments.

Potential approaches to investigate:
- collective-coordinate / stealthy hyperuniform optimization;
- energy minimization;
- centroidal Voronoi-like methods with disorder constraints;
- direct reproduction of methods used in avian-retina literature;
- multi-component hyperuniform optimization.

Do not assume all these methods are equivalent.

---

## 15. Verify MHU quantitatively

At minimum consider:

- structure factor \(S(k)\)
- low-k behavior
- number variance \(\sigma_N^2(R)\)
- pair correlation \(g_2(r)\)
- nearest-neighbor distribution
- Voronoi cell-area statistics
- subtype-specific versions
- union-of-types version
- optional anisotropy metrics

For MHU:
verify both:
1. each subtype;
2. the combined pattern.

Define thresholds or diagnostics sufficient for v0.1.
Do not require impossible asymptotic proof from a finite sample.

Specify how finite-size effects should be handled.

---

## 16. Geometry plasticity

Question:
Should node coordinates or topology change during learning?

Current project view:
performance matters more than biological fidelity, but geometry should initially be frozen so the MHU hypothesis can be tested.

Recommended staged family to evaluate:

### Frozen
- coordinates fixed;
- edges fixed;
- train only neural parameters.

### Edge-plastic
- coordinates fixed;
- learned edge gates / edge weights;
- possibly sparse rewiring;
- analyze whether topology drifts toward hubs, modules, small-world, etc.

### Geometry-plastic
- coordinates themselves can move;
- perhaps include an MHU regularizer.

Important epistemic caveat:
If free geometry moves away from MHU, this does NOT automatically prove MHU is bad.
Possible interpretations:
- task-specific specialization,
- optimizer bias,
- insufficient MHU regularization,
- useful MHU initialization but suboptimal final geometry,
- benchmark mismatch.

Design experiments capable of distinguishing:
- "MHU is a good fixed inductive bias"
- "MHU is a good initialization"
- "MHU is unnecessary"
- "MHU is actively harmful"

---

## 17. Connectivity multihyperuniformity

The user has a further idea:

not only should nodes be multihyperuniform; perhaps connectivity itself should have multiple structured relation classes.

Possible interpretation:

\[
E = E_{\text{local}} \cup E_{\text{same-type}} \cup E_{\text{cross-type}}
\]

or a multiplex graph where different edge classes obey different spatial statistics.

This is NOT required for v0.1.

Your task:
- assess whether this is mathematically coherent;
- suggest a precise future formulation;
- warn against conflating node MHU with edge MHU;
- state what measurements would characterize a "multihyperuniform connectivity" pattern.

---

## 18. Future hybrid candidate

Analyze but do not automatically include in v0.1:

\[
\text{MHU local substrate}
+
\text{few global shortcuts}
+
\text{learned dynamic routing/gating}
\]

Hypothesized division of labor:

- MHU: distributed local coverage
- small-world: short global path lengths
- gating/attention: state-dependent routing

Determine what minimal evidence from v0.1 would justify testing this hybrid.

---

## 19. Initial task ladder

Do not use one benchmark only.

### Stage 0 — smoke tests
Examples:
- distant XOR
- distant parity
- majority

Purpose:
verify information can propagate and combine.

Do NOT treat success here as evidence of architectural superiority.

### Stage 1 — routing / memory
Examples:
- copy signal from one region to another;
- select one of several remote sources;
- delayed spatial recall;
- permutation-controlled routing.

Purpose:
measure information transport.

### Stage 2 — algorithmic spatial problem solving
Examples:
- maze solving;
- shortest path;
- connected components;
- flood fill;
- graph reachability;
- cellular automata prediction.

Purpose:
test iterative local-to-global computation.

### Stage 3 — generalization
Train on smaller domains, test on larger:
- more nodes;
- larger spatial extent;
- longer path lengths;
- more recurrent steps.

Purpose:
test algorithmic/systemic scaling rather than memorization.

### Stage 4 — perturbation / robustness
- random node dropout;
- localized lesion;
- subtype-specific lesion;
- edge removal;
- input relocation;
- output relocation.

Purpose:
test coverage and resilience hypotheses.

### Stage 5 — sequence tasks
Only if earlier results justify:
- copying sequences;
- associative recall;
- finite-state problems;
- sequence prediction.

### Stage 6 — SLM / language
Only after evidence supports continuation.

You must recommend exact first tasks, not merely categories.

---

## 20. Why distant XOR is not the endpoint

Distant XOR is only useful because:
- two remote inputs must influence one output;
- local architectures require propagation;
- it is easy to debug.

Its ceiling is extremely low.

Use it only as:
- implementation sanity check;
- propagation sanity check;
- not as evidence of reasoning ability.

---

## 21. Metrics

Do not report only final accuracy.

At minimum specify:

### Task performance
- accuracy / success rate
- task-specific score
- final loss

### Optimization
- steps to threshold
- wall-clock time
- sample efficiency
- training stability
- seed variance

### Capacity / efficiency
- trainable parameters
- active edges
- FLOPs or a practical proxy
- memory use

### Spatial / graph properties
- average degree
- degree variance
- clustering
- shortest-path distribution
- diameter
- spectral gap / algebraic connectivity if useful
- edge-length distribution

### Robustness
- performance vs % node removal
- performance vs lesion radius
- performance vs subtype-specific damage
- performance vs edge deletion

### Positional robustness
- performance as input/output locations change

### Scaling
- train size vs test size
- train recurrent steps vs test recurrent steps

### Mechanism diagnostics
If H3 is considered important, directly quantify:
- local availability of each subtype;
- functional specialization by type;
- activation routing by type;
- whether subtype embeddings/functions differentiate;
- whether benefit disappears when subtype identities are permuted.

---

## 22. Fairness constraints

The v0.1 implementation must control or report:

- same training dataset
- same train/test split
- same optimizer unless architecture requires otherwise
- same learning-rate search budget
- same total training-step budget
- same seeds
- parameter-matched variants when possible
- degree/edge-count matched causal comparisons
- same readout capacity
- same input encoder capacity
- same hidden dimension unless explicitly ablated
- no benchmark-specific tuning unique to MHU
- no cherry-picking best seeds
- no discarding failed runs without logging them
- no post-hoc benchmark selection based on favorable MHU results

If perfect matching is impossible, state the residual confound.

---

## 23. Pre-registration style experiment records

Every experiment should generate a record with:

- experiment ID
- date
- code commit
- dataset/task version
- architectures
- parameter counts
- edge counts
- seeds
- optimizer settings
- prior hypotheses
- expected discriminating outcomes
- results
- mechanism diagnostics
- Bayesian/qualitative update
- next experiment justification

The aim is to preserve the history of belief updates.

---

## 24. Abductive-Bayesian methodology

Before evidence:
- generate hypotheses;
- select best explanations abductively;
- state mechanisms;
- record priors.

After evidence:
update:

\[
P(H_i \mid E)
\propto
P(E \mid H_i)P(H_i)
\]

Exact likelihoods may be unavailable.

If so:
- use coarse Bayes factors or ordinal evidence grades;
- document the mapping transparently;
- do not pretend qualitative updates are mathematically exact.

Crucially distinguish:

### Architecture-level proposition
"MHU improves task X."

from:

### Mechanism-level proposition
"MHU improves task X because subtype-specific coverage suppresses functional deserts."

Possible outcome:
architecture proposition gains support while mechanism proposition loses support.

This distinction is mandatory.

---

## 25. Edge-as-computation / relational branch

Separate future research idea, partly inspired by Luhmannian emphasis on communication/relations.

Instead of passive edge \(i\leftrightarrow j\), assign edge state:

\[
e_{ij}(t)
\]

Potential updates:

\[
e_{ij}(t+1)
=
\phi_e(e_{ij}(t),h_i(t),h_j(t),\text{neighboring edges})
\]

\[
h_i(t+1)
=
\phi_v(h_i(t),\{e_{ij}(t+1)\})
\]

More radical form:
- edges/communications become primary computational entities;
- nodes become constraints, addresses, environments, or attachment points;
- edges may message other edges.

Research relatives to compare:
- edge-centric GNNs
- line graphs
- hypergraphs
- factor graphs
- higher-order message passing
- relational networks
- cellular complexes / simplicial complexes
- graph networks with edge updates

Do NOT integrate this into v0.1 unless there is an overwhelming reason.
Analyze as a distinct future branch.

---

## 26. Hardware / implementation constraints

Target machine:
- ordinary personal laptop/workstation
- approximately 32 GB RAM
- first prototype should be feasible without datacenter hardware
- CPU implementation is acceptable for initial scientific validation
- GPU acceleration is optional, not assumed

Preferred stack:
- Python
- PyTorch
- NumPy/SciPy
- NetworkX only where scale permits
- PyTorch Geometric only if justified and setup complexity is acceptable
- Matplotlib for scientific figures
- deterministic/reproducible seeds where practical

The coding stage will likely be delegated to Codex.

Therefore your output must be precise enough that Codex does not need to make scientific choices silently.

---

## 27. Suggested starting scale

Current provisional thought:
- N around 2,000–5,000 nodes
- candidate default N = 4096
- hidden state d = 16–32
- local degree roughly 6–12
- recurrent steps roughly 8–20

These are NOT fixed.
Choose concrete v0.1 values and justify them.

The first experiment should finish in hours or less on domestic hardware, not days.

---

## 28. Research questions you must answer

You MUST provide concrete recommendations on all of the following:

1. Exact v0.1 node count.
2. Exact subtype proportions.
3. Exact geometry-generation algorithm.
4. Exact finite-sample diagnostics for claiming "MHU enough for experiment".
5. Exact neighbor rule for natural MHU.
6. Exact neighbor rule for controlled comparisons.
7. Exact hidden-state dimension.
8. Exact message function.
9. Exact aggregation function.
10. Exact node update function.
11. Whether to use residual connections.
12. Whether to use normalization.
13. Whether to use tied recurrent weights.
14. Exact number of recurrent steps.
15. Exact readout mechanism.
16. Exact input injection mechanism.
17. Exact implementation of MHU-G.
18. Exact implementation of MHU-T.
19. Exact implementation of MHU-F.
20. How to parameter-match MHU-F.
21. Exact first three tasks.
22. Exact baseline suite.
23. Exact seed count for pilot and confirmatory stages.
24. Exact metrics for pilot.
25. Exact robustness tests.
26. Stop/go criteria after v0.1.
27. What results would justify v0.2.
28. What v0.2 should be if v0.1 is promising.
29. What result would make MHU substantially less plausible.
30. What result would specifically support the functional-coverage mechanism.
31. Whether and when to test topology plasticity.
32. Whether and when to test 3D.
33. Whether and when to test global shortcuts.
34. Whether and when to test language.

Avoid "it depends" unless you immediately resolve the dependency into an experiment or decision rule.

---

## 29. Literature review requirements

Search current literature before finalizing recommendations.

At minimum verify or investigate:

- avian photoreceptor multihyperuniformity;
- exact subtype proportions and spatial statistics;
- multicomponent hyperuniform point processes;
- hyperuniform graph/network constructions;
- IBM Hyperuniform / Nearly Hyperuniform Neural Networks;
- neural cellular automata;
- recurrent message-passing networks;
- sparse graph neural networks;
- small-world neural computation;
- learned sparse connectivity / rewiring;
- topology optimization in neural networks;
- spatially embedded recurrent networks;
- edge-centric GNNs / line graphs / hypergraphs;
- scaling/generalization of local recurrent neural systems.

For every important literature-dependent claim:
- cite the source;
- distinguish peer-reviewed work, preprints, patents, and blog/author claims;
- do not treat patents as independent empirical validation.

Flag any prior art that is closer to LARP/MHU than currently known.

---

## 30. Output format

Produce one structured Markdown response with the following sections.

### A. Executive verdict
Max ~1,000 words.
State:
- whether the project is technically coherent;
- where the strongest hypothesis lies;
- where the idea is weakest;
- whether v0.1 is worth implementing.

### B. Corrections to current premises
List anything in this brief that is:
- false;
- misleading;
- poorly framed;
- experimentally confounded.

### C. Literature map
Table:
- concept
- closest prior work
- evidence strength
- relevance to LARP
- gap remaining

### D. Competing hypotheses and priors
For each:
- hypothesis
- causal mechanism
- prior
- observations predicted
- observations that would hurt it

### E. Architecture Decision Record — LARP v0.1
Provide exact values and decisions.

Required fields:
- N
- dimensionality
- subtype proportions
- geometry algorithm
- graph construction
- hidden dimension
- message function
- aggregation
- update rule
- recurrence depth
- input encoding
- output readout
- normalization
- residuals
- parameter count target
- expected memory footprint
- expected runtime class
- implementation stack

### F. Architecture schematics in equations
Use mathematical notation, not decorative ASCII.

### G. MHU-G / MHU-T / MHU-F definitions
Implementation-level precision.

### H. Baseline definitions
Implementation-level precision.

### I. Ablation matrix
Rows = experiments/conditions.
Columns should include:
- geometry
- type identity
- type-specific parameters
- connectivity
- degree
- parameter count
- recurrent steps
- purpose

### J. First experiment sequence
Order by:
- cost
- expected information gain

For each:
- exact task
- dataset generation
- train size
- test size
- metrics
- expected outcomes under each hypothesis
- go/no-go implication

### K. Robustness protocol
Exact lesion/dropout tests.

### L. AB update protocol
Give a practical template for:
- prior
- predicted evidence
- result
- likelihood assessment
- posterior/update
- mechanism update
- next experiment

### M. Stop / pivot / continue criteria
Concrete thresholds or qualitative rules.

### N. v0.2 roadmap
Conditional on possible v0.1 outcomes.

### O. Path toward problem solving and later LM
Separate:
- what would need to be demonstrated first;
- what architectural changes would likely be needed;
- what would falsify the LM ambition.

### P. Edge-as-computation research branch
Prior art + minimal future experiment.

### Q. Implementation contract for Codex
A checklist precise enough that Codex should implement, not reinterpret, the science.

### R. Machine-readable decision block
End with a fenced JSON object named conceptually `larp_v0_1_decisions` containing all concrete v0.1 decisions.

Do not leave unresolved scientific choices in this JSON unless you explicitly mark them as experimental factors.

---

## 31. Required reasoning style

Be adversarial toward attractive stories.

Do NOT reason:
- "biological therefore better";
- "complex therefore intelligent";
- "emergent therefore powerful";
- "hyperuniform therefore robust";
without a mechanism and a discriminating test.

Prefer:
- causal decomposition;
- ablations;
- competing explanations;
- measurement;
- falsifiable predictions.

When making a speculative claim, label it explicitly as:
- inference,
- hypothesis,
- speculation,
or equivalent.

When evidence is weak, say so.

Do not optimize the answer for enthusiasm.

---

## 32. Final standard

The response should leave the project in a state where:

1. another model can implement v0.1 without inventing scientific decisions;
2. we know what evidence would favor or weaken MHU;
3. we can distinguish geometry effects from subtype-function effects;
4. we can compare fairly against strong baselines;
5. the first round is computationally feasible on consumer hardware;
6. the project has a documented AB belief-update path;
7. failure would still yield scientifically interpretable information.

The goal is not "make LARP work."

The goal is:

> **maximize information gained about whether multihyperuniform organization is a useful neural-computation inductive bias, and why.**
