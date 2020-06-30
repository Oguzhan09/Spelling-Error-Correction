# Spelling-Error-Correction
Implement an isolated word spelling error corrector based on the noisy channel model.
HOW TO RUN PROGRAM ?  
1. Open the terminal in the specific folder which contain program files
2. Write this "python3 'python-project-name' 'input1' 'input2' 'input3' 'input4'
3. After that my program create "output.txt" file in the folder.

My project name: spell-corrector.py <br/>
input1 : "corpus.txt" <br/>
input2 : "spell-errors.txt" <br/>
input3 : "test-words-misspelled.txt" <br/>
input4 : "smooth" or "nonsmooth" <br/>

So, I am writing for testing provided file: <br/>
With smoothing:  <br/>
``` python3 spell-corrector.py corpus.txt spell-errors.txt test-words-misspelled.txt smooth``` <br/>
With non smoothing:  <br/>
``` python3 spell-corrector.py corpus.txt spell-errors.txt test-words-misspelled.txt nonsmooth ``` <br/>
