.data

.text
.globl main

main:

move $s8, $sp

li $t0, 25
addi $t1, $t0, 0
li $t2, 0
li $t3, 0
sub $t4, $t2, $t3
bne $t4, $zero, _L9
j _L10
_L9:
li $v0, 1
move $a0, $t1
syscall
j _L8
_L10:
li $t4, 0
li $t5, 1
sub $t6, $t2, $t4
beq $t6, $zero, _L15
li $v0, 1
move $a0, $t5
syscall
j _L16
_L15:
li $v0, 1
move $a0, $t4
syscall
_L16:
_L8:
move $sp, $s8
jr $ra

