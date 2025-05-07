# agent.py
import os
from openai import OpenAI
from typing import List, Dict, Any

# Import our XSLT Code Analyzer
from xslt_code_analyzer import XSLTCodeAnalyzerTool

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize our XSLT code analyzer tool with the path to your XSLT codebase
xslt_tool = XSLTCodeAnalyzerTool("/path/to/your/xslt/files")  # Replace with your actual path

# Define the available tools
tools = [
    {
        "type": "function",
        "function": xslt_tool.get_schema()
    }
]

async def handle_user_query(user_query: str) -> str:
    """
    Handle a user query about the XSLT codebase.
    
    Args:
        user_query: The user's question about the code
        
    Returns:
        A response to the user's query
    """
    # First, index the codebase if it hasn't been done already
    if not xslt_tool.analyzer.indexed:
        await xslt_tool.query("index")
    
    # Create a thread for the conversation
    thread = client.beta.threads.create()
    
    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_query
    )
    
    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=os.environ.get("OPENAI_ASSISTANT_ID"),  # Replace with your assistant ID
        tools=tools
    )
    
    # Poll for the run completion
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        if run_status.status == "requires_action":
            # Handle tool calls
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            
            for tool_call in tool_calls:
                # Execute the XSLT analyzer tool
                if tool_call.function.name == "xslt_code_analyzer":
                    # Parse the arguments
                    import json
                    args = json.loads(tool_call.function.arguments)
                    
                    # Execute the query
                    result = await xslt_tool.query(**args)
                    
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })
            
            # Submit the tool outputs
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        
        elif run_status.status == "completed":
            # Get the assistant's response
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            # Return the most recent assistant message
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
        
        elif run_status.status in ["failed", "cancelled", "expired"]:
            return f"Error: The assistant encountered an error. Status: {run_status.status}"
        
        # Wait before polling again
        import time
        time.sleep(1)

# Example of how to use the agent
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example queries users might ask
        queries = [
            "In how many files does the function 'transformRequest' appear?",
            "Show me the code for the 'convertToJSON' function",
            "Which files import 'common-utils.xsl'?",
            "Find all functions that process payment data",
            "Which templates are most frequently used across the codebase?",
            "Are there any unused functions in the codebase?",
            "Generate a dependency graph for file 'api-gateway.xsl'"
        ]
        
        # Test with one query
        response = await handle_user_query(queries[0])
        print(f"Query: {queries[0]}")
        print(f"Response: {response}")
    
    asyncio.run(main())

# Add imports
                for imported in self.file_dependencies[current]["imports"]:
                    if imported in self.files:
                        graph["edges"].append({
                            "source": current,
                            "target": imported,
                            "type": "import"
                        })
                        if imported not in visited:
                            queue.append(imported)
                
                # Add includes
                for included in self.file_dependencies[current]["includes"]:
                    if included in self.files:
                        graph["edges"].append({
                            "source": current,
                            "target": included,
                            "type": "include"
                        })
                        if included not in visited:
                            queue.append(included)
            
            return graph
        else:
            # Generate graph for entire codebase
            graph = {"nodes": [], "edges": []}
            
            # Add all files as nodes
            for file_path in self.files.keys():
                graph["nodes"].append({
                    "id": file_path,
                    "label": os.path.basename(file_path)
                })
            
            # Add all dependencies as edges
            for source, deps in self.file_dependencies.items():
                for imported in deps["imports"]:
                    if imported in self.files:
                        graph["edges"].append({
                            "source": source,
                            "target": imported,
                            "type": "import"
                        })
                
                for included in deps["includes"]:
                    if included in self.files:
                        graph["edges"].append({
                            "source": source,
                            "target": included,
                            "type": "include"
                        })
            
            return graph
    
    def get_file_summary(self, file_path: str) -> Dict:
        """
        Generate a summary of a specific file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file summary information
        """
        if not self.indexed:
            raise ValueError("Code not indexed. Please call index_codebase() first.")
            
        # Find the canonical path in the index
        canonical_path = None
        for path in self.files.keys():
            if file_path in path or os.path.basename(file_path) == os.path.basename(path):
                canonical_path = path
                break
        
        if not canonical_path:
            return {"error": "File not found"}
        
        content = self.files[canonical_path]
        
        # Count functions, variables, and templates in this file
        functions = []
        for func_name, funcs in self.functions.items():
            for func in funcs:
                if func.file_path == canonical_path:
                    functions.append(func_name)
        
        variables = []
        for var_name, vars_list in self.variables.items():
            for var in vars_list:
                if var.file_path == canonical_path:
                    variables.append(var_name)
        
        templates = []
        for template_id, templates_list in self.templates.items():
            for template in templates_list:
                if template.file_path == canonical_path:
                    template_info = template.name or f"match:{template.match}"
                    if template.mode:
                        template_info += f" (mode:{template.mode})"
                    templates.append(template_info)
        
        # Check for stylesheet info
        stylesheet_version = "Unknown"
        stylesheet_pattern = re.compile(r'<xsl:stylesheet[^>]*version=[\'"]([^\'"]+)[\'"]')
        match = stylesheet_pattern.search(content)
        if match:
            stylesheet_version = match.group(1)
        
        # Count lines of code
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "file_path": canonical_path,
            "file_name": os.path.basename(canonical_path),
            "stylesheet_version": stylesheet_version,
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "functions": {
                "count": len(functions),
                "names": functions
            },
            "variables": {
                "count": len(variables),
                "names": variables
            },
            "templates": {
                "count": len(templates),
                "names": templates
            },
            "imports": self.file_dependencies[canonical_path]["imports"],
            "includes": self.file_dependencies[canonical_path]["includes"]
        }
    
    def get_code_statistics(self) -> Dict:
        """
        Generate statistics about the indexed codebase.
        
        Returns:
            Dictionary with code statistics
        """
        if not self.indexed:
            raise ValueError("Code not indexed. Please call index_codebase() first.")
        
        # Calculate statistics
        total_files = len(self.files)
        total_lines = sum(content.count('\n') + 1 for content in self.files.values())
        non_empty_lines = sum(len([line for line in content.split('\n') if line.strip()]) 
                             for content in self.files.values())
        
        unique_functions = len(self.functions)
        total_functions = sum(len(funcs) for funcs in self.functions.values())
        
        unique_variables = len(self.variables)
        total_variables = sum(len(vars_list) for vars_list in self.variables.values())
        
        unique_templates = len(self.templates)
        total_templates = sum(len(templates_list) for templates_list in self.templates.values())
        
        # Find most referenced functions
        function_references = {}
        for func_name, funcs in self.functions.items():
            references = 0
            for func in funcs:
                references += len(func.called_by)
            function_references[func_name] = references
        
        most_referenced_functions = sorted(function_references.items(), 
                                          key=lambda x: x[1], 
                                          reverse=True)[:10]
        
        # Find files with most functions
        functions_by_file = {}
        for funcs in self.functions.values():
            for func in funcs:
                if func.file_path not in functions_by_file:
                    functions_by_file[func.file_path] = 0
                functions_by_file[func.file_path] += 1
        
        files_with_most_functions = sorted(functions_by_file.items(),
                                          key=lambda x: x[1],
                                          reverse=True)[:10]
        
        return {
            "general": {
                "total_files": total_files,
                "total_lines": total_lines,
                "non_empty_lines": non_empty_lines,
                "avg_lines_per_file": round(total_lines / total_files if total_files else 0, 2)
            },
            "functions": {
                "unique_functions": unique_functions,
                "total_function_implementations": total_functions,
                "avg_implementations_per_function": round(total_functions / unique_functions if unique_functions else 0, 2),
                "most_referenced_functions": most_referenced_functions
            },
            "variables": {
                "unique_variables": unique_variables,
                "total_variable_definitions": total_variables,
                "avg_definitions_per_variable": round(total_variables / unique_variables if unique_variables else 0, 2)
            },
            "templates": {
                "unique_templates": unique_templates,
                "total_template_implementations": total_templates,
                "avg_implementations_per_template": round(total_templates / unique_templates if unique_templates else 0, 2)
            },
            "files": {
                "files_with_most_functions": [(os.path.basename(path), count) for path, count in files_with_most_functions]
            }
        }
    
    def find_similar_functions(self, function_name: str, threshold: float = 0.5) -> List[Dict]:
        """
        Find functions with similar signatures/usage patterns.
        
        Args:
            function_name: The name of the function to find similar functions for
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of similar functions with similarity scores
        """
        if not self.indexed:
            raise ValueError("Code not indexed. Please call index_codebase() first.")
            
        if function_name not in self.functions:
            return []
        
        # Get the target function's details
        target_funcs = self.functions[function_name]
        if not target_funcs:
            return []
            
        target_func = target_funcs[0]  # Use the first implementation as reference
        target_params = set(target_func.parameters)
        target_calls = target_func.calls
        target_called_by = target_func.called_by
        
        similar_funcs = []
        
        # Compare with all other functions
        for other_name, other_funcs in self.functions.items():
            if other_name == function_name:
                continue
                
            for other_func in other_funcs:
                similarity_score = 0.0
                reasons = []
                
                # Compare parameters
                other_params = set(other_func.parameters)
                param_similarity = 0
                if target_params and other_params:
                    common_params = target_params.intersection(other_params)
                    param_similarity = len(common_params) / max(len(target_params), len(other_params))
                    if param_similarity > 0:
                        reasons.append(f"Similar parameters ({len(common_params)} in common)")
                
                # Compare function calls
                call_similarity = 0
                if target_calls and other_func.calls:
                    common_calls = target_calls.intersection(other_func.calls)
                    call_similarity = len(common_calls) / max(len(target_calls), len(other_func.calls))
                    if call_similarity > 0:
                        reasons.append(f"Calls similar functions ({len(common_calls)} in common)")
                
                # Compare called by relationships
                called_by_similarity = 0
                if target_called_by and other_func.called_by:
                    common_called_by = target_called_by.intersection(other_func.called_by)
                    called_by_similarity = len(common_called_by) / max(len(target_called_by), len(other_func.called_by))
                    if called_by_similarity > 0:
                        reasons.append(f"Called by similar functions ({len(common_called_by)} in common)")
                
                # Calculate overall similarity
                similarity_score = (param_similarity + call_similarity + called_by_similarity) / 3
                
                if similarity_score >= threshold:
                    similar_funcs.append({
                        "name": other_name,
                        "file_path": other_func.file_path,
                        "similarity_score": round(similarity_score, 2),
                        "reasons": reasons
                    })
        
        # Sort by similarity score
        similar_funcs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_funcs
    
    def find_unused_functions(self) -> List[Dict]:
        """
        Find functions that are defined but not referenced elsewhere.
        
        Returns:
            List of unused functions with their locations
        """
        if not self.indexed:
            raise ValueError("Code not indexed. Please call index_codebase() first.")
            
        unused_functions = []
        
        for func_name, funcs in self.functions.items():
            for func in funcs:
                if not func.called_by:
                    # Check if it might be called dynamically
                    dynamic_call_pattern = re.compile(
                        rf'<xsl:call-template\s+name="[${{].*[}}].*"[^>]*>|' + 
                        rf'<xsl:[^>]*select="[^"]*{re.escape(func_name)}\s*\([^"]*"',
                        re.IGNORECASE
                    )
                    
                    dynamic_calls = False
                    for file_content in self.files.values():
                        if dynamic_call_pattern.search(file_content):
                            dynamic_calls = True
                            break
                    
                    if not dynamic_calls:
                        unused_functions.append({
                            "name": func_name,
                            "file_path": func.file_path,
                            "line_number": func.line_number,
                            "parameters": func.parameters
                        })
        
        return unused_functions
    
    def execute_query(self, query_type: str, **kwargs) -> Dict:
        """
        Execute a specific type of query on the codebase.
        This is the main entry point for the OpenAI Agent SDK.
        
        Args:
            query_type: The type of query to execute
            **kwargs: Parameters for the specific query
            
        Returns:
            Query results
        """
        if not self.indexed and query_type != "index":
            raise ValueError("Code not indexed. Please call index_codebase() first.")
        
        if query_type == "index":
            return self.index_codebase(**kwargs)
        
        elif query_type == "search_function":
            return {
                "results": self.search_function(**kwargs),
                "query": kwargs.get("query", "")
            }
        
        elif query_type == "get_function_code":
            return {
                "results": self.get_function_code(**kwargs),
                "function_name": kwargs.get("function_name", "")
            }
        
        elif query_type == "find_function_references":
            return {
                "results": self.find_function_references(**kwargs),
                "function_name": kwargs.get("function_name", "")
            }
        
        elif query_type == "search_template":
            return {
                "results": self.search_template(**kwargs),
                "query": kwargs.get("query", "")
            }
        
        elif query_type == "get_template_code":
            return {
                "results": self.get_template_code(**kwargs),
                "template_id": kwargs.get("template_id", "")
            }
        
        elif query_type == "search_variable":
            return {
                "results": self.search_variable(**kwargs),
                "query": kwargs.get("query", "")
            }
        
        elif query_type == "get_variable_code":
            return {
                "results": self.get_variable_code(**kwargs),
                "variable_name": kwargs.get("variable_name", "")
            }
        
        elif query_type == "find_function_occurrences":
            return {
                "results": self.find_function_occurrences(**kwargs),
                "function_name": kwargs.get("function_name", "")
            }
        
        elif query_type == "find_related_files":
            return {
                "results": self.find_related_files(**kwargs),
                "file_path": kwargs.get("file_path", "")
            }
        
        elif query_type == "text_search":
            return {
                "results": self.text_search(**kwargs),
                "query": kwargs.get("query", "")
            }
        
        elif query_type == "generate_dependency_graph":
            return {
                "results": self.generate_dependency_graph(**kwargs),
                "file_path": kwargs.get("file_path", None)
            }
        
        elif query_type == "get_file_summary":
            return {
                "results": self.get_file_summary(**kwargs),
                "file_path": kwargs.get("file_path", "")
            }
        
        elif query_type == "get_code_statistics":
            return {
                "results": self.get_code_statistics(),
            }
        
        elif query_type == "find_similar_functions":
            return {
                "results": self.find_similar_functions(**kwargs),
                "function_name": kwargs.get("function_name", ""),
                "threshold": kwargs.get("threshold", 0.5)
            }
        
        elif query_type == "find_unused_functions":
            return {
                "results": self.find_unused_functions(),
            }
        
        else:
            return {
                "error": f"Unknown query type: {query_type}",
                "available_queries": [
                    "index", "search_function", "get_function_code", 
                    "find_function_references", "search_template", "get_template_code",
                    "search_variable", "get_variable_code", "find_function_occurrences",
                    "find_related_files", "text_search", "generate_dependency_graph",
                    "get_file_summary", "get_code_statistics", "find_similar_functions",
                    "find_unused_functions"
                ]
            }


# OpenAI Agent SDK Tool Integration

class XSLTCodeAnalyzerTool:
    """
    Tool for analyzing XSLT code for use with OpenAI Agent SDK.
    """
    
    def __init__(self, code_directory: str = None):
        """
        Initialize the XSLT code analyzer tool.
        
        Args:
            code_directory: Path to the directory containing XSLT files
        """
        self.analyzer = XSLTCodeAnalyzer(code_directory)
    
    async def query(self, query_type: str, **kwargs) -> Dict:
        """
        Execute a specific type of query on the XSLT codebase.
        This is the main entry point for the OpenAI Agent SDK.
        
        Args:
            query_type: The type of query to execute
            **kwargs: Parameters for the specific query
            
        Returns:
            Query results
        """
        try:
            return self.analyzer.execute_query(query_type, **kwargs)
        except Exception as e:
            return {
                "error": str(e),
                "query_type": query_type,
                "parameters": kwargs
            }
    
    def get_schema(self) -> Dict:
        """
        Return the schema for this tool.
        
        Returns:
            Dictionary representing the tool schema
        """
        return {
            "name": "xslt_code_analyzer",
            "description": "Analyze XSLT code files and answer questions about functions, templates, variables, and dependencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_type": {
                        "type": "string",
                        "description": "The type of query to execute",
                        "enum": [
                            "index",
                            "search_function",
                            "get_function_code",
                            "find_function_references",
                            "search_template",
                            "get_template_code",
                            "search_variable",
                            "get_variable_code",
                            "find_function_occurrences",
                            "find_related_files",
                            "text_search",
                            "generate_dependency_graph",
                            "get_file_summary",
                            "get_code_statistics",
                            "find_similar_functions",
                            "find_unused_functions"
                        ]
                    },
                    "code_directory": {
                        "type": "string",
                        "description": "Path to the directory containing XSLT files (used with 'index' query type)"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (used with search_* query types)"
                    },
                    "function_name": {
                        "type": "string",
                        "description": "Name of the function to look up"
                    },
                    "template_id": {
                        "type": "string",
                        "description": "ID of the template to look up"
                    },
                    "variable_name": {
                        "type": "string",
                        "description": "Name of the variable to look up"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to a specific file"
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether the search should be case-sensitive (default: false)"
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Similarity threshold for function comparison (0-1, default: 0.5)"
                    }
                },
                "required": ["query_type"]
            }
        }

# Example usage
if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = XSLTCodeAnalyzer("path/to/xslt/files")
    
    # Index the codebase
    stats = analyzer.index_codebase()
    print(f"Indexed {stats['files_processed']} files, found {stats['functions_found']} functions")
    
    # Example queries
    functions = analyzer.search_function("transform")
    print(f"Found {len(functions)} functions matching 'transform'")
    
    occurrences = analyzer.find_function_occurrences("convertToJSON")
    print(f"Function 'convertToJSON' occurs in {occurrences['count']} files")
    
    # Tool setup for OpenAI Agent SDK
    tool = XSLTCodeAnalyzerTool("path/to/xslt/files")
    schema = tool.get_schema()
    print(f"Tool schema: {schema['name']} - {schema['description']}")