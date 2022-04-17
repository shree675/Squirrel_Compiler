.text
.globl main

main:

move $s8, $sp

li $t0, 0
li $v0, 5
syscall
move $t0, $v0
li $t1, 48
li $v0, 12
syscall
move $t1, $v0
addi $sp, $sp, -4
sw $t0, 4($sp)
li.s $t0, 0.0
li $v0, 6
syscall
addi $sp, $sp, -4
sw $t1, 4($sp)
move $t1, $v0
move $sp, $s8
jr $ra

