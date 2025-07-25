# API Dependency Experiments

This repository explores techniques for analyzing and visualizing API usage and dependency flows within a codebase. The approach focuses on identifying APIs, ranking their importance, and visually mapping dependencies for clarity and architectural insight.

## Overview

The core methodology includes:
- **API Identification:** Catalog all external and internal APIs used in a target repository.
- **Dependency Ranking:** Organize APIs into architectural tiers based on their role and interdependencies.
- **Data Flow Visualization:** Use diagrams (e.g., Mermaid) to show relationships, dependencies, and data flow direction.
- **Usage Annotation:** Indicate API call frequency using arrow labels or thickness for added context.

## Example

The [prompt-summary.md](api-experiments/prompt-summary.md) file demonstrates this approach using the `ingka-group-digital/returns` repository as a case study. It provides:
- A tiered table of APIs and their dependencies.
- Sample Mermaid diagrams with annotated usage.
- Steps for iterative diagram refinement.

## How to Use

1. **Adapt the Methodology:**  
   Apply the identification, ranking, and visualization process to your repository.
2. **Generate Diagrams:**  
   Use Mermaid or compatible tools for diagramming.  
   Example code is provided in `prompt-summary.md`.
3. **Annotate for Clarity:**  
   Add call frequency and explicit dependency arrows to make diagrams actionable for architecture reviews.

## Resources

- [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor/)
- [prompt-summary.md](api-experiments/prompt-summary.md) – Full workflow and examples

## License

This repository is open for experimentation and knowledge sharing. See [LICENSE](LICENSE) for details.

## Contributions

Feel free to open issues or pull requests to suggest improvements or add new case studies.
