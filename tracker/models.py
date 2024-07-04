from django.db import models
import datetime


### BEGIN WORKOUT MODELS ###

# A workout is a record of a user's exercise session after they complete it
class Workout(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    duration = models.DurationField(default=datetime.timedelta(seconds=1))
    distance = models.FloatField(default=1) # in meters, use props when displaying
    units = models.CharField(max_length=200, default='miles')
    calories = models.IntegerField(default=1)
    notes = models.TextField(default='', blank=True)

    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1, related_name='workouts')
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, default=1, related_name='workouts')
    is_completed = models.BooleanField(default=False)

    # for more specific workout pieces
    warmup = models.OneToOneField('Piece', on_delete=models.CASCADE, related_name='warmup', blank=True, null=True)
    cooldown = models.OneToOneField('Piece', on_delete=models.CASCADE, related_name='cooldown', blank=True, null=True)

    # can be 'Lift', 'Run', 'Swim', 'Bike', 'Mobility', 'Row', 'Other'
    # possibly add support for more in the future
    workout_type = models.CharField(max_length=200, default='Other')
    is_indoor = models.BooleanField(default=False)

    @property
    def distance_miles(self) -> float:
        return self.distance * 0.000621371
    
    @property
    def distance_kilometers(self) -> float:
        return self.distance * 0.001
    
    @property
    def distance_yards(self) -> float:
        return self.distance * 1.09361
    
    @property
    def day(self):
        return self.date.day
    
    def get_distance(self) -> float:
        if self.units == 'miles':
            return self.distance_miles
        elif self.units == 'kilometers':
            return self.distance_kilometers
        elif self.units == 'yards':
            return self.distance_yards
        else:
            return self.distance
    
    def __str__(self):
        return self.workout_type + " on " + self.date.strftime("%Y-%m-%d")

class Piece(models.Model):
    id = models.AutoField(primary_key=True)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, default=1, related_name='main_pieces')
    name = models.CharField(max_length=200, default='Piece')
    training_zone = models.ForeignKey('TrainingZone', on_delete=models.CASCADE, default=1, related_name='pieces')
    duration = models.DurationField(default=datetime.timedelta(seconds=1))
    distance = models.FloatField(default=1) # in meters, use props when displaying
    units = models.CharField(max_length=200, default='miles')
    calories = models.IntegerField(default=1)
    notes = models.TextField(default='')
    is_distance_piece = models.BooleanField(default=False)

    @property
    def distance_miles(self) -> float:
        return self.distance * 0.000621371
    
    @property
    def distance_kilometers(self) -> float:
        return self.distance * 0.001
    
    @property
    def distance_yards(self) -> float:
        return self.distance * 1.09361
    
    def get_distance(self) -> float:
        if self.units == 'miles':
            return self.distance_miles
        elif self.units == 'kilometers':
            return self.distance_kilometers
        elif self.units == 'yards':
            return self.distance_yards
        else:
            return self.distance
        

    def __str__(self):
        return self.name

class Lift(models.Model):
    id = models.AutoField(primary_key=True)
    workout = models.OneToOneField('Workout', on_delete=models.CASCADE, default=1, related_name='lift')
    name = models.CharField(max_length=200, default='Lift')


    def __str__(self):
        return self.name
    
class Movement(models.Model):
    id = models.AutoField(primary_key=True)
    lift = models.ForeignKey('Lift', on_delete=models.CASCADE, default=1, related_name='movements')
    name = models.CharField(max_length=200, default='Movement')

    def __str__(self):
        return f'{len(self.sets.all())} sets of {self.name}'

class Set(models.Model):
    id = models.AutoField(primary_key=True)
    lift = models.ForeignKey('Movement', on_delete=models.CASCADE, default=1, related_name='sets')
    num_reps = models.IntegerField(default=1)
    weight = models.FloatField(default=1) # default to pounds
    units = models.CharField(max_length=200, default='pounds')

    @property
    def weight_kilograms(self) -> float:
        return self.weight * 0.453592
    
    @property
    def weight_pounds(self) -> float:
        return self.weight
    
    def get_weight(self) -> float:
        if self.units == 'kilograms':
            return self.weight_kilograms
        else:
            return self.weight
    
    def __str__(self):
        return str(self.num_reps) + " x " + str(self.weight) + " " + self.units

### END WORKOUT MODELS ###
    
class User(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, default='User')
    email = models.EmailField(max_length=200, default='')
    default_plan = models.OneToOneField('Plan', on_delete=models.CASCADE, related_name='default_user', null=True, blank=True)
    followers = models.ManyToManyField('User', related_name='following', blank=True)

    def get_workouts(self):
        return self.workouts.all()
    
    def get_plans(self):
        return self.plans.all()
    
    def get_planned_workouts(self):
        return self.planned_workouts.all()
    
    def get_completed_workouts(self):
        return self.completed_workouts.all()
    
    def __str__(self):
        return self.name
    
class FollowRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, default=1, related_name='follow_requests_sent')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, default=1, related_name='follow_requests_received')
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.from_user.name + " -> " + self.to_user.name + " (" + str(self.approved) + ")"
    
class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='Plan')
    description = models.TextField(max_length=200 ,default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1, related_name='plans', null=True)

    def get_planned_workouts(self):
        return self.planned_workouts.all()
    
    def get_completed_workouts(self):
        return self.completed_workouts.all()
    
    def __str__(self):
        return self.name

class TrainingZone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='Zone 0')
    description = models.TextField(max_length=200 ,default='')
    min_hr = models.IntegerField(default=1)
    max_hr = models.IntegerField(default=1)

    def __str__(self):
        return self.name