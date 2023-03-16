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
![13](https://user-images.githubusercontent.com/107920651/225586254-bb226de2-ab9f-4ee1-ba79-5e94ad140279.PNG)
![14](https://user-images.githubusercontent.com/107920651/225586325-49fe3175-e55d-40ea-a4b6-f0c0dbf8c076.PNG)
![15](https://user-images.githubusercontent.com/107920651/225586403-1ecd7c6a-5912-4ea1-80a3-d62963e9d3d6.PNG)
![16](https://user-images.githubusercontent.com/107920651/225586496-e5cc1941-4bdd-4cae-ac24-173b6e8e7261.PNG)
![17](https://user-images.githubusercontent.com/107920651/224984341-9ae3d6b1-dd80-44a3-8d06-b7ff45dcd629.PNG)
![18](https://user-images.githubusercontent.com/107920651/224984368-4e22896f-a402-4647-87a4-6b4f78046b4d.PNG)
