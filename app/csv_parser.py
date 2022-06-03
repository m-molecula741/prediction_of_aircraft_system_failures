from models import *
import os
from csv import reader
from datetime import datetime


def parse(path, file_name=None, delimiter=';'):
    if file_name is None:
        file_name = os.path.basename(path)
    file_name = file_name.split('.')[0]
    names = file_name.split('_')
    if len(names) != 2:
        raise 'Неверный формат именования файла'
    board_reg_num = names[0]
    system_name = names[1]
    with open(path) as csvfile:
        stream = reader(csvfile, delimiter=delimiter)
        board = get_or_create(Boards, query={'reg_num': board_reg_num})
        system = get_or_create(Systems, query={'name': system_name, 'parent_system': board})
        headers = next(stream)
        parameter_names = headers[4:]
        for parameter in parameter_names:
            get_or_create(Parameters, query={
                'param_name': parameter,
                'full_param_name': parameter,
                'system' : system
            })
        for line in stream:
            parse_data(
                flight_number=line[0],
                flight_phase=line[1],
                date=line[2],
                time=line[3],
                parameters=dict(zip(parameter_names, line[4:])),
                board=board,
            )


def parse_data(
        flight_number,
        flight_phase,
        date,
        time,
        parameters,
        board,
):
    flight = get_or_create(
        Flights,
        query={'num_flight': flight_number, 'board': board}
        #start_time=date_time
    )
    flight_phase = get_or_create(
        Flight_phases,
        query={'name': flight_phase}
    )
    flight_data = Flight_data(
        board=board,
        flight=flight,
        phase=flight_phase,
        #date_time=date_time,
        param_values=parameters,
    )
    flight_data.save()


def get_or_create(model, query: dict, **kwargs):
    try:
        obj = model.objects.get(**query)
    except model.DoesNotExist:
        obj = model(**query, **kwargs)
        obj.save()
    return obj