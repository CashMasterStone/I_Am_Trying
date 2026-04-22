# Copilot Instructions: Flip-It Base-180 Encryption System

## Project Overview
This codebase implements a **Base-180 cryptographic system** with 74,880 unique cipher alphabets. Each cipher generates exactly 180 symbols using combinatorial transformations across 8 semantic volumes.

## Architecture Patterns

### Core Components
- **`cipher_generator.py`**: `CipherGenerator` class creates 180-symbol alphabets using volume transformations
- **`cipher_registry.py`**: `CipherRegistry` tracks all 74,880 cipher combinations (`180 × 52 × 8`)
- **`Codex/`**: 8-volume symbol foundation with semantic transformation rules
- **`cipher_registry.json`**: Persistent storage of generated cipher metadata (14MB when populated)

### Cipher Generation Flow
```python
# Generate random cipher from unexplored space
manager = CipherManager()
cipher = manager.generate_random_cipher()
# Returns: {'cipher_id': 'III-086-C', 'alphabet': [...180 symbols...], 'entropy_score': 0.97}
```

### Key Patterns

#### Cipher ID Format
- **Format**: `{volume}-{n:03d}-{alpha}` (e.g., `III-086-C`)
- **Parameters**:
  - `volume`: I-VIII (8 semantic volumes)
  - `n`: 0-179 (Base-180 position)
  - `alpha`: A-Z, a-z (52 alphabetic modifiers)

#### Volume Transformations
Each volume applies unique bracket/modifier patterns:
- **I**: `[{base}]{alpha.upper()}` - Mathematical foundations
- **II**: `⟨{base}⟩{alpha.lower()}` - Connections/relations
- **III**: `⌈{base}⌉{alpha}` - Philosophy & logic
- **IV**: `⚚{base}⚚{alpha}` - Esoteric symbols
- **V**: `❮{base}❯{alpha.upper()}` - Language structures
- **VI**: `⌘{base}⌘{alpha.lower()}` - Applied systems
- **VII**: `⟲{base}⟲{alpha}` - Meta-symbolism
- **VIII**: `⚝{base}⚝{alpha}` - Hidden esoteric

#### Base-180 Skeleton Generation
```python
def generate_base180_skeleton(self, n: int) -> str:
    if n < 60: return f"[{n:02d}]"           # Base-60 style numerals
    elif n < 120: return f"[{greek[n-60]}...]"  # Greek letters
    else: return f"[{esoteric[n-120]}...]"      # Esoteric symbols
```

## Development Workflow

### Running the System
```bash
# Generate random cipher and update registry
python cipher_generator.py

# Check registry status
python cipher_registry.py
```

### Testing Cipher Generation
- Run `python cipher_generator.py` multiple times
- Verify registry persistence in `cipher_registry.json`
- Check entropy scores (target: >0.95)
- Confirm 180 symbols per alphabet

### Code Patterns

#### Registry Management
```python
registry = CipherRegistry()
registry.load_registry()  # Load from cipher_registry.json
entry = registry.get_random_ungenerated_cipher()
registry.mark_cipher_generated(entry.cipher_id, entropy_score)
registry.save_registry()
```

#### Cipher Validation
```python
def validate_cipher_entropy(alphabet: List[str]) -> float:
    unique_symbols = len(set(alphabet))
    uniqueness_score = unique_symbols / 180.0
    avg_length = sum(len(s) for s in alphabet) / 180.0
    diversity_score = min(1.0, avg_length / 10.0)
    return round((uniqueness_score * 0.7) + (diversity_score * 0.3), 3)
```

## Critical Conventions

### File Structure
- **Mathematical foundation**: `Change Mathematical Statement & New.txt`
- **Symbol codex**: `Codex/Symbol Codex Volume {I-VIII}.{md,txt}`
- **Registry persistence**: `cipher_registry.json` (auto-generated, large file)

### Error Handling
- Validate volume parameters: `if volume not in self.volume_transforms: raise ValueError`
- Check cipher existence: `if cipher_id not in self.ciphers: raise ValueError`
- Ensure 180-symbol alphabets: `if len(cipher_alphabet) != 180: return 0.0`

### Performance Considerations
- Registry initializes 74,880 combinations on startup
- JSON serialization for persistence (large file size)
- Random selection from ungenerated ciphers only

## Security Validation

### Entropy Requirements
- **Uniqueness**: All 180 symbols must be distinct
- **Diversity**: Average symbol length favors moderate complexity
- **Score threshold**: >0.95 for cryptographic validity

### Coverage Tracking
- Monitor progress through 74,880 cipher space
- Prevent duplicate generation
- Balance across volumes I-VIII

## Key Integration Points

### Volume Symbol Sources
- **Volume I**: Mathematical symbols (∑, ∫, π, Δ)
- **Volume II**: Logic operators (→, ↔, ∴, ∵)
- **Volume III**: Modal logic (□, ◇, ¬, ∀)
- **Volume IV**: Esoteric symbols (☿, ♄, ✡, ☥)
- **Volume V**: Phonetic marks (ʃ, θ, ŋ, ˈ)
- **Volume VI**: Tech symbols (@, #, &, %)
- **Volume VII**: Recursive patterns (⊕, ∞, Ω)
- **Volume VIII**: Hidden symbols (⸸, ◬, 𓂀)

### Extension Points
- Add new volumes beyond VIII
- Implement Base-180 arithmetic operations
- Create encryption/decryption functions using generated ciphers
