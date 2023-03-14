# SicAssembler V16.00 :computer:

## Project Objectives
- Implementing an assembler for the SIC hypothetical machine.
- Improving programming skills.

## Project Description
The project is a simulation of the assembler of the SIC hypothetical machine. I implement both Pass1 and Pass2 of the SIC assembler language. My assembler consider all the issues:

- Directives: START, END, BYTE, WORD, RESB, RESW, LTORG.
- Comments: If a source line contains a period (.) in the first byte, the entire line is treated as a comment.
- Addressing modes: Simple, Indirect
- Instruction Set: Specified in Appendix A in text book: Beck, Leland L., System Software: An Introduction to Systems Programming, 3rd
Edition. Addison Wesley Longman, Inc., 1997.
- Errors: Assembler flag ALL expected errors.

I am included test files. Assumed a fixed format source code with all text written in uppercase.

### Pass 1
The output of Pass 1 is:

1. Symbol Table SYBTAB: displayed on the screen.
2. LOCCTR, PRGLTH, PRGNAME, ...
3. Intermediate file (.mdt): Stored on the secondary storage.

### Pass 2
The output of Pass 2 is:

1. The object file (.obj)
2. The listing file (.lst)
3. List of errors if happened (duplicate labels, invalid mnemonic, inappropriate operand...).

My source code has a fixed format, I am committed to the following dimensions:
Columns: 
1-10 Label 
11-11 Blank 
12-20 Operation code (or Assembler directive) 
21-21 Blank 
22-39 Operand 
40-70 Comment 

### My project has a GUI for users to interact with it.

## Regulations
- I am used PYTHON programming language to implement the project.
## Images
![11](https://user-images.githubusercontent.com/107920651/224984128-3213a912-bc18-4444-8d79-115e0d7108ce.PNG)
![12](https://user-images.githubusercontent.com/107920651/224984153-b0900093-fa1c-45d3-a1ba-6f64af79a672.PNG)
![13](https://user-images.githubusercontent.com/107920651/224984190-daf5163c-496b-489e-981c-37718d3f9305.PNG)
![14](https://user-images.githubusercontent.com/107920651/224984238-efbb062e-d451-45a4-8bd6-5e0f6f7cf9f1.PNG)
![15](https://user-images.githubusercontent.com/107920651/224984274-2fd89c7a-ad12-4e56-b69f-47e9e5157aa9.PNG)
![16](https://user-images.githubusercontent.com/107920651/224984307-a27621f3-c669-4f9a-a1b2-5ed9103b06cd.PNG)
![17](https://user-images.githubusercontent.com/107920651/224984341-9ae3d6b1-dd80-44a3-8d06-b7ff45dcd629.PNG)
![18](https://user-images.githubusercontent.com/107920651/224984368-4e22896f-a402-4647-87a4-6b4f78046b4d.PNG)
