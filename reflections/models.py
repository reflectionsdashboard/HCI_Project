from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name


class Topic(models.Model):
    class Meta:
        unique_together = (('id', 'subject_id'),)

    subject_id = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE)
    id = models.TextField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.subject_id.name + ": " + self.name + '(' + self.id + ')'

    def mapping(self):
        return self.id + "-" + self.name


class InAccuracyCategory(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.description


class Reflection(models.Model):
    class Meta:
        unique_together = (('id', 'student_id'),)

    id = models.AutoField(primary_key=True)
    tweet_id = models.CharField('Tweet Id', max_length=20);
    student_id = models.CharField('Student Id', max_length=50)
    student_handle = models.CharField('User Name', max_length=50)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, default=None, blank=True, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, default=None, on_delete=models.CASCADE, blank=True, null=True)
    tweet_date = models.DateTimeField('Tweet Date');

    accuracy = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ],
        blank=True
    )
    inaccuracy_category = models.ForeignKey(InAccuracyCategory, default=None, on_delete=models.DO_NOTHING,
                                            blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    is_pending = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + " " + self.description

    def formatted_description(self):
        sentences = self.description.split(". ")
        sentences2 = [sentence[0].capitalize() + sentence[1:] for sentence in sentences]
        formatted_string = '. '.join(sentences2)
        return formatted_string

    def accuracy_percentage(self):
        return self.accuracy * 10
