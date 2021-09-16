# Hamming distance, assume word is in s0
	addi 	s1, x0, 0	# s1 = 0
	add	t0, x0, s0	# t0 = s0
loop:
	bgt	t0, x0, skip	# if t0 > 0, then MSB != 1, skip: incrementing the counter
	addi	s1, s1, 1	# increment counter since MSB == 1
skip:
	slli	t0, t0, 1	# shift the copy of s0 << 1 bit so we get a new MSB
	bne	t0, 0, loop	# if s0 == 0 there are no more bits to count, otherwise continue
	
