# Create a working DomCode assembler/compiler prototype
# This will translate DomCode to NASM x86-64 assembly

class DomCodeAssembler:
    def __init__(self):
        # Instruction mapping from DomCode to x86-64
        self.instruction_map = {
            # Power Dynamics
            "SUBMIT": lambda args: f"mov {self.translate_register(args[2])}, {self.translate_operand(args[0])}",
            "DOMINATE": lambda args: f"add {self.translate_register(args[0])}, {self.translate_operand(args[2])}" if args[2] != "1" else f"inc {self.translate_register(args[0])}",
            "CONTROL": lambda args: f"mov {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "OBEY": lambda args: f"cmp {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "YIELD": lambda args: f"sub {self.translate_register(args[0])}, {self.translate_operand(args[2])}" if args[2] != "1" else f"dec {self.translate_register(args[0])}",
            
            # Consent & Verification
            "VERIFY_CONSENT": lambda args: f"cmp {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "SAFE_WORD": lambda args: f"jmp {args[1]}",
            "NEGOTIATE": lambda args: f"test {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "BOUNDARY_CHECK": lambda args: f"cmp {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            
            # Financial Domination  
            "TRIBUTE": lambda args: f"push {self.translate_register(args[0])}",
            "DRAIN": lambda args: f"pop {self.translate_register(args[1])}",
            "PAYPIG_SERVE": lambda args: f"mov {self.translate_register(args[2])}, {self.translate_operand(args[0])}",
            "WALLET_RAPE": lambda args: f"xor {self.translate_register(args[0])}, {self.translate_register(args[0])}",
            "FINDOM_DEMAND": lambda args: f"imul {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            
            # Control Flow
            "IF_OBEDIENT": lambda args: f"je {args[1]}",
            "IF_DISOBEDIENT": lambda args: f"jne {args[1]}",
            "IF_WORTHY": lambda args: f"jge {args[1]}",
            "IF_INSUFFICIENT": lambda args: f"jl {args[1]}",
            "PUNISH": lambda args: f"jmp {args[1]}",
            "REWARD": lambda args: f"jmp {args[1]}",
            
            # Data Manipulation
            "BIND": lambda args: f"lea {self.translate_register(args[0])}, {self.translate_memory(args[2])}",
            "RESTRAIN": lambda args: f"and {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "RELEASE_CONTROL": lambda args: f"or {self.translate_register(args[0])}, {self.translate_operand(args[2])}",
            "COLLAR": lambda args: f"shl {self.translate_register(args[0])}, {self.translate_operand(args[3])}" if args[1] == "LEFT" else f"shr {self.translate_register(args[0])}, {self.translate_operand(args[3])}",
            
            # Memory Operations
            "CHAIN_TO": lambda args: f"mov {self.translate_memory(args[0])}, {self.translate_register(args[2])}",
            "FETCH_FROM": lambda args: f"mov {self.translate_register(args[2])}, {self.translate_memory(args[0])}",
            "DUNGEON_ALLOC": lambda args: f"sub rsp, {args[0]}",
            "DUNGEON_FREE": lambda args: f"add rsp, {args[0]}",
            
            # System Operations
            "KNEEL": lambda args: f"call {args[1]}",
            "DISMISS": lambda args: "ret",
            "SERVE": lambda args: f"int {self.translate_operand(args[0])}",
            "TERMINATE_SESSION": lambda args: f"mov rax, 60\n    mov rdi, {self.translate_register(args[1])}\n    syscall"
        }
        
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
        """Parse a single DomCode instruction line"""
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
        
        tokens = line.split()
        if not tokens:
            return None
            
        instruction = tokens[0]
        
        if instruction in self.instruction_map:
            try:
                return f"    {self.instruction_map[instruction](tokens)}"
            except Exception as e:
                return f"    ; ERROR translating {line}: {e}"
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

# Test the assembler with our sample program
assembler = DomCodeAssembler()

# Updated sample program with correct syntax
sample_domcode = '''
SECTION .text
GLOBAL main

main:
    DUNGEON_ALLOC 64
    SUBMIT 19 TO SUB1
    VERIFY_CONSENT SUB1 MEETS 18
    IF_INSUFFICIENT GOTO violation_handler
    PAYPIG_SERVE 500 TO TRIBUTE1
    VERIFY_CONSENT TRIBUTE1 MEETS 100
    IF_INSUFFICIENT GOTO insufficient_tribute
    REWARD WITH approval_sequence

violation_handler:
    SUBMIT 1 TO MISTRESS
    PUNISH WITH terminate_session

insufficient_tribute:
    FINDOM_DEMAND TRIBUTE1 BY 2
    REWARD WITH approval_sequence

approval_sequence:
    BIND SLAVE TO [DUNGEON_BASE + 8]
    CHAIN_TO [DUNGEON_BASE + 8] VALUE SUB1
    CHAIN_TO [DUNGEON_BASE + 16] VALUE TRIBUTE1
    SUBMIT 0 TO MISTRESS

terminate_session:
    DUNGEON_FREE 64
    TERMINATE_SESSION WITH MISTRESS
'''

print("=== DOMCODE TO x86-64 ASSEMBLY TRANSLATION ===")
print()
print("INPUT DOMCODE:")
print("-" * 50)
print(sample_domcode.strip())
print()
print("OUTPUT x86-64 ASSEMBLY:")
print("-" * 50)
compiled_assembly = assembler.assemble(sample_domcode)
print(compiled_assembly)