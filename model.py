from tortoise import fields
from tortoise.models import Model
from tortoise import Tortoise, run_async


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    events = fields.ManyToManyField('models.Event', related_name='tournaments')

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    teams = fields.ManyToManyField('models.Team', related_name='events')

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    events = fields.ManyToManyField('models.Event', related_name='teams')

    def __str__(self):
        return self.name


async def create_tournament_event_team():
    # Создание турнира
    tournament = Tournament(name="Tournament 1")
    await tournament.save()

    # Создание события
    event = Event(name="Event 1", tournament=tournament)
    await event.save()

    # Создание команды
    team = Team(name="Team 1")
    await team.save()

    # Добавление события команде
    event.teams.add(team)


async def main():
    # Инициализация подключения к базе данных
    await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['models']})
    await Tortoise.generate_schemas()

    # Выполнение операции с базой данных
    await create_tournament_event_team()

    # Закрытие соединения с базой данных
    await Tortoise.close_connections()

# Запуск асинхронной программы
#run_async(main())
