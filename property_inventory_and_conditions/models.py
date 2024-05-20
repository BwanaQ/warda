from django.db import models
from authentication.models import (
    TimeStampedModel
)

ASSESSMENT_STATUS_CHOICES = [
    ('O', 'On Going'),
    ('P', 'Pending'),
    ('C', 'Completed'),

]
CONDITION_CHOICES = [
    ('NE','Not Evaluated'),
    ('F','Fair'),
    ('G','Good'),
    ('E','Excellent'),
    ('C','Critical'),
    ('B','Bad'),
    ('D','Damaged'),
    ('U','Unsure')
]

class UnitInventoryCategory(models.Model):
    """Inventory category model e.g Showers,Furniture, Appliances, etc"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UnitInventoryItem(models.Model):
    """Unit inventory item model
    TODO: Help check electricity & water meter readings of specific unit 
    """
    unit = models.ForeignKey('portfolio.Unit', on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,blank=True)
    category = models.ForeignKey(UnitInventoryCategory, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

class UnitConditionQuestion(models.Model):
    """UnitConditionCheckList model"""
    inventory_item = models.ForeignKey(UnitInventoryItem, on_delete=models.CASCADE)
    question = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.question

class UnitConditionQuestionTemplate(TimeStampedModel):
    """CheckListTemplate model 
    TODO Different landlords woll see their own twmplates

    Make some fields read only especially for the answers
    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    questions = models.ManyToManyField(UnitConditionQuestion)

    def __str__(self):
        return self.name

class UnitConditionCheckList(TimeStampedModel):
    """UnitConditionAnswers model"""
    ANSWER_CHOICES = [
        ('Y','Yes'),
        ('N','No'),
        ('U','Unsure')
    ]
    question = models.ForeignKey(UnitConditionQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='F')
    comments = models.TextField(null=True,blank=True)
    is_electricity_utility = models.BooleanField(default=False)
    is_water_utility = models.BooleanField(default=False)
    water_meter_reading = models.CharField(max_length=100, null=True,blank=True)
    electricity_meter_reading = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.answer


class UnitConditionAssesment(TimeStampedModel):
    """UnitConditionAssesment model
     The template will populate answer instances depending on the number of questions.

     is_compiliant = meeting or in accordance with rules or standards.
     populate empty answers from template then update later checklist
    """
    status = models.CharField(max_length=10, choices=ASSESSMENT_STATUS_CHOICES, default='F')
    tempalate = models.ForeignKey(UnitConditionQuestionTemplate, on_delete=models.CASCADE)
    unit = models.ForeignKey('portfolio.Unit', on_delete=models.CASCADE)
    checklist = models.ManyToManyField(UnitConditionCheckList,blank=True)
    comments = models.TextField(null=True,blank=True)
    is_compliant = models.BooleanField(default=False)
    assessed_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    date_assessed = models.DateTimeField(auto_now_add=True)
    overall_house_condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='P')

    def __str__(self):
        return self.unit.unit_number


