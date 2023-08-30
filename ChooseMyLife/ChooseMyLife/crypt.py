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
    shuffle_alphabet = alphabet
    print("SHUFFLE :",shuffle_alphabet)
    result_alphabet=create_resultdic(shuffle_alphabet)

    ls=[]
    for letter in data:
        ls.append(_position(letter,shuffle_alphabet))
    password_ls = []
    for i in range(0, len(ls)):
        password_ls.append(_position(password[i%len(password)],shuffle_alphabet))
    print("LS",ls)
    print("PASSWORD LS",password_ls)
    new_nb = []
    for i in range(0,len(ls)):
        new_nb.append(ls[i]+password_ls[i])
    print("NEW NB :",new_nb)
    result_nb = []
    for i in new_nb:
        if i>=len(shuffle_alphabet):
            result_nb.append(i-len(shuffle_alphabet))
        else:
            result_nb.append(i)
    print("RESULT NB",result_nb)
    result=""
    for i in result_nb:
        result += shuffle_alphabet[i]
    print("MESSAGE CRYPT :", result)
    result2 = ""
    for i in result:
        result2 += result_alphabet[i]
    return result2

def decrypt_data(data, password):
    alphabet = " azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é\"'()-è_çà=^$*ù!:;,~#{[]|}`\\@?./§%µ£¨+°0987654321ÀÈÙÌÒùìòôîûÔÎÛÊÂâêöïüëäÖÏÜËÄñõÑÕãÃ"
    shuffle_alphabet = _shuffler_alphabet(alphabet, password)
    print("SHUFFLE :",shuffle_alphabet)
    result_alphabet=create_reverse_resultdic(shuffle_alphabet)
    new_message=""
    for i in range(0,len(data),2):
        new_message += result_alphabet[data[i:i+2]]
    print("MESSAGE CRYPT :",new_message)
    result=""
    t=1
    ls=[]
    for letter in new_message:
        ls.append(_position(letter,shuffle_alphabet))
    password_ls = []
    for i in range(0, len(ls)):
        password_ls.append(_position(password[i%len(password)],shuffle_alphabet))
    print("LS",ls)
    print("PASSWORD LS",password_ls)
    new_nb = []
    for i in range(0,len(ls)):
        new_nb.append(ls[i]-password_ls[i])
    print("NEW NB :",new_nb)
    result_nb = []
    for i in new_nb:
        if i<0:
            result_nb.append(i+len(shuffle_alphabet))
        else:
            result_nb.append(i)
    print("RESULT NB",result_nb)
    result=""
    for i in result_nb:
        result += shuffle_alphabet[i]
    return result

"""
TEST BECAUSE OF MULTIPLE ERROR
"""

def position(letter, alphabet):
    t=0
    for i in alphabet:
        if i == letter:
            return t
        t+=1
    return 0

def shuffle(alphabet, password):
    result=""
    i=0
    for letter in alphabet:
        if position(password[i],alphabet)%2==0:
            result = result + letter
        else:
            result = letter + result
        i+=1
        if i >= len(password):
            i=0
    return result

def create_result_ls(password):
    alphabet = shuffle("ABCDEFGHIJKLMNOPQRSTUVWXYZ", password.upper())
    result=[]
    c=[-1,0]
    while c[1] < (len(alphabet)-1):
        c[0]= c[0] + 1
        if c[0] >= len(alphabet):
            c[0] = 0
            c[1] = c[1] + 1
        r = ''
        for i in c:
            r+=alphabet[i]
        result.append(r)
    return result
        

def crypt_v2(data, password):
    alphabet=" azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890&é\"'(-è_çà)=+~#{}[]|`\\^@^¨$*ù%!§:/;.,?"
    result_shape = create_result_ls(password)
    msg = []
    for i in data:
        msg.append(position(i, alphabet))
    msg_crypt=[]
    t=0
    for nb in msg:
        n2 = position(password[t], alphabet)
        msg_crypt.append(nb+n2)
        t+=1
        if t>= len(password):
            t=0
    result=""
    for nb in msg_crypt:
        result += result_shape[nb]
    return result

def decrypt_v2(data, password):
    alphabet=" azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890&é\"'(-è_çà)=+~#{}[]|`\\^@^¨$*ù%!§:/;.,?"
    result_shape = create_result_ls(password)
    msg = []
    for i in range(0,len(data),2):
        section=data[i:i+2]
        t=0
        for shape in result_shape:
            if shape == section:
                msg.append(t)
            t+=1
    msg_decrypt=[]
    t=0
    for nb in msg:
        n2 = position(password[t], alphabet)
        msg_decrypt.append(nb-n2)
        t+=1
        if t>= len(password):
            t=0
    result=""
    for i in msg_decrypt:
        result += alphabet[i]
    return result



m1 = crypt_v2("NEejsdJ7qSuoD7ICEIpKDuEEGCDEpIDs0ah9ztGGII8ty9eeFKDGECqEetGKIGHu","math")
print(m1)
print(decrypt_v2(m1, "math"))