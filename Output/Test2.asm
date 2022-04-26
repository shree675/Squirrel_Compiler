.data

__t0:
	.asciiz "Enter a number: "
__t4:
	.asciiz " "
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
_L12:
sub $t4, $t3, $t0
ble $t4, $zero, _L13
j _L2
_L13:
li $t4, 1
addi $t5, $t4, 0
li $t6, 1
addi $t7, $t6, 0
_L24:
sub $t4, $t7, $t3
ble $t4, $zero, _L25
j _L18
_L25:
move $a0, $t5
li $v0, 1
syscall
la $t8, __t4
li $v0, 4
la $a0, __t4
syscall
sub $t9, $t3, $t7
mult $t5, $t9
mflo $s0
div $s0, $t7
mflo $s1
addi $t5, $s1, 0
li $s2, 1
add $s3, $t7, $s2
addi $t7, $s3, 0
j _L24
_L18:
la $s4, __t10
li $v0, 4
la $a0, __t10
syscall
li $s5, 1
add $s6, $t3, $s5
addi $t3, $s6, 0
j _L12
_L2:
move $sp, $s8
jr $ra

