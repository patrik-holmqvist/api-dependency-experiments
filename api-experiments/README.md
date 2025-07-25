## API Dependency Analysis Tool

This tool analyzes a GitHub repository and provides comprehensive API dependency analysis with visualizations. It goes beyond simple file listing to identify API usage patterns, rank dependencies by architectural tiers, and generate detailed Mermaid diagrams.

### Features

- **API Discovery**: Identifies external and internal API calls across multiple programming languages
- **Architectural Tiering**: Categorizes APIs into 7 architectural tiers (Auth/Core → Customer → Orders → Business → Fulfillment → Integration → Communication)
- **Usage Analytics**: Counts API call frequencies and usage patterns
- **Dependency Mapping**: Shows relationships and dependencies between API tiers
- **Mermaid Visualization**: Generates interactive diagrams with usage annotations and tier-based styling

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python repo_analysis.py
```
Enter the GitHub repo URL when prompted (supports various URL formats).

### Output

The tool provides:

1. **Analysis Summary**: File count, unique APIs found, total API calls
2. **Tiered API Table**: APIs organized by architectural importance with usage counts
3. **Mermaid Dependency Diagram**: Visual representation showing:
   - API relationships and data flow
   - Usage frequency on connection labels  
   - Color-coded tiers for architectural clarity
   - Compatible with Mermaid Live Editor and GitHub markdown

### Supported Languages

- Python (.py)
- JavaScript/TypeScript (.js, .ts)
- Java (.java)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- C# (.cs)

### API Pattern Detection

The tool identifies various API patterns including:
- HTTP requests (requests, httpx, urllib, aiohttp)
- API endpoints and URLs
- Microservice calls
- Database API calls  
- Message queue operations
- API class and function definitionsl

This tool analyzes a GitHub repository and outputs a Mermaid diagram of Python files.

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python repo_analysis.py
```
Enter the GitHub repo URL when prompted.

### Output

You’ll get a Mermaid diagram listing all Python files in the repo.


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
