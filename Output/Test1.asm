.data

__t0:
	.asciiz "Enter a number: "
__t2:
	.asciiz "The factorial of "
__t3:
	.asciiz " is "
__t10:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 0
la $t1, __t0
li $v0, 4
la $a0, __t0
syscall
li $v0, 5
syscall
move $t0, $v0
li $t2, 1
addi $t3, $t2, 0
la $t4, __t2
li $v0, 4
la $a0, __t2
syscall
move $a0, $t0
li $v0, 1
syscall
la $t5, __t3
li $v0, 4
la $a0, __t3
syscall
li $t6, 0
<<<<<<< HEAD
sub $t4, $t0, $t6
beq $t4, $zero, _L21
=======
sub $t7, $t0, $t6
beq $t7, $zero, _L21
>>>>>>> final
j _L22
_L21:
li $t7, 1
move $a0, $t7
li $v0, 1
syscall
j _L20
_L22:
<<<<<<< HEAD
li $t8, 1
addi $t9, $t8, 0
_L32:
sub $t4, $t9, $t0
ble $t4, $zero, _L33
j _L30
_L33:
mult $t3, $t9
mflo $s0
addi $t3, $s0, 0
li $s1, 1
add $s2, $t9, $s1
addi $t9, $s2, 0
=======
li $s0, 1
addi $s1, $s0, 0
_L32:
sub $s2, $s1, $t0
ble $s2, $zero, _L33
j _L30
_L33:
mult $t3, $s1
mflo $s2
addi $t3, $s2, 0
li $s3, 1
add $s4, $s1, $s3
addi $s1, $s4, 0
>>>>>>> final
j _L32
_L30:
move $a0, $t3
li $v0, 1
syscall
_L20:
<<<<<<< HEAD
la $s3, __t10
=======
la $s5, __t10
>>>>>>> final
li $v0, 4
la $a0, __t10
syscall
move $sp, $s8
jr $ra

