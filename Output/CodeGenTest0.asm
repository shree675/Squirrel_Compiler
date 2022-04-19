.data

.text
.globl main

main:

move $s8, $sp

li $t0, 6
addi $t1, $t0, 0
li $t2, 0
li $t3, 0
li $t4, 2
li $t5, 3
sub $t6, $t5, $t4
blt $t6, $zero, _L15
j _L16
_L15:
li $t6, 5
addi $t2, $t6, 0
j _L14
_L16:
addi $t3, $t1, 0
_L14:
li $v0, 1
move $a0, $t3
syscall
li $v0, 1
move $a0, $t2
syscall
move $sp, $s8
jr $ra

