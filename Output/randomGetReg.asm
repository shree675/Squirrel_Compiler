.data

__t13:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
_L9:
li $t7, 2
move $t4, $t3
move $t5, $t7
sub $t6, $t4, $t5
blt $t6, $zero, _L10
j _L7
_L10:
li $t8, 0
addi $t9, $t8, 0
_L16:
li $s0, 3
move $t4, $t9
move $t5, $s0
sub $t6, $t4, $t5
blt $t6, $zero, _L17
j _L14
_L17:
li $s1, 0
addi $s2, $s1, 0
_L23:
li $s3, 2
move $t4, $s2
move $t5, $s3
sub $t6, $t4, $t5
blt $t6, $zero, _L24
j _L21
_L24:
move $a0, $t1
li $v0, 1
syscall
la $s4, __t13
li $v0, 4
la $a0, __t13
syscall
li $s5, 1
add $s6, $t1, $s5
addi $t1, $s6, 0
li $s7, 1
addi $sp, $sp, -4
sw $t0, 4($sp)
add $t0, $s2, $s7
addi $s2, $t0, 0
j _L23
_L21:
addi $sp, $sp, -4
sw $t1, 4($sp)
li $t1, 1
addi $sp, $sp, -4
sw $t2, 4($sp)
add $t2, $t9, $t1
addi $t9, $t2, 0
j _L16
_L14:
addi $sp, $sp, -4
sw $t3, 4($sp)
li $t3, 1
addi $sp, $sp, -4
sw $t7, 4($sp)
lw $t7, -12($s8)
addi $sp, $sp, -4
sw $t8, 4($sp)
add $t8, $t7, $t3
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t8, 0
j _L9
_L7:
move $sp, $s8
jr $ra

