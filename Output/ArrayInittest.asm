.data
	charArray__2:
		.byte 'a', 'b', 'c', 'd', 'e'
	floatArray__2:
		.float 1.1, 2.2, 3.3
	specialArrayChar__2:
		.byte 'a', 'b'

.text
.globl main

main:

move $s8, $sp

sw $t0, charArray__2($t0)
sw $t0, charArray__2($t0)
sw $t0, charArray__2($t0)
sw $t0, charArray__2($t0)
sw $t0, specialArrayChar__2($t0)
sw $t0, specialArrayChar__2($t0)
move $sp, $s8
jr $ra

