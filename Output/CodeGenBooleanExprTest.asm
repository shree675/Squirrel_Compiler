.data

.text
.globl main

main:

move $s8, $sp

li $t0, 97
addi $t1, $t0, 0
li.s $f3, 2.0
mov.s $f4, $f3
li.s $f5, 3.0
mov.s $f6, $f5
li $t2, 0
addi $t3, $t2, 0
cvt.w.s $f1, $f4
mfc1 $t4, $f1
cvt.w.s $f1, $f6
mfc1 $t5, $f1
li $t6, 0
sub $t7, $t4, $t6
beq $t7, $zero, _L17
sub $t7, $t5, $t6
beq $t7, $zero, _L17
li $t7, 1
j _L16
_L17:
li $t7, 0
_L16:
addi $s0, $t7, 0
li $s1, 0
sub $s2, $s0, $s1
bne $s2, $zero, _L19
sub $s2, $t3, $s1
bne $s2, $zero, _L19
li $s2, 0
j _L18
_L19:
li $s2, 1
_L18:
addi $s3, $s2, 0
addi $t1, $s3, 0
move $a0, $t1
li $v0, 11
syscall
move $sp, $s8
jr $ra

