import random
from celery import shared_task
from celery import shared_task, current_task
from time import sleep
import csv
from .models import Schema, Column
from random import randint
import copy
import os
from csvgen.settings import MEDIA_ROOT, MEDIA_URL
from faker import Faker

fake = Faker()


@shared_task
def generate_csv(schema_id, quantity):

    print('get task ', schema_id, quantity)

    fake_gen = []
    fake_gen_args = []  # store arguments of int generators
    columns = list(Schema.objects.get(pk=schema_id).column_set.all())
    for column in columns:
        fake_gen_args.append(())
        print(column.type)
        if column.type == 'Full name':
            fake_gen.append((fake.name() for i in range(quantity)))
        elif column.type == 'Company':
            fake_gen.append((fake.company() for i in range(quantity)))
        elif column.type == 'Job':
            fake_gen.append((fake.job() for i in range(quantity)))
        elif column.type == 'Domain':
            fake_gen.append((fake.domain_name() for i in range(quantity)))
        else:
            fake_gen_args.pop()
            int_min = copy.copy(column.start)
            int_max = copy.copy(column.end)
            column_ind = copy.copy(columns.index(column))

            fake_gen_args.append((column_ind, int_min, int_max))

            # this generator will do nothing
            fake_gen.append(
                (fake.pyint(
                    min_value=int_min,
                    max_value=int_max) for i in range(quantity))
            )
    file_name = str(schema_id) + '_' + fake.pystr() + '.csv'
    try:
        with open(os.path.join(MEDIA_ROOT, file_name), mode='w') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                delimiter=Schema.objects.get(pk=schema_id).column_separator,
                quotechar=Schema.objects.get(pk=schema_id).string_character,
                quoting=csv.QUOTE_MINIMAL
            )
            for i in range(quantity):
                fake_slice = [
                    next(i) if len(fake_gen_args[fake_gen.index(i)]) == 0 else randint(
                        fake_gen_args[fake_gen.index(i)][1],
                        fake_gen_args[fake_gen.index(i)][2]) for i in fake_gen]

                # print(('fake_slice: ', fake_slice))
                csv_writer.writerow([fake_slice])

    except Exception as e:
        print(type(e), e)

    print('done task ', schema_id,file_name)

    return MEDIA_URL + file_name
