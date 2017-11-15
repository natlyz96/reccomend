import csv
import math
import requests
filename = "data.csv"
user = 21;
rows = 41;
movies = list()
with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    users_list = list(reader)
    #print(len(users_list))
    row = users_list[user]
    i=1
    k=0
    sr_u=0
    films_list = list()
    while i < 31:
        if int(row[i].strip(" ")) == -1:
            ##смотрим, какие фильмы пользователь не оценил
            films_list.append(i)
        else:
            ##рассчитываем среднюю оценку для нашего пользователя
            k+=1
            sr_u+=int(row[i].strip(" "))
        i+=1
    sr_u = round(sr_u/k,2)
    #print (sr_u)
    ##рассчет метрики похожести
    i=1
    #v - номер пользователя, для которого ищем коэфф похожести с нашим пользователем
    #последней колонкой в список каждого пользователя добавляем его коэфф похожести с нужным юзером и среднюю оценку
    while i<41:
        if i!=user:
            v = users_list[i]
            sim = 0
            sim_u = 0
            sim_v = 0
            #сразу рассчитаем среднюю оценку для всех
            sr = 0
            count = 0
            j=1
            ##рассматриваем все фильмы
            while j<31:
                #если оценка любого пользоватея за этот фильм стоит
                if int(v[j].strip(" ")) != -1:
                    sr += int(v[j].strip(" "))
                    count+=1
                    #и оценка нашего пользователя стоит
                    if int(row[j].strip(" ")) != -1:
                        #то их произведение помещаем в сумму
                        sim += int(v[j].strip(" "))*int(row[j].strip(" "))
                        sim_u+=int(v[j].strip(" "))*int(v[j].strip(" "))
                        sim_v+=int(row[j].strip(" "))*int(row[j].strip(" "))
                #if i == 1:
                    #print(sim)
                j+=1
            #метрика похожести
            v.append(round(sim/math.sqrt(sim_u)/math.sqrt(sim_v), 3)),
            #средняя оценка
            v.append(round((sr/count),3))
         #   print(v[0]," ",v[31], " ", v[32])
        row.append(0)
        i+=1
    sim_list = list()
    i = 1
    k=1
    c=0
    #ищем 5 наиболее похожих пользователей
    while k<6:
        max = 0
        c = 0
        while (i<41):
            if i not in sim_list:
                v = users_list[i]
                if v[31]>max:
                    max = v[31]
                    c = i
            i += 1
        sim_list.append(c)
        k+=1
        i=1
        #print(c)
    i = 0
    j = 0
    cnt = len(films_list)
    for i in range(0,cnt):
        answer = 0
        numer = 0
        denom = 0
        for j in range(0,5):
            v= users_list[sim_list[j]]
            if int(v[films_list[i]].strip(" "))!=-1:
                numer+=v[31]*(int(v[films_list[i]].strip(" "))-v[32])
            #else:
             #   numer += v[31]
            denom +=math.fabs(v[31])
       # print(sr_u)
       # print (numer)
        #print(round(numer / denom, 2))
        answer = sr_u + round(numer/denom, 2)
        print("movie ",films_list[i],": ", answer)
        movies.append(round(answer,2))
    #вариант рекомендации фильма буду рассчитывать следующим образом
    #предполагается, что рекомендовать пользователю надо тот фильм, который он еще не смотрел
    #используя метрику похожести посмотрю, какие фильмы из films_list смотрели пятеро наиболее похожих пользователей в будние дни
    #рассчитаю среднюю оценку для каждого фильма по этим пяти пользователям и выберу фильм с наиболее высокой средней оценкой
    filename_c = "context.csv"
    with open(filename_c, "r", newline="") as file:
        reader = csv.reader(file)
        context_list = list(reader)
        i=0
        #проходимся по всем похожим пользоватеям и смотрим, кто поставил оценку интересующим нас фильмам в будний день
        max = 0
        number = 0
        for i in range(0,len(films_list)):
                sr = 0
                c = 0
                for j in range(0, 5):
                    v_c = context_list[sim_list[j]]
                    v = users_list[sim_list[j]]
                    if (v_c[films_list[i]].strip(" ")!="Sat")&(v_c[films_list[i]].strip(" ")!="Sun")&(v_c[films_list[i]].strip(" ")!="-"):
                        sr+=int(v[films_list[i]].strip(" "))
                        c+=1
                if c<2:
                    sr=0
                else:
                    sr = round(sr/c, 2)
                    if sr>max:
                        max=sr
                        number = films_list[i]
                #print(films_list[i], " ", sr)
        if (max>3):
            print("you can watch movie ", number)
        elif (max!=0):
            print("i can recommend you a movie, but you might not like it ", number)
        else:
            print("sorry, i cant find a movie for you")
reg = 'https://cit-home1.herokuapp.com/api/rs_homework_1'
jsargs = {
    "user": 21,
    "1":{
        "movie "+str(films_list[0]):movies[0],
        "movie "+str(films_list[1]):movies[1],
        "movie "+str(films_list[2]):movies[2],
        "movie "+str(films_list[3]):movies[3],
        "movie "+str(films_list[4]):movies[4]
    },
    "2":{
        "movie ": number
    }
}
head = {'content-type': 'application/json'}
#r = requests.post(reg, json=jsargs,headers=head)
#print(r.text)
