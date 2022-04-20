.data

.text
.globl main

li $t0, 4
addi $t1, $t0, 0
li.s $f3, 1.2
mov.s $f4, $f3
li $t0, 4
addi $t1, $t0, 0
li.s $f3, 1.2
mov.s $f4, $f3
main:

move $s8, $sp

li $t0, 0
li $t1, 20
move $a0, $t1
li $v0, 1
syscall
sub $t2, $t2, $t1
bne $t2, $zero, _L7
li.s $f3, 8.4
mov.s $f4, $f3
j _L6
_L7:
li $t2, 4
move $a0, $t2
li $v0, 1
syscall
sub $t3, $t3, $t2
bne $t3, $zero, _L12
li $t3, 82
addi $t0, $t3, 0
lw $t1, 0($t0)
li $v0, 1
syscall
j _L6
_L12:
li $t4, 0
j _L6
_L6:
move $sp, $s8
jr $ra

