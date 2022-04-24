.data

__t1:
	.asciiz "\n"
__t2:
	.asciiz "\n"
__t3:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li.s $f3, 0.0
mov.s $f4, $f3
li.s $f5, 0.0
mov.s $f6, $f5
li.s $f7, 0.0
mov.s $f8, $f7
li.s $f9, 0.0
mov.s $f10, $f9
_L12:
li.s $f11, 2.0
c.lt.s $f6, $f11
bc1t _L13
j _L2
_L13:
li.s $f20, 0.0
mov.s $f4, $f20
_L22:
li.s $f21, 2.0
c.lt.s $f4, $f21
bc1t _L23
j _L18
_L23:
li.s $f22, 0.0
mov.s $f8, $f22
_L32:
li.s $f23, 10.0
c.lt.s $f8, $f23
bc1t _L33
j _L28
_L33:
li.s $f24, 0.0
mov.s $f10, $f24
_L42:
li.s $f25, 3.0
c.lt.s $f10, $f25
bc1t _L43
j _L38
_L43:
cvt.w.s $f1, $f10
mfc1 $t0, $f1
addi $t1, $t0, 0
move $a0, $t1
li $v0, 1
syscall
li.s $f26, 1.0
add.s $f27, $f10, $f26
mov.s $f10, $f27
j _L42
_L38:
la $t2, __t1
li $v0, 4
la $a0, __t1
syscall
li.s $f28, 1.0
add.s $f29, $f8, $f28
mov.s $f8, $f29
j _L32
_L28:
la $t3, __t2
li $v0, 4
la $a0, __t2
syscall
li.s $f30, 1.0
add.s $f31, $f4, $f30
mov.s $f4, $f31
j _L22
_L18:
la $t4, __t3
li $v0, 4
la $a0, __t3
syscall
addi $sp, $sp, -4
s.s $f6, 4($sp)
li.s $f6, 1.0
addi $sp, $sp, -4
s.s $f6, 4($sp)
addi $sp, $sp, -4
s.s $f6, 4($sp)
l.s $f6, 0($s8)
s.s $f6, -8($s8)
l.s $f6, -4($s8)
add.s $f6, $f6, $f6
s.s $f6, -8($s8)
mov.s $f6, $f6
j _L12
_L2:
move $sp, $s8
jr $ra

