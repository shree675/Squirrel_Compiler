.data
	cc__5:
		.byte 'a', 'b', 'c'

.text
.globl main

<<<<<<< HEAD
pp:
move $s8, $sp

addi $t0, $a0, 0
addi $t1, $a1, 0
addi $t2, $a2, 0
move $a0, $t0
li $v0, 11
syscall
move $a0, $t1
li $v0, 11
syscall
move $a0, $t2
li $v0, 11
syscall
move $sp, $s8
jr $ra
main:

move $s8, $sp

li $t0, 0
li $t1, 1
mult $t0, $t1
mflo $t1
li $t2, 1
mult $t1, $t2
mflo $t2
lw $t2, cc__5($t2)
li $t3, 1
li $t4, 1
mult $t3, $t4
mflo $t4
li $t5, 1
mult $t4, $t5
mflo $t5
lw $t5, cc__5($t5)
li $t6, 2
li $t7, 1
mult $t6, $t7
mflo $t7
li $s0, 1
mult $t7, $s0
mflo $s0
lw $s0, cc__5($s0)
=======
fun2:
move $s8, $sp

addi $t0, $a0, 0
move $a0, $t0
li $v0, 1
syscall
li $t1, 0
sub $t2, $t0, $t1
beq $t2, $zero, _L13
j _L12
_L13:
move $sp, $s8
jr $ra
_L12:
li $t2, 1
sub $t3, $t0, $t2
>>>>>>> 6cf31541f72570c341fa57b9778dd8fdbbb9bbc8

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
sw $t2, 4($s8)
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $sp, $sp, -4
<<<<<<< HEAD
sw $t4, 4($sp)
sw $t5, 4($s8)
=======
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t3
jal fun2
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
move $sp, $s8
jr $ra
main:

move $s8, $sp

li $t0, 10
addi $t1, $t0, 0

# -------------------------------- 
>>>>>>> 6cf31541f72570c341fa57b9778dd8fdbbb9bbc8
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
<<<<<<< HEAD
sw $t7, 4($sp)
sw $s0, 4($s8)
=======
sw $t1, 4($sp)
>>>>>>> 6cf31541f72570c341fa57b9778dd8fdbbb9bbc8
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
<<<<<<< HEAD
move $a2, $s0
move $a1, $t5
move $a0, $t2
jal pp
=======
move $a0, $t1
jal fun2
>>>>>>> 6cf31541f72570c341fa57b9778dd8fdbbb9bbc8
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
<<<<<<< HEAD
lw $t2, 4($s8)
lw $t3, -8($s8)
lw $t4, -12($s8)
lw $t5, 4($s8)
lw $t6, -16($s8)
lw $t7, -20($s8)
lw $s0, 4($s8)
=======
>>>>>>> 6cf31541f72570c341fa57b9778dd8fdbbb9bbc8
move $sp, $s8
jr $ra

