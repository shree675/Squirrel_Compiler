.data

__t5:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 42
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
_L11:
addi $sp, $sp, -4
sw $t3, 4($sp)
li $t3, 10
addi $sp, $sp, -4
sw $t3, 4($sp)
lw $t3, 0($s8)
sub $t3, $t3, $t3
blt $t3, $zero, _L12
j _L9
_L12:
move $a0, $t3
li $v0, 1
syscall
sw $t3, 0($s8)
li $t3, 1
addi $sp, $sp, -4
sw $t3, 4($sp)
lw $t3, 0($s8)
sw $t3, -8($s8)
add $t3, $t3, $t3
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t3, 0
j _L11
_L9:
sw $t3, 0($s8)
la $t3, __t5
li $v0, 4
la $a0, __t5
syscall
move $sp, $s8
jr $ra

