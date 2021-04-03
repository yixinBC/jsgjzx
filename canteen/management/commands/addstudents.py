import os
from hashlib import md5
from django.core.management.base import BaseCommand, CommandError
import xlrd
from canteen.models import Student, Class, Meal


def encrypt(password):
    encoded = md5()
    encoded.update(password.encode())
    return encoded.hexdigest().upper()


class Command(BaseCommand):
    help = '批量从excel中导入学生'

    def add_arguments(self, parser):
        parser.add_argument('excel_path',  nargs='+')

    def handle(self, *args, **options):
        meal = Meal.objects.all().first()
        class_id = {obj.class_id: obj for obj in Class.objects.all()}
        for excel in options['excel_path']:
            if os.path.exists(excel) and not os.path.isdir(excel):
                work_book = xlrd.open_workbook(filename=excel)
                sheet = work_book.sheet_by_index(0)
                stu_ids = sheet.col_values(0)
                stu_names = sheet.col_values(1)
                for i in range(len(stu_ids)):
                    if not stu_ids[i][0:4] in class_id.keys():
                        try:
                            obj = Class(class_id=stu_ids[i][0:4])
                            obj.save()
                            class_id[stu_ids[i][0:4]] = obj
                        except Exception as err:
                            self.stderr.write(str(err))
                    Student.objects.get_or_create(stu_class=class_id[stu_ids[i][0:4]],
                                                  stu_id=stu_ids[i],
                                                  name=stu_names[i],
                                                  password=encrypt(stu_ids[i]),
                                                  last_order=meal
                                                  )

            else:
                raise CommandError('无效的文件路径！')
