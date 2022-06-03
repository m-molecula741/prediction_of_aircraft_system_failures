from app import app, db2

class Test2(db2.Document):
    name = db2.StringField()

class Boards(db2.Document):
    #Конкретные воздушные судна
    reg_num = db2.StringField(max_length=20)
    description = db2.StringField(max_length=300)

class Systems(db2.Document):
    #информация о системах воздушного судна
    name = db2.StringField(max_length=200)
    parent_system = db2.ReferenceField(Boards)

class Flight_phases(db2.Document):
    #Типовые полетные режимы
    name = db2.StringField(max_length=20)
    description = db2.StringField(max_length=300)

class Parameters(db2.Document):
    #Информация о параметрах
    param_name =  db2.StringField(max_length=10)
    full_param_name = db2.StringField(max_length=200)
    system = db2.ReferenceField(Systems)

class Flights(db2.Document):
    #Общая информация о полетах, выполненным конкртеным ВС
    num_flight = db2.IntField(min_value=-1, max_value=100000)
    board = db2.ReferenceField(Boards)


class Flight_data(db2.Document):
    #Значения параметров
    board = db2.ReferenceField(Boards)
    flight = db2.ReferenceField(Flights)
    phase = db2.ReferenceField(Flight_phases)
    param_values = db2.DictField()