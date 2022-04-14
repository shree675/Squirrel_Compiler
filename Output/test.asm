.data
	arr__2:
		.word 0, 0, 0, 0



.text
.globl main

main:
li $t0, 0
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
_L13:
li $t4, 4
sub $t5, $t3, $t4
blt $t5, $zero, _L14
j _L11
_L14:
addi $t5, $zero, 1
mult $t3, $t5
mflo $t5
addi $t6, $zero, 4
mult $t5, $t6
mflo $t6
addi $t7, $t3, 0
sw $t7, arr__2($t6)
mult $t1, $t3
mflo $s0
addi $t1, $s0, 0
addi $s1, $zero, 1
mult $t3, $s1
mflo $s1
addi $s2, $zero, 4
mult $s1, $s2
mflo $s2
li $v0, 1
lw $a0, arr__2($s2)
syscall
addi $a0, $0, 0xA
addi $v0, $0, 0xB
syscall
li $s3, 1
add $s4, $t3, $s3
addi $t3, $s4, 0
j _L13
_L11:
li $v0, 1
la $a0, 0($t1)
syscall
addi $a0, $0, 0xA
addi $v0, $0, 0xB
syscall
jr $ra

