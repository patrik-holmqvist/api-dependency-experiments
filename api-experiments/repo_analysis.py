import os
import ast
import re
import shutil
from git import Repo
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

class APIAnalyzer:
    def __init__(self):
        # Common API patterns to look for
        self.api_patterns = {
            'http_requests': [
                r'requests\.(get|post|put|delete|patch)\s*\(',
                r'httpx\.(get|post|put|delete|patch)\s*\(',
                r'urllib\.request\.',
                r'aiohttp\.',
            ],
            'api_endpoints': [
                r'["\']https?://[^"\']+["\']',
                r'["\'][^"\']*api[^"\']*["\']',
                r'["\'][^"\']*endpoint[^"\']*["\']',
            ],
            'microservice_calls': [
                r'\.call\(',
                r'\.invoke\(',
                r'\.request\(',
                r'ServiceClient',
                r'ApiClient',
            ],
            'database_apis': [
                r'\.query\(',
                r'\.execute\(',
                r'\.fetch\(',
                r'Session\(',
                r'connection\.',
            ],
            'message_queue': [
                r'publish\(',
                r'subscribe\(',
                r'send_message\(',
                r'consume\(',
            ]
        }
        
        # API tier definitions based on common architectural patterns
        self.api_tiers = {
            1: ['gateway', 'auth', 'token', 'login', 'security'],
            2: ['customer', 'user', 'profile', 'account'],
            3: ['order', 'product', 'catalog', 'inventory', 'sales'],
            4: ['business', 'core', 'domain', 'service'],
            5: ['fulfillment', 'shipping', 'logistics', 'warehouse'],
            6: ['integration', 'external', 'third-party', 'partner'],
            7: ['notification', 'messaging', 'email', 'sms']
        }

    def clone_repo(self, repo_url: str, local_dir: str):
        """Clone repository to local directory"""
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        
        # Format URL if needed
        if not repo_url.startswith('http'):
            if '/' in repo_url and not repo_url.startswith('github.com'):
                repo_url = f"https://github.com/{repo_url}"
            elif not repo_url.startswith('github.com'):
                repo_url = f"https://github.com/{repo_url}"
        
        print(f"Cloning from: {repo_url}")
        Repo.clone_from(repo_url, local_dir)

    def find_source_files(self, local_dir: str) -> List[str]:
        """Find all relevant source files (Python, JavaScript, Java, etc.)"""
        source_files = []
        extensions = ['.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.cs']
        
        for root, _, files in os.walk(local_dir):
            # Skip common non-source directories
            if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', '.pytest_cache', 'venv', '.venv']):
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    source_files.append(os.path.join(root, file))
        
        return source_files

    def analyze_file_for_apis(self, file_path: str) -> Dict[str, List[str]]:
        """Analyze a single file for API calls and patterns"""
        apis_found = defaultdict(list)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Search for API patterns
            for category, patterns in self.api_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        apis_found[category].extend(matches)
            
            # Extract URLs and endpoints
            url_pattern = r'["\']https?://[^"\']+["\']'
            urls = re.findall(url_pattern, content)
            if urls:
                apis_found['endpoints'].extend([url.strip('"\'') for url in urls])
            
            # Look for API class/function names
            api_names = re.findall(r'class\s+(\w*[Aa]pi\w*)', content)
            api_names.extend(re.findall(r'def\s+(\w*api\w*)', content, re.IGNORECASE))
            if api_names:
                apis_found['api_definitions'].extend(api_names)
                
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
        return apis_found

    def categorize_api_by_tier(self, api_name: str) -> int:
        """Categorize API into architectural tier based on name patterns"""
        api_lower = api_name.lower()
        
        for tier, keywords in self.api_tiers.items():
            if any(keyword in api_lower for keyword in keywords):
                return tier
                
        return 4  # Default to tier 4 (business/core)

    def analyze_repository(self, local_dir: str) -> Dict:
        """Analyze entire repository for API usage patterns"""
        source_files = self.find_source_files(local_dir)
        all_apis = defaultdict(list)
        api_usage_count = Counter()
        file_api_map = {}
        
        print(f"Analyzing {len(source_files)} source files...")
        
        for file_path in source_files:
            file_apis = self.analyze_file_for_apis(file_path)
            file_api_map[file_path] = file_apis
            
            # Aggregate APIs
            for category, apis in file_apis.items():
                all_apis[category].extend(apis)
                for api in apis:
                    api_usage_count[api] += 1
        
        # Extract unique API names and categorize
        unique_apis = set()
        for apis in all_apis.values():
            unique_apis.update(apis)
        
        # Create tier mapping
        api_tiers = {}
        for api in unique_apis:
            tier = self.categorize_api_by_tier(str(api))
            api_tiers[api] = tier
        
        return {
            'apis': dict(all_apis),
            'usage_counts': api_usage_count,
            'api_tiers': api_tiers,
            'file_count': len(source_files),
            'files_analyzed': file_api_map
        }

    def generate_tiered_table(self, analysis_result: Dict) -> str:
        """Generate a markdown table showing API tiers"""
        api_tiers = analysis_result['api_tiers']
        usage_counts = analysis_result['usage_counts']
        
        # Group APIs by tier
        tiers = defaultdict(list)
        for api, tier in api_tiers.items():
            tiers[tier].append((api, usage_counts.get(api, 0)))
        
        table = "## API Architectural Tiers\n\n"
        table += "| Tier | API Category | APIs | Usage Count | Dependencies |\n"
        table += "|------|--------------|------|-------------|-------------|\n"
        
        tier_names = {
            1: "Authentication & Core",
            2: "Customer Data", 
            3: "Order & Sales",
            4: "Business Core",
            5: "Fulfillment",
            6: "Integration",
            7: "Communication"
        }
        
        for tier in sorted(tiers.keys()):
            apis_list = ", ".join([f"{api} ({count})" for api, count in sorted(tiers[tier], key=lambda x: x[1], reverse=True)[:5]])
            deps = f"Tier {tier-1}" if tier > 1 else "None"
            table += f"| {tier} | {tier_names.get(tier, 'Other')} | {apis_list} | - | {deps} |\n"
        
        return table

    def generate_mermaid_diagram(self, analysis_result: Dict) -> str:
        """Generate enhanced Mermaid diagram showing API dependencies and usage"""
        api_tiers = analysis_result['api_tiers']
        usage_counts = analysis_result['usage_counts']
        
        # Group APIs by tier
        tiers = defaultdict(list)
        for api, tier in api_tiers.items():
            if usage_counts.get(api, 0) > 0:  # Only include APIs that are actually used
                tiers[tier].append((api, usage_counts[api]))
        
        mermaid = "```mermaid\nflowchart TD\n"
        
        # Create nodes for each tier
        node_counter = 0
        node_map = {}
        
        for tier in sorted(tiers.keys()):
            # Get top APIs for this tier (limit to avoid clutter)
            top_apis = sorted(tiers[tier], key=lambda x: x[1], reverse=True)[:3]
            
            for api, count in top_apis:
                node_id = f"N{node_counter}"
                clean_api = str(api).replace('"', '').replace("'", '')[:20]  # Clean and truncate
                node_map[api] = (node_id, tier, count)
                mermaid += f"    {node_id}[\"{clean_api}\"]\n"
                node_counter += 1
        
        # Add connections between tiers
        mermaid += "\n    %% Tier connections\n"
        tier_nodes = defaultdict(list)
        for api, (node_id, tier, count) in node_map.items():
            tier_nodes[tier].append((node_id, api, count))
        
        # Connect tiers (higher tiers depend on lower tiers)
        for tier in sorted(tier_nodes.keys()):
            if tier > 1 and tier-1 in tier_nodes:
                # Connect some nodes from current tier to previous tier
                current_tier_nodes = tier_nodes[tier][:2]  # Limit connections
                prev_tier_nodes = tier_nodes[tier-1][:2]
                
                for curr_node, curr_api, curr_count in current_tier_nodes:
                    for prev_node, prev_api, prev_count in prev_tier_nodes:
                        mermaid += f"    {prev_node} --\"{curr_count} calls\"--> {curr_node}\n"
        
        # Add styling for tiers
        mermaid += "\n    %% Styling\n"
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#ff99cc", "#c2c2f0", "#ffb3e6"]
        
        for tier, color in enumerate(colors, 1):
            if tier in tier_nodes:
                for node_id, _, _ in tier_nodes[tier]:
                    mermaid += f"    classDef tier{tier} fill:{color}\n"
                    mermaid += f"    class {node_id} tier{tier}\n"
        
        mermaid += "```\n"
        return mermaid

def main():
    analyzer = APIAnalyzer()
    
    repo_url = input("Enter GitHub repo URL: ")
    local_dir = "temp_repo"
    
    # Extract repo name for output files
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    output_file = f"{repo_name}_api_analysis.md"
    
    print("Cloning repository...")
    analyzer.clone_repo(repo_url, local_dir)
    
    print("Analyzing API dependencies...")
    analysis_result = analyzer.analyze_repository(local_dir)
    
    print(f"\nAnalysis Complete!")
    print(f"Files analyzed: {analysis_result['file_count']}")
    print(f"Unique APIs found: {len(analysis_result['api_tiers'])}")
    print(f"Total API calls: {sum(analysis_result['usage_counts'].values())}")
    
    # Generate outputs
    tiered_table = analyzer.generate_tiered_table(analysis_result)
    mermaid_diagram = analyzer.generate_mermaid_diagram(analysis_result)
    
    # Display in terminal
    print("\n" + "="*50)
    print(tiered_table)
    
    print("\n" + "="*50)
    print("## Mermaid Dependency Diagram")
    print(mermaid_diagram)
    
    # Save to file
    full_report = f"# API Dependency Analysis Report\n\n"
    full_report += f"**Repository:** {repo_url}\n"
    full_report += f"**Analysis Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    full_report += f"## Summary\n"
    full_report += f"- Files analyzed: {analysis_result['file_count']}\n"
    full_report += f"- Unique APIs found: {len(analysis_result['api_tiers'])}\n"
    full_report += f"- Total API calls: {sum(analysis_result['usage_counts'].values())}\n\n"
    full_report += tiered_table + "\n\n"
    full_report += "## Mermaid Dependency Diagram\n\n"
    full_report += mermaid_diagram
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    print(f"\n" + "="*50)
    print(f"📝 Full analysis saved to: {output_file}")
    print(f"🎨 You can copy the Mermaid code from the file and paste it into:")
    print(f"   - Mermaid Live Editor: https://mermaid-js.github.io/mermaid-live-editor/")
    print(f"   - GitHub markdown files")
    print(f"   - VS Code with Mermaid extension")
    
    # Cleanup
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)

if __name__ == "__main__":
    main()