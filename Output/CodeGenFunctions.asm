.data

.text
.globl main

sum:
move $s8, $sp

addi $t0, $a0, 0
addi $t1, $a1, 0
add $t2, $t0, $t1
move $sp, $s8
move $v0, $t2
jr $ra
jr $ra
main:

move $s8, $sp

li $t0, 1
addi $t1, $t0, 0
li $t2, 12
addi $t3, $t2, 0
li $t4, 133
addi $t5, $t4, 0

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $sp, $sp, -4
sw $t4, 4($sp)
addi $sp, $sp, -4
sw $t5, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a1, $t3
move $a0, $t1
jal sum
move $t6, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
lw $t4, -16($s8)
lw $t5, -20($s8)
add $t7, $t5, $t6
addi $t5, $t7, 0
move $a0, $t5
li $v0, 1
syscall
move $sp, $s8
jr $ra

