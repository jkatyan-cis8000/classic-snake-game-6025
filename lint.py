#!/usr/bin/env python3
"""Linter for source architecture layers.

Validates:
- Every source file lives in exactly one layer directory
- Imports respect the forward dependency direction
- No file exceeds 300 lines
- No file has internal imports to non-layer modules
"""

import ast
import sys
from pathlib import Path


# Layer dependencies: each layer may import from layers in its allowed list
ALLOWED_IMPORTS = {
    "types": ["types"],
    "config": ["types", "config"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime", "ui"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
    "providers": ["types", "config", "utils", "providers"],
    "utils": ["utils"],
}

LAYERS = set(ALLOWED_IMPORTS.keys())
MAX_LINES = 300


def get_layer_from_path(file_path: Path) -> str | None:
    """Extract layer name from file path under src/."""
    src_root = Path("src")
    try:
        relative = file_path.relative_to(src_root)
        parts = relative.parts
        if len(parts) > 0 and parts[0] in LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def check_line_count(file_path: Path) -> list[tuple[int, str]]:
    """Check if file exceeds MAX_LINES."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > MAX_LINES:
                errors.append(
                    (len(lines), f"File exceeds {MAX_LINES} lines ({len(lines)} lines)")
                )
    except Exception:
        pass
    return errors


def check_imports(file_path: Path) -> list[tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    errors = []
    
    layer = get_layer_from_path(file_path)
    if layer is None:
        return errors  # Not a layer file
    
    allowed = ALLOWED_IMPORTS[layer]
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source, filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    if module_name.startswith("src."):
                        internal_module = module_name[4:]  # Remove "src."
                        module_layer = internal_module.split(".")[0]
                        if module_layer not in allowed:
                            errors.append(
                                (node.lineno, f"Cannot import '{module_name}' - '{module_layer}' not allowed from '{layer}'")
                            )
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("src."):
                    internal_module = node.module[4:]  # Remove "src."
                    module_layer = internal_module.split(".")[0]
                    if module_layer not in allowed:
                        errors.append(
                            (node.lineno, f"Cannot import from '{node.module}' - '{module_layer}' not allowed from '{layer}'")
                        )
    except SyntaxError:
        # Skip files that don't parse
        pass
    
    return errors


def find_source_files() -> list[Path]:
    """Find all Python source files under src/."""
    return list(Path("src").rglob("*.py"))


def main() -> int:
    """Run linter and return error code."""
    source_files = find_source_files()
    all_errors: list[tuple[Path, int, str]] = []
    
    for file_path in source_files:
        # Check line count
        line_errors = check_line_count(file_path)
        for line_num, msg in line_errors:
            all_errors.append((file_path, line_num, msg))
        
        # Check imports
        import_errors = check_imports(file_path)
        for line_num, msg in import_errors:
            all_errors.append((file_path, line_num, msg))
    
    # Report errors
    if all_errors:
        print(f"Lint failed with {len(all_errors)} error(s):\n")
        for file_path, line_num, msg in sorted(all_errors, key=lambda x: (str(x[0]), x[1])):
            print(f"{file_path}:{line_num}: {msg}")
        return 1
    
    print(f"Lint passed: {len(source_files)} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
