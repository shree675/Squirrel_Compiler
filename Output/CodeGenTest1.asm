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
move $a0, $t1
li $v0, 1
syscall
move $a0, $t3
li $v0, 1
syscall
move $a0, $t5
li $v0, 1
syscall
move $a0, $s1
li $v0, 1
syscall
move $a0, $s3
li $v0, 1
syscall
move $a0, $s5
li $v0, 1
syscall
move $a0, $s7
li $v0, 1
syscall
move $sp, $s8
jr $ra

