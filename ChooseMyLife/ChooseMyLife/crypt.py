def _position(lettre, alphabet):
    t=0
    for i in alphabet:
        if i==lettre:
            return t
        t+=1
    return 0

def _shuffler_alphabet(alphabet, password):
    shuffle_alphabet=""
    t=0
    for l in alphabet:
        if _position(password[t%len(password)],alphabet)%2==0:
            shuffle_alphabet = l + shuffle_alphabet
        else:
            shuffle_alphabet = shuffle_alphabet + l
        t+=1
    return shuffle_alphabet

def create_resultdic(alphabet):
    result={}
    result_aplhabet="AZERTYUIOPQSDFGHJKLMWXCVBN"
    c = [0, 0]
    for i in alphabet:
        c[0] = c[0] + 1
        if c[0] >= len(result_aplhabet):
            c[0] = 0
            c[1] = c[1] + 1
        combinaison = result_aplhabet[c[0]] + result_aplhabet[c[1]]
        result[i]=combinaison
    #print(result)
    return result
def create_reverse_resultdic(alphabet):
    dic = create_resultdic(alphabet) #INVERSE KEY <-> VALUE
    new_dic = {} # 'AK': '('
    for key in dic:
        new_dic[dic[key]] = key
    #print(new_dic)
    return new_dic

def crypt_data(data, password):
    alphabet = " azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é\"'()-è_çà=^$*ù!:;,~#{[]|}`\\@?./§%µ£¨+°0987654321ÀÈÙÌÒùìòôîûÔÎÛÊÂâêöïüëäÖÏÜËÄñõÑÕãÃ"
    shuffle_alphabet = _shuffler_alphabet(alphabet, password)
    result_alphabet=create_resultdic(shuffle_alphabet)
    result=""
    for i in range(0,len(data)):
        nb=(_position(data[i],shuffle_alphabet) + _position(password[i%len(password)],shuffle_alphabet))%len(shuffle_alphabet)
        letter = shuffle_alphabet[nb]
        new_letter = result_alphabet[letter]
        result+=new_letter
    return result

def decrypt_data(data, password):
    alphabet = " azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é\"'()-è_çà=^$*ù!:;,~#{[]|}`\\@?./§%µ£¨+°0987654321ÀÈÙÌÒùìòôîûÔÎÛÊÂâêöïüëäÖÏÜËÄñõÑÕãÃ"
    shuffle_alphabet = _shuffler_alphabet(alphabet, password)
    result_alphabet=create_reverse_resultdic(shuffle_alphabet)
    new_message=""
    for i in range(0,len(data),2):
        new_message += result_alphabet[data[i:i+2]]
    #print(new_message)
    result=""
    for i in range(0,len(new_message)):
        nb=(_position(new_message[i],shuffle_alphabet) - _position(password[i%len(password)],shuffle_alphabet))
        if nb<0:
            nb+=len(shuffle_alphabet)
        result+=shuffle_alphabet[nb]
    return result

m1 = crypt_data("Getl5keIaGt23DGFAbcFottEGEIjtFfetntztFGFEuu0uztGGKI89EIeeFGFGDIq","math")
print(m1)
print(decrypt_data(m1,"math"))