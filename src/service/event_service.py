from typing import List
from telegram import InlineKeyboardButton
from datetime import datetime

from controller.statistic_controller import StatisticController
from service.time_service import TimeService
from repo.event_repo import EventRepo
from repo.group_repo import GroupRepo
from entity.event import Event


class EventService:

    @staticmethod
    def active_jobs(job_queue, group_id: int) -> List:
        active = list()
        for job in job_queue.jobs():
            job_group_id = int(job.name.split('/')[1])
            if not job.removed and group_id == job_group_id:
                active.append(job)

        return active

    ####################################################################################

    @staticmethod
    def remove_group_event(job_queue, group_id: int, time: int):
        EventRepo.delete(group_id, time)
        job_name = EventService.create_job_name(group_id, time)
        for job in job_queue.get_jobs_by_name(job_name):
            job.schedule_removal()

    @staticmethod
    def remove_all_group_events(job_queue, group_id: int):
        active_jobs = EventService.active_jobs(job_queue, group_id)

        EventRepo.delete_all_for_group(group_id)
        for job in active_jobs:
            job.schedule_removal()

    @staticmethod
    def rmv_event_keyboard(job_queue, group_id: int) -> List[List[InlineKeyboardButton]]:
        active_jobs = EventService.active_jobs(job_queue, group_id)

        keyboard = list()
        for job in active_jobs:
            job_event_time = job.name.split('/')[0]
            option = [InlineKeyboardButton("Remove " + job_event_time, callback_data="rmv_event " + job_event_time)]
            keyboard.append(option)

        if len(active_jobs) > 1:
            keyboard.append([InlineKeyboardButton("Remove all events", callback_data="rmv_event_all")])

        return keyboard

    ###################################################################################################

    @staticmethod
    def is_event_already_active(update, context, time: int):
        job_name = EventService.create_job_name(update.message.chat_id, time)

        job_exists = len(context.job_queue.get_jobs_by_name(job_name)) > 0
        event_exists = EventRepo.exists(update.message.chat_id, time)

        return job_exists or event_exists

    ###################################################################################################

    @staticmethod
    def create_job_name(group_id: int, time: int):
        return str(time) + '/' + str(group_id)

    @staticmethod
    def create_event(job_queue, group_id: int, time: int):
        EventRepo.create(Event(time=time, group=group_id))
        EventService.create_job(job_queue, group_id, time)

    @staticmethod
    def create_job(job_queue, group_id, time: int):
        hours = int(time / 1000) * 10
        hours += int(time / 100) - hours
        minute = time - (hours * 100)

        group = GroupRepo.get_or_none(group_id)

        given_start_time = datetime.utcnow().replace(hour=hours, minute=minute + 1, second=5)
        start_time_tz = TimeService.datetime_apply_tz(given_start_time, group.timezone)
        server_diff_to_utc = (datetime.now() - datetime.utcnow())
        temp = (start_time_tz + server_diff_to_utc)
        server_start_time = (temp - start_time_tz.utcoffset())
        server_start_time = server_start_time.replace(microsecond=0, tzinfo=None)

        job_name = EventService.create_job_name(group_id, time)
        job_queue.run_repeating(StatisticController.stats_by_job, interval=86400,
                                first=server_start_time.time(), context=group_id, name=job_name)
