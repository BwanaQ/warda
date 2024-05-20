from django.contrib import admin
from .models import (
    UnitInventoryCategory,
    UnitInventoryItem,
    UnitConditionQuestion,
    UnitConditionQuestionTemplate,
    UnitConditionCheckList,
    UnitConditionAssesment
)

from portfolio.models import (
    Unit
)

admin.site.register(UnitInventoryCategory)
admin.site.register(UnitInventoryItem)
admin.site.register(UnitConditionQuestion)
admin.site.register(UnitConditionQuestionTemplate)
admin.site.register(UnitConditionCheckList)
admin.site.register(UnitConditionAssesment)


class UnitInventoryItemInline(admin.TabularInline):
    model = UnitInventoryItem
    extra = 1
    fields = ('name','quantity','description')
    readonly_fields = ('name','quantity','description')
    can_delete = False

class UnitInventoryAdmin(admin.ModelAdmin):
    inlines = [
        UnitInventoryItemInline,
    ]
    list_display = ('unit_no',)
    list_filter = ('unit_no',)
    search_fields = ('unit_no',)

# admin.site.register(Unit,UnitInventoryAdmin)