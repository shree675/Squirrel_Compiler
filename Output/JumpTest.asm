.data

.text
.globl main

main:

move $s8, $sp

li $t0, 0
li $t1, 0
li $t2, 0
_L14:
li $t3, 5
sub $t4, $t0, $t3
blt $t4, $zero, _L15
j _L6
_L15:
li $t4, 0
sub $t5, $t2, $t4
beq $t5, $zero, _L19
j _L20
_L19:
li $t5, 1
mtc1 $t5, $f1
cvt.s.w $f3, $f1
cvt.w.s $f1, $f3
mfc1 $t6, $f1
addi $t2, $t6, 0
j _L6
_L20:
li $t7, 1
add $s0, $t0, $t7
addi $t0, $s0, 0
_L18:
j _L14
_L6:
move $a0, $t0
li $v0, 1
syscall
mult $t0, $t1
mflo $s1
add $s2, $t0, $s1
add $s3, $t0, $t1
mult $t1, $s3
mflo $s4
add $s5, $s2, $s4
move $sp, $s8
move $v0, $s5
jr $ra
jr $ra

