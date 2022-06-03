from email import message
from logging import debug
from os import read
from flask.wrappers import Request
from app import app, db
from flask import Response, flash, got_request_exception, redirect, render_template, make_response, url_for
from bson import json_util, ObjectId
from flask import request
import requests
import flask
import pandas
import openpyxl
import json
import numpy as np
import math
import matplotlib.pyplot as plt
import math
from mnk import main
from models import *
import os
from csv import reader
from datetime import datetime
from csv_parser import *
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """ Функция проверки расширения файла """
    # расширения файлов, которые разрешено загружать
    ALLOWED_EXTENSIONS = {'xls', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def multiplication(x,y):
    # поэлементное произведение списков
    mult = []
    for i in range(len(x)):
        mult.append(x[i] * y[i])
    return mult


def sum(k):
    # функция суммы элементов списка
    sum = 0
    r = len(k)-1
    for i in range(len(k)-1):
        sum += k[i]
    return sum


def vable(x,a,b):
    # формула функции распределения Вейбулла
    return 1 - math.exp(-(a*x+b))


def quantile(y,a,b):
    #считаем квантиль х по известному y
    return (- math.log(1-y) - b) / a


def res_y(x,coef):
        return coef[0] * (x**2) + coef[1] * x + coef[2]



def MNK_V(x, y, n):
    # функция вычисления коэф-тов методом МНК для распределения Вейбулла
    # вычисляем а по формуле 
    # a = (( - sum(yi)*sum(xi)/n) + sum(xi*yi)) / (sum(xi^2)-sum^2(xi)/n)
    a = (- sum(y)*sum(x)/n + sum(multiplication(x,y))) / ( sum(multiplication(x,x)) - (sum(x)*sum(x))/n)

    # b = (sum(yi) - a * sum(xi)) / n
    b = (sum(y) - a*sum(x)) / n

    result = [a,b]
    return result




    


@app.route('/test', methods=['POST'])
def test():
    # получаем данные от клиента
    j = request.get_json()
    print(j)
    print(type(j))
    # j - номер полета
    #j_list = j['j']
    j_value = j['j']
    j_list = [i for i in range(1,int(j_value))]
    # x - интересующий параметр
    x_list = j['x']
    print('x_list is ', x_list)

    print(len(j_list))

    # вытаскиваем данные о полетах из бд
    data = db.info.find()
    print('data is',data)
    data = json.loads(json_util.dumps(data))
    data = dict(data[0])
    #print(data)
    print()

    #-----------------------------------------------------------------------------
    data_inf = {}
    # выбираем  информацию  только о нужных полетах из j_list, который отправил нам клиент
    for i in j_list:
        print('печатаем номера полетов которые ввел клиент')
        print("i is", i)
        clean_data = data['data_maga'][i+1]
        data_inf[i] = clean_data
    print('нужные данные из бд',data_inf)



    print()
    print()
    print()
    #print('печатаем все данные из бд')
    #print('data is',data)

    # минимальные и максимальные значения для всех параметров
    datamin = data['data_maga'][0]
    print('data_min is ', datamin)
    datamax = data['data_maga'][1]
    print('data_max is', datamax)

    vremmin = []
    for j in x_list:
        for key, value in datamin.items():
            if key == j:
                vremmin.append(float(datamin[key]))
                print(vremmin)
    vectmin = np.array(vremmin)

    print()
    # печатаем вектор минимальных значений параметров
    print('vectmin is',vectmin)

    vremmax = []
    for j in x_list:
        for key, value in datamax.items():
            if key == j:
                vremmax.append(float(value))
    vectmax = np.array(vremmax)

    # печатаем вектор максмальных значений параметров
    print('vectmax is',vectmax)
    print()


    vect_x = []
    for i in j_list:
        vrem_x = []
        for j in x_list:
            #print(data_inf[i])
            vrem_x.append(float(data_inf[i][j]))
            print('проверка data_inf[{}][{}] = {}'.format(i,j,data_inf[i][j]))
        print()
        vect = np.array(vrem_x)
        vect_x.append(vect)
    # печатаем все нужные данные параметров полетов без минимальных и максимальных
    print('itog vect_x = ', vect_x)
    print()

    # считаем  Zi
    z_itog = []
    for i in range(len(j_list)):
        z_list = []
        for j in range(len(x_list)):
            z = (vect_x[i][j] - 1/2*(vectmax[j]+vectmin[j]))/((vectmax[j] - vectmin[j])*1/2)
            #print('z[{}][{}] = {} '.format(i,j,z))
            z_list.append(z)
        print('z_list = ',z_list)
        z_vect = np.array(z_list)
        z_itog.append(z_vect)
    print('-------------------------------------------')
    print()
    print('z itog is = ',z_itog)

    # по известному выражению считаем выбранную функцию Ф
    F = []
    for j in range(len(z_itog)):
        sum = 0
        for i in range(len(z_itog[j])):
            sum+= z_itog[j][i]**2
        f = math.sqrt(1/len(z_itog[j])*sum)
        F.append(f)
    print()
    print()
    print('F = ',F)

    # рисуем данную функцию Ф
    j_graph = [i+1 for i in range(len(j_list))]
    plt.figure(1)
    plt.title('расчет целевой функции')
    plt.xlabel('q полет')
    plt.ylabel('Ф')
    plt.plot(j_graph, F, marker='o')
    plt.legend()
    plt.savefig("my1.png")

    # сортируем функцию Ф по возрастанию
    F_sort = sorted(F)
    print()
    print('F sort is ', F_sort)
    
    # считаем функцию F
    P = []
    print(len(F_sort))
    for i in range(len(F_sort)):
        P.append((i+1)/len(F_sort))
        print('p[{}] = {}'.format(i , P[i]))
    print('P = ',P)
    print()

    # рисуем функцию F
    plt.figure(2)
    plt.title('выборочная функция распределения')
    plt.xlabel('Ф')
    plt.ylabel('F')
    plt.plot(F_sort, P, marker='o')
    plt.legend()
    plt.savefig("graph.png")

    print()
    # логарифмируем значение функции и отнимаем от 1
    mu = []
    for i in range(len(P)):
        mu.append(-math.log((1.0000000001 - P[i])))
    print('mu = ', mu)



    """метод наименьших квадратов"""
    # приравниваем частную производную dP/da = 0
    # приравниваем частную производную dP/db = 0
    # методом крамера, либо подстановкой вычисляем для функции нашего распределения формулы коэф-тов а и b
    # вызываем функцию MNK которая посчитает коэф-ты
    coef = MNK_V(F_sort,mu,len(mu))
    print()
    print()
    print("a = {}, b = {}".format(coef[0],coef[1]))
    print()
    print()


    #посчитаем значения для ф-ции Вейбла
    xi_vable = F_sort[0] 
    x_vable = []
    y_vable = []

    # считаем функцию по Вейбла по точкам
    dx = 0.001
    while xi_vable <= F_sort[len(F_sort)-1] + 0.00001:
        x_vable.append(xi_vable)
        y_vable.append(vable(xi_vable,coef[0],coef[1]))
        xi_vable += dx
    

    #посчитаем квантиль для данного полета
    y_q = 0.95
    x_quantile = quantile(y_q, coef[0], coef[1])
    print()
    print('quantile = ', x_quantile)

        
    
    # рисуем графики функций 
    plt.figure(3)
    plt.title('аппроксимация')
    plt.xlabel('Ф')
    plt.ylabel('F')
    plt.plot(F_sort, P, marker='o')
    plt.plot(x_vable,y_vable)
    plt.legend()
    plt.savefig("comparison.png")






    return flask.jsonify(message="201")



#-----------------------------------------------------------------------------------


@app.route('/proba', methods=['POST'])
def proba():
    # получаем данные от клиента
    j = request.get_json()
    print(j)
    print(type(j))
    # j - номер полета
    #j_list = j['j']
    j_value = j['j']
    j_list = [i for i in range(1,int(j_value))]
    # x - интересующий параметр
    x_list = j['x']
    print('x_list is ', x_list)

    print(len(j_list))

    # вытаскиваем данные о полетах из бд
    data = db.info.find()
    print('data is',data)
    data = json.loads(json_util.dumps(data))
    data = dict(data[0])
    #print(data)
    print()

    #-----------------------------------------------------------------------------
    data_inf = {}
    # выбираем  информацию  только о нужных полетах из j_list, который отправил нам клиент
    for i in j_list:
        print('печатаем номера полетов которые ввел клиент')
        print("i is", i)
        clean_data = data['data_maga'][i+1]
        data_inf[i] = clean_data
    print('нужные данные из бд',data_inf)



    print()
    print()
    print()
    #print('печатаем все данные из бд')
    #print('data is',data)

    # минимальные и максимальные значения для всех параметров
    datamin = data['data_maga'][0]
    print('data_min is ', datamin)
    datamax = data['data_maga'][1]
    print('data_max is', datamax)

    vremmin = []
    for j in x_list:
        for key, value in datamin.items():
            if key == j:
                vremmin.append(float(datamin[key]))
                print(vremmin)
    vectmin = np.array(vremmin)

    print()
    # печатаем вектор минимальных значений параметров
    print('vectmin is',vectmin)

    vremmax = []
    for j in x_list:
        for key, value in datamax.items():
            if key == j:
                vremmax.append(float(value))
    vectmax = np.array(vremmax)

    # печатаем вектор максмальных значений параметров
    print('vectmax is',vectmax)
    print()


    #ищем все квантили
    quantile_list = []
    step = 0
    sum_step = 0
    number_of_flights = []
    while sum_step <= 45:
        j_list = j_list[2:(len(j_list)-step)]
        number_of_flights.append(len(j_list))
        print('количество полетов', number_of_flights)
        print('j list is ',j_list)
        vect_x = []
        for i in j_list:
            vrem_x = []
            for j in x_list:
                #print(data_inf[i])
                vrem_x.append(float(data_inf[i][j]))
                #print('проверка data_inf[{}][{}] = {}'.format(i,j,data_inf[i][j]))
            #print()
            vect = np.array(vrem_x)
            vect_x.append(vect)
        # печатаем все нужные данные параметров полетов без минимальных и максимальных
        #print('itog vect_x = ', vect_x)
        print()

        # считаем  Zi
        z_itog = []
        for i in range(len(j_list)):
            z_list = []
            for j in range(len(x_list)):
                z = (vect_x[i][j] - 1/2*(vectmax[j]+vectmin[j]))/((vectmax[j] - vectmin[j])*1/2)
                #print('z[{}][{}] = {} '.format(i,j,z))
                z_list.append(z)
            #print('z_list = ',z_list)
            z_vect = np.array(z_list)
            z_itog.append(z_vect)
        #print('-------------------------------------------')
        print()
        #print('z itog is = ',z_itog)

        # по известному выражению считаем выбранную функцию Ф
        F = []
        for j in range(len(z_itog)):
            sum = 0
            for i in range(len(z_itog[j])):
                sum+= z_itog[j][i]**2
            f = math.sqrt(1/len(z_itog[j])*sum)
            F.append(f)
        #print()
        #print()
        #print('F = ',F)



        # сортируем функцию Ф по возрастанию
        F_sort = sorted(F)
        #print()
        #print('F sort is ', F_sort)
        
        # считаем функцию F
        P = []
        #print(len(F_sort))
        for i in range(len(F_sort)):
            P.append((i+1)/len(F_sort))
            #print('p[{}] = {}'.format(i , P[i]))
        #print('P = ',P)
        #print()



        #print()
        # логарифмируем значение функции и отнимаем от 1
        mu = []
        for i in range(len(P)):
            mu.append(-math.log((1.000000000 - P[i])))
        #print('mu = ', mu)



        """метод наименьших квадратов"""
        # приравниваем частную производную dP/da = 0
        # приравниваем частную производную dP/db = 0
        # методом крамера, либо подстановкой вычисляем для функции нашего распределения формулы коэф-тов а и b
        # вызываем функцию MNK которая посчитает коэф-ты
        coef = MNK_V(F_sort,mu,len(mu))
        #print()
        #print()
        print("a = {}, b = {}".format(coef[0],coef[1]))
        #print()
        #print()


        #посчитаем значения для ф-ции Вейбла
        xi_vable = F_sort[0] 
        x_vable = []
        y_vable = []

        # считаем функцию Вейбулла по точкам
        dx = 0.001
        while xi_vable <= F_sort[len(F_sort)-1] + 0.00001:
            x_vable.append(xi_vable)
            y_vable.append(vable(xi_vable,coef[0],coef[1]))
            xi_vable += dx
        

        #посчитаем квантиль для данного полета
        y_q = 0.95
        x_quantile = quantile(y_q, coef[0], coef[1])
        print()
        print('quantile = ', x_quantile)
        quantile_list.append(x_quantile)
            
        print('iterarion is ',(sum_step//5+1))
        step = 5
        sum_step += step
        
    
    #print()
    print('список квантилей', quantile_list)
    print('длина списка квантилей', len(quantile_list))
    print('step = ',step)


    plt.figure(4)
    plt.title('график 4')
    plt.xlabel('количество  полетов')
    plt.ylabel('квантили')
    plt.plot(number_of_flights, quantile_list, marker='o')
    plt.legend()
    plt.grid()
    plt.savefig("itog.png")

    result = main(number_of_flights,quantile_list)
    print(result)
    qi = np.max(number_of_flights)
    res_qi = 0
    while res_qi <= 1:
        res_qi = result[0] * qi**2 + result[1] * qi + result[2]
        qi += 1
    print(res_qi)
    print('в точке x = {} происходит пересечение'.format(qi))
    forecast_x = np.linspace(np.min(number_of_flights), qi+50, 300)
    forecast_y = res_y(forecast_x,result)
    #print('forecat_y',forecast_y)


    qi_list = [qi , qi]
    res_qi_list = [0, res_qi]
    plt.plot(number_of_flights, quantile_list, 'b.', forecast_x, forecast_y, 'g', qi_list, res_qi_list, 'r-', [np.min(number_of_flights),qi],[res_qi, res_qi], 'r')
    plt.title(r'прогноз отказа')
    plt.text(qi,-0.08,str(qi), color='red')
    plt.grid(True)
    plt.savefig("result.png")


    return flask.jsonify(message="201")



@app.route('/teng', methods=['GET'])
def teng():
    #n = parse('/home/magomedali/Рабочий стол/my_diplom/app/TestBoard_Engine.xls')
    board = Boards.objects.first()
    system = Systems.objects.get(parent_system = board)
    print(system.name)
    sys = Systems.objects().first().parent_system
    print(sys.reg_num)
    values = Flight_data.objects
    return flask.jsonify(message="201")


@app.route('/flyinfo', methods=['GET'])
def flyinfo():
    boards = Boards.objects()
    for b in boards:
        print(b.reg_num)
    print('boards is ', boards)
    return render_template('flyinfo.html')

@app.route('/listAircraft', methods=['GET'])
def listAircraft():
    b = Boards.objects()
    lis = []
    for i in b :
        #print(i.reg_num)
        #print(type(i.reg_num))
        dic = {"ssj":i.reg_num}
        lis.append(dic)
    boards = {
        "airbus": lis
        }
    return flask.jsonify(boards)

@app.route('/boardSystems/', methods=['GET'])
def boardSystems():
    val = request.args.get('settings')
    #print(val)
    b = Boards.objects.get(reg_num=val)
    fl = Flights.objects(board=b)
    system = Systems.objects(parent_system = b)
    lis = []
    for i in fl :
        dic = {"set":i.num_flight}
        lis.append(dic)
    lis2 = []
    for i in system :
        dic = {"set":i.name}
        lis2.append(dic)
    data = {
        "sys": lis2,
        "fly": lis
    }
    return flask.jsonify(data)


@app.route('/listParam', methods=['GET'])
def listParam():
    val = request.args.get('sys')
    print(val)
    syst = Systems.objects.get(name=val)

    #достаем из базы минимальные и максимальные значения
    b = syst.parent_system
    schet = 0
    fly_extr_data = Flight_data.objects.filter(board=b)[:2]
    #print(fly_extr_data)
    for i in fly_extr_data:
        #print(i.param_values)
        if schet == 0:
            vremmin = dict(i.param_values)
        else:
            vremmax = dict(i.param_values)
        schet += 1
    print('vremmin', vremmin)
    print('vremmax',vremmax)
    clean_extr = []
    for key in vremmin:
        for key2 in vremmax:
            if (key == key2)  and (vremmin[key] < vremmax[key2]):
                clean_extr.append(key)
    print(clean_extr)
        

    params = Parameters.objects(system=syst)
    lis = []
    for i in params :
        if str(i.param_name) in clean_extr:
            print(i.param_name)
            dic = {"set":i.param_name}
            lis.append(dic)
    paramerers = {
        "params": lis
        }
    #print(paramerers)
    return flask.jsonify(paramerers)


@app.route('/forecast', methods=['POST'])
def active():
    val = request.data
    data = val.decode('utf-8')
    new_data = json.loads(data)
    print(new_data)
    print(type(new_data))
    param_id = []
    b = Boards.objects.get(reg_num=new_data['airbus'])
    sys = Systems.objects.get(name=new_data['sys'])
    fly = Flights.objects.get(num_flight=new_data['fly'])
    params = Parameters.objects()
    print(params)
    for i in params:
        for j in range(len(new_data['param'])):
            if i.param_name == new_data['param'][j]:
                param_id.append(i.id)
    print(param_id)
    print(param_id[0])
    #достаем из базы минимальные и максимальные значения
    if int(fly.num_flight) >= 1:
        schet = 0
        fly_extr_data = Flight_data.objects.filter(board=b)[:2]
        #print(fly_extr_data)
        for i in fly_extr_data:
            #print(i.param_values)
            if schet == 0:
                vremmin = dict(i.param_values)
            else:
                vremmax = dict(i.param_values)
            schet += 1
    print('vremmin', vremmin)
    print('vremmax',vremmax)

    #сосчитали максимальные и минимальные допустимые значения параметров.
    vremmax_list = []
    for j in new_data['param']:
        print('j',j)
        for key, value in vremmax.items():
            #print('key',key)
            if key == j:
                vremmax_list.append(float(value))
                #print(vremmax_list)
    vectmax = np.array(vremmax_list)
    print('vectmax',vectmax)

    vremmin_list = []
    for j in new_data['param']:
        print('j',j)
        for key, value in vremmin.items():
            #print('key',key)
            if key == j:
                vremmin_list.append(float(value))
                #print(vremmin_list)
    vectmin = np.array(vremmin_list)
    print('vectmin',vectmin)

    #далее нужно положить все остальные значения в списочек
    print('max полет = ', fly.num_flight)

    quantile_list = []
    step = 0
    sum_step = 0
    number_of_flights = []
    while sum_step <= 45:
        fly_i = int(fly.num_flight) - sum_step 
        number_of_flights.append(fly_i)
        print('количество полетов', number_of_flights)
        vect_x = []
        fly_data = Flight_data.objects.filter(board=b)[3:fly_i + 2]
        for i in fly_data:
            print('номер полета',i.flight.num_flight)
            param_dict = dict(i.param_values)
            #print(type(param_dict))
            #print(param_dict['x1'])
            vrem_x = []
            for j in new_data['param']:
                for key, value in param_dict.items():
                    if key == j:
                        vrem_x.append(float(value))
            vect_x.append(vrem_x)
        print('vect_x = ', vect_x)

        # считаем  Zi
        z_itog = []
        for i in range(1,fly_i-2):
            z_list = []
            for j in range(len(new_data['param'])):
                z = (vect_x[i][j] - 1/2*(vectmax[j]+vectmin[j]))/((vectmax[j] - vectmin[j])*1/2)
                #print('z[{}][{}] = {} '.format(i,j,z))
                z_list.append(z)
            #print('z_list = ',z_list)
            z_vect = np.array(z_list)
            z_itog.append(z_vect)
        #print('-------------------------------------------')
        print()
        #print('z itog is = ',z_itog)

        # по известному выражению считаем выбранную функцию Ф
        F = []
        for j in range(len(z_itog)):
            sum = 0
            for i in range(len(z_itog[j])):
                sum+= z_itog[j][i]**2
            f = math.sqrt(1/len(z_itog[j])*sum)
            F.append(f)
        #print()
        #print()
        #print('F = ',F)



        # сортируем функцию Ф по возрастанию
        F_sort = sorted(F)
        #print()
        #print('F sort is ', F_sort)
        
        # считаем функцию F
        P = []
        #print(len(F_sort))
        for i in range(len(F_sort)):
            P.append((i+1)/len(F_sort))
            #print('p[{}] = {}'.format(i , P[i]))
        #print('P = ',P)
        #print()



        #print()
        # логарифмируем значение функции и отнимаем от 1
        mu = []
        for i in range(len(P)):
            mu.append(-math.log((1.0000000001 - P[i])))
        #print('mu = ', mu)



        """метод наименьших квадратов"""
        # приравниваем частную производную dP/da = 0
        # приравниваем частную производную dP/db = 0
        # методом крамера, либо подстановкой вычисляем для функции нашего распределения формулы коэф-тов а и b
        # вызываем функцию MNK которая посчитает коэф-ты
        coef = MNK_V(F_sort,mu,len(mu))
        #print()
        #print()
        print("a = {}, b = {}".format(coef[0],coef[1]))
        #print()
        #print()


        #посчитаем значения для ф-ции Вейбла
        xi_vable = F_sort[0] 
        x_vable = []
        y_vable = []

        # считаем функцию Вейбулла по точкам
        dx = 0.001
        while xi_vable <= F_sort[len(F_sort)-1] + 0.00001:
            x_vable.append(xi_vable)
            y_vable.append(vable(xi_vable,coef[0],coef[1]))
            xi_vable += dx
        

        #посчитаем квантиль для данного полета
        y_q = 0.95
        x_quantile = quantile(y_q, coef[0], coef[1])
        print()
        print('quantile = ', x_quantile)
        quantile_list.append(x_quantile)
            
        print('iterarion is ',(sum_step//5+1))
        step = 5
        sum_step += step
        
    
    #print()
    print('список квантилей', quantile_list)
    print('длина списка квантилей', len(quantile_list))
    print('step = ',step)
    print('номера полетов', number_of_flights)


    plt.figure(4)
    plt.title('график 4')
    plt.xlabel('количество  полетов')
    plt.ylabel('квантили')
    plt.plot(number_of_flights, quantile_list, marker='o')
    plt.legend()
    plt.grid()
    plt.savefig("itog.png")

    result = main(number_of_flights,quantile_list)
    print(result)
    qi = np.max(number_of_flights)
    res_qi = 0
    while res_qi <= 1:
        res_qi = result[0] * qi**2 + result[1] * qi + result[2]
        qi += 1
    print(res_qi)
    print('на {} полете произойдет отказ '.format(qi))
    forecast_x = np.linspace(np.min(number_of_flights), qi+50, 300)
    forecast_y = res_y(forecast_x,result)
    #print('forecat_y',forecast_y)


    qi_list = [qi , qi]
    res_qi_list = [0, res_qi]
    dt_now = str(datetime.now())
    filename = dt_now.replace('-','').replace('.','').replace(' ','').replace(':','')
    print(filename)
    
    plt.figure(int(filename))
    plt.plot(number_of_flights, quantile_list, 'b.', forecast_x, forecast_y, 'g', qi_list, res_qi_list, 'r-', [np.min(number_of_flights),qi],[res_qi, res_qi], 'r')
    plt.title(r'прогноз отказа')
    plt.xlabel('количество полетов')
    plt.ylabel('квантиль')
    plt.text(qi,-0.08,str(qi), color='red')
    plt.grid(True)
    plt.savefig("/home/magomedali/Рабочий стол/forecast/app/static/images/" + str(filename))

    context = {'text': 'отказ произойдет на {}-м полете'.format(qi), 'image':'http://localhost:5000/static/images/' + str(filename) + '.png'}
    
    return flask.jsonify(context)

@app.route('/add', methods=['GET','POST'])
def add():
    print('got_request!')
    return render_template('add.html')


@app.route('/uploadFiles', methods=['GET','POST'])
def uploadFiles():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            print('нет, передается')
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            mes = {'статус':'не получается прочитать файл'}
            return flask.jsonify(mes)
        file = request.files['file']
        print('file')
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            print('зашли вот сюда')
            mes = {'статус':'нет выбранного файла'}
            return flask.jsonify(mes)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            print('зашли сюда')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(type(os.path.join(app.config['UPLOAD_FOLDER'])))
            print(type(filename))
            #n = parse('/home/magomedali/Рабочий стол/my_diplom/app/TestBoard_Engine.xls')
            # если все прошло успешно, то перенаправляем  
            # на функцию-представление `download_file` 
            # для скачивания файла

            print('все прошло')
            mes = {'статус':'загрузка завершена'}
            return flask.jsonify(mes)
    return flask.jsonify({'статус':'неправильное расширение файла'})

    

if __name__ == '__main__':
    app.run(debug=True)





    
