.data
	abc__2:
		.float 1.1, 2.2, 3.3, 4.4

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
l.s $f3, abc__2($t2)
cvt.w.s $f1, $f3
mfc1 $t3, $f1
bne $t3, $zero, ___L0
addi $t3, $zero, 0
j ___L1
___L0:
addi $t3, $zero, 1
___L1:
addi $t4, $t3, 0
li $t5, 1
sub $t6, $t4, $t5
beq $t6, $zero, _L7
j _L8
_L7:
li $t6, 9
move $a0, $t6
li $v0, 1
syscall
j _L6
_L8:
li $t7, 2
li $s0, 1
mult $t7, $s0
mflo $s0
li $s1, 4
mult $s0, $s1
mflo $s1
l.s $f4, abc__2($s1)
cvt.w.s $f1, $f4
mfc1 $s2, $f1
li $s3, 3
addi $s4, $s2, 0
sub $s5, $s4, $s3
beq $s5, $zero, _L11
j _L12
_L11:
li $s5, 10
move $a0, $s5
li $v0, 1
syscall
j _L6
_L12:
li $s6, 11
move $a0, $s6
li $v0, 1
syscall
_L6:
move $sp, $s8
jr $ra

