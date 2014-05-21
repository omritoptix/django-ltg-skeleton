'''
will hold the admin interface models
Created on November 7, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================
from django.contrib import admin
from ltg_backend_app.models import *
from django.contrib.auth.admin import UserAdmin
from ltg_backend_app.forms import UserChangeForm, UserCreationForm

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================

    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','index','answer')
        
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'question', 'attempt', 'answer', 'duration')
    
class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id','title')

class QuestionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','question', 'attempt', 'mean_time','std_time','percentage_right','score', 'attempts_num')

class ConceptStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','concept', 'mean_score', 'std_score')

class SectionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id','section', 'mean_score', 'std_score')

class UserConceptScoreAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'concept', 'score', 'date')

class UserSectionScoreAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'section', 'score', 'date')

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'score', 'date')

class ScoreTableAdmin(admin.ModelAdmin):
    list_display = ('id','percentile', 'score')
    
class LtgUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','username','first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email','username','password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()


#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================
admin.site.register(LtgUser, LtgUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ScoreTable, ScoreTableAdmin)
admin.site.register(QuestionStatistics, QuestionStatisticsAdmin)
admin.site.register(ConceptStatistics, ConceptStatisticsAdmin)
admin.site.register(SectionStatistics, SectionStatisticsAdmin)
admin.site.register(UserScore, UserScoreAdmin)
admin.site.register(UserSectionScore, UserSectionScoreAdmin)
admin.site.register(UserConceptScore, UserConceptScoreAdmin)

#===============================================================================
# end admin site registration
#===============================================================================