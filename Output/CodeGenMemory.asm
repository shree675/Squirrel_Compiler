.text
.globl main

main:

move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
li $t2, 10
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t2, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 11
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t2, 0
move $sp, $s8
jr $ra

