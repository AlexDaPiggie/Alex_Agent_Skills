---
name: md_2_marp
description: Generate Marp presentations from markdown documents while keeping exact original content and preventing KaTeX/math parsing errors. Use when asked to convert notes or documents into Marp slides.
---

# Marp Presentation Generator

Use this skill when converting markdown documents or notes into a Marp presentation.

## Core Rules

### 1. Preserve Original Content
* Keep the exact wording, math formulas, code snippets, and explanations from the source document.
* Do not summarize, truncate, or omit details unless explicitly requested by the user.

### 2. Marp Header Configuration
Always start the output file with proper Marp frontmatter:
```yaml
---
marp: true
theme: gaia
paginate: true
backgroundColor: #ffffff
color: #333333
math: mathjax
---
```

### 3. Slide Layout & Pagination
* Use `---` to separate slides.
* Break slides logically at section headers (`#`, `##`, `###`) or natural topic transitions.
* If a section is long, split it across multiple slides using `---` and add `(Continued)` to the slide header.

### 4. KaTeX / Math Syntax Rules (CRITICAL)
To prevent KaTeX parse errors in Marp renderers:
* **Dedicated Block Lines:** Always place `$$` block math equations on their own dedicated lines with empty lines around them.
* **No Trailing Text on Block Math:** NEVER place text or inline math on the same line as a block math closing `$$`.
  * ❌ **INCORRECT:** `$$P_{final} = (I - K \cdot H) \cdot P_{new}$$ (where $I$ is identity)`
  * ✅ **CORRECT:**
    ```markdown
    $$P_{final} = (I - K \cdot H) \cdot P_{new}$$

    (where $I$ is identity)
    ```
* **Verify Delimiters:** Ensure all inline math uses `$ ... $` and block math uses `$$ ... $$` with matching pairs.

### 5. File Naming Rule
* The output presentation file **MUST** have a different filename than the original markdown document (e.g., append `_presentation` or `_slides` to the name, such as `document_slides.md`).
