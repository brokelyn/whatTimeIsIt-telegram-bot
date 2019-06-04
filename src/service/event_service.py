from typing import List
from telegram import InlineKeyboardButton


class EventService:

    @staticmethod
    def active_jobs(job_queue) -> List:
        active = list()
        for job in job_queue.jobs():
            if not job.removed:
                active.append(job)

        return active

    @staticmethod
    def remove_job(job_queue, job_name: str):
        for job in job_queue.get_jobs_by_name(job_name):
            job.schedule_removal()

    @staticmethod
    def remove_all_jobs(job_queue):
        active_jobs = EventService.active_jobs(job_queue)

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
