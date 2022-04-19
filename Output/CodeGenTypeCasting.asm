.data

.text
.globl main

main:

move $s8, $sp

li.s $t0, 0.2
cvt.s.w $f1, $t0, 0
li.s $t1, 3.4
addi $t2, $t1, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
li $t0, 0
addi $sp, $sp, -4
sw $t1, 4($sp)
li.s $t1, 3.4
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $t1, $t1, 0
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $t1, $t1, 0
addi $t0, $t1, 0
move $sp, $s8
jr $ra

