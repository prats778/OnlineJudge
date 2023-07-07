import os, filecmp    

out1 ='output.txt'
out2 ='actual_output1.txt'
if(filecmp.cmp(out1,out2,shallow=False)):
    verdict = 'Accepted'
else:
    verdict = 'Wrong Answer'

print(verdict)  