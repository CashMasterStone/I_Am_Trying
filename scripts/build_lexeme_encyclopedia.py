#!/usr/bin/env python3
"""
Lexeme Encyclopedia Builder for I_Am_Trying repository.

Extracts terminology, concepts, and definitions from markdown and text files
to build a navigable encyclopedia of LLW/LLWΦ concepts, principles, and entities.
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class LexemeExtractor:
    """Extracts lexemes (key terms and concepts) from repository documents."""
    
    # Key LLW/LLWΦ terminology patterns
    LLW_TERMS = [
        'LLW', 'LLWΦ', 'field', 'fields', 'unit', 'units', 'interaction', 'interactions',
        'coupling', 'couplings', 'resource', 'resources', 'invariant', 'invariants',
        'conservation', 'provenance', 'deterministic', 'Merkle', 'Lumen',
        'DEVICE_ATTEST', 'TSS_PARTIAL', 'NORMALFORMHASH', 'quorum',
        'emit', 'absorb', 'transfer', 'couple', 'measure', 'constrain'
    ]
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.lexemes = defaultdict(lambda: {'files': [], 'contexts': [], 'count': 0})
        self.documents = {}
        
    def scan_repository(self):
        """Scan repository for markdown and text files."""
        extensions = {'.md', '.txt'}
        
        for file_path in self.input_dir.rglob('*'):
            if file_path.suffix in extensions and not self._should_skip(file_path):
                self._process_file(file_path)
    
    def _should_skip(self, file_path: Path) -> bool:
        """Determine if a file should be skipped."""
        skip_patterns = ['.git', '__pycache__', 'node_modules', 'build', 'dist']
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _process_file(self, file_path: Path):
        """Process a single file to extract lexemes."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                relative_path = file_path.relative_to(self.input_dir)
                
                # Store document
                self.documents[str(relative_path)] = {
                    'path': str(relative_path),
                    'size': len(content),
                    'lines': content.count('\n') + 1
                }
                
                # Extract lexemes
                self._extract_terms(content, str(relative_path))
                self._extract_definitions(content, str(relative_path))
                self._extract_headers(content, str(relative_path))
                
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {e}")
    
    def _extract_terms(self, content: str, file_path: str):
        """Extract LLW terminology from content."""
        for term in self.LLW_TERMS:
            # Case-sensitive search for technical terms
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = list(re.finditer(pattern, content, re.IGNORECASE if term.isupper() else 0))
            
            if matches:
                self.lexemes[term]['files'].append(file_path)
                self.lexemes[term]['count'] += len(matches)
                
                # Extract context snippets (up to 3)
                for match in matches[:3]:
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].strip()
                    context = ' '.join(context.split())  # Normalize whitespace
                    
                    if context not in self.lexemes[term]['contexts']:
                        self.lexemes[term]['contexts'].append(context)
    
    def _extract_definitions(self, content: str, file_path: str):
        """Extract explicit definitions (pattern: 'Term: definition' or '**Term** - definition')."""
        # Pattern 1: **Term** - definition or **Term**: definition
        pattern1 = r'\*\*([^*]+)\*\*\s*[-:]\s*([^\n]+)'
        # Pattern 2: Term: definition at start of line
        pattern2 = r'^([A-Z][A-Za-z0-9 ]{2,30}):\s*([^\n]+)'
        
        for pattern in [pattern1, pattern2]:
            for match in re.finditer(pattern, content, re.MULTILINE):
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                lexeme_key = f"DEF:{term}"
                if lexeme_key not in self.lexemes or file_path not in self.lexemes[lexeme_key]['files']:
                    self.lexemes[lexeme_key]['files'].append(file_path)
                    self.lexemes[lexeme_key]['contexts'].append(f"{term}: {definition}")
                    self.lexemes[lexeme_key]['count'] += 1
    
    def _extract_headers(self, content: str, file_path: str):
        """Extract markdown headers as structural lexemes."""
        pattern = r'^(#{1,6})\s+(.+)$'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            level = len(match.group(1))
            header = match.group(2).strip()
            
            lexeme_key = f"SECTION:{header}"
            if lexeme_key not in self.lexemes or file_path not in self.lexemes[lexeme_key]['files']:
                self.lexemes[lexeme_key]['files'].append(file_path)
                self.lexemes[lexeme_key]['contexts'].append(f"Level {level}: {header}")
                self.lexemes[lexeme_key]['count'] += 1
    
    def build_encyclopedia(self):
        """Build the final encyclopedia structure."""
        encyclopedia = {
            'metadata': {
                'repository': 'I_Am_Trying',
                'description': 'Lexeme encyclopedia for LLW/LLWΦ architecture and narrative',
                'document_count': len(self.documents),
                'lexeme_count': len(self.lexemes)
            },
            'documents': self.documents,
            'lexemes': {}
        }
        
        # Convert defaultdict to regular dict and sort
        for term, data in sorted(self.lexemes.items()):
            encyclopedia['lexemes'][term] = {
                'occurrences': data['count'],
                'files': sorted(set(data['files'])),
                'contexts': data['contexts'][:5]  # Limit to 5 contexts
            }
        
        return encyclopedia
    
    def generate_outputs(self):
        """Generate encyclopedia outputs in multiple formats."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build encyclopedia data
        encyclopedia = self.build_encyclopedia()
        
        # 1. JSON output
        json_path = self.output_dir / 'lexeme_encyclopedia.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(encyclopedia, f, indent=2, ensure_ascii=False)
        print(f"✓ Generated: {json_path}")
        
        # 2. Markdown index
        md_path = self.output_dir / 'LEXEME_INDEX.md'
        self._generate_markdown_index(encyclopedia, md_path)
        print(f"✓ Generated: {md_path}")
        
        # 3. Term frequency report
        freq_path = self.output_dir / 'term_frequency.txt'
        self._generate_frequency_report(encyclopedia, freq_path)
        print(f"✓ Generated: {freq_path}")
        
        # Summary
        print(f"\n📊 Encyclopedia Summary:")
        print(f"   Documents processed: {encyclopedia['metadata']['document_count']}")
        print(f"   Lexemes extracted: {encyclopedia['metadata']['lexeme_count']}")
    
    def _generate_markdown_index(self, encyclopedia: dict, output_path: Path):
        """Generate a human-readable markdown index."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Lexeme Encyclopedia Index\n\n")
            f.write("Auto-generated index of terminology and concepts in I_Am_Trying repository.\n\n")
            f.write("---\n\n")
            
            # Group lexemes by type
            terms = []
            definitions = []
            sections = []
            
            for lexeme, data in sorted(encyclopedia['lexemes'].items()):
                if lexeme.startswith('DEF:'):
                    definitions.append((lexeme[4:], data))
                elif lexeme.startswith('SECTION:'):
                    sections.append((lexeme[8:], data))
                else:
                    terms.append((lexeme, data))
            
            # Write core LLW terms
            if terms:
                f.write("## Core LLW/LLWΦ Terms\n\n")
                for term, data in terms:
                    f.write(f"### `{term}`\n\n")
                    f.write(f"- **Occurrences**: {data['occurrences']}\n")
                    f.write(f"- **Files**: {', '.join(f'`{fp}`' for fp in data['files'][:5])}\n")
                    if data['contexts']:
                        f.write(f"- **Context**: _{data['contexts'][0]}_\n")
                    f.write("\n")
            
            # Write definitions
            if definitions:
                f.write("## Explicit Definitions\n\n")
                for term, data in definitions:
                    f.write(f"### {term}\n\n")
                    if data['contexts']:
                        f.write(f"_{data['contexts'][0]}_\n\n")
                    f.write(f"Found in: {', '.join(f'`{fp}`' for fp in data['files'])}\n\n")
    
    def _generate_frequency_report(self, encyclopedia: dict, output_path: Path):
        """Generate a term frequency report."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("TERM FREQUENCY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Sort by occurrence count
            sorted_lexemes = sorted(
                encyclopedia['lexemes'].items(),
                key=lambda x: x[1]['occurrences'],
                reverse=True
            )
            
            for lexeme, data in sorted_lexemes[:50]:  # Top 50
                if not lexeme.startswith('SECTION:'):
                    f.write(f"{lexeme:40} {data['occurrences']:>6} occurrences\n")


def main():
    parser = argparse.ArgumentParser(
        description='Build lexeme encyclopedia from I_Am_Trying repository'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='.',
        help='Input directory (repository root)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='build',
        help='Output directory for encyclopedia artifacts'
    )
    
    args = parser.parse_args()
    
    print("🔍 Building Lexeme Encyclopedia...")
    print(f"   Input: {args.input}")
    print(f"   Output: {args.output}\n")
    
    extractor = LexemeExtractor(args.input, args.output)
    extractor.scan_repository()
    extractor.generate_outputs()
    
    print("\n✅ Lexeme encyclopedia build complete!")


if __name__ == '__main__':
    main()
