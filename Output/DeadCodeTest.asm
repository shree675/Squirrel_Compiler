.data

.text
.globl main

foo:
move $s8, $sp

addi $t0, $a0, 0
li $t1, 8
move $a0, $t1
li $v0, 1
syscall
li $t2, 3
move $sp, $s8
move $v0, $t2
jr $ra
jr $ra
li $t3, 2
move $a0, $t3
li $v0, 1
syscall
move $sp, $s8
move $v0, $t4
jr $ra
jr $ra
main:

move $s8, $sp

li $t0, 4

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t0
jal foo
move $t1, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
mtc1 $t1, $f1
cvt.s.w $f3, $f1
mov.s $f12, $f3
li $v0, 2
syscall
move $sp, $s8
jr $ra

