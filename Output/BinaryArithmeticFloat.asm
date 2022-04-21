.data

__t1:
	.asciiz "\n"
__t2:
	.asciiz "\n"
__t3:
	.asciiz "\n"
__t4:
	.asciiz "\n"
__t5:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li.s $f3, 2.7
mov.s $f4, $f3
li.s $f5, 3.9
mov.s $f6, $f5
add.s $f7, $f4, $f6
mov.s $f8, $f7
li $t0, 2
mtc1 $t0, $f1
cvt.s.w $f9, $f1
mul.s $f10, $f6, $f9
sub.s $f11, $f4, $f10
mov.s $f20, $f11
mul.s $f21, $f4, $f6
mov.s $f22, $f21
div.s $f23, $f4, $f6
mov.s $f24, $f23
mov.s $f12, $f4
li $v0, 2
syscall
la $t1, __t1
li $v0, 4
la $a0, __t1
syscall
mov.s $f12, $f6
li $v0, 2
syscall
la $t2, __t2
li $v0, 4
la $a0, __t2
syscall
mov.s $f12, $f8
li $v0, 2
syscall
la $t3, __t3
li $v0, 4
la $a0, __t3
syscall
mov.s $f12, $f20
li $v0, 2
syscall
la $t4, __t4
li $v0, 4
la $a0, __t4
syscall
mov.s $f12, $f22
li $v0, 2
syscall
la $t5, __t5
li $v0, 4
la $a0, __t5
syscall
mov.s $f12, $f24
li $v0, 2
syscall
move $sp, $s8
jr $ra

