from django.db import models

# Create your models here.

#created accidentally, but a good practice

# class Event(models.Model):
# 	#tweets info
# 	tweet_id = models.CharField('Tweet Id', max_length=20, primary_key=True)
# 	tweet_date = models.DateTimeField('Tweet Date');
# 	user_id = models.CharField('User Id', max_length=25)
# 	user_name = models.CharField('User Name', max_length=50)
# 	content = models.TextField()

# 	#expert comments 
# 	topic = models.CharField(max_length=100, blank=True)
# 	accuracy = models.IntegerField(default=0)
# 	in_accuracy_category = models.CharField(max_length=50, blank=True)
# 	comments = models.TextField(blank=True);
