---
name: how_to_explain_stem
description: Provides a user guide and quick reference on how to use the STEM explanation skills (stem_explainer, concept_decomposer, deep_stem_learning_path).
---

# STEM Explanation System - User Guide

Use this skill whenever asked how to explain STEM topics, how the explanation framework works, or how to invoke the STEM explanation skills.

## Available STEM Skills

1. **`deep_stem_learning_path`** (Full Meta-Skill Pipeline):
   - Recursively maps prerequisites down to high school level.
   - Generates individual `.md` files in `Explanation/` folder.
   - Combines everything into `Explanation/Comprehensive_<Topic>_Guide.md`.
   - **Trigger**: `"Use deep_stem_learning_path to explain <Topic>"`

2. **`stem_explainer`** (Single Topic Explainer):
   - High-school friendly tone without buzzwords.
   - 3-Stage math notation: Algebra -> Calculus -> Linear Algebra.
   - Step-by-step derivation with no skipped steps.
   - **Trigger**: `"Use stem_explainer to explain <Topic>"`

3. **`concept_decomposer`** (Prerequisite Analyzer):
   - Analyzes a topic and outputs a dependency tree of prerequisite concepts.
   - **Trigger**: `"Use concept_decomposer on <Topic>"`
