.data

.text
.globl main

foo:
move $s8, $sp

addi $t0, $a0, 0
move $a0, $t0
li $v0, 1
syscall
move $sp, $s8
jr $ra
main:

move $s8, $sp

li $t0, 10
addi $t1, $t0, 0
li $t2, 0
sub $t2, $t2, $t1

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t2
jal foo
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
move $sp, $s8
jr $ra

