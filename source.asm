COPY     START  1000 
FIRST    STL    RETADR            SAVE RETURN ADDRESS       
CLOOP    JSUB   RDREC
         LDA    LENGTH            TEST FOR EOF
         COMP   ZERO
         JEQ    ENDFIL
         J      CLOOP
         BASE
ENDFIL   LDB    =C'EOF'
         LDA    =X'F1'
         STA    BUFFER
         LDA    THREE
         STA    LENGTH
         RSUB
         LTORG
EOF      BYTE   C'EOF'
         BYTE   X'F1'
THREE    WORD   3
ZERO     WORD   0
RETADR   RESW   1
LENGTH   RESW   1
BUFFER   RESB   4096
.      SUBROUTINE TO READ RECORD INTO BUFFER
RDREC    LDX    ZERO
         LDA    ZERO
         LDA    =X'F2'
RLOOP    TD     LENGTH
         JEQ    RLOOP
         COMP   ZERO
         JEQ    EXIT
         STCH   BUFFER,X
         JLT    RLOOP
EXIT     STX    LENGTH
         RSUB       
         END    FIRST         
