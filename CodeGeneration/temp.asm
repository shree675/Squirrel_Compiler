.data
.text

.globl main
main:
    li.s $f0, 13.2
    li.s $f1, 3.8
    div.s $f2, $f0, $f1

    li $v0, 2
    mov.d $f12, $f2
    syscall

    jr $ra