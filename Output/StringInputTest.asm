.data

.text
.globl main

main:

move $s8, $sp

li $t0, 0.0
cvt.w.s $t0, $t0
li $v0, 6
syscall
move $f3, $v0
mov.s $f12, $f3
li $v0, 2
syscall
move $sp, $s8
jr $ra

