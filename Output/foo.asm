.data

__t12:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

# t0 -> ~t0
li $t0, 42

# t1 -> a2
addi $t1, $t0, 0

# t2 -> ~t1
li $t2, 23

# t3 -> b2
addi $t3, $t2, 0

# spilling t0
addi $sp, $sp, -4
sw $t0, 4($sp)

li $t0, 12
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $t1, $t0, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 11
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t2, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 0
addi $sp, $sp, -4
sw $t1, 4($sp)

# $t1 -> i
addi $t1, $t0, 0
_L17:
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 2
sub $t3, $t1, $t2
blt $t3, $zero, _L18
j _L15
_L18:
addi $sp, $sp, -4
sw $t0, 4($sp)

# $t0 -> t8
li $t0, 0
addi $sp, $sp, -4
sw $t1, 4($sp)

# $t1 -> 
addi $t1, $t0, 0
_L24:
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 10
sub $t3, $t1, $t2
blt $t3, $zero, _L25
j _L22
_L25:
move $a0, $t1
li $v0, 1
syscall
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 1
addi $sp, $sp, -4
sw $t1, 4($sp)
add $t1, $t1, $t0
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t1, 0
j _L24
_L22:
addi $sp, $sp, -4
sw $t3, 4($sp)
li $t3, 1
addi $sp, $sp, -4
sw $t0, 4($sp)
lw $t0, -32($s8)
addi $sp, $sp, -4
sw $t1, 4($sp)
add $t1, $t0, $t3
sw $t2, -44($s8)
addi $t2, $t1, 0
j _L17
_L15:
addi $sp, $sp, -4
sw $t3, 4($sp)
la $t3, __t12
li $v0, 4
la $a0, __t12
syscall
move $sp, $s8
jr $ra

