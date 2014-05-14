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
#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin admin models
#===============================================================================

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','uuid','full_name','get_email')
    search_fields=['user__email','user__first_name','user__last_name']
    
    def full_name(self,user_profile):
        return ("%s %s" % (user_profile.user.last_name, user_profile.user.first_name))
    full_name.short_description = "Full Name"
    
    def get_email(self, user_profile):
        return user_profile.user.email
    get_email.short_description = "Email"
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','index','answer')
        
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id','user_profile', 'question', 'attempt', 'answer', 'duration')
    
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
    list_display = ('id','user_profile', 'concept', 'score', 'date')

class UserSectionScoreAdmin(admin.ModelAdmin):
    list_display = ('id','user_profile', 'section', 'score', 'date')

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('id','user_profile', 'score', 'date')

class ScoreTableAdmin(admin.ModelAdmin):
    list_display = ('id','percentile', 'score')

#===============================================================================
# end admin models
#===============================================================================

#===============================================================================
# begin admin site regitration
#===============================================================================

admin.site.register(UserProfile, UserProfileAdmin)
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