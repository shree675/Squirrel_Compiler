.data
	abc__2:
		.float 1.1, 2.2, 3.3, 4.4

.text
.globl main

main:

move $s8, $sp

li $t0, 2
li $t1, 1
mult $t0, $t1
mflo $t1
li $t2, 4
mult $t1, $t2
mflo $t2
l.s $f3, abc__2($t2)
li.s $f4, 3.3
c.eq.s $t2, $t3
bc1t _L7
j _L8
_L7:
li $t3, 9
move $a0, $t3
li $v0, 1
syscall
j _L6
_L8:
li $t4, 2
li $t5, 1
mult $t4, $t5
mflo $t5
li $t6, 4
mult $t5, $t6
mflo $t6
l.s $f5, abc__2($t6)
li.s $f6, 4.4
c.eq.s $t6, $t7
bc1t _L11
j _L12
_L11:
li $t7, 10
move $a0, $t7
li $v0, 1
syscall
j _L6
_L12:
li $s0, 11
move $a0, $s0
li $v0, 1
syscall
_L6:
move $sp, $s8
jr $ra

