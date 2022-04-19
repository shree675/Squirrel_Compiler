.data

.text
.globl main

main:

move $s8, $sp

li $t0, 97
addi $t1, $t0, 0
addi $t2, $t1, 0
li $t3, 1
addi $t4, $t3, 0
addi $t5, $t4, 0
li $t6, 97
mtc1 $t6, $f1
cvt.s.w $f3, $f1
mov.s $f4, $f3
addi $t7, $t5, 0
add $s0, $t2, $t7
mtc1 $s0, $f1
cvt.s.w $f5, $f1
li $v0, 2
mov.s $f12, $f5
syscall
move $sp, $s8
jr $ra

