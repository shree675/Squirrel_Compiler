.data
.text

.globl main
main:
    li $t0, 'a'
    # li $t1, 'b'

    sub $t2, $zero, $t0
    
    li $v0, 1
    move $a0, $t2
    syscall
    
    jr $ra