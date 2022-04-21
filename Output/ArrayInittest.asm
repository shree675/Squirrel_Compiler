.data
	floatArray__2:
		.float 1.1, 5.0, 3.3

.text
.globl main

main:

move $s8, $sp

li $t0, 2
li $t1, 1
mult $t0, $t1
mflo $t1
li $t2, 4
mult $t1, $t2
mflo $t2
li $t3, 1
li $t4, 1
mult $t3, $t4
mflo $t4
li $t5, 4
mult $t4, $t5
mflo $t5
l.s $f3, floatArray__2($t5)
li $t6, 0
li $t7, 1
mult $t6, $t7
mflo $t7
li $s0, 4
mult $t7, $s0
mflo $s0
l.s $f4, floatArray__2($s0)
add.s $f5, $f3, $f4
mov.s $f6, $f5
s.s $f6, floatArray__2($t2)
li $s1, 2
li $s2, 1
mult $s1, $s2
mflo $s2
li $s3, 4
mult $s2, $s3
mflo $s3
l.s $f7, floatArray__2($s3)
mov.s $f12, $f7
li $v0, 2
syscall
move $sp, $s8
jr $ra

