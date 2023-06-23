from textwrap import dedent

from django.contrib import admin

from tg_bot.bot_functions import get_menu_markup
from tg_bot.bot_env import bot
from tg_bot.models import *


@admin.register(Particiant)
class AdminParticiant(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('role',)


@admin.register(Event)
class AdminSEvent(admin.ModelAdmin):
    list_display = ('date',)

    actions = ['send_all_users_notification']

    @admin.action(description='Отправить оповещение всем users')
    def send_all_users_notification(self, request, queryset):
        next_event = queryset[0]
        users = Particiant.objects.filter(role=3)
        if users:
            users_count = len(users)
            for user in users:
                message_text = f'''
                <b>{user.name}, здравствуйте!</b>
                Информируем вас о предстоящем Python митапе,
                который состоится <b>{next_event.date.strftime('%d.%m.%Y')}</b>
                
                Приглащаем вас принять участие в качесстве гостя или докладчика
                '''
                message_text = dedent(message_text)
                msg = bot.send_message(user.telegram_id,
                                       message_text,
                                       parse_mode='HTML',
                                       reply_markup=get_menu_markup(user.telegram_id)
                                       )
            admins = Particiant.objects.filter(role=1)
            for admin in admins:
                msg = bot.send_message(admin.telegram_id,
                                       f'{admin.name}. Оповещений разослано: {users_count}'
                                       )


@admin.register(Lecture)
class AdminLecture(admin.ModelAdmin):
    list_display = ('get_time', 'title', 'speaker', 'start', 'event',)
    list_filter = ('event',)
    ordering = ('start',)

    def get_time(self, obj):
        lecture = Lecture.objects.get(pk=obj.pk)
        return f'{lecture.start} - {lecture.end}'
