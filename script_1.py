# Now let's create a complete DomCode program example and the grammar specification

# Sample DomCode program for age verification and compliance
sample_program = '''
; ACCCaaS Compliance Verification Routine
; This DomCode program demonstrates age verification with BDSM/FinDom semantics

SECTION .text
    GLOBAL main

main:
    ; Initialize the dungeon (allocate stack space)
    DUNGEON_ALLOC 64
    
    ; Load user age into SUB1 register
    SUBMIT 19 TO SUB1
    
    ; Verify consent meets legal requirements
    VERIFY_CONSENT SUB1 MEETS 18
    IF_INSUFFICIENT GOTO violation_handler
    
    ; Age verified - now check financial tribute
    PAYPIG_SERVE 500 TO TRIBUTE1
    VERIFY_CONSENT TRIBUTE1 MEETS 100
    IF_INSUFFICIENT GOTO insufficient_tribute
    
    ; Both age and tribute verified - proceed to reward
    REWARD WITH approval_sequence
    
violation_handler:
    ; Underage violation - terminate immediately
    SUBMIT 1 TO MISTRESS
    PUNISH WITH terminate_session
    
insufficient_tribute:
    ; Tribute too low - demand more
    FINDOM_DEMAND TRIBUTE1 BY 2
    REWARD WITH approval_sequence
    
approval_sequence:
    ; Successful verification - bind user data
    BIND SLAVE TO [DUNGEON_BASE + 8]
    CHAIN_TO [DUNGEON_BASE + 8] VALUE SUB1
    CHAIN_TO [DUNGEON_BASE + 16] VALUE TRIBUTE1
    
    ; Release user to platform
    SUBMIT 0 TO MISTRESS
    
terminate_session:
    DUNGEON_FREE 64
    TERMINATE_SESSION WITH MISTRESS
'''

print("=== SAMPLE DOMCODE PROGRAM ===")
print(sample_program)

# Now create the grammar specification
grammar_spec = '''
=== DOMCODE GRAMMAR SPECIFICATION ===

1. LEXICAL STRUCTURE:
   - Instructions: ALL_CAPS with underscores (VERIFY_CONSENT, PAYPIG_SERVE)
   - Registers: ALL_CAPS thematic names (MISTRESS, SLAVE, SUB1)
   - Constants: Decimal numbers (18, 500) or hex (0xFF)
   - Labels: lowercase_with_underscores (violation_handler, main)
   - Comments: ; (semicolon) to end of line
   - Memory: [register + offset] or [register]
   
2. INSTRUCTION FORMATS:
   - Zero operand: DISMISS, WALLET_RAPE register
   - One operand: TRIBUTE register, SAFE_WORD TO label  
   - Two operand: SUBMIT value TO register, CONTROL reg FROM source
   - Three operand: CHAIN_TO [address] VALUE register
   
3. REGISTER CLASSES:
   - Power registers: MISTRESS, MASTER (rax, rbx)
   - Submissive registers: SUB1, SUB2, SLAVE, SERVANT (rcx, rdx, rdi, rsi)  
   - Financial registers: TRIBUTE1-4, PAYPIG1-2, WALLET1-2 (r8-r15)
   - System registers: DUNGEON_BASE, COLLAR_PTR (rbp, rsp)
   
4. MEMORY ADDRESSING:
   - Direct: [address]
   - Register indirect: [DUNGEON_BASE]
   - Register + offset: [DUNGEON_BASE + 8]
   - Register + register: [DUNGEON_BASE + SUB1]
   - Register + register*scale: [DUNGEON_BASE + SUB1*4]
   
5. CONTROL FLOW:
   - Conditional branches use thematic conditions:
     IF_OBEDIENT, IF_DISOBEDIENT, IF_WORTHY, IF_INSUFFICIENT
   - Unconditional: PUNISH WITH label, REWARD WITH label, SAFE_WORD TO label
   - Function calls: KNEEL BEFORE function_name
   - Returns: DISMISS
   
6. COMPLIANCE-SPECIFIC CONSTRUCTS:
   - Age verification: VERIFY_CONSENT register MEETS threshold
   - Boundary checking: BOUNDARY_CHECK value WITHIN limit  
   - Financial operations: TRIBUTE, DRAIN, PAYPIG_SERVE, FINDOM_DEMAND
   - Memory protection: BIND, CHAIN_TO, RESTRAIN, RELEASE_CONTROL
   
7. ASSEMBLER DIRECTIVES:
   - SECTION .text, .data, .bss (standard NASM)
   - GLOBAL main (standard NASM)
   - Labels: name: (standard assembly)
   
8. TYPE SYSTEM:
   - All registers are 64-bit by default
   - Size prefixes: BYTE, WORD, DWORD, QWORD
   - Thematic sizing: COLLAR_TIGHT (byte), COLLAR_LOOSE (qword)
'''

print(grammar_spec)

# Create the lexer token specification
token_specification = '''
=== DOMCODE LEXER TOKEN SPECIFICATION ===

Token Types:
1. INSTRUCTION    - DomCode instruction mnemonics
2. REGISTER      - Thematic register names  
3. CONSTANT      - Numeric literals (decimal/hex)
4. LABEL         - Code labels and identifiers
5. MEMORY_REF    - Memory reference [...]
6. KEYWORD       - Syntax keywords (TO, WITH, FROM, etc.)
7. COMMENT       - ; comments
8. NEWLINE       - Line endings
9. DIRECTIVE     - Assembler directives (SECTION, GLOBAL)

Regular Expressions:
INSTRUCTION:  ^(SUBMIT|DOMINATE|CONTROL|VERIFY_CONSENT|TRIBUTE|...)$
REGISTER:     ^(MISTRESS|MASTER|SUB[1-4]|SLAVE|SERVANT|...)$  
CONSTANT:     ^([0-9]+|0x[0-9A-Fa-f]+)$
LABEL:        ^[a-z_][a-z0-9_]*:?$
MEMORY_REF:   ^\[[^\]]+\]$
KEYWORD:      ^(TO|WITH|FROM|BY|MEETS|WITHIN|GOTO|BEFORE|INTO|VALUE)$
COMMENT:      ^;.*$
DIRECTIVE:    ^(SECTION|GLOBAL|EXTERN)$
'''

print(token_specification)

# Create the parser BNF grammar
bnf_grammar = '''
=== DOMCODE BNF GRAMMAR ===

program         ::= directive* section*
section         ::= 'SECTION' section_name statement*
section_name    ::= '.text' | '.data' | '.bss'
statement       ::= label | instruction | directive | comment
label           ::= LABEL ':'
instruction     ::= power_instr | control_instr | memory_instr | system_instr | findom_instr
comment         ::= ';' TEXT

; Power dynamic instructions
power_instr     ::= 'SUBMIT' operand 'TO' register
                 | 'DOMINATE' register 'WITH' operand  
                 | 'CONTROL' register 'FROM' operand
                 | 'OBEY' register 'AGAINST' operand
                 | 'YIELD' register 'BY' operand

; Control flow instructions  
control_instr   ::= 'IF_OBEDIENT' 'GOTO' label
                 | 'IF_DISOBEDIENT' 'GOTO' label
                 | 'IF_WORTHY' 'GOTO' label
                 | 'IF_INSUFFICIENT' 'GOTO' label
                 | 'PUNISH' 'WITH' label
                 | 'REWARD' 'WITH' label
                 | 'SAFE_WORD' 'TO' label

; Memory instructions
memory_instr    ::= 'BIND' register 'TO' memory_ref
                 | 'CHAIN_TO' memory_ref 'VALUE' register
                 | 'FETCH_FROM' memory_ref 'INTO' register
                 | 'DUNGEON_ALLOC' constant
                 | 'DUNGEON_FREE' constant

; System instructions
system_instr    ::= 'KNEEL' 'BEFORE' label
                 | 'DISMISS' 
                 | 'SERVE' operand
                 | 'TERMINATE_SESSION' 'WITH' register

; Financial domination instructions
findom_instr    ::= 'TRIBUTE' register
                 | 'DRAIN' 'INTO' register
                 | 'PAYPIG_SERVE' operand 'TO' register
                 | 'WALLET_RAPE' register
                 | 'FINDOM_DEMAND' register 'BY' operand

; Compliance instructions
compliance_instr ::= 'VERIFY_CONSENT' register 'MEETS' operand
                  | 'BOUNDARY_CHECK' operand 'WITHIN' operand
                  | 'NEGOTIATE' register 'WITH' operand

operand         ::= register | constant | memory_ref
register        ::= MISTRESS | MASTER | SUB1 | SUB2 | SLAVE | SERVANT | 
                   DUNGEON_BASE | COLLAR_PTR | TRIBUTE1 | TRIBUTE2 | 
                   TRIBUTE3 | TRIBUTE4 | PAYPIG1 | PAYPIG2 | WALLET1 | WALLET2
constant        ::= NUMBER | HEX_NUMBER  
memory_ref      ::= '[' register ']' | '[' register '+' constant ']' |
                   '[' register '+' register ']' | '[' register '+' register '*' scale ']'
scale           ::= '1' | '2' | '4' | '8'
'''

print(bnf_grammar)