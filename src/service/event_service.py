from typing import List
from telegram import InlineKeyboardButton
import datetime

from controller.statistic_controller import StatisticController
from service.time_service import TimeService
from repo.event_repo import EventRepo
from entity.event import Event


class EventService:

    @staticmethod
    def active_jobs(job_queue) -> List:
        active = list()
        for job in job_queue.jobs():
            if not job.removed:
                active.append(job)

        return active

    ####################################################################################

    @staticmethod
    def remove_event(job_queue, job_name: str):
        EventRepo.delete(int(job_name))
        for job in job_queue.get_jobs_by_name(job_name):
            job.schedule_removal()

    @staticmethod
    def remove_all_events(job_queue):
        active_jobs = EventService.active_jobs(job_queue)

        EventRepo.delete_all()
        for job in active_jobs:
            job.schedule_removal()

    @staticmethod
    def rmv_event_keyboard(job_queue) -> List[InlineKeyboardButton]:
        active_jobs = EventService.active_jobs(job_queue)

        keyboard = list()
        for job in active_jobs:
            option = [InlineKeyboardButton("Remove " + job.name, callback_data="rmv_event " + job.name)]
            keyboard.append(option)

        if len(active_jobs) > 1:
            keyboard.append([InlineKeyboardButton("Remove all events", callback_data="rmv_event_all")])

        return keyboard

    ####################################################################################

    @staticmethod
    def create_event(job_queue, chat_id, time: int):
        EventRepo.create(Event(time=time, chat_id=chat_id))
        EventService.create_job(job_queue, chat_id, time)

    @staticmethod
    def create_job(job_queue, chat_id, time: int):
        hours = int(str(time)[0] + str(time)[1])
        minute = (time - (hours * 100)) + 1
        job_queue.run_repeating(StatisticController.stats_by_job, 86400,
                                first=TimeService.time_apply_tz(datetime.time(hours, minute, 5)),
                                context=chat_id, name=str(time))
