.data

.text
.globl main

main:

move $s8, $sp

li $t0, 2
addi $t1, $t0, 0
li $t2, 3
addi $t3, $t2, 0
add $t4, $t1, $t3
addi $t5, $t4, 0
li $t6, 2
mult $t3, $t6
mflo $t7
sub $s0, $t1, $t7
addi $s1, $s0, 0
mult $t1, $t3
mflo $s2
addi $s3, $s2, 0
div $t1, $t3
mflo $s4
addi $s5, $s4, 0
div $t1, $t3
mfhi $s6
addi $s7, $s6, 0
li $v0, 1
move $a0, $t1
syscall
li $v0, 1
move $a0, $t3
syscall
li $v0, 1
move $a0, $t5
syscall
li $v0, 1
move $a0, $s1
syscall
li $v0, 1
move $a0, $s3
syscall
li $v0, 1
move $a0, $s5
syscall
li $v0, 1
move $a0, $s7
syscall
move $sp, $s8
jr $ra

