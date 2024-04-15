# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adminuser(models.Model):
    admin_user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        # managed = False
        db_table = 'AdminUser'


class Auction(models.Model):
    auction_id = models.IntegerField(primary_key=True)
    phone = models.ForeignKey('Phone', models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # managed = False
        db_table = 'Auction'


class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING, blank=True, null=True)
    normal_user = models.ForeignKey('Normaluser', models.DO_NOTHING, blank=True, null=True)
    admin_user = models.ForeignKey(Adminuser, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # managed = False
        db_table = 'Bid'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'Category'
    
    def __str__(self):
        return self.category_name


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transaction', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Normaluser', models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Feedback'


class Normaluser(models.Model):
    normal_user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        # managed = False
        db_table = 'NormalUser'


class Paymentinfo(models.Model):
    payment_info_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Normaluser, models.DO_NOTHING, blank=True, null=True)
    payment_method = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'PaymentInfo'


class Phone(models.Model):
    phone_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Phone'


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    admin_user = models.ForeignKey(Adminuser, models.DO_NOTHING, blank=True, null=True)
    report_content = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = 'Report'


class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transaction', models.DO_NOTHING, blank=True, null=True)
    shipping_address = models.CharField(max_length=255)
    shipping_date = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = 'Shipping'


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey(Normaluser, models.DO_NOTHING, blank=True, null=True)
    seller = models.ForeignKey(Normaluser, models.DO_NOTHING, related_name='transaction_seller_set', blank=True, null=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = 'Transaction'
