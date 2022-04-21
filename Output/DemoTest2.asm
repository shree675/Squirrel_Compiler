.data

.text
.globl main

main:

move $s8, $sp

li $t0, 0
li $t1, 20
addi $t2, $t1, 0
li.s $f3, 1.2
mov.s $f4, $f3
li $t3, 20
sub $t4, $t2, $t3
bne $t4, $zero, _L11
li.s $f5, 8.4
mov.s $f4, $f5
mov.s $f12, $f4
li $v0, 2
syscall
j _L10
_L11:
li $t4, 4
sub $t5, $t2, $t4
bne $t5, $zero, _L18
li $t5, 82
addi $t0, $t5, 0
move $a0, $t0
li $v0, 1
syscall
j _L10
_L18:
li $t6, 0
li $t7, 0
li $s0, 1
sub $s1, $t6, $t7
beq $s1, $zero, _L29
move $a0, $s0
li $v0, 1
syscall
j _L30
_L29:
move $a0, $t7
li $v0, 1
syscall
_L30:
j _L10
_L10:
move $sp, $s8
jr $ra

