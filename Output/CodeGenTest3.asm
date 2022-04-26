.data
	arr__2:
		.float 0.0, 0.0, 0.0, 0.0

__t12:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li.s $f3, 1.0
mov.s $f4, $f3
li $t0, 0
addi $t1, $t0, 0
_L13:
li $t2, 4
sub $t3, $t1, $t2
blt $t3, $zero, _L14
j _L11
_L14:
li $t3, 1
mult $t1, $t3
mflo $t3
li $t4, 4
mult $t3, $t4
mflo $t4
li $t5, 1
add $t6, $t1, $t5
mtc1 $t6, $f1
cvt.s.w $f5, $f1
s.s $f5, arr__2($t4)
li $t7, 1
mult $t1, $t7
mflo $t7
li $s0, 4
mult $t7, $s0
mflo $s0
l.s $f6, arr__2($s0)
mul.s $f7, $f4, $f6
mov.s $f4, $f7
li $s1, 1
mult $t1, $s1
mflo $s1
li $s2, 4
mult $s1, $s2
mflo $s2
l.s $f8, arr__2($s2)
mov.s $f12, $f8
li $v0, 2
syscall
la $s3, __t12
li $v0, 4
la $a0, __t12
syscall
li $s4, 1
add $s5, $t1, $s4
addi $t1, $s5, 0
j _L13
_L11:
mov.s $f12, $f4
li $v0, 2
syscall
move $sp, $s8
jr $ra

