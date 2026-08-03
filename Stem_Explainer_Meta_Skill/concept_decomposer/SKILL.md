---
name: concept_decomposer
description: Extracts non-high-school prerequisite concepts from a STEM topic or text, producing a list of underlying concepts to explain recursively.
---

# Concept Decomposer

Use this skill to break down a STEM topic into a dependency tree of prerequisite concepts.

## Core Rules

1. **Input Analysis**:
   - Given a target STEM topic or draft explanation, identify all mathematical, statistical, physical, or technical concepts required to fully understand it.

2. **Filtering Level**:
   - Mark whether each concept is **High School Level** (algebra, basic trigonometry, simple 1D velocity) or **Post-High School Level** (calculus, linear algebra, multivariable calculus, probability distributions, matrix operations, complex differential equations).

3. **Output Format**:
   - Produce a structured list of prerequisite concepts that need recursive explanation:
     - Concept Name
     - Level (High School / Advanced)
     - Direct Dependency (Which concept requires this)
     - Reason / Brief Context
