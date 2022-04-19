.data

.text
.globl main

main:

move $s8, $sp

li $t0, 2
addi $t1, $t0, 0
li $t2, 3
addi $t3, $t2, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
add $t0, $t1, $t3
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 2
addi $sp, $sp, -4
sw $t0, 4($sp)
mult $t3, $t0
mflo $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
sub $t0, $t1, $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
mult $t1, $t3
mflo $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
div $t1, $t3
mflo $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
div $t1, $t3
mfhi $t0
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
li $v0, 1
move $a0, $t1
syscall
li $v0, 1
move $a0, $t3
syscall
li $v0, 1
move $a0, $t2
syscall
addi $sp, $sp, -4
sw $t0, 4($sp)
lw $t0, -24($s8)
li $v0, 1
move $a0, $t0
syscall
sw $t0, -24($s8)
lw $t0, -32($s8)
li $v0, 1
move $a0, $t0
syscall
sw $t0, -32($s8)
lw $t0, -40($s8)
li $v0, 1
move $a0, $t0
syscall
sw $t0, -40($s8)
lw $t0, -48($s8)
li $v0, 1
move $a0, $t0
syscall
move $sp, $s8
jr $ra

