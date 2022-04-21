.data

.text
.globl main

main:

move $s8, $sp

li $t0, 98
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
li $t4, 98
sub $t5, $t1, $t4
bne $t5, $zero, _L9
li $t5, 50
sub $t6, $t3, $t5
bne $t6, $zero, _L15
li $t6, 2
addi $t7, $t6, 0
move $a0, $t7
li $v0, 1
syscall
j _L14
_L15:
li $s0, 4
addi $s1, $s0, 0
move $a0, $s1
li $v0, 1
syscall
j _L14
_L14:
j _L8
_L9:
li $s2, 97
sub $s3, $t1, $s2
bne $s3, $zero, _L26
li $s3, 1
addi $s4, $s3, 0
li $s5, 3
addi $s6, $s5, 0
add $s7, $s4, $s6
addi $t8, $s7, 0
move $a0, $t8
li $v0, 1
syscall
_L26:
li $t9, 12
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
move $a0, $t9
li $v0, 1
syscall
j _L8
_L8:
move $sp, $s8
jr $ra

