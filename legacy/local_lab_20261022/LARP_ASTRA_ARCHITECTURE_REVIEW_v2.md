# LARP / MHU — Research Architecture Decision Brief
Version: v2 — pre-experiment review
Date: 2026-10-07
Primary reviewer: high-capability reasoning model
Downstream implementer: SOL 6.1 UltraCode
Project: LARP — Large Avian Retina Pattern

---

# 0. Mission

Design a scientifically defensible, computationally feasible `LARP v0.1` experiment that tests whether **multihyperuniform (MHU) organization** provides a useful neural-computation inductive bias.

Do not optimize for a positive MHU result.

Your job is to resolve the hard scientific and architectural decisions in this document so that a downstream coding model can implement the experiment without silently making scientific choices.

The central question is:

> Does multihyperuniform organization improve neural computation under any identifiable conditions, relative to strong alternative topologies, and if so through what mechanism?

The project must remain informative even if MHU fails.

---

# 1. Methodological philosophy

The project begins abductively and becomes **abductive-Bayesian (AB)** once experimental evidence appears.

Before experiments:
- generate competing explanations;
- state mechanisms;
- assign subjective priors when useful;
- define discriminating observations;
- precommit to what would count against each hypothesis.

After experiments:
- update beliefs explicitly;
- distinguish architecture-level evidence from mechanism-level evidence;
- avoid retrospective storytelling.

Important distinction:

Architecture claim:
> MHU improves task X.

Mechanism claim:
> MHU improves task X because subtype-specific spatial coverage suppresses functional deserts.

One can gain support while the other loses support.

Use Bayesian language honestly. If exact likelihoods are unavailable, use transparent qualitative or coarse Bayes-factor updates rather than pseudo-precision.

---

# 2. Names

Use:

- **LARP** = overall project / architecture family
- **MHU** = multihyperuniform neural geometry / architecture
- **RAMHU** = optional descriptive term for the avian-retina multihyperuniform inspiration

Do not use previous joke/provisional names.

---

# 3. Biological inspiration

The motivating biological system is the avian retina, especially chicken photoreceptor mosaics.

Verify from primary or high-quality literature before relying on these premises:

- several photoreceptor subtypes form interpenetrating mosaics;
- each subtype is hyperuniform or near-hyperuniform at large scales;
- the total population is also hyperuniform;
- this motivates multihyperuniformity.

Do not infer computational superiority from biological existence.

The relevant computational hypothesis is narrower:

> If distributed computation benefits from several distinct functional resources being available throughout space with suppressed large-scale density fluctuations, then MHU organization may reduce large spatial deficits of any functional class while preserving disorder and isotropy.

This mechanism must be separated from:
- sparsity;
- locality;
- degree control;
- generic hyperuniformity;
- regular spacing;
- small-world effects;
- attention/routing;
- parameter count.

---

# 4. Scientific scope

## Immediate goal
Determine whether MHU contributes measurable value relative to strong topology baselines.

## Intermediate goal
If justified, develop a strong general problem-solving architecture emphasizing:
- local-to-global computation;
- iterative reasoning;
- routing;
- robustness;
- scaling to larger domains.

## Long-term optional goal
Only if prior stages justify continuation:
- sequential modeling;
- SLM;
- language modeling.

Do not design v0.1 around language.

---

# 5. Dimensionality

Current default:

- `v0.1 = 2D`

Rationale:
- closest to the photoreceptor mosaic being copied;
- cheaper;
- easier to visualize;
- easier to verify spatial statistics;
- cleaner causal comparison.

3D should be considered later.

Evaluate whether this default is correct.

Important clarification:
Modern LMs are not meaningfully "2D" or "3D" in this spatial sense. Hidden-state dimensionality is not spatial geometry.

---

# 6. Biological subtype proportions

Current remembered approximate chicken-retina global proportions:

- double cones: ~40.7%
- green: ~21.1%
- red: ~17.1%
- blue: ~12.6%
- violet: ~8.5%

Verify these values and their source before adopting them.

Preferred plan:
- primary biological-proportion MHU condition;
- equal-proportion ablation: 20% each.

Purpose:
separate MHU effects from subtype-frequency effects.

If the biological mapping is not appropriate for computation, explain why and propose a better design.

---

# 7. Core LARP variants

We need a clean decomposition between geometry and functional heterogeneity.

## MHU-G — geometry only
- five subtype labels used only to construct/verify MHU;
- all nodes computationally identical;
- same update function and parameters;
- subtype labels should not provide useful computational input.

Purpose:
test whether MHU geometry alone adds value.

## MHU-T — type-conditioned
- MHU geometry;
- shared main update function;
- subtype identity available through a small learned embedding or equivalent conditioning signal.

Purpose:
test whether distributed functional identity helps.

## MHU-F — functionally heterogeneous
- MHU geometry;
- node type changes parameters/function;
- possible implementations:
  - subtype-specific adapters;
  - subtype-conditioned low-rank deltas;
  - separate small update functions;
  - mixture-of-experts style specialization.

Constraint:
parameter matching must prevent MHU-F from winning merely because it has more trainable parameters.

You may improve this taxonomy, but preserve the causal distinction:

\[
\text{geometry only}
\;\; vs \;\;
\text{type-conditioned}
\;\; vs \;\;
\text{functionally heterogeneous}
\]

---

# 8. Current abductive hypotheses

Refine if necessary.

## H1 — generic sparsity/locality null
MHU contributes little beyond generic sparse/local structure.

Prediction:
MHU-G approximately matches a strong HU baseline when graph statistics and parameter count are controlled.

## H2 — coverage/robustness
MHU's main advantage is not clean-task accuracy but:
- spatial coverage;
- positional robustness;
- graceful degradation;
- local lesion robustness;
- subtype-specific damage resilience.

## H3 — distributed functional heterogeneity
MHU becomes useful when distinct learned functions need broad spatial availability.

Prediction:
MHU-T or MHU-F gains more than MHU-G on tasks requiring spatially distributed heterogeneous computation.

## H4 — global-routing dominance
Long-distance communication is more important than MHU coverage.

Prediction:
small-world / learned-routing / attention-like structures dominate pure local MHU on routing-heavy tasks.

## H5 — initialization rather than final topology
MHU may be useful as:
- initialization;
- regularizer;
- early-training topology;
while optimal learned connectivity later drifts away.

## H6 — overconstraint
MHU may harm performance by suppressing useful:
- clustering;
- modular specialization;
- hubs;
- asymmetric organization.

Assign reasoned subjective priors before seeing results.

---

# 9. Current priors from the project

These are provisional beliefs, not findings:

- MHU-G is not strongly expected to beat a strong HU model on generic clean tasks.
- MHU-T is more promising than MHU-G for heterogeneous distributed computation.
- MHU advantages may appear more clearly under perturbation, scaling, or relocation than in raw accuracy.
- pure local MHU is unlikely to dominate small-world/global-routing designs on long-range communication tasks.
- a later hybrid may be more promising:

\[
\text{MHU local substrate}
+
\text{sparse global shortcuts}
+
\text{dynamic learned routing/gating}
\]

Challenge these priors if necessary.

---

# 10. Strong baselines

Do not compare MHU only against weak or naive alternatives.

At minimum evaluate:

## B1 — regular grid
Strong structured spatial baseline.

## B2 — IBM-inspired HU/NHU
Investigate the closest public IBM work on hyperuniform/nearly-hyperuniform neural networks.

Requirements:
- verify exact public source(s);
- separate patents from peer-reviewed validation;
- state what can and cannot be faithfully reproduced;
- call it `IBM-inspired` unless exact reproduction is justified.

## B3 — random-regular / degree-matched graph
Controls degree and sparsity without MHU geometry.

## B4 — small-world
Strong long-range communication baseline.

## B5 — Poisson spatial random graph
Cheap negative/control condition.
Not the main opponent.

Optionally include stronger sparse graph baselines only if they materially improve interpretation.

---

# 11. Two comparison regimes

## 11.1 Causal regime
Hold constant as much as possible:
- node count;
- hidden dimension;
- parameter count;
- degree / edge count;
- update rule;
- optimizer;
- training budget;
- recurrence depth;
- input encoder;
- output readout.

Change topology/geometry.

Goal:
estimate the causal effect of geometry.

## 11.2 Ecological regime
Each architecture uses a connectivity pattern natural to it.

Examples:
- MHU + Delaunay;
- grid + grid neighborhood;
- small-world + native shortcuts;
- IBM-inspired + its natural graph construction.

Goal:
compare viable complete architectures.

Both regimes are required.

---

# 12. Neighbor / graph construction decision

Candidate rules:

## k-nearest neighbors
Pros:
- approximately controlled degree;
- simple causal comparisons.

Cons:
- local radius varies;
- can create long links in sparse areas.

## fixed radius
Pros:
- true physical locality.

Cons:
- degree varies by local density and geometry.

## Delaunay
Pros:
- natural geometric neighborhood;
- closely related to Voronoi;
- relevant to hyperuniform graph work;
- biologically/geometrically motivated.

Cons:
- degree emerges from geometry;
- more confounding in causal comparisons.

Current provisional plan:
- **Delaunay** for the natural/ecological MHU architecture;
- **kNN or mutual-kNN** for controlled causal comparisons.

You must decide whether this is the best v0.1 choice.

Consider:
- mutual-kNN;
- Gabriel graph;
- relative-neighborhood graph;
- radius + degree cap;
if they offer a clearer design.

---

# 13. Node state and message passing

Major unresolved issue.

For node \(i\):

\[
h_i(t)\in\mathbb{R}^d
\]

Candidate hidden sizes:
- 16
- 32
- 64

Choose a concrete default.

General message-passing template:

\[
m_i(t)
=
\operatorname{AGG}_{j\in N(i)}
\phi(
h_i(t),
h_j(t),
e_{ij},
c_i,
c_j
)
\]

\[
h_i(t+1)
=
\psi(
h_i(t),
m_i(t),
c_i
)
\]

Decide concretely:

- hidden dimension;
- message function;
- aggregation:
  - sum
  - mean
  - normalized sum
  - gated sum
  - local attention
  - other;
- edge features:
  - Euclidean distance
  - relative direction
  - subtype pair
  - learned edge gate
  - none;
- update:
  - residual vs replacement;
- normalization;
- activation;
- whether weights are shared over recurrent steps;
- how MHU-G/T/F differ while preserving fair comparison.

Prefer scientific clarity and cheap computation over sophistication.

Do not choose attention merely because it is popular.

---

# 14. Recurrent substrate vs stacked layers

## Recurrent substrate

\[
H_{t+1}=F_{\theta}(H_t,G)
\]

Same graph and same update parameters reused over time.

Advantages:
- parameter efficient;
- close to dynamical systems;
- clean test of repeated local interaction;
- potentially scalable to more steps at test time.

Risks:
- oversmoothing;
- optimization difficulty;
- limited expressivity.

## Stacked blocks

\[
H_{l+1}=F_{\theta_l}(H_l,G_l)
\]

Advantages:
- expressive;
- closer to mainstream deep learning.

Risks:
- more parameters;
- harder causal interpretation;
- less clean emergence/dynamics story.

Current preference:
start recurrent and later test stacked/hybrid architectures.

Resolve v0.1:
- tied or untied weights;
- exact recurrent steps;
- whether test-time extra steps should be evaluated.

---

# 15. Geometry generation

Critical requirement:

Do NOT produce a pattern that merely looks evenly disordered.

Need a reproducible, quantitatively verified **multicomponent MHU** generator.

Investigate and select a practical method, possibly based on:
- collective-coordinate / stealthy hyperuniform optimization;
- energy minimization;
- multicomponent hyperuniform point-process methods;
- biologically inspired avian-retina models;
- other literature-supported generators.

Requirements:
- target subtype proportions;
- reproducible seeds;
- finite domain treatment;
- periodic boundary conditions if appropriate;
- subtype-level MHU;
- total-population HU.

Do not assume a generic blue-noise / Poisson-disk pattern automatically counts as MHU.

---

# 16. MHU verification

At minimum evaluate:

- structure factor \(S(k)\);
- low-k behavior;
- number variance \(\sigma_N^2(R)\);
- pair correlation \(g_2(r)\);
- nearest-neighbor statistics;
- Voronoi cell-area distribution;
- subtype-specific diagnostics;
- union-of-types diagnostics;
- anisotropy if relevant.

Need finite-sample criteria appropriate for N around a few thousand.

Do not demand an impossible asymptotic proof.

Define a practical criterion for:
> "MHU enough to use in the experiment."

---

# 17. Geometry and topology plasticity

Performance matters more than preserving biological fidelity, but plasticity must not destroy causal interpretability.

Recommended staged sequence to evaluate:

## Frozen
- coordinates fixed;
- edges fixed;
- train neural parameters only.

Purpose:
test MHU as an inductive bias.

## Edge-plastic
- coordinates fixed;
- learn edge gates and/or controlled rewiring.

Purpose:
ask whether MHU is a useful substrate that evolves toward:
- hubs;
- modules;
- small-worldness;
- other topology.

## Geometry-plastic
- learn coordinates themselves;
- optionally retain a soft MHU regularizer.

Purpose:
ask whether MHU is:
- useful fixed topology;
- useful initialization;
- unnecessary;
- harmful.

Important:
moving away from MHU does NOT by itself prove MHU was useless.

Design discriminating tests.

---

# 18. Multihyperuniform connectivity idea

Future research idea:

not only node classes, but relation classes may possess structured spatial statistics.

Possible multiplex decomposition:

\[
E
=
E_{\text{local}}
\cup
E_{\text{same-type}}
\cup
E_{\text{cross-type}}
\]

or multiple relation layers with separate spatial constraints.

Not required for v0.1.

Assess:
- mathematical coherence;
- how to define "edge MHU";
- how to measure it;
- whether edge-midpoint distributions are meaningful;
- whether relation-class MHU adds anything beyond node MHU.

---

# 19. Future hybrid

Do not automatically include in v0.1:

\[
\text{MHU local}
+
\text{few global shortcuts}
+
\text{learned dynamic routing}
\]

Hypothesized roles:

- MHU → distributed local coverage
- small-world links → short global path length
- gating/attention → state-dependent routing

Define what v0.1 evidence would justify this v0.2 direction.

---

# 20. Task ladder

Do not use one benchmark only.

## Stage 0 — smoke tests
Examples:
- distant XOR;
- distant parity;
- majority.

Purpose:
debug propagation and aggregation.

Success here is not evidence of superiority.

## Stage 1 — routing / memory
Examples:
- copy one remote signal;
- choose one of several remote sources;
- delayed spatial recall.

Purpose:
information transport.

## Stage 2 — algorithmic spatial problem solving
Examples:
- maze solving;
- shortest path;
- reachability;
- connected components;
- flood fill;
- local-rule simulation/prediction.

Purpose:
iterative local-to-global computation.

## Stage 3 — scaling/generalization
Train small, test larger:
- more nodes;
- larger spatial extent;
- longer path lengths;
- more recurrent steps.

## Stage 4 — perturbation
- random node removal;
- localized lesions;
- subtype-specific lesions;
- edge deletion;
- relocated input/output sites.

## Stage 5 — sequence tasks
Only if earlier evidence justifies:
- copy;
- associative recall;
- finite-state tasks;
- sequence prediction.

## Stage 6 — SLM / LM
Only if previous stages justify it.

You must choose the exact first three tasks for v0.1.

---

# 21. Metrics

Do not optimize on final accuracy alone.

## Task
- accuracy/success;
- task-specific score;
- final loss.

## Optimization
- steps to threshold;
- sample efficiency;
- wall-clock;
- seed variance;
- failure rate.

## Efficiency
- trainable parameters;
- active edges;
- FLOPs or practical proxy;
- memory.

## Graph/spatial
- degree mean/variance;
- clustering;
- shortest-path distribution;
- diameter;
- spectral gap / algebraic connectivity if useful;
- edge-length distribution.

## Robustness
- performance vs random node removal;
- performance vs lesion radius;
- performance vs subtype-specific damage;
- performance vs edge deletion.

## Positional robustness
- performance when input/output locations change.

## Scaling
- train-domain size vs test-domain size;
- train recurrent steps vs test recurrent steps.

## Mechanism tests
If H3 is central, directly measure:
- local availability of each type;
- specialization by type;
- whether type embeddings/functions diverge;
- activation/use by type;
- effect of permuting type labels;
- effect of spatially clustering types while preserving counts;
- whether MHU benefit disappears when per-type coverage is disrupted.

---

# 22. Fairness constraints

Control or report:

- same datasets;
- same splits;
- same optimizer unless justified;
- equal hyperparameter-search budget;
- same training-step budget;
- same seeds;
- parameter matching where possible;
- edge-count/degree matching in causal comparisons;
- same input encoder;
- same readout capacity;
- same hidden size unless explicitly ablated;
- no MHU-exclusive tuning;
- no best-seed reporting;
- log failed runs;
- no post-hoc benchmark selection based on favorable results.

If perfect matching is impossible, state residual confounds.

---

# 23. Experimental records

Every experiment should log:

- experiment ID;
- date;
- code commit;
- task version;
- architecture;
- geometry seed;
- training seed;
- parameter count;
- edge count;
- graph metrics;
- optimizer;
- budget;
- hypotheses;
- priors;
- predicted discriminating outcomes;
- results;
- mechanism diagnostics;
- AB update;
- next-experiment rationale.

This history is part of the scientific product.

---

# 24. Edge-as-computation branch

Separate future idea, partly motivated by a relational/Luhmannian framing.

Instead of passive edge \(i\leftrightarrow j\), give each edge state:

\[
e_{ij}(t)
\]

Potential update:

\[
e_{ij}(t+1)
=
\phi_e(
e_{ij}(t),
h_i(t),
h_j(t),
\text{neighboring edges}
)
\]

\[
h_i(t+1)
=
\phi_v(
h_i(t),
\{e_{ij}(t+1)\}
)
\]

More radical interpretation:
- edges/communications become primary computational entities;
- nodes become support, environment, attachment points, or constraints;
- edges may message other edges.

Compare with:
- edge-centric GNNs;
- line graphs;
- hypergraphs;
- factor graphs;
- higher-order message passing;
- cellular/simplicial complexes;
- graph networks with edge updates.

Do not integrate into v0.1 unless exceptionally justified.

---

# 25. Hardware and engineering constraints

Target:
- ordinary consumer laptop/workstation;
- approximately 32 GB RAM;
- no datacenter hardware;
- CPU-only should remain possible for initial validation;
- GPU optional.

Preferred stack:
- Python;
- PyTorch;
- NumPy;
- SciPy;
- Matplotlib;
- optional PyTorch Geometric only if its benefits outweigh setup complexity;
- NetworkX only where scale permits.

Downstream implementation will likely be performed by **SOL 6.1 UltraCode**.

Therefore the scientific reviewer must make the scientific decisions now.

UltraCode should implement, not reinterpret, the experiment.

---

# 26. Starting scale

Current provisional range:
- N = 2,000–5,000;
- candidate N = 4096;
- hidden d = 16–32;
- degree ≈ 6–12;
- recurrent steps ≈ 8–20.

Choose exact defaults.

Pilot experiments should finish in minutes to hours, not days.

---

# 27. High-priority unresolved questions

Spend most reasoning effort here.

Resolve:

1. Best practical algorithm for generating finite multicomponent MHU patterns.
2. Best finite-sample diagnostic for validating those patterns.
3. Best natural neighbor rule for MHU.
4. Best controlled neighbor rule across topologies.
5. Best minimal message-passing architecture for isolating topology.
6. Exact MHU-G / T / F parameterization.
7. Parameter matching for MHU-F.
8. Best strong HU baseline approximating IBM's proposal.
9. Best non-HU deliberate topology baseline.
10. First tasks with highest expected information gain.
11. Metrics that distinguish coverage from routing.
12. Whether recurrent tied weights are the correct v0.1 choice.
13. Whether topology plasticity belongs in v0.1 or only v0.2.
14. Clear stop/pivot/continue criteria.
15. What evidence would specifically support the functional-coverage mechanism rather than merely MHU performance.

Do not spend many tokens re-explaining basic ML concepts.

---

# 28. Required concrete decisions

Your output MUST provide a recommendation for:

1. N.
2. 2D vs 3D for v0.1.
3. subtype proportions.
4. MHU generator.
5. boundary conditions.
6. MHU validation metrics and pass criteria.
7. natural MHU graph rule.
8. controlled graph rule.
9. hidden dimension.
10. edge features.
11. message function.
12. aggregation function.
13. node update function.
14. activation.
15. normalization.
16. residual structure.
17. recurrent vs stacked design.
18. tied vs untied weights.
19. recurrent steps.
20. input injection.
21. output readout.
22. MHU-G definition.
23. MHU-T definition.
24. MHU-F definition.
25. parameter-matching strategy.
26. baseline suite.
27. first three tasks.
28. pilot seed count.
29. confirmatory seed count.
30. optimizer.
31. learning-rate strategy.
32. training budget.
33. core metrics.
34. robustness protocol.
35. stop criteria.
36. pivot criteria.
37. continue criteria.
38. v0.2 path.
39. when to test topology plasticity.
40. when to test 3D.
41. when to test global shortcuts.
42. when to test sequence modeling / LM.

Avoid "it depends" unless immediately converted into a decision rule or explicit experimental factor.

---

# 29. Literature requirements

Search current literature before final recommendations.

At minimum investigate:

- avian photoreceptor MHU;
- subtype proportions;
- multicomponent hyperuniform point processes;
- hyperuniform graph/network constructions;
- IBM hyperuniform/nearly-hyperuniform neural networks;
- neural cellular automata;
- recurrent message-passing networks;
- sparse GNNs;
- small-world neural computation;
- learned sparse connectivity / rewiring;
- topology optimization in neural networks;
- spatially embedded recurrent networks;
- edge-centric GNNs;
- line graphs;
- hypergraphs;
- higher-order graph models.

For literature-dependent claims:
- cite sources;
- distinguish peer review / preprint / patent / author commentary;
- do not treat patents as independent empirical validation.

Flag prior art closer to LARP than currently known.

---

# 30. Output constraints

Do not summarize this brief.

Do not repeat obvious background.

Spend tokens on unresolved decisions, evidence, mechanisms, and experimental design.

Target:
approximately 8,000–12,000 words maximum unless significantly more is truly necessary.

No production code.
Equations and pseudocode are allowed.

---

# 31. Required output structure

## A. Executive verdict
Concise.
State:
- technical coherence;
- strongest hypothesis;
- weakest assumption;
- whether v0.1 is worth implementing.

## B. Corrections
Identify false, weak, misleading, or confounded premises in this brief.

## C. Prior-art map
Table:
- concept
- closest prior work
- evidence strength
- relevance
- remaining gap

## D. Competing hypotheses + priors
For each:
- mechanism;
- subjective prior;
- expected evidence;
- disconfirming evidence.

## E. Architecture Decision Record — LARP v0.1
Exact values.

Include:
- N;
- dimensions;
- subtype proportions;
- geometry generator;
- graph;
- hidden dimension;
- message/update;
- recurrence;
- input/output;
- normalization/residual;
- parameter target;
- expected compute/memory;
- software stack.

## F. Mathematical specification
Equations only where useful.

## G. MHU-G / MHU-T / MHU-F
Implementation-level definitions.

## H. Baselines
Implementation-level definitions.

## I. Ablation matrix
Include:
- geometry;
- type identity;
- type-specific parameters;
- connectivity;
- degree;
- parameters;
- recurrent steps;
- scientific purpose.

## J. First experiment sequence
For each:
- task;
- generator;
- train/test sizes;
- metrics;
- expected outcomes by hypothesis;
- interpretation.

## K. Robustness protocol
Exact lesion/dropout tests.

## L. AB update protocol
Practical template:
- prior;
- predicted evidence;
- result;
- likelihood assessment;
- posterior/update;
- mechanism update;
- next test.

## M. Stop / pivot / continue
Concrete decision rules.

## N. v0.2 roadmap
Conditional on plausible v0.1 outcomes.

## O. Route toward problem solving and later LM
State prerequisites and likely architectural changes.

## P. Edge-as-computation branch
Prior art + minimal later experiment.

## Q. Implementation contract for SOL 6.1 UltraCode
A precise checklist.

## R. Machine-readable decision block
End with a fenced JSON object conceptually named:

`larp_v0_1_decisions`

It must contain all concrete v0.1 decisions.

Scientific choices should not be left unresolved in this JSON unless explicitly marked as experimental factors.

---

# 32. Reasoning standard

Be adversarial toward attractive narratives.

Reject unsupported reasoning of the form:
- biological therefore better;
- complex therefore intelligent;
- emergent therefore powerful;
- hyperuniform therefore robust.

For every important architectural claim, seek:
- mechanism;
- plausible failure mode;
- confound;
- discriminating test.

Label uncertainty explicitly.

Do not optimize for enthusiasm.

---

# 33. Success condition for this review

The review succeeds if:

1. a downstream coding model can implement v0.1 without making hidden scientific decisions;
2. the experiment can falsify or weaken the MHU hypothesis;
3. geometry effects can be separated from type-function effects;
4. comparisons are fair against strong baselines;
5. the first round is feasible on consumer hardware;
6. the project has a clear AB update protocol;
7. failure is still scientifically informative.

Ultimate objective:

> Maximize information gained per unit of compute about whether multihyperuniform organization is a useful neural-computation inductive bias, under what conditions, and why.
