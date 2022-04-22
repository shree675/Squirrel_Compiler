.data

.text
.globl main

main:

move $s8, $sp

move $a0, $t0
li $v0, 1
syscall
move $sp, $s8
jr $ra

