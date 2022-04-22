.data

.text
.globl main

main:

move $s8, $sp

addi $t0, $a0, 0
li $t1, 0
li $t2, 0
li $t3, 0
_L14:
li $t4, 5
sub $t5, $t1, $t4
blt $t5, $zero, _L15
j _L6
_L15:
li $t5, 0
sub $t6, $t3, $t5
beq $t6, $zero, _L19
j _L20
_L19:
li $t6, 1
mtc1 $t6, $f1
cvt.s.w $f3, $f1
cvt.w.s $f1, $f3
mfc1 $t7, $f1
addi $t3, $t7, 0
j _L6
_L20:
li $s0, 1
add $s1, $t1, $s0
addi $t1, $s1, 0
_L18:
j _L14
_L6:
move $a0, $t1
li $v0, 1
syscall
mult $t1, $t2
mflo $s2
add $s3, $t1, $s2
add $s4, $t1, $t2
mult $t2, $s4
mflo $s5
add $s6, $s3, $s5
move $sp, $s8
move $v0, $s6
jr $ra
jr $ra

