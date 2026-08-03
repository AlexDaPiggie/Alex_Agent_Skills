---
name: deep_stem_learning_path
description: Meta-skill orchestrating recursive STEM explanations using stem_explainer and concept_decomposer, saving individual concept markdown files in Explanation/ and synthesizing a master comprehensive guide.
---

# Deep STEM Learning Path (Meta-Skill Orchestrator)

Use this skill when asked to create a complete, recursive, multi-level STEM explanation package for a primary topic.

## Workflow Execution Steps

### Phase 1: Recursive Concept Graph Building
1. Take target STEM topic.
2. Invoke `concept_decomposer` to identify all prerequisite concepts.
3. For each non-high-school concept identified, recursively run `concept_decomposer` until all terminal leaf nodes are basic high-school level concepts.
4. Construct a topological ordering (Foundational concepts -> Intermediate concepts -> Primary topic).

### Phase 2: Individual File Generation (Bottom-Up)
1. For each concept in the topological order (starting from deepest prerequisites up to primary topic):
   - Apply `stem_explainer` to generate a beginner-friendly explanation with 3-stage math progression (Algebra -> Calculus -> Linear Algebra).
   - Write output file to `Explanation/<Concept_Name>.md`.

### Phase 3: Comprehensive Master Guide Synthesis
1. Create `Explanation/Comprehensive_<Topic>_Guide.md`.
2. Synthesize content from all generated concept files in `Explanation/` into a single continuous, comprehensive master guide.
3. Structure master guide chronologically from ground-level foundations to advanced topic.
4. Include explicit step-by-step mathematical proofs linking foundational concepts to the final primary topic.
