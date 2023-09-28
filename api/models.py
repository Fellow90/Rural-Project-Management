from django.db import models

from api.enums import status_choices, budget_choices, humanitarian_choices, province_choices

class Province(models.Model):
    code = models.CharField(max_length=30, choices = province_choices, unique = True)
    name = models.CharField(max_length=30, choices = province_choices, unique = True)

    def __str__(self) -> str:
        return self.name


class District(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    

class Municipality(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District,on_delete= models.CASCADE, related_name='municipalities')
    province = models.ForeignKey(Province,on_delete=models.CASCADE, related_name='municipalities')
    country = models.CharField(max_length=5, default='Nepal', editable=False)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200, blank = True)
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING  ,blank = True, related_name='municipalites')
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, blank = True, related_name='municipalites')
    municipality = models.ForeignKey(Municipality, on_delete=models.DO_NOTHING, blank = True, related_name='municipalites')
    status = models.CharField(max_length=20, choices = status_choices, blank = True)
    donor = models.CharField(max_length=100, blank = True)
    executing_agency = models.CharField(max_length=100, blank = True)
    implementing_partner = models.CharField(max_length=100, blank = True)
    counterpart_ministry = models.CharField(max_length=100,blank = True)
    type_of_assistance = models.CharField(max_length=100,blank = True)
    budget_type = models.CharField(max_length=15, choices = budget_choices, blank = True)
    humanitarian = models.CharField(max_length=1,choices = humanitarian_choices, blank = True)
    sector = models.CharField(max_length = 100,blank = True)
    agreement_date = models.DateField( blank = True)
    commitments = models.DecimalField(default=0, decimal_places = 2, max_digits = 10,blank = True)
    disbursement = models.DecimalField(default=0, decimal_places = 2, max_digits = 10, blank = True)
    
    def __str__(self):
        return self.title
    

class Excel(models.Model):
    excel_file = models.FileField()