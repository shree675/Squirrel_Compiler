.data

.text
.globl main

main:

move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
addi $t2, $t1, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t2, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
sub $t2, $t0, $t2
bne $t2, $zero, _L9
j _L8
_L9:
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 1
addi $sp, $sp, -4
sw $t0, 4($sp)
lw $t0, -12($s8)
sw $t0, -12($s8)
lw $t0, -16($s8)
sw $t0, -16($s8)
sub $t0, $t0, $t0
beq $t0, $zero, _L12
sw $t0, -16($s8)
lw $t0, -20($s8)
li $v0, 1
move $a0, $t0
syscall
j _L13
_L12:
sw $t0, -20($s8)
lw $t0, -16($s8)
li $v0, 1
move $a0, $t0
syscall
_L13:
_L8:
move $sp, $s8
jr $ra

