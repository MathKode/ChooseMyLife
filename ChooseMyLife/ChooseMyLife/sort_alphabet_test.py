def _position(lettre, alphabet):
    t=0
    for i in alphabet:
        if i==lettre:
            return t
        t+=1
    return 0

def _compare_letter(l1,l2, alphabet):
    if l1 not in alphabet: l1=alphabet[-1]
    if l2 not in alphabet: l2=alphabet[-1]
    n1 = _position(l1, alphabet)
    n2 = _position(l2, alphabet)
    if n1 > n2:
        return 0
    elif n1 == n2:
        return 1
    else: #n2>n1
        return 2

def _compare_word(w1,w2,alphabet):
    t=0
    for l1 in w1:
        try:
            l2=w2[t]
        except:
            l2=alphabet[-1]
        comp = _compare_letter(l1,l2, alphabet)
        if comp == 0:
            return w1
        if comp == 2:
            return w2
        t+=1
    return w1

def sort_ls(mp_list):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    print("UNSORT MP",mp_list)
    result=[] # [ [site, username, password ] ]
    for mp in mp_list:
        w1 = str(mp[0]).lower()
        if w1 == '': w1='9'
        position = 0
        for mp_sort in result:
            w2 = str(mp_sort[0]).lower()
            if w2 == '': w2='9'
            winner = _compare_word(w1,w2,alphabet)
            if winner == w1:
                #This mean w1 is bigger than w2
                position+=1
        try:result.insert(position,mp)
        except:result.append(mp)
    return result

print(sort_ls([["Ok"],["Albert"],["Zèbre"],["Aragon"]]))