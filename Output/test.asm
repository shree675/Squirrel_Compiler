.data

.text
.globl main

main:

move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
li $t2, 10
addi $t3, $t2, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 11
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t0, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 12
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t0, 0
addi $sp, $sp, -4
sw $t3, 4($sp)
li $t3, 13
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t3, 0
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t1, 0
move $sp, $s8
jr $ra

