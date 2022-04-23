.data

__t0:
	.asciiz "\n"
__t1:
	.asciiz "\n"
__t4:
	.asciiz "\n"
__t11:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li.s $f3, 2.5
cvt.w.s $f1, $f3
mfc1 $t0, $f1
move $a0, $t0
li $v0, 1
syscall
la $t1, __t0
li $v0, 4
la $a0, __t0
syscall
li.s $f4, 110.345
cvt.w.s $f1, $f4
mfc1 $t2, $f1
move $a0, $t2
li $v0, 11
syscall
la $t3, __t1
li $v0, 4
la $a0, __t1
syscall
li.s $f5, 32.21
cvt.w.s $f1, $f5
mfc1 $t4, $f1
li $t5, 0
li $t6, 1
sub $t7, $t4, $t5
beq $t7, $zero, _L24
move $a0, $t6
li $v0, 1
syscall
j _L25
_L24:
move $a0, $t5
li $v0, 1
syscall
_L25:
la $t7, __t4
li $v0, 4
la $a0, __t4
syscall
li $s0, 0
sub $s1, $t4, $s0
bne $s1, $zero, _L27
j _L28
_L27:
li $s1, 1
addi $s2, $t2, 0
add $s3, $s1, $s2
addi $s4, $s3, 0
move $a0, $s4
li $v0, 11
syscall
j _L26
_L28:
li $s5, 0
li $s6, 1
sub $s7, $t4, $s5
beq $s7, $zero, _L35
move $a0, $s6
li $v0, 1
syscall
j _L36
_L35:
move $a0, $s5
li $v0, 1
syscall
_L36:
_L26:
la $s7, __t11
li $v0, 4
la $a0, __t11
syscall
move $sp, $s8
jr $ra

