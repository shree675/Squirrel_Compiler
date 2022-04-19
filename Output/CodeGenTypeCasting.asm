.data

.text
.globl main

main:

move $s8, $sp

li.s $f1, 0.2
mov.s $f3, $f1
li.s $f4, 3.4
cvt.w.s $t0, $f4, 0
li $t1, 0
li.s $f5, 3.4
cvt.w.s $t2, $f5, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t2, 0
addi $t1, $t2, 0
move $sp, $s8
jr $ra

