from django.contrib import admin
from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'type', 'category', 'date',)


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'user',)
