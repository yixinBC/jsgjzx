from django.db import models


# Create your models here.
class Class(models.Model):
    class_id = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f"班级编号：{self.class_id}"


class Student(models.Model):
    student_class = models.ForeignKey(Class, verbose_name="班级", on_delete=models.CASCADE)
    student_id = models.CharField(verbose_name="学号", max_length=6)
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码—md5加密", max_length=32)

    def __str__(self) -> str:
        return f"{self.student_id} {self.name}"


class Meal(models.Model):
    date = models.DateField(verbose_name="日期")
    index = models.PositiveSmallIntegerField(verbose_name="索引")
    description = models.CharField(verbose_name="描述", max_length=4)

    def __str__(self) -> str:
        return f"{self.date}{self.description}"

    def __lt__(self, other) -> bool:
        if self.date < other.date:
            return True
        elif self.date == other.date and self.index < other.index:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        return not self < other

    def __eq__(self, other) -> bool:
        return self.date == other.date and self.index == other.index

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return self > other or self == other


class Food(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32)
    commented = models.IntegerField(verbose_name="评价人数")
    photo = models.ImageField(verbose_name="菜品图片", upload_to="foods", null=True)
    # 菜品评价后的总打星数
    stars = models.BigIntegerField(verbose_name="总星数")

    def __str__(self) -> str:
        return self.name
