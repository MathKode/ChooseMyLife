from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.conf import settings
import shutil
import os


def homepage_render(request):
    if request.method == "POST":
        password = request.POST["password"]
        if password!="":
            page = redirect(desktop_render)
            page.set_cookie("PASSWORD",password,max_age=600)
            return page    
    page = render(request, "homepage.html")
    return page

def profile_render(request, hash_id):
    try:
        password=request.COOKIES['PASSWORD']
    except:
        password=""
    if password == "":
        page = redirect(homepage_render)
        return page
    if request.method == "GET":
        #Verif si c'est pour la suppression d'un mp
        try:
            print("here")
            usr = request.GET['remove_username']
            print(usr)
            st = request.GET['remove_site']
            print("REMOVE",st,usr)
            supp_password(hash_id,password,st,usr)
            print("Remove success")
        except: pass
    if request.method == "POST":
        try:
            for i in request.POST:
                print(i, request.POST[i])
            site = request.POST['site']
            username = request.POST['username']
            site_mp = request.POST['password_site']
            old_site = request.POST['old_site']
            old_username = request.POST['old_username']
            if old_site=='' or old_username=='':
                print("Nouveau MP")
            else:
                #Modif on supp l'ancien
                supp_password(hash_id,password,old_site,old_username)
            create_password(hash_id,password,site,username,site_mp)
        except:pass
    info = read_ID(password)
    first_name = "Profile"
    last_name = "Password"
    birthday = ""
    sex="M/F"
    pic="../media/p3.jpg"
    for i in info:
        if i[0] == hash_id:
            if i[1] != "": first_name=i[1]
            if i[2] != "": last_name=i[2]
            if i[3] != "": birthday=i[3]
            if i[6] != "": sex=i[6]
            if i[5] != "": pic="../media/" + i[5]
    mp_list = read_password(hash_id, password)
    print("MP LIST:",mp_list)
    context={"hash_id":hash_id, "first_name":first_name, "last_name":last_name, "mp_list":mp_list, "birthday":birthday, "sex":sex, "pic":pic}
    page = render(request, "profile.html", context)
    return page

def desktop_render(request):
    try:
        password=request.COOKIES['PASSWORD']
    except:
        password=""
    if password == "":
        page = redirect(homepage_render)
        return page
    try:
        hash_id = request.GET["remove"]
        supp_ID(hash_id, password)
    except:pass
    #create_ID("jhdqkjhkjqzhdkjqzhdkjqzhd","jijdiqjdijqzjdiqzd","ijijijij",'ijijidqjildjlqijdlqizjdlqizjdlqijdzlqizjdlqzdij',"../media/face1.jpeg","F",password)
    #create_ID("Jules","KREDER BAIL","11/03/2006","Thionville","","M",password)
    people = read_ID(password)
    print("PEOPLE :", people)
    context={"people": people}
    page = render(request, "deskboard.html", context)
    return page

def create_people_render(request):
    try:
        password=request.COOKIES['PASSWORD']
    except:
        password=""
    if password == "":
        page = redirect(homepage_render)
        return page
    if request.method == "POST":
        try:first_name = request.POST["fname"]
        except:first_name = ""
        try:last_name = request.POST["lname"]
        except:last_name = ""
        try:sex = request.POST["sex"]
        except:sex = ""
        try:birthday = request.POST["birthday"]
        except:birthday = ""
        try:city = request.POST["city"]
        except:city = ""
        try:picture = request.POST["picture"]
        except:picture = ""
        picture_name = create_ID(first_name,last_name,birthday,city,sex,password)
        try:
            picture=request.FILES["picture"]
            path = default_storage.save(f"{picture_name}", ContentFile(picture.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        except: pass
        
        page = redirect(desktop_render)
        return page  
    else:
        page = render(request, "newpeople.html")
        return page

def modify_profile_render(request, hash_id):
    try:
        password=request.COOKIES['PASSWORD']
    except:
        password=""
    if password == "":
        page = redirect(homepage_render)
        return page
    all_info = read_ID(password)
    info=['','','','','','','']
    for i in all_info:
        if str(i[0]) == hash_id:
            info = i
    print(info)

    if request.method == "POST":
        try:first_name = request.POST["fname"]
        except:first_name = ""
        try:last_name = request.POST["lname"]
        except:last_name = ""
        try:sex = request.POST["sex"]
        except:sex = ""
        try:birthday = request.POST["birthday"]
        except:birthday = ""
        try:city = request.POST["city"]
        except:city = ""
        try:picture=request.FILES["picture"]
        except: picture=""
        picture_name = create_ID(first_name, last_name, birthday, city, sex, password)
        new_hashid = ""
        all_info = read_ID(password)
        new_info=['','','','','','','']
        for i in all_info:
            if str(i[5]) == picture_name:
                new_info = i
                new_hashid = i[0]
        print("NEW INFO", new_info)
        print("NEW HASHID", new_hashid)

        if picture != "":
            try: 
                path = default_storage.save(f"{picture_name}", ContentFile(picture.read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            except: pass
        else:
            #Garde la même image
            path = settings.MEDIA_ROOT
            print(path)
            src=path + "/" + f"{hash_id}.jpeg"
            dst=path + "/" + picture_name
            print("COPY IMAGE :", src, dst)
            try:
                shutil.copy(src, dst)
            except:
                print("ERROR #182")
        #Copie des mots de passe
        file=open(f"{hash_id}.txt","r")
        c=file.read()
        file.close()
        file=open(f"{new_hashid}.txt","w")
        file.write(c)
        file.close()

        #Suppression de l'ancien
        supp_ID(hash_id, password)
        page = redirect(desktop_render)
        return page


    context = {"hash_id":hash_id,
               "first_name": info[1],
               "last_name": info[2],
               "birthday": info[3],
               "city" : info[4],
               "picture" : info[5],
               "sex" : info[6]}
    page = render(request, "modifyprofile.html",context)
    return page

def ID_render(request):
    page = render(request, "id.html")
    return page

def Tools_render(request):
    page = render(request, "tools.html")
    return page

def export_render(request):
    try:
        password=request.COOKIES['PASSWORD']
    except:
        password=""
    if password == "":
        page = redirect(homepage_render)
        return page
    c=["--NAME","ID.txt"]
    try:
        file = open("ID.txt","r")
        for i in file.read().split("\n"):
            c.append(i)
        file.close()
    except:
        pass
    c.append("--END")
    info = read_ID(password)
    for person in info:
        hash_id = person[0]
        c.append("--NAME")
        c.append(f"{hash_id}.txt")
        try:
            file = open(f"{hash_id}.txt","r")
            for i in file.read().split("\n"):
                c.append(i)
            file.close()
        except:
            pass
        c.append("--END")
    while '' in c:
        c.remove('')
    
    page = HttpResponse("<body style=\"word-wrap: break-word; white-space: pre-wrap;\">\n" + "\n".join(c) + "</body>")
    return page
        
def import_render(request):
    if request.method == "POST":
        try: data = request.POST["data"]
        except: data = None
        if data != None:
            _reader = False
            c=[]
            t = []
            for line in data.split('\n'):
                print(line)
                if str(line)[0:4] == "--NAME"[0:4]:
                    print("HERE")
                    _reader=True
                    t = []
                elif str(line)[0:3] == "--END"[0:3]:
                    _reader=False
                    if t != []:
                        c.append(t)
                elif _reader:
                    t.append(line[:-1])
            for line in c:
                try:
                    file = open(line[0], "r")
                    content = file.read().split('\n')
                    file.close()
                except:
                    content=[]
                for i in line[1:]:
                    content.append(i)
                file = open(line[0], "w")
                file.write("\n".join(content))
                file.close()
            page = redirect(desktop_render)
            return page
    page = render(request, "import.html")
    return page


def create_ID(first_name,last_name,birthday,city,sex,password):
    from random import randint
    from datetime import datetime

    try:
        file=open("ID.txt","r")
        c=file.read().split("\n")
        file.close()

    except:
        c=[]
    hash_id = f"{str(my_hash(str(first_name+last_name+str(randint(1000000,10000000))+str(datetime.timestamp(datetime.now())))))}"
    picture = f"{hash_id}.jpeg"
    info=[hash_id,first_name,last_name,birthday,city,picture,sex]
    print("NEW MEMBER INFO",info)
    info_crypt=[]
    for i in info:
        info_crypt.append(crypt_data(i,password))
    info_crypt2=";info;".join(info_crypt)
    print("NEW MEMBER INFO CRYPT :",info_crypt)
    c.append(crypt_data(info_crypt2,password))
    file = open("ID.txt","w")
    file.write("\n".join(c))
    file.close()
    file = open(f"{hash_id}.txt","w")
    file.close()
    return picture

def supp_ID(hash_id, password):
    try:
        c=read_ID(password)
        result=[]
        print("BEFORE SUPP : ",c)
        for i in c:
            #Ne l'ajoute pas si le hash correspond à la personne qu'on veut kick
            print(i)
            if str(i[0]) != str(hash_id):
                result.append(i)
        print("AFTER SUPP : ",result,"\n\n\n")
        crypt1=[]
        for i in result:
            r=[]
            for j in i:
                r.append(crypt_data(j,password))
            crypt1.append(";info;".join(r))
        crypt2=[]
        for i in crypt1:
            crypt2.append(crypt_data(i,password))

        file = open("ID.txt","w")
        file.write("\n".join(crypt2))
        file.close()
        os.remove(f"{hash_id}.txt")
        try: os.remove(f"ChooseMyLife/media/{hash_id}.jpeg")
        except: pass
        return True
    except:
        return False

def read_ID(password):
    try:
        file=open("ID.txt","r")
        c=file.read().split("\n")
        file.close()
    except:
        return []
    print("READ CONTENT ID.TXT :",c)
    decrypt1=[]
    for i in c:
        decrypt1.append(decrypt_data(i,password))
    decrypt2=[]
    for i in decrypt1:
        r=[]
        for j in i.split(";info;"):
            r.append(decrypt_data(j,password))
        if len(r) == 7:
            decrypt2.append(r)
    return decrypt2


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

def crypt_data(data, password):
    return crypt_v2(data, password)

def decrypt_data(data, password):
    return decrypt_v2(data, password)


def my_hash(txt):
    def txt_to_nb(txt):
        alphabet=" azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN&é\"'()è_çà=^$*ù!:;,~#{[]|}`\\@?./§%µ£¨+°0987654321ÀÈÙÌÒùìòôîûÔÎÛÊÂâêöïüëäÖÏÜËÄñõÑÕãÃ"
        result=[]
        for lettre in txt:
            t=0
            r=0
            for i in alphabet:
                if i == lettre:
                    r=t
                t+=1
            result.append(r)
        return result
  
    def nb_to_txt(ls_nb):
        alphabet= "azertyuiopqsdfghjklmwxcvbn1234567890ABCDEFGHIJKLMNOPQRSTUV"
        result=""
        for nb in ls_nb:
            result+=alphabet[nb%len(alphabet)]
        return result
  
    t=0
    while len(txt)%128!=0 or len(txt)==0:
            txt += "azerty1234"[t%10]
            t+=1
  
    r_buff = []
    for i in range(0,len(txt),64):
        buff=txt[i:(i+64)]
        #print(buff, len(buff))
        inverse_buff=buff[::-1]
        nb_ls1 = txt_to_nb(buff)
        nb_ls2 = txt_to_nb(inverse_buff)
    
        result_nb = []
        for i in range(0,64):
            n1 = nb_ls1[i]
            n2 = nb_ls2[i]
            n3 = n1 | n2
            n4 = n3 & n1
            n5 = n1 ^ n2
            n6 = n3 ^ n5
            n7 = n4 ^ n6
            result_nb.append(n7)
        r_buff.append(result_nb)
 
    final_buff=[]
    for i in r_buff:
        t=0
        for j in i:
            try:
                final_buff[t]+=j
            except:
                final_buff.append(j)
            t+=1
    txt = nb_to_txt(final_buff)
    print("NEW HASH :",txt)
    return txt


def create_password(hash_id, password, site_name, username, site_password):
    print("Here to create password")
    try:
        file = open(f"{hash_id}.txt","r")
        c = file.read().split("\n")
        file.close()
    except:
        c=[]
    i0 = crypt_data(site_name, password)
    i1 = crypt_data(username, password)
    i2 = crypt_data(site_password, password)
    i3 = ";site;".join([i0, i1,i2])
    print("I3 :",i3)
    i4 = crypt_data(i3,password)
    c.append(i4)
    print("Crypt data :",c)
    file = open(f"{hash_id}.txt", "w")
    file.write("\n".join(c))
    file.close()

def read_password(hash_id, password):
    try:
        file = open(f"{hash_id}.txt","r")
        c = file.read().split("\n")
        file.close()
    except:
        c=[]
    result = []
    for site in c:
        try:
            i4_ = decrypt_data(site, password)
            i3_ = i4_.split(";site;")
            i2_ = decrypt_data(i3_[2], password)
            i1_ = decrypt_data(i3_[1], password)
            i0_ = decrypt_data(i3_[0], password)
            result.append([i0_,i1_,i2_])
        except: pass
    result2 = sort_password_alphabetic(result)
    return result2

def supp_password(hash_id, password, site_name, username):
    c = read_password(hash_id, password)
    new_list = []
    for site in c:
        # [site, username, password]
        if site[0] == site_name and site[1] == username:
            print("Delete", site)
        else:
            new_list.append(site)
    
    try: os.remove(f"{hash_id}.txt")
    except:pass 

    for i in new_list:
        create_password(hash_id, password, i[0], i[1], i[2])
    return True

def _compare_letter(l1,l2, alphabet):
    if l1 not in alphabet: l1=alphabet[-1]
    if l2 not in alphabet: l2=alphabet[-1]
    n1 = position(l1, alphabet)
    n2 = position(l2, alphabet)
    if n1 > n2:
        return 0
    elif n1 == n2:
        return 1
    else: #n2>n1
        return 2

def _compare_word(w1,w2,alphabet):
    #print("WORD COMPARE :",w1,w2)
    t=0
    for l1 in w1:
        try:
            l2=w2[t]
        except:
            l2=alphabet[0]
        comp = _compare_letter(l1,l2, alphabet)
        if comp == 0:
            #print("WIN",w1)
            return w1
        if comp == 2:
            #print("WIN",w2)
            return w2
        t+=1
    if len(w1)<len(w2):
        return w2
    else:
        return w1

def sort_password_alphabetic(mp_list):
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
            
