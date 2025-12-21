#!/usr/bin/env python3
"""
Codebase Indexer - Generate relationship and dependency maps for codebases
Framework-agnostic with TOON format support for token-efficient output
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Tuple, Any
from collections import defaultdict
import argparse


# Framework configurations
FRAMEWORK_CONFIGS = {
    "astro": {
        "extensions": [".astro", ".tsx", ".jsx"],
        "component_dirs": ["src/components", "src/layouts", "src/pages"],
        "data_patterns": [r'client\.fetch\([\'"]([^\'"]+)[\'"]'],
    },
    "react": {
        "extensions": [".jsx", ".tsx"],
        "component_dirs": ["src/components", "src/pages", "app", "components"],
        "data_patterns": [
            r'fetch\([\'"]([^\'"]+)[\'"]',
            r'axios\.get\([\'"]([^\'"]+)[\'"]',
        ],
    },
    "vue": {
        "extensions": [".vue"],
        "component_dirs": ["src/components", "src/views", "src/pages"],
        "data_patterns": [r'fetch\([\'"]([^\'"]+)[\'"]'],
    },
    "svelte": {
        "extensions": [".svelte"],
        "component_dirs": ["src/components", "src/routes", "src/lib"],
        "data_patterns": [r'fetch\([\'"]([^\'"]+)[\'"]'],
    },
    "next": {
        "extensions": [".jsx", ".tsx"],
        "component_dirs": ["components", "app", "pages", "src/components"],
        "data_patterns": [r'fetch\([\'"]([^\'"]+)[\'"]'],
    },
    "angular": {
        "extensions": [".ts", ".component.ts"],
        "component_dirs": ["src/app"],
        "data_patterns": [r'http\.get\([\'"]([^\'"]+)[\'"]'],
    },
    "solid": {
        "extensions": [".jsx", ".tsx"],
        "component_dirs": ["src/components", "src/pages"],
        "data_patterns": [r'fetch\([\'"]([^\'"]+)[\'"]'],
    },
}


class TOONEncoder:
    """Encode Python data structures to TOON format"""
    
    def __init__(self, indent: int = 2, delimiter: str = ","):
        self.indent = indent
        self.delimiter = delimiter
        self.delimiter_display = {
            ",": "",  # implicit
            "\t": "\t",
            "|": "|",
        }.get(delimiter, "")
    
    def encode(self, data: Any, level: int = 0) -> str:
        """Encode data to TOON format"""
        if data is None or data == {}:
            return ""
        
        if isinstance(data, dict):
            return self._encode_object(data, level)
        elif isinstance(data, list):
            return self._encode_array(data, level)
        else:
            return self._encode_primitive(data)
    
    def _encode_object(self, obj: dict, level: int) -> str:
        """Encode object to TOON"""
        lines = []
        indent_str = " " * (level * self.indent)
        
        for key, value in obj.items():
            quoted_key = self._quote_key(key)
            
            if isinstance(value, dict):
                if not value:  # empty dict
                    lines.append(f"{indent_str}{quoted_key}:")
                else:
                    lines.append(f"{indent_str}{quoted_key}:")
                    lines.append(self._encode_object(value, level + 1))
            elif isinstance(value, list):
                array_str = self._encode_array(value, level + 1)
                if array_str.startswith('['):  # Array header
                    lines.append(f"{indent_str}{quoted_key}{array_str}")
                else:
                    lines.append(f"{indent_str}{quoted_key}: {array_str}")
            else:
                quoted_value = self._quote_value(value)
                lines.append(f"{indent_str}{quoted_key}: {quoted_value}")
        
        return "\n".join(line for line in lines if line)
    
    def _encode_array(self, arr: list, level: int) -> str:
        """Encode array to TOON"""
        if not arr:
            return "[0]:"
        
        # Check if it's a uniform array of objects (tabular)
        if self._is_tabular(arr):
            return self._encode_tabular(arr, level)
        
        # Check if it's a primitive array
        if all(not isinstance(item, (dict, list)) for item in arr):
            return self._encode_primitive_array(arr)
        
        # Mixed/list format
        return self._encode_list(arr, level)
    
    def _is_tabular(self, arr: list) -> bool:
        """Check if array can use tabular format"""
        if not arr or not all(isinstance(item, dict) for item in arr):
            return False
        
        # Get keys from first item
        first_keys = set(arr[0].keys())
        
        # Check all items have same keys and only primitive values
        for item in arr:
            if set(item.keys()) != first_keys:
                return False
            if any(isinstance(v, (dict, list)) for v in item.values()):
                return False
        
        return True
    
    def _encode_tabular(self, arr: list, level: int) -> str:
        """Encode uniform array as tabular"""
        keys = list(arr[0].keys())
        delimiter_sep = self.delimiter_display
        
        # Header
        keys_str = self.delimiter.join(keys)
        header = f"[{len(arr)}{delimiter_sep}]{{{keys_str}}}:"
        
        # Rows
        rows = []
        indent_str = " " * (level * self.indent)
        
        for item in arr:
            values = [self._quote_value(item[k]) for k in keys]
            row = self.delimiter.join(values)
            rows.append(f"{indent_str}{row}")
        
        if not rows:
            return header
        
        return header + "\n" + "\n".join(rows)
    
    def _encode_primitive_array(self, arr: list) -> str:
        """Encode array of primitives"""
        delimiter_sep = self.delimiter_display
        values = [self._quote_value(v) for v in arr]
        return f"[{len(arr)}{delimiter_sep}]: {self.delimiter.join(values)}"
    
    def _encode_list(self, arr: list, level: int) -> str:
        """Encode mixed array as list"""
        lines = [f"[{len(arr)}]:"]
        indent_str = " " * (level * self.indent)
        
        for item in arr:
            if isinstance(item, dict):
                # First field on hyphen line
                first_key = list(item.keys())[0] if item else None
                if first_key:
                    first_value = self._quote_value(item[first_key])
                    lines.append(f"{indent_str}- {self._quote_key(first_key)}: {first_value}")
                    # Rest of fields
                    for key in list(item.keys())[1:]:
                        value = self._quote_value(item[key])
                        lines.append(f"{indent_str}  {self._quote_key(key)}: {value}")
            elif isinstance(item, list):
                sub_array = self._encode_array(item, level + 1)
                lines.append(f"{indent_str}- {sub_array}")
            else:
                lines.append(f"{indent_str}- {self._quote_value(item)}")
        
        return "\n".join(lines)
    
    def _quote_key(self, key: str) -> str:
        """Quote key if necessary"""
        # Keys must be quoted if they don't match identifier pattern
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_\.]*$', key):
            return key
        return f'"{key}"'
    
    def _quote_value(self, value: Any) -> str:
        """Quote value if necessary"""
        if value is None:
            return "null"
        
        if isinstance(value, bool):
            return "true" if value else "false"
        
        if isinstance(value, (int, float)):
            return str(value)
        
        # String quoting rules
        s = str(value)
        
        # Empty string
        if not s:
            return '""'
        
        # Check if needs quoting
        needs_quote = (
            s[0] == ' ' or s[-1] == ' ' or  # Leading/trailing spaces
            any(c in s for c in [self.delimiter, ':', '"', '\\', '\n', '\r', '\t']) or
            s in ['true', 'false', 'null'] or
            s.startswith('- ') or
            self._looks_like_number(s) or
            s.startswith('[') or s.startswith('{')
        )
        
        if needs_quote:
            # Escape quotes and backslashes
            escaped = s.replace('\\', '\\\\').replace('"', '\\"')
            escaped = escaped.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            return f'"{escaped}"'
        
        return s
    
    def _looks_like_number(self, s: str) -> bool:
        """Check if string looks like a number"""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def _encode_primitive(self, value: Any) -> str:
        """Encode primitive value"""
        return self._quote_value(value)


class CodebaseIndexer:
    def __init__(self, project_root: str, output_format: str = "toon", 
                 framework: Optional[str] = None, delimiter: str = ","):
        self.project_root = Path(project_root).resolve()
        self.output_format = output_format.lower()
        self.delimiter = delimiter
        self.framework = framework
        
        # Auto-detect framework if not specified
        if not self.framework:
            self.framework = self._detect_framework()
        
        # Get framework config
        self.config = FRAMEWORK_CONFIGS.get(self.framework, {
            "extensions": [".jsx", ".tsx", ".vue", ".svelte", ".astro"],
            "component_dirs": ["src/components", "src"],
            "data_patterns": [],
        })
        
        # Find source directories
        self.src_dirs = self._find_source_dirs()
        self.output_dir = self.src_dirs[0] / ".ai" if self.src_dirs else self.project_root / ".ai"
        
        # Results storage
        self.components = {}
        self.dependencies = {"npmPackages": {}, "utilities": {}, "styles": {}, "schemas": {}}
        self.data_queries = {"dataSources": {}, "staticPaths": {}}
        
        # Statistics
        self.stats = {
            "components_scanned": 0,
            "relationships_found": 0,
            "utilities_found": 0,
            "schemas_found": 0,
            "queries_found": 0,
            "framework": self.framework,
            "errors": []
        }
    
    def _detect_framework(self) -> str:
        """Auto-detect framework from package.json"""
        package_json = self.project_root / "package.json"
        
        if not package_json.exists():
            return "react"  # default
        
        try:
            with open(package_json) as f:
                data = json.load(f)
            
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            
            # Check for framework-specific packages
            if "astro" in deps:
                return "astro"
            elif "next" in deps:
                return "next"
            elif "vue" in deps or "@vue/compiler-sfc" in deps:
                return "vue"
            elif "svelte" in deps:
                return "svelte"
            elif "@angular/core" in deps:
                return "angular"
            elif "solid-js" in deps:
                return "solid"
            elif "react" in deps:
                return "react"
            
        except Exception as e:
            self.stats["errors"].append(f"Error detecting framework: {e}")
        
        return "react"  # default fallback
    
    def _find_source_dirs(self) -> List[Path]:
        """Find source directories based on framework"""
        possible_dirs = []
        
        # Check framework-specific directories
        for dir_name in self.config["component_dirs"]:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                possible_dirs.append(dir_path)
        
        # Fallback to src/
        src_dir = self.project_root / "src"
        if src_dir.exists() and src_dir not in possible_dirs:
            possible_dirs.append(src_dir)
        
        return possible_dirs or [self.project_root]
    
    def scan(self):
        """Main scanning entry point"""
        print(f"Scanning {self.framework} codebase...")
        
        # Scan components
        self._scan_components()
        
        # Scan utilities
        self._scan_utilities()

        # Scan schemas
        self._scan_schemas()

        # Scan package.json
        self._scan_package_json()

        # Scan data queries
        self._scan_data_queries()

        # Scan CSS
        self._scan_styles()
        
        # Generate output files
        self._generate_outputs()
        
        # Print summary
        self._print_summary()
    
    def _scan_components(self):
        """Scan all components and their relationships"""
        component_extensions = set(self.config["extensions"])
        
        for src_dir in self.src_dirs:
            for file_path in src_dir.rglob('*'):
                # Skip node_modules and dot directories
                if any(part.startswith('.') or part == 'node_modules' 
                       for part in file_path.parts):
                    continue
                
                if file_path.suffix in component_extensions:
                    self._process_component_file(file_path)
        
        self.stats["components_scanned"] = len(self.components)
    
    def _process_component_file(self, file_path: Path):
        """Process a single component file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            relative_path = str(file_path.relative_to(self.project_root))
            # FIX: Use full relative path as key to avoid filename collisions
            # Previously used file_path.stem which caused collisions with duplicate filenames
            # (e.g., index.astro, [slug].astro in different directories)
            component_name = relative_path
            
            # Determine component type from path
            component_type = self._get_component_type(file_path)
            
            # Determine framework/file type
            framework_type = self._get_framework_type(file_path)
            
            # Parse imports
            imports = self._parse_imports(content, file_path)
            
            # Check for metadata file (multiple formats)
            # Try both Component.astro.metadata.ts and Component.metadata.ts patterns
            metadata_formats = ['.metadata.json', '.metadata.ts', '.metadata.tsx']
            metadata_path = None
            has_metadata = False

            for ext in metadata_formats:
                # Try: Component.astro.metadata.ts
                potential_path = file_path.with_suffix(file_path.suffix + ext)
                if potential_path.exists():
                    metadata_path = potential_path
                    has_metadata = True
                    break

                # Try: Component.metadata.ts (remove original extension first)
                potential_path = file_path.with_suffix(ext)
                if potential_path.exists():
                    metadata_path = potential_path
                    has_metadata = True
                    break
            
            # Store component info
            component_info = {
                "path": relative_path,
                "type": component_type,
                "framework": framework_type,
                "uses": [imp["name"] for imp in imports if imp["is_component"]],
                "usedBy": [],  # Will be populated later
                "externalDependencies": [imp["source"] for imp in imports if imp["is_external"]],
                "utilityDependencies": [imp["source"] for imp in imports if imp["is_utility"]],
                "schemaDependencies": [imp["source"] for imp in imports if imp["is_schema"]]
            }
            
            if has_metadata:
                component_info["metadata"] = str(metadata_path.relative_to(self.project_root))

            # Check for collision (shouldn't happen with full paths, but good to log)
            if component_name in self.components:
                self.stats["errors"].append(
                    f"WARNING: Component name collision for '{component_name}'\n"
                    f"  Existing: {self.components[component_name]['path']}\n"
                    f"  New: {relative_path}\n"
                    f"  Using new entry (overwriting)"
                )

            self.components[component_name] = component_info
            
        except Exception as e:
            self.stats["errors"].append(f"Error processing {file_path.name}: {str(e)}")
    
    def _get_component_type(self, file_path: Path) -> str:
        """Determine component type from file path"""
        path_str = str(file_path).lower()
        
        # Atomic design patterns
        if '/atoms/' in path_str or '/atom/' in path_str:
            return 'atom'
        elif '/molecules/' in path_str or '/molecule/' in path_str:
            return 'molecule'
        elif '/organisms/' in path_str or '/organism/' in path_str:
            return 'organism'
        elif '/templates/' in path_str or '/template/' in path_str:
            return 'template'
        
        # Common patterns
        elif '/ui/' in path_str or '/components/ui/' in path_str:
            return 'ui'
        elif '/layouts/' in path_str or '/layout/' in path_str:
            return 'layout'
        elif '/pages/' in path_str or '/views/' in path_str or '/routes/' in path_str:
            return 'page'
        elif '/hooks/' in path_str:
            return 'hook'
        elif '/contexts/' in path_str or '/context/' in path_str:
            return 'context'
        else:
            return 'component'
    
    def _get_framework_type(self, file_path: Path) -> str:
        """Determine framework type from file extension"""
        ext = file_path.suffix
        mapping = {
            '.astro': 'astro',
            '.vue': 'vue',
            '.svelte': 'svelte',
            '.jsx': 'react',
            '.tsx': 'react',
        }
        return mapping.get(ext, 'javascript')
    
    def _parse_imports(self, content: str, file_path: Path) -> List[Dict]:
        """Parse import statements from file content"""
        imports = []
        
        # Regex patterns for different import styles
        patterns = [
            r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+\{\s*([^\}]+)\s*\}\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                groups = match.groups()
                imported_names = groups[0].strip()
                source = groups[1].strip()
                
                # Handle multiple imports in braces
                if '{' in imported_names or ',' in imported_names:
                    names = [n.strip() for n in imported_names.replace('{', '').replace('}', '').split(',')]
                else:
                    names = [imported_names]
                
                for name in names:
                    if not name or name in ['type', 'typeof']:
                        continue
                    
                    import_info = {
                        "name": name,
                        "source": source,
                        "is_component": self._is_component_import(source),
                        "is_external": self._is_external_import(source),
                        "is_utility": self._is_utility_import(source),
                        "is_schema": self._is_schema_import(source)
                    }
                    imports.append(import_info)
                    self.stats["relationships_found"] += 1
        
        return imports
    
    def _is_component_import(self, source: str) -> bool:
        """Check if import is a component"""
        component_extensions = tuple(self.config["extensions"])
        return any(source.endswith(ext) for ext in component_extensions) or '/components/' in source
    
    def _is_external_import(self, source: str) -> bool:
        """Check if import is from node_modules"""
        return not (source.startswith('.') or source.startswith('/') or 
                   source.startswith('@/') or source.startswith('~/'))
    
    def _is_utility_import(self, source: str) -> bool:
        """Check if import is from lib/utils"""
        return ('/lib/' in source or '/utils/' in source or '/helpers/' in source or
                source.startswith('@/lib/') or source.startswith('~/lib/'))

    def _is_schema_import(self, source: str) -> bool:
        """Check if import is from schemas"""
        return ('/schemas/' in source or '/schema/' in source or
                source.startswith('@/schemas/') or source.startswith('~/schemas/'))
    
    def _scan_utilities(self):
        """Scan utility files"""
        util_dirs = ['lib', 'utils', 'helpers', 'utilities']
        
        for src_dir in self.src_dirs:
            for util_dir_name in util_dirs:
                util_dir = src_dir / util_dir_name
                
                if not util_dir.exists():
                    continue
                
                for file_path in util_dir.rglob('*.ts'):
                    if file_path.name.endswith('.d.ts'):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        exports = self._parse_exports(content)
                        relative_path = str(file_path.relative_to(self.project_root))
                        used_in = self._find_utility_usage(relative_path)
                        purpose = self._infer_utility_purpose(file_path.stem, content)
                        
                        self.dependencies["utilities"][relative_path] = {
                            "exports": exports,
                            "usedIn": used_in,
                            "purpose": purpose
                        }
                        
                        self.stats["utilities_found"] += 1
                        
                    except Exception as e:
                        self.stats["errors"].append(f"Error scanning utility: {str(e)}")
    
    def _parse_exports(self, content: str) -> List[str]:
        """Parse exported functions/constants"""
        exports = []
        export_patterns = [
            r'export\s+(?:const|let|var|function|class)\s+(\w+)',
            r'export\s+\{\s*([^\}]+)\s*\}',
        ]
        
        for pattern in export_patterns:
            for match in re.finditer(pattern, content):
                export_str = match.group(1)
                if ',' in export_str:
                    exports.extend([e.strip() for e in export_str.split(',')])
                else:
                    exports.append(export_str.strip())
        
        return list(set(exports))
    
    def _find_utility_usage(self, utility_path: str) -> List[str]:
        """Find files that import this utility"""
        used_in = []
        utility_name = Path(utility_path).stem
        
        for component_name, info in self.components.items():
            if utility_path in info.get("utilityDependencies", []) or \
               any(utility_name in dep for dep in info.get("utilityDependencies", [])):
                used_in.append(info["path"])
        
        return used_in
    
    def _infer_utility_purpose(self, filename: str, content: str) -> str:
        """Infer utility purpose"""
        purposes = {
            "sanity": "Sanity CMS client",
            "contentful": "Contentful CMS client",
            "api": "API utilities",
            "utils": "General utilities",
            "helpers": "Helper functions",
            "constants": "Constants",
            "config": "Configuration",
            "types": "Type definitions",
            "validation": "Validation utilities",
            "shiki": "Code syntax highlighting",
            "github": "GitHub API integration",
            "clarity": "Analytics integration",
            "skills": "Skills management",
        }
        return purposes.get(filename.lower(), "Utility functions")

    def _scan_schemas(self):
        """Scan schema files"""
        for src_dir in self.src_dirs:
            schemas_dir = src_dir / "schemas"

            if not schemas_dir.exists():
                continue

            for file_path in schemas_dir.rglob('*.ts'):
                if file_path.name.endswith('.d.ts'):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    exports = self._parse_exports(content)
                    relative_path = str(file_path.relative_to(self.project_root))
                    used_in = self._find_schema_usage(relative_path, file_path.stem)
                    schema_type = self._infer_schema_type(file_path.stem, content)

                    self.dependencies["schemas"][relative_path] = {
                        "name": file_path.stem,
                        "exports": exports,
                        "usedIn": used_in,
                        "type": schema_type,
                        "purpose": f"Schema definition for {file_path.stem}"
                    }

                    self.stats["schemas_found"] += 1

                except Exception as e:
                    self.stats["errors"].append(f"Error scanning schema: {str(e)}")

    def _find_schema_usage(self, schema_path: str, schema_name: str) -> List[str]:
        """Find files that import this schema"""
        used_in = []

        for component_name, info in self.components.items():
            if schema_path in info.get("schemaDependencies", []) or \
               any(schema_name in dep for dep in info.get("schemaDependencies", [])):
                used_in.append(info["path"])

        return used_in

    def _infer_schema_type(self, filename: str, content: str) -> str:
        """Infer schema type based on content"""
        filename_lower = filename.lower()

        # Check for Sanity schema patterns
        if "defineType" in content or "defineField" in content:
            return "sanity"

        # Check for Zod patterns
        if "z.object" in content or "import { z }" in content:
            return "zod"

        # Check for TypeScript types/interfaces
        if "interface " in content or "type " in content:
            if "Schema" in content or "schema" in filename_lower:
                return "typescript-schema"
            return "typescript"

        # Specific schema types based on common naming
        schema_types = {
            "thought": "content-schema",
            "chat": "content-schema",
            "codeblock": "content-schema",
            "contentSection": "content-schema",
            "columngroup": "layout-schema",
        }

        return schema_types.get(filename_lower, "schema")
    
    def _scan_package_json(self):
        """Scan package.json"""
        package_json_path = self.project_root / "package.json"
        
        if not package_json_path.exists():
            return
        
        try:
            with open(package_json_path) as f:
                package_data = json.load(f)
            
            dependencies = {**package_data.get("dependencies", {}), 
                          **package_data.get("devDependencies", {})}
            
            for pkg_name, version in dependencies.items():
                used_in = self._find_package_usage(pkg_name)
                purpose = self._infer_package_purpose(pkg_name)
                
                frameworks = ['astro', 'react', 'vue', 'svelte', 'next', 'angular', 'solid']
                if used_in or any(fw in pkg_name for fw in frameworks):
                    self.dependencies["npmPackages"][pkg_name] = {
                        "version": version,
                        "usedIn": used_in if used_in else ["framework"],
                        "purpose": purpose
                    }
        
        except Exception as e:
            self.stats["errors"].append(f"Error reading package.json: {str(e)}")
    
    def _find_package_usage(self, package_name: str) -> List[str]:
        """Find files that import this package"""
        used_in = []
        
        for component_name, info in self.components.items():
            if package_name in info.get("externalDependencies", []):
                used_in.append(info["path"])
        
        return used_in
    
    def _infer_package_purpose(self, package_name: str) -> str:
        """Infer package purpose"""
        purposes = {
            "astro": "Astro framework",
            "react": "React library",
            "vue": "Vue framework",
            "next": "Next.js framework",
            "svelte": "Svelte framework",
            "sanity": "Sanity CMS",
            "tailwindcss": "CSS framework",
        }
        return purposes.get(package_name, f"Package: {package_name}")
    
    def _scan_data_queries(self):
        """Scan for data queries"""
        for src_dir in self.src_dirs:
            for file_path in src_dir.rglob('*'):
                if file_path.suffix not in self.config["extensions"] + ['.ts', '.js']:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    relative_path = str(file_path.relative_to(self.project_root))
                    
                    for pattern in self.config.get("data_patterns", []):
                        for match in re.finditer(pattern, content):
                            query = match.group(1) if match.groups() else match.group(0)
                            
                            source_type = "api"
                            if "client.fetch" in content:
                                source_type = "sanity"
                            
                            if source_type not in self.data_queries["dataSources"]:
                                self.data_queries["dataSources"][source_type] = {"queries": {}}
                            
                            query_name = f"query_{len(self.data_queries['dataSources'][source_type]['queries'])}"
                            self.data_queries["dataSources"][source_type]["queries"][query_name] = {
                                "files": [relative_path],
                                "query": query,
                                "purpose": "Data fetching"
                            }
                            
                            self.stats["queries_found"] += 1
                    
                except Exception as e:
                    pass  # Silent fail for data queries
    
    def _scan_styles(self):
        """Scan CSS files"""
        for src_dir in self.src_dirs:
            styles_dir = src_dir / "styles"
            
            if not styles_dir.exists():
                continue
            
            for css_file in styles_dir.glob('*.css'):
                try:
                    with open(css_file) as f:
                        content = f.read()
                    
                    relative_path = str(css_file.relative_to(self.project_root))
                    
                    if 'token' in css_file.stem.lower():
                        self._parse_css_tokens(content, relative_path)
                    else:
                        self._parse_css_classes(content, relative_path)
                        
                except Exception as e:
                    pass
    
    def _parse_css_tokens(self, content: str, file_path: str):
        """Parse CSS tokens"""
        tokens = defaultdict(list)
        token_pattern = r'--([\w-]+):'
        
        for match in re.finditer(token_pattern, content):
            token_name = f"--{match.group(1)}"
            
            if any(kw in token_name for kw in ['spacing', 'gap', 'padding', 'margin']):
                tokens['spacing'].append(token_name)
            elif any(kw in token_name for kw in ['color', 'bg']):
                tokens['colors'].append(token_name)
            elif any(kw in token_name for kw in ['font', 'text']):
                tokens['typography'].append(token_name)
            else:
                tokens['other'].append(token_name)
        
        self.dependencies["styles"][file_path] = {
            "type": "design-tokens",
            "tokens": dict(tokens)
        }
    
    def _parse_css_classes(self, content: str, file_path: str):
        """Parse CSS classes"""
        classes = []
        class_pattern = r'\.([a-zA-Z][a-zA-Z0-9_-]*)\s*\{'

        for match in re.finditer(class_pattern, content):
            classes.append(match.group(1))

        # Determine style purpose based on filename
        filename = Path(file_path).stem.lower()
        style_purposes = {
            "global": "Global styles and base configuration",
            "tokens": "Design tokens and CSS variables",
            "reset": "CSS reset and normalization",
            "layout": "Layout utilities and grid systems",
            "utilities": "Utility classes",
            "effects": "Visual effects and animations",
            "syntax-highlighting": "Code syntax highlighting styles",
        }

        self.dependencies["styles"][file_path] = {
            "type": "stylesheet",
            "classes": sorted(set(classes)),
            "purpose": style_purposes.get(filename, "Stylesheet"),
            "usedIn": "global"
        }
    
    def _populate_used_by(self):
        """Populate usedBy relationships"""
        # Build a mapping of component simple names to full paths for lookup
        name_to_paths = {}
        for full_path, info in self.components.items():
            # Extract simple component name from path
            simple_name = Path(full_path).stem
            if simple_name not in name_to_paths:
                name_to_paths[simple_name] = []
            name_to_paths[simple_name].append(full_path)

        for component_path, info in self.components.items():
            for used_component_name in info.get("uses", []):
                # Try exact match first (full path)
                if used_component_name in self.components:
                    self.components[used_component_name]["usedBy"].append(info["path"])
                # Otherwise try simple name lookup
                elif used_component_name in name_to_paths:
                    # If multiple components have same name, add to all (ambiguous)
                    for target_path in name_to_paths[used_component_name]:
                        self.components[target_path]["usedBy"].append(info["path"])
    
    def _generate_outputs(self):
        """Generate output files"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        relationships_dir = self.output_dir / "relationships"
        relationships_dir.mkdir(exist_ok=True)
        
        self._populate_used_by()
        
        # Component usage
        component_stats = self._calculate_component_stats()
        component_usage = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "components": self.components,
            "statistics": component_stats
        }
        
        self._write_output(relationships_dir / f"component-usage.{self.output_format}",
                          component_usage)
        print(f"Generated component-usage.{self.output_format}")

        # Dependencies
        dependencies_output = {
            "generated": datetime.now(timezone.utc).isoformat(),
            **self.dependencies
        }
        self._write_output(relationships_dir / f"dependencies.{self.output_format}",
                          dependencies_output)
        print(f"Generated dependencies.{self.output_format}")

        # Data flow
        data_flow_output = {
            "generated": datetime.now(timezone.utc).isoformat(),
            **self.data_queries
        }
        self._write_output(relationships_dir / f"data-flow.{self.output_format}",
                          data_flow_output)
        print(f"Generated data-flow.{self.output_format}")

        # Index
        index_output = self._generate_index()
        self._write_output(self.output_dir / f"index.{self.output_format}", index_output)
        print(f"Generated index.{self.output_format}")
    
    def _calculate_component_stats(self) -> Dict:
        """Calculate component statistics"""
        stats = defaultdict(int)
        stats["totalComponents"] = len(self.components)
        
        for comp_info in self.components.values():
            comp_type = comp_info.get("type", "other")
            stats[comp_type] += 1
        
        return dict(stats)
    
    def _generate_index(self) -> Dict:
        """Generate index file"""
        metadata_count = sum(1 for info in self.components.values() if "metadata" in info)

        return {
            "version": "1.0.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "generatedBy": "codebase-indexer-skill",
            "framework": self.framework,
            "format": self.output_format,
            "summary": {
                "totalComponents": len(self.components),
                "componentsWithMetadata": metadata_count,
                "utilities": len(self.dependencies.get("utilities", {})),
                "schemas": len(self.dependencies.get("schemas", {})),
                "styleFiles": len(self.dependencies.get("styles", {})),
                "relationshipsMapped": self.stats["relationships_found"]
            },
            "sources": {
                "componentMetadata": {
                    "location": "**/*.metadata.{ts,tsx,json}",
                    "purpose": "Component API, props, variants, UX patterns",
                    "type": "manual",
                    "count": metadata_count,
                    "formats": ["ts", "tsx", "json"]
                },
                "relationships": {
                    "location": ".ai/relationships/",
                    "purpose": "Component relationships and dependencies",
                    "type": "auto-generated",
                    "format": self.output_format,
                    "files": [
                        "component-usage.toon",
                        "dependencies.toon",
                        "data-flow.toon"
                    ]
                }
            },
            "usage": {
                "loadOnce": "Read index.toon and relationships/* once at conversation start",
                "keepInContext": "Maintain loaded data for entire conversation (~4000 tokens)",
                "loadMetadataOnDemand": "Read component *.metadata.* files only when working with that component",
                "tokenEfficiency": "TOON format is 30-60% more efficient than JSON"
            }
        }
    
    def _write_output(self, file_path: Path, data: Dict):
        """Write output"""
        if self.output_format == "toon":
            encoder = TOONEncoder(indent=2, delimiter=self.delimiter)
            content = encoder.encode(data)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _print_summary(self):
        """Print summary"""
        print("\n" + "="*50)
        print("Summary:")
        print("="*50)
        print(f"Framework: {self.framework}")
        print(f"Format: {self.output_format.upper()}")
        print(f"{self.stats['components_scanned']} components indexed")
        print(f"{self.stats['relationships_found']} relationships mapped")
        print(f"{self.stats['utilities_found']} utilities tracked")
        print(f"{self.stats['schemas_found']} schemas tracked")
        print(f"{self.stats['queries_found']} queries documented")
        print(f"Output: {self.output_dir}")

        if self.stats['errors']:
            print(f"\nWARNING: {len(self.stats['errors'])} errors (showing first 3):")
            for error in self.stats['errors'][:3]:
                print(f"   - {error}")

        if self.output_format == "toon":
            print("\nTOON format: 30-60% more token-efficient than JSON")


def main():
    parser = argparse.ArgumentParser(description="Codebase indexer")
    parser.add_argument("project_root", help="Project root path")
    parser.add_argument("--format", choices=["toon", "json"], default="toon")
    parser.add_argument("--framework", choices=list(FRAMEWORK_CONFIGS.keys()))
    parser.add_argument("--delimiter", choices=[",", "\t", "|"], default=",")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project_root):
        print(f"Error: '{args.project_root}' not found")
        return 1
    
    indexer = CodebaseIndexer(
        args.project_root,
        output_format=args.format,
        framework=args.framework,
        delimiter=args.delimiter
    )
    indexer.scan()
    
    return 0


if __name__ == "__main__":
    exit(main())
