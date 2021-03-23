from django.db import models
from django_resized import ResizedImageField


# Create your models here.
class Class(models.Model):
    class_id = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f"班级编号：{self.class_id}"


class Meal(models.Model):
    date = models.DateField(verbose_name="日期")
    index = models.PositiveSmallIntegerField(verbose_name="当日索引")
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
        if isinstance(other, Meal):
            return self.date == other.date and self.index == other.index
        else:
            return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return self > other or self == other


class Food(models.Model):
    meal = models.ManyToManyField(Meal, through="FoodForMeal", verbose_name="关联餐")
    name = models.CharField(verbose_name="名称", max_length=32)
    commented = models.IntegerField(verbose_name="评价人数", default=0)
    photo = ResizedImageField(size=[600, 600], verbose_name="菜品图片", upload_to="foods", null=True, blank=True)
    # 菜品评价后的总打星数
    stars = models.BigIntegerField(verbose_name="总星数", default=0)
    price = models.PositiveIntegerField(verbose_name="价格", default=0)

    def __str__(self) -> str:
        return self.name


class FoodForMeal(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="菜品")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="餐")
    total = models.IntegerField(verbose_name="总份数")
    wanted = models.IntegerField(verbose_name="想要人数", default=0)

    def __str__(self):
        return f"{self.meal} {self.food} {self.wanted}想要"


class Student(models.Model):
    asked_meal = models.ManyToManyField(FoodForMeal, through="FoodForStudent", blank=True, verbose_name="已点的餐")
    stu_class = models.ForeignKey(Class, verbose_name="班级", on_delete=models.CASCADE)
    stu_id = models.CharField(verbose_name="学号", max_length=6)
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码—md5加密", max_length=32)
    last_order = models.ForeignKey(Meal, verbose_name="上次点餐的Meal", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.stu_id} {self.name}"


class FoodForStudent(models.Model):
    food_for_meal = models.ForeignKey(FoodForMeal, on_delete=models.CASCADE, verbose_name="点的菜")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")


class Comment(models.Model):
    food = models.ForeignKey(Food, verbose_name="所评食物", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="评价学生", on_delete=models.CASCADE)
    pub_date = models.DateTimeField(verbose_name="发表日期")
    stars = models.PositiveSmallIntegerField(verbose_name="打分")
    content = models.CharField(verbose_name="评论内容", max_length=1024)

    def __str__(self) -> str:
        return f"{self.content}"
