# while loops
# while (cond) {
# ;
# }

# Implement the following loop with RISC-V instructions
# sum = 0;
# i = 0;
# while (i < 100) {
# sum+=i;
# i+=1; }

# Method 1, test at the start (more instructions!)
# these instructions are executed once
addi s0, x0, 0   # i =0
addi s1, s0, 0   # sum = 0
addi s2, x0, 100 # end when we reach 100

# the loop will run 100 times, top instruction is executed an
# additional time. Each time the loop executes 4 instructions are executed

loop:
	bge s0, s2, exit # if s0 >= s2 -> exit:
	add s1, s1, s0
	addi s0, s0, 1
	beq x0, x0, loop

exit:
		
# 404 total instructions


# Method 2, test at the end
addi s0, x0, 0
addi s1, s0, 0	
addi s2, x0, 100
# 3 instructions	

beq x0, x0, test

loop: 
add s1,s1, test
addi s0, s0, 1		

test:
blt s0, s2, loop
# 305 instructions!
	







