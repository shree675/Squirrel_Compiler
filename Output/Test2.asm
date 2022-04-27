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
sub $s0, $t7, $t3
ble $s0, $zero, _L25
j _L18
_L25:
move $a0, $t5
li $v0, 1
syscall
la $s0, __t4
li $v0, 4
la $a0, __t4
syscall
sub $s1, $t3, $t7
mult $t5, $s1
mflo $s2
div $s2, $t7
mflo $s3
addi $t5, $s3, 0
li $s4, 1
add $s5, $t7, $s4
addi $t7, $s5, 0
j _L24
_L18:
la $s6, __t10
li $v0, 4
la $a0, __t10
syscall
li $s7, 1
add $t8, $t3, $s7
addi $t3, $t8, 0
j _L12
_L2:
move $sp, $s8
jr $ra

