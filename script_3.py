# Fixed DomCode assembler with proper parsing

import re

class DomCodeAssembler:
    def __init__(self):
        # Register mapping from DomCode to x86-64
        self.register_map = {
            "MISTRESS": "rax",
            "MASTER": "rbx", 
            "SUB1": "rcx",
            "SUB2": "rdx",
            "SLAVE": "rdi",
            "SERVANT": "rsi",
            "DUNGEON_BASE": "rbp",
            "COLLAR_PTR": "rsp",
            "TRIBUTE1": "r8",
            "TRIBUTE2": "r9", 
            "TRIBUTE3": "r10",
            "TRIBUTE4": "r11",
            "PAYPIG1": "r12",
            "PAYPIG2": "r13",
            "WALLET1": "r14",
            "WALLET2": "r15"
        }
    
    def translate_register(self, reg):
        """Translate DomCode register to x86-64 register"""
        return self.register_map.get(reg, reg.lower())
    
    def translate_operand(self, operand):
        """Translate operand (register, constant, or memory reference)"""
        if operand in self.register_map:
            return self.translate_register(operand)
        elif operand.startswith('[') and operand.endswith(']'):
            return self.translate_memory(operand)
        else:
            return operand  # Assume it's a constant
    
    def translate_memory(self, mem_ref):
        """Translate memory reference"""
        # Remove brackets
        inner = mem_ref[1:-1]
        
        # Handle register + offset
        if '+' in inner:
            parts = inner.split('+')
            reg = parts[0].strip()
            offset = parts[1].strip()
            return f"[{self.translate_register(reg)} + {offset}]"
        else:
            # Simple register indirect
            return f"[{self.translate_register(inner.strip())}]"
    
    def parse_instruction(self, line):
        """Parse a single DomCode instruction line with proper syntax handling"""
        # Remove comments
        if ';' in line:
            line = line.split(';')[0]
        
        line = line.strip()
        if not line:
            return None
            
        # Handle labels
        if line.endswith(':'):
            return f"{line}"
        
        # Handle directives
        if line.startswith('SECTION') or line.startswith('GLOBAL'):
            return f"    {line.lower()}"
        
        # Parse instruction with proper keyword handling
        return self.parse_domcode_instruction(line)
    
    def parse_domcode_instruction(self, line):
        """Parse specific DomCode instruction patterns"""
        line = line.strip()
        
        # SUBMIT value TO register
        if line.startswith('SUBMIT ') and ' TO ' in line:
            parts = line.split(' TO ')
            value = parts[0].replace('SUBMIT ', '').strip()
            register = parts[1].strip()
            return f"    mov {self.translate_register(register)}, {self.translate_operand(value)}"
        
        # DOMINATE register WITH value
        elif line.startswith('DOMINATE ') and ' WITH ' in line:
            parts = line.split(' WITH ')
            register = parts[0].replace('DOMINATE ', '').strip()
            value = parts[1].strip()
            if value == "1":
                return f"    inc {self.translate_register(register)}"
            else:
                return f"    add {self.translate_register(register)}, {self.translate_operand(value)}"
        
        # VERIFY_CONSENT register MEETS threshold
        elif line.startswith('VERIFY_CONSENT ') and ' MEETS ' in line:
            parts = line.split(' MEETS ')
            register = parts[0].replace('VERIFY_CONSENT ', '').strip()
            threshold = parts[1].strip()
            return f"    cmp {self.translate_register(register)}, {self.translate_operand(threshold)}"
        
        # IF_INSUFFICIENT GOTO label
        elif line.startswith('IF_INSUFFICIENT ') and ' GOTO ' in line:
            label = line.split(' GOTO ')[1].strip()
            return f"    jl {label}"
        
        # IF_OBEDIENT GOTO label
        elif line.startswith('IF_OBEDIENT ') and ' GOTO ' in line:
            label = line.split(' GOTO ')[1].strip()
            return f"    je {label}"
        
        # IF_DISOBEDIENT GOTO label
        elif line.startswith('IF_DISOBEDIENT ') and ' GOTO ' in line:
            label = line.split(' GOTO ')[1].strip()
            return f"    jne {label}"
        
        # IF_WORTHY GOTO label
        elif line.startswith('IF_WORTHY ') and ' GOTO ' in line:
            label = line.split(' GOTO ')[1].strip()
            return f"    jge {label}"
        
        # PAYPIG_SERVE amount TO register
        elif line.startswith('PAYPIG_SERVE ') and ' TO ' in line:
            parts = line.split(' TO ')
            amount = parts[0].replace('PAYPIG_SERVE ', '').strip()
            register = parts[1].strip()
            return f"    mov {self.translate_register(register)}, {self.translate_operand(amount)}"
        
        # REWARD WITH label
        elif line.startswith('REWARD ') and ' WITH ' in line:
            label = line.split(' WITH ')[1].strip()
            return f"    jmp {label}"
        
        # PUNISH WITH label
        elif line.startswith('PUNISH ') and ' WITH ' in line:
            label = line.split(' WITH ')[1].strip()
            return f"    jmp {label}"
        
        # FINDOM_DEMAND register BY factor
        elif line.startswith('FINDOM_DEMAND ') and ' BY ' in line:
            parts = line.split(' BY ')
            register = parts[0].replace('FINDOM_DEMAND ', '').strip()
            factor = parts[1].strip()
            return f"    imul {self.translate_register(register)}, {self.translate_operand(factor)}"
        
        # BIND register TO [memory]
        elif line.startswith('BIND ') and ' TO ' in line:
            parts = line.split(' TO ')
            register = parts[0].replace('BIND ', '').strip()
            memory = parts[1].strip()
            return f"    lea {self.translate_register(register)}, {self.translate_memory(memory)}"
        
        # CHAIN_TO [memory] VALUE register
        elif line.startswith('CHAIN_TO ') and ' VALUE ' in line:
            parts = line.split(' VALUE ')
            memory = parts[0].replace('CHAIN_TO ', '').strip()
            register = parts[1].strip()
            return f"    mov {self.translate_memory(memory)}, {self.translate_register(register)}"
        
        # DUNGEON_ALLOC size
        elif line.startswith('DUNGEON_ALLOC '):
            size = line.replace('DUNGEON_ALLOC ', '').strip()
            return f"    sub rsp, {size}"
        
        # DUNGEON_FREE size
        elif line.startswith('DUNGEON_FREE '):
            size = line.replace('DUNGEON_FREE ', '').strip()
            return f"    add rsp, {size}"
        
        # TERMINATE_SESSION WITH register
        elif line.startswith('TERMINATE_SESSION ') and ' WITH ' in line:
            register = line.split(' WITH ')[1].strip()
            return f"    mov rax, 60\n    mov rdi, {self.translate_register(register)}\n    syscall"
        
        else:
            return f"    ; Unknown instruction: {line}"
    
    def assemble(self, domcode_source):
        """Assemble DomCode source to NASM x86-64 assembly"""
        lines = domcode_source.strip().split('\n')
        output = []
        
        # Add NASM header
        output.append("BITS 64")
        output.append("DEFAULT REL")
        output.append("")
        
        for line in lines:
            translated = self.parse_instruction(line)
            if translated:
                output.append(translated)
        
        return '\n'.join(output)

# Test the fixed assembler
assembler = DomCodeAssembler()

print("=== FIXED DOMCODE TO x86-64 ASSEMBLY TRANSLATION ===")
print()
print("INPUT DOMCODE:")
print("-" * 50)
print(sample_domcode.strip())
print()
print("OUTPUT x86-64 ASSEMBLY:")  
print("-" * 50)
compiled_assembly = assembler.assemble(sample_domcode)
print(compiled_assembly)

# Also create a more comprehensive compliance example
compliance_example = '''
SECTION .text
GLOBAL verify_creator_compliance

verify_creator_compliance:
    DUNGEON_ALLOC 64
    
    ; Load creator age from input
    SUBMIT 21 TO SUB1
    
    ; Verify age compliance (18 U.S.C. 2257)
    VERIFY_CONSENT SUB1 MEETS 18
    IF_INSUFFICIENT GOTO age_violation
    
    ; Load financial tribute amount
    PAYPIG_SERVE 1000 TO TRIBUTE1
    
    ; Verify minimum tribute requirement
    VERIFY_CONSENT TRIBUTE1 MEETS 500
    IF_INSUFFICIENT GOTO insufficient_payment
    
    ; Both checks passed - bind creator data
    BIND SLAVE TO [DUNGEON_BASE + 8]
    CHAIN_TO [DUNGEON_BASE + 8] VALUE SUB1
    CHAIN_TO [DUNGEON_BASE + 16] VALUE TRIBUTE1
    
    ; Grant platform access
    SUBMIT 1 TO MISTRESS
    REWARD WITH platform_access_granted
    
age_violation:
    SUBMIT 2 TO MISTRESS
    PUNISH WITH compliance_violation
    
insufficient_payment:
    FINDOM_DEMAND TRIBUTE1 BY 2
    SUBMIT 3 TO MISTRESS
    REWARD WITH payment_increase_demanded
    
platform_access_granted:
    SUBMIT 0 TO MISTRESS
    DUNGEON_FREE 64
    TERMINATE_SESSION WITH MISTRESS
    
compliance_violation:
    SUBMIT 1 TO MISTRESS
    DUNGEON_FREE 64
    TERMINATE_SESSION WITH MISTRESS
    
payment_increase_demanded:
    SUBMIT 0 TO MISTRESS
    DUNGEON_FREE 64
    TERMINATE_SESSION WITH MISTRESS
'''

print("\n\n=== ADVANCED COMPLIANCE EXAMPLE ===")
print()
print("DOMCODE SOURCE:")
print("-" * 50)
print(compliance_example.strip())
print()
print("COMPILED x86-64 ASSEMBLY:")
print("-" * 50)
advanced_compiled = assembler.assemble(compliance_example)
print(advanced_compiled)