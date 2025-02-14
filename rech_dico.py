def reach_dico (num, liste) :
    if len(liste) != 0 :
        left_i = 0
        right_i = len(liste) - 1
        while left_i <= right_i :
            middle = (left_i + right_i) // 2
            elt_middle = liste[middle]
            if elt_middle == num :
                return middle
            elif elt_middle > num :
                right_i = middle -1
            elif elt_middle < num :
                left_i = middle + 1
        return -1

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
num = 5
print (reach_dico(num, liste))
