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
sw $t0, 4($sp)
sw $t0, 0($s8)
li $t0, 6
li $t0, 6
mult $t1, $t0
mflo $t0
addi $sp, $sp, -4
sw $t2, 4($sp)
sw $t2, -4($s8)
li $t2, 2
li $t2, 2
mult $t3, $t2
mflo $t2
addi $sp, $sp, -4
sw $t4, 4($sp)
add $t4, $t0, $t2
addi $sp, $sp, -4
sw $t6, 4($sp)
sw $t6, -12($s8)
li $t6, 1
li $t6, 1
mult $t5, $t6
mflo $t6
addi $sp, $sp, -4
sw $s1, 4($sp)
add $s1, $t4, $t6
addi $sp, $sp, -4
sw $s3, 4($sp)
sw $s3, -20($s8)
li $s3, 4
li $s3, 4
mult $s1, $s3
mflo $s3
addi $sp, $sp, -4
sw $s5, 4($sp)
li $s5, 12
addi $sp, $sp, -4
sw $s7, 4($sp)
addi $s7, $s5, 0
sw $s7, arrx__2($s3)
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -32($s8)
li $t9, 1
li $t9, 1
mult $t1, $t9
mflo $t9
addi $sp, $sp, -4
sw $t2, 4($sp)
sw $t2, -36($s8)
li $t2, 1
li $t2, 1
mult $t9, $t2
mflo $t2
addi $sp, $sp, -4
sw $t6, 4($sp)
li $t6, 102
addi $sp, $sp, -4
sw $s3, 4($sp)
addi $s3, $t6, 0
sw $s3, charArray__2($t2)
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 0
addi $sp, $sp, -4
sw $t6, 4($sp)
li $t6, 18
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t6, 0
addi $sp, $sp, -4
sw $t6, 4($sp)
li $t6, 0
addi $sp, $sp, -4
sw $t6, 4($sp)
addi $t6, $t6, 0
_L35:
addi $sp, $sp, -4
sw $t6, 4($sp)
li $t6, 3
addi $sp, $sp, -4
sw $t6, 4($sp)
lw $t6, -72($s8)
sw $t6, -72($s8)
sub $t6, $t6, $t6
blt $t6, $zero, _L36
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
lw $t9, -88($s8)
sw $t9, -88($s8)
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
lw $t9, -100($s8)
sw $t9, -100($s8)
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
lw $t9, -112($s8)
sw $t9, -112($s8)
sub $t9, $t9, $t9
blt $t9, $zero, _L57
j _L54
_L57:
sw $t9, -112($s8)
sw $t9, -112($s8)
li $t9, 12
li $t9, 12
mult $t6, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -120($s8)
lw $t9, -88($s8)
sw $t9, -88($s8)
li $t9, 6
li $t9, 6
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -124($s8)
lw $t9, -120($s8)
sw $t9, -120($s8)
lw $t9, -124($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -128($s8)
lw $t9, -100($s8)
sw $t9, -100($s8)
li $t9, 3
li $t9, 3
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -132($s8)
lw $t9, -128($s8)
sw $t9, -128($s8)
lw $t9, -132($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -136($s8)
lw $t9, -112($s8)
sw $t9, -112($s8)
li $t9, 1
li $t9, 1
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -140($s8)
lw $t9, -136($s8)
sw $t9, -136($s8)
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
lw $t9, -112($s8)
sw $t9, -112($s8)
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
lw $t9, -100($s8)
sw $t9, -100($s8)
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
lw $t9, -88($s8)
sw $t9, -88($s8)
lw $t9, -168($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L42
_L40:
sw $t6, -72($s8)
li $t6, 1
addi $sp, $sp, -4
sw $t6, 4($sp)
sw $t6, -176($s8)
lw $t6, -72($s8)
sw $t6, -72($s8)
lw $t6, -176($s8)
add $t6, $t6, $t6
addi $sp, $sp, -4
sw $t6, 4($sp)
addi $t6, $t6, 0
j _L35
_L33:
move $sp, $s8
jr $ra

