.data

__t3:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li.s $f10, 0.0
mov.s $f7, $f10
li.s $f27, 0.0
mov.s $f9, $f27
li.s $f28, 0.0
mov.s $f3, $f28
li.s $f21, 0.0
mov.s $f6, $f21
li $t6, 0
addi $sp, $sp, -4
sw $t6, 4($sp)
addi $t6, $t6, 0
_L18:
li.s $f24, 2.0
addi $sp, $sp, -4
s.s $f6, 4($sp)
c.lt.s $f9, $f24
bc1t _L19
j _L6
_L19:
li.s $f23, 0.0
mov.s $f7, $f23
_L26:
li.s $f11, 2.0
c.lt.s $f7, $f11
bc1t _L27
j _L22
_L27:
li.s $f8, 0.0
mov.s $f3, $f8
_L34:
addi $sp, $sp, -4
s.s $f7, 4($sp)
li.s $f7, 10.0
addi $sp, $sp, -4
s.s $f7, 4($sp)
c.lt.s $f3, $f7
bc1t _L35
j _L30
_L35:
li.s $f25, 0.0
mov.s $f6, $f25
_L42:
addi $sp, $sp, -4
s.s $f10, 4($sp)
li.s $f10, 3.0
c.lt.s $f6, $f10
bc1t _L43
j _L38
_L43:
li $t5, 1
addi $sp, $sp, -4
sw $t6, 4($sp)
add $t6, $t6, $t5
addi $t3, $t6, 0
move $a0, $t3
li $v0, 1
syscall
addi $sp, $sp, -4
sw $t5, 4($sp)
la $t5, __t3
li $v0, 4
la $a0, __t3
syscall
li.s $f5, 1.0
add.s $f20, $f6, $f5
mov.s $f6, $f20
j _L42
_L38:
addi $sp, $sp, -4
s.s $f25, 4($sp)
li.s $f25, 1.0
s.s $f7, -12($s8)
add.s $f7, $f3, $f25
mov.s $f3, $f7
j _L34
_L30:
addi $sp, $sp, -4
s.s $f10, 4($sp)
li.s $f10, 1.0
addi $sp, $sp, -4
s.s $f28, 4($sp)
l.s $f28, -8($s8)
add.s $f4, $f28, $f10
addi $sp, $sp, -4
s.s $f8, 4($sp)
mov.s $f8, $f4
j _L26
_L22:
li.s $f29, 1.0
addi $sp, $sp, -4
s.s $f11, 4($sp)
add.s $f11, $f9, $f29
mov.s $f9, $f11
j _L18
_L6:
li $t4, 3
sw $t3, -20($s8)
addi $t3, $t4, 0
addi $sp, $sp, -4
s.s $f9, 4($sp)
li.s $f9, 0.2
addi $sp, $sp, -4
s.s $f11, 4($sp)
mov.s $f11, $f9
move $sp, $s8
jr $ra

