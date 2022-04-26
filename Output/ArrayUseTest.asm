.data
	arr__2:
		.word 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6
	arrx__2:
		.word 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6
	charArray__2:
		.byte 'a', 'b', 'c', 'd', 'e'
	floatArray__2:
		.float 1.1, 2.2, 3.3, 4.4, 5.5, 6.6

.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
li $t4, 0
addi $t5, $t4, 0
li $t6, 0
addi $t7, $t6, 0
li $s0, 12
mult $t1, $s0
mflo $s0
li $s1, 6
mult $t3, $s1
mflo $s1
add $s2, $s0, $s1
li $s3, 3
mult $t5, $s3
mflo $s3
add $s4, $s2, $s3
li $s5, 1
mult $t7, $s5
mflo $s5
add $s6, $s4, $s5
li $s7, 4
mult $s6, $s7
mflo $s7
li $t8, 10
addi $t9, $t8, 0
sw $t9, arr__2($s7)
addi $sp, $sp, -4
sw $s0, 4($sp)
sw $s0, 0($s8)
li $s0, 6
li $s0, 6
mult $t1, $s0
mflo $s0
addi $sp, $sp, -4
sw $s2, 4($sp)
sw $s2, -4($s8)
li $s2, 2
li $s2, 2
mult $t3, $s2
mflo $s2
addi $sp, $sp, -4
sw $s4, 4($sp)
add $s4, $s0, $s2
addi $sp, $sp, -4
sw $s6, 4($sp)
sw $s6, -12($s8)
li $s6, 1
li $s6, 1
mult $t5, $s6
mflo $s6
addi $sp, $sp, -4
sw $t8, 4($sp)
add $t8, $s4, $s6
addi $sp, $sp, -4
sw $s7, 4($sp)
sw $s7, -20($s8)
li $s7, 4
li $s7, 4
mult $t8, $s7
mflo $s7
addi $sp, $sp, -4
sw $s0, 4($sp)
li $s0, 12
addi $sp, $sp, -4
sw $s4, 4($sp)
addi $s4, $s0, 0
sw $s4, arrx__2($s7)
addi $sp, $sp, -4
sw $t8, 4($sp)
sw $t8, -32($s8)
li $t8, 1
li $t8, 1
mult $t1, $t8
mflo $t8
addi $sp, $sp, -4
sw $s0, 4($sp)
sw $s0, -36($s8)
li $s0, 1
li $s0, 1
mult $t8, $s0
mflo $s0
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 102
addi $sp, $sp, -4
sw $s0, 4($sp)
addi $s0, $s7, 0
addi $sp, $sp, -4
sw $s0, 4($sp)
lw $s0, -44($s8)
sw $s0, charArray__2($s0)
sw $s0, -44($s8)
li $s0, 0
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 0
addi $sp, $sp, -4
sw $t8, 4($sp)
li $t8, 18
addi $sp, $sp, -4
sw $t8, 4($sp)
addi $t8, $t8, 0
addi $sp, $sp, -4
sw $s4, 4($sp)
li $s4, 0
addi $sp, $sp, -4
sw $s4, 4($sp)
addi $s4, $s4, 0
_L35:
addi $sp, $sp, -4
sw $s4, 4($sp)
li $s4, 3
addi $sp, $sp, -4
sw $s4, 4($sp)
sub $s4, $s4, $s4
blt $s4, $zero, _L36
j _L33
_L36:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
_L42:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 2
addi $sp, $sp, -4
sw $t9, 4($sp)
sub $t9, $t9, $t9
blt $t9, $zero, _L43
j _L40
_L43:
sw $t9, -88($s8)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
_L49:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 2
addi $sp, $sp, -4
sw $t9, 4($sp)
sub $t9, $t9, $t9
blt $t9, $zero, _L50
j _L47
_L50:
sw $t9, -100($s8)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
_L56:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 3
addi $sp, $sp, -4
sw $t9, 4($sp)
sub $t9, $t9, $t9
blt $t9, $zero, _L57
j _L54
_L57:
sw $t9, -112($s8)
sw $t9, -112($s8)
li $t9, 12
li $t9, 12
mult $s4, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -120($s8)
li $t9, 6
li $t9, 6
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -124($s8)
lw $t9, -124($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -128($s8)
li $t9, 3
li $t9, 3
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -132($s8)
lw $t9, -132($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -136($s8)
li $t9, 1
li $t9, 1
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -140($s8)
lw $t9, -140($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -144($s8)
li $t9, 4
li $t9, 4
mult $t9, $t9
mflo $t9
lw $t9, arr__2($t9)
move $a0, $t9
li $v0, 1
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -152($s8)
lw $t9, -152($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L56
_L54:
sw $t9, -112($s8)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -160($s8)
lw $t9, -160($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L49
_L47:
sw $t9, -100($s8)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -168($s8)
lw $t9, -168($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L42
_L40:
sw $s4, -72($s8)
li $s4, 1
addi $sp, $sp, -4
sw $s4, 4($sp)
sw $s4, -176($s8)
lw $s4, -176($s8)
add $s4, $s4, $s4
addi $sp, $sp, -4
sw $s4, 4($sp)
addi $s4, $s4, 0
j _L35
_L33:
move $sp, $s8
jr $ra

