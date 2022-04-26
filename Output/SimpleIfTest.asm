.data

__t3:
	.asciiz "Yes"
__t4:
	.asciiz "Maybe"
__t5:
	.asciiz "No"
__t6:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 42
addi $t1, $t0, 0
li $t2, 0
li $t3, 51
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t3, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 100
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
sub $t1, $t1, $t2
blt $t1, $zero, _L15
j _L16
_L15:
addi $sp, $sp, -4
sw $t3, 4($sp)
la $t3, __t3
li $v0, 4
la $a0, __t3
syscall
j _L14
_L16:
addi $sp, $sp, -4
sw $t3, 4($sp)
lw $t3, -12($s8)
sub $t3, $t3, $t0
blt $t3, $zero, _L19
j _L20
_L19:
sw $t3, -12($s8)
la $t3, __t4
li $v0, 4
la $a0, __t4
syscall
j _L14
_L20:
addi $sp, $sp, -4
sw $t3, 4($sp)
la $t3, __t5
li $v0, 4
la $a0, __t5
syscall
_L14:
addi $sp, $sp, -4
sw $t3, 4($sp)
la $t3, __t6
li $v0, 4
la $a0, __t6
syscall
move $sp, $s8
jr $ra

