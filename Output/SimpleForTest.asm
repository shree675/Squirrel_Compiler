.data

__t12:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 42
addi $t1, $t0, 0
li $t2, 23
addi $t3, $t2, 0
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
addi $t1, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $t3, 4($sp)
_L17:
li $t2, 2
lw $t3, -28($s8)
sub $t0, $t3, $t2
blt $t0, $zero, _L18
move $t0, $zero
move $t1, $zero
addi $sp, $sp, -4
sw $t2, 4($sp)
move $t2, $zero
sw $t3, -28($s8)
move $t3, $zero
j _L15
sw $t2, -40($s8)
sw $t3, -28($s8)
_L18:
li $t1, 0
sw $t2, -40($s8)
addi $t2, $t1, 0
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
sw $t3, -28($s8)
_L24:
sw $t3, -28($s8)
li $t3, 10
sub $t0, $t2, $t3
blt $t0, $zero, _L25
move $t0, $zero
sw $t1, -44($s8)
move $t1, $zero
sw $t2, -48($s8)
move $t2, $zero
addi $sp, $sp, -4
sw $t3, 4($sp)
move $t3, $zero
j _L22
sw $t1, -44($s8)
sw $t2, -48($s8)
sw $t3, -52($s8)
_L25:
move $a0, $t2
li $v0, 1
syscall
sw $t1, -44($s8)
li $t1, 1
sw $t2, -48($s8)
add $t2, $t2, $t1
sw $t3, -52($s8)
addi $t3, $t2, 0
move $t0, $zero
addi $sp, $sp, -4
sw $t1, 4($sp)
move $t1, $zero
addi $sp, $sp, -4
sw $t2, 4($sp)
move $t2, $zero
sw $t3, -48($s8)
move $t3, $zero
j _L24
sw $t1, -56($s8)
sw $t2, -60($s8)
sw $t3, -48($s8)
_L22:
li $t0, 1
sw $t1, -56($s8)
lw $t1, -28($s8)
sw $t2, -60($s8)
add $t2, $t1, $t0
sw $t3, -48($s8)
addi $t3, $t2, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
move $t0, $zero
sw $t1, -56($s8)
move $t1, $zero
addi $sp, $sp, -4
sw $t2, 4($sp)
move $t2, $zero
sw $t3, -28($s8)
move $t3, $zero
j _L17
sw $t0, -64($s8)
sw $t1, -56($s8)
sw $t2, -68($s8)
sw $t3, -28($s8)
_L15:
sw $t0, -64($s8)
la $t0, __t12
li $v0, 4
la $a0, __t12
syscall
move $sp, $s8
jr $ra

