# Let's create a comprehensive DomCode instruction mapping
# This maps BDSM/FinDom concepts to x86-64 instructions with 1:1 correspondence

domcode_instruction_set = {
    # === POWER DYNAMICS ===
    "SUBMIT": {
        "x86_64": "mov",
        "semantic": "Transfer value/control to another (move data)",
        "usage": "SUBMIT value TO register",
        "example": "SUBMIT 100 TO rax  ; mov rax, 100"
    },
    
    "DOMINATE": {
        "x86_64": "add/inc",
        "semantic": "Assert power/control by increasing",
        "usage": "DOMINATE register WITH value",
        "example": "DOMINATE rax WITH 1  ; add rax, 1"
    },
    
    "CONTROL": {
        "x86_64": "mov",
        "semantic": "Take possession/control of data",
        "usage": "CONTROL register FROM source",
        "example": "CONTROL rax FROM rbx  ; mov rax, rbx"
    },
    
    "OBEY": {
        "x86_64": "cmp",
        "semantic": "Submit to comparison/evaluation",
        "usage": "OBEY register AGAINST value",
        "example": "OBEY rax AGAINST 18  ; cmp rax, 18"
    },
    
    "YIELD": {
        "x86_64": "sub/dec",
        "semantic": "Give up/reduce power",
        "usage": "YIELD register BY value",
        "example": "YIELD rax BY 1  ; sub rax, 1"
    },
    
    # === CONSENT & VERIFICATION ===
    "VERIFY_CONSENT": {
        "x86_64": "cmp",
        "semantic": "Check consent/compliance status",
        "usage": "VERIFY_CONSENT register MEETS threshold",
        "example": "VERIFY_CONSENT rax MEETS 18  ; cmp rax, 18"
    },
    
    "SAFE_WORD": {
        "x86_64": "jmp",
        "semantic": "Emergency exit/halt execution",
        "usage": "SAFE_WORD TO label",
        "example": "SAFE_WORD TO exit_routine  ; jmp exit_routine"
    },
    
    "NEGOTIATE": {
        "x86_64": "test",
        "semantic": "Test conditions before proceeding",
        "usage": "NEGOTIATE register WITH mask",
        "example": "NEGOTIATE rax WITH 0xFF  ; test rax, 0xFF"
    },
    
    "BOUNDARY_CHECK": {
        "x86_64": "cmp",
        "semantic": "Verify limits are respected",
        "usage": "BOUNDARY_CHECK value WITHIN limit",
        "example": "BOUNDARY_CHECK rax WITHIN 100  ; cmp rax, 100"
    },
    
    # === FINANCIAL DOMINATION ===
    "TRIBUTE": {
        "x86_64": "push",
        "semantic": "Offer financial submission",
        "usage": "TRIBUTE amount",
        "example": "TRIBUTE rax  ; push rax"
    },
    
    "DRAIN": {
        "x86_64": "pop",
        "semantic": "Extract tribute/payment",
        "usage": "DRAIN INTO register",
        "example": "DRAIN INTO rbx  ; pop rbx"
    },
    
    "PAYPIG_SERVE": {
        "x86_64": "mov",
        "semantic": "Financial submissive serves with payment",
        "usage": "PAYPIG_SERVE amount TO mistress",
        "example": "PAYPIG_SERVE 500 TO rdi  ; mov rdi, 500"
    },
    
    "WALLET_RAPE": {
        "x86_64": "xor",
        "semantic": "Complete financial drain (zero out)",
        "usage": "WALLET_RAPE register",
        "example": "WALLET_RAPE rax  ; xor rax, rax"
    },
    
    "FINDOM_DEMAND": {
        "x86_64": "mul",
        "semantic": "Multiply tribute requirements",
        "usage": "FINDOM_DEMAND register BY factor",
        "example": "FINDOM_DEMAND rax BY rbx  ; mul rbx"
    },
    
    # === CONTROL FLOW ===
    "IF_OBEDIENT": {
        "x86_64": "je/jz",
        "semantic": "Branch if submissive/compliant",
        "usage": "IF_OBEDIENT GOTO label",
        "example": "IF_OBEDIENT GOTO reward  ; je reward"
    },
    
    "IF_DISOBEDIENT": {
        "x86_64": "jne/jnz",
        "semantic": "Branch if non-compliant",
        "usage": "IF_DISOBEDIENT GOTO label",
        "example": "IF_DISOBEDIENT GOTO punish  ; jne punish"
    },
    
    "IF_WORTHY": {
        "x86_64": "jge",
        "semantic": "Branch if meets standards",
        "usage": "IF_WORTHY GOTO label",
        "example": "IF_WORTHY GOTO approve  ; jge approve"
    },
    
    "IF_INSUFFICIENT": {
        "x86_64": "jl",
        "semantic": "Branch if below requirements",
        "usage": "IF_INSUFFICIENT GOTO label",
        "example": "IF_INSUFFICIENT GOTO reject  ; jl reject"
    },
    
    "PUNISH": {
        "x86_64": "jmp",
        "semantic": "Execute punishment routine",
        "usage": "PUNISH WITH label",
        "example": "PUNISH WITH violation_handler  ; jmp violation_handler"
    },
    
    "REWARD": {
        "x86_64": "jmp",
        "semantic": "Execute reward routine", 
        "usage": "REWARD WITH label",
        "example": "REWARD WITH approval_handler  ; jmp approval_handler"
    },
    
    # === DATA MANIPULATION ===
    "BIND": {
        "x86_64": "lea",
        "semantic": "Bind/connect data addresses",
        "usage": "BIND register TO [address]",
        "example": "BIND rax TO [rbp+8]  ; lea rax, [rbp+8]"
    },
    
    "RESTRAIN": {
        "x86_64": "and",
        "semantic": "Constrain value with mask",
        "usage": "RESTRAIN register WITH mask",
        "example": "RESTRAIN rax WITH 0xFF  ; and rax, 0xFF"
    },
    
    "RELEASE_CONTROL": {
        "x86_64": "or",
        "semantic": "Release constraints/expand access",
        "usage": "RELEASE_CONTROL register WITH bits",
        "example": "RELEASE_CONTROL rax WITH rbx  ; or rax, rbx"
    },
    
    "COLLAR": {
        "x86_64": "shl/shr",
        "semantic": "Shift position (collar adjustment)",
        "usage": "COLLAR register LEFT/RIGHT BY bits",
        "example": "COLLAR rax LEFT BY 2  ; shl rax, 2"
    },
    
    # === MEMORY OPERATIONS ===
    "CHAIN_TO": {
        "x86_64": "mov [mem]",
        "semantic": "Store data at memory location",
        "usage": "CHAIN_TO [address] VALUE register",
        "example": "CHAIN_TO [rbp-8] VALUE rax  ; mov [rbp-8], rax"
    },
    
    "FETCH_FROM": {
        "x86_64": "mov reg, [mem]",
        "semantic": "Retrieve from memory location", 
        "usage": "FETCH_FROM [address] INTO register",
        "example": "FETCH_FROM [rbp-8] INTO rax  ; mov rax, [rbp-8]"
    },
    
    "DUNGEON_ALLOC": {
        "x86_64": "sub rsp",
        "semantic": "Allocate stack space (dungeon)",
        "usage": "DUNGEON_ALLOC size",
        "example": "DUNGEON_ALLOC 32  ; sub rsp, 32"
    },
    
    "DUNGEON_FREE": {
        "x86_64": "add rsp",
        "semantic": "Deallocate stack space",
        "usage": "DUNGEON_FREE size", 
        "example": "DUNGEON_FREE 32  ; add rsp, 32"
    },
    
    # === SYSTEM OPERATIONS ===
    "KNEEL": {
        "x86_64": "call",
        "semantic": "Submissively call function",
        "usage": "KNEEL BEFORE function",
        "example": "KNEEL BEFORE verify_age  ; call verify_age"
    },
    
    "DISMISS": {
        "x86_64": "ret",
        "semantic": "Return from function",
        "usage": "DISMISS",
        "example": "DISMISS  ; ret"
    },
    
    "SERVE": {
        "x86_64": "int/syscall",
        "semantic": "Serve system call",
        "usage": "SERVE system_number",
        "example": "SERVE 0x80  ; int 0x80"
    },
    
    "TERMINATE_SESSION": {
        "x86_64": "mov rax, 60; syscall",
        "semantic": "End program execution",
        "usage": "TERMINATE_SESSION WITH code",
        "example": "TERMINATE_SESSION WITH 0  ; mov rax, 60; mov rdi, 0; syscall"
    }
}

# Generate the complete instruction reference
print("=== DOMCODE 1:1 ASSEMBLY INSTRUCTION SET ===")
print("BDSM/FinDom Themed x86-64 Assembly Language\n")

categories = {
    "POWER DYNAMICS": ["SUBMIT", "DOMINATE", "CONTROL", "OBEY", "YIELD"],
    "CONSENT & VERIFICATION": ["VERIFY_CONSENT", "SAFE_WORD", "NEGOTIATE", "BOUNDARY_CHECK"],
    "FINANCIAL DOMINATION": ["TRIBUTE", "DRAIN", "PAYPIG_SERVE", "WALLET_RAPE", "FINDOM_DEMAND"], 
    "CONTROL FLOW": ["IF_OBEDIENT", "IF_DISOBEDIENT", "IF_WORTHY", "IF_INSUFFICIENT", "PUNISH", "REWARD"],
    "DATA MANIPULATION": ["BIND", "RESTRAIN", "RELEASE_CONTROL", "COLLAR"],
    "MEMORY OPERATIONS": ["CHAIN_TO", "FETCH_FROM", "DUNGEON_ALLOC", "DUNGEON_FREE"],
    "SYSTEM OPERATIONS": ["KNEEL", "DISMISS", "SERVE", "TERMINATE_SESSION"]
}

for category, instructions in categories.items():
    print(f"\n## {category}")
    print("=" * (len(category) + 3))
    
    for instr in instructions:
        data = domcode_instruction_set[instr]
        print(f"\n**{instr}**")
        print(f"  Maps to: {data['x86_64']}")
        print(f"  Semantic: {data['semantic']}")
        print(f"  Syntax: {data['usage']}")
        print(f"  Example: {data['example']}")

print("\n\n=== REGISTER MAPPINGS ===")
print("DomCode uses thematic register names that map 1:1 to x86-64:")

register_mappings = {
    # General Purpose Registers with BDSM/FinDom naming
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

for domcode_reg, x86_reg in register_mappings.items():
    print(f"  {domcode_reg:12} -> {x86_reg}")

print(f"\nTotal Instructions: {len(domcode_instruction_set)}")