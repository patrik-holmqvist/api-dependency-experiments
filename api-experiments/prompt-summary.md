# API Dependency Experiment
# API Usage & Dependency Flow Prompt Summary

## Repository
- **Repo:** `ingka-group-digital/returns`

## Goals
- Identify all external and internal APIs called in the repo.
- Rank these APIs by their importance and interdependencies.
- Visualize the data flows and dependencies between APIs using diagrams.
- Annotate the diagram with API usage/call frequency.
- Make the diagram suitable for rendering in Mermaid and/or other tools.

## Key Steps
1. **API Identification:**  
   - Gathered a list of APIs (external and internal) used in the repo, based on docs and code.
2. **Dependency Ranking:**  
   - Created a tiered ranking table of APIs, from core gateway/auth to communication and integration.
   - Each tier represents a dependency level: higher tiers depend on lower ones.
3. **Data Flow Visualization:**  
   - Provided Mermaid diagrams showing API tiers, explicit dependencies, and direction of data flow.
   - Iteratively improved diagrams for compatibility and clarity.
4. **Usage Annotation:**  
   - Adjusted diagrams to indicate usage frequency, first via arrow thickness, then by showing actual numbers on the arrow labels.

## Architectural Tiers

| Tier | API Category           | APIs                                                      | Dependencies             | Purpose                              |
|------|------------------------|-----------------------------------------------------------|--------------------------|--------------------------------------|
| 1    | Authentication & Core  | APIM (Kong Gateway), Guest Token API                      | None                     | Core gateway, authentication         |
| 2    | Customer Data          | ECD, Customer Master Read API V2, BCM                     | Tier 1                   | Customer information                 |
| 3    | Order & Sales          | Selling API (MFS), Sales Item API, Customer Order 360, SPE| Tiers 1, 2               | Order and product info               |
| 4    | Return Core            | Return Authorization, Return Management, Return Options, Return Payment | Tiers 1, 2, 3 | Core return processing               |
| 5    | Fulfillment            | Fulfillment Options, Fulfillment Order, Track and Trace   | Tiers 1, 3, 4            | Return fulfillment                   |
| 6    | Integration            | RPA APIs, SAMS, OM Print API                              | Tiers 1-5                | External systems integration         |
| 7    | Communication          | Customer Messaging v2                                     | All tiers                | Customer notifications               |

## Diagram Features
- Each arrow is labeled with the API name and usage/call count.
- Tiers are grouped for architectural clarity.
- Explicit direction of data flow, showing dependencies.
- Mermaid code is compatible with Mermaid Live Editor and GitHub markdown rendering.

## Example Mermaid Diagram

````mermaid
flowchart TD
    A[APIM Kong Gateway] -- ECD (900) --> C[ECD]
    C -- Selling API (1200) --> F[Selling API]
    F -- Return Authorization API (1800) --> J[Return Authorization]
    J -- Fulfillment Options API (1200) --> N[Fulfillment Options]
    N -- RPA API (300) --> Q[RPA]
    J -- Messaging API (300) --> T[Customer Messaging]
    %% (see full diagram in conversation)