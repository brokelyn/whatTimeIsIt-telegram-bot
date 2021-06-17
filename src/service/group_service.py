from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pytz

from entity.group import Group
from repo.group_repo import GroupRepo
import service.event_service as EventService


def group_settings_keyboard(group: Group) -> InlineKeyboardMarkup:
    keyboard = list()

    text = "Violation Action:  " + group.violation_action
    callback_data = "settings violation_action"
    keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    text = "Timezone:  " + group.timezone
    callback_data = "settings select_timezone"
    keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    text = "Auto Events:  " + str(group.auto_events)
    callback_data = "settings auto_events"
    keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    text = "Show Invite Link"
    callback_data = "settings invite_link"
    keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    return InlineKeyboardMarkup(keyboard)

def timezone_keyboard(selection=None):
    keyboard = list()

    if selection == None:
        continents = set()

        for timezone in pytz.common_timezones:
            continents.add(timezone.split("/")[0])

        continents.remove("UTC")
        continents.remove("GMT")
        for con in continents:
            callback_data = "settings select_timezone " + con
            keyboard.append([InlineKeyboardButton(con, callback_data=callback_data)])

        callback_data = "settings set_timezone GMT"
        keyboard.append([InlineKeyboardButton("GMT", callback_data=callback_data)])

        callback_data = "settings"
        keyboard.append([InlineKeyboardButton("<< BACK", callback_data=callback_data)])
    else:
        regions = set()

        for timezone in pytz.common_timezones:
            split_timezone = timezone.split("/")

            if split_timezone[0] == selection:
                regions.add(split_timezone[1])

        for region in regions:
            full_timezone =  selection + "/" + region
            callback_data = "settings set_timezone " + full_timezone
            keyboard.append([InlineKeyboardButton(full_timezone, callback_data=callback_data)])

        callback_data = "settings select_timezone"
        keyboard.append([InlineKeyboardButton("<< BACK", callback_data=callback_data)])

    return InlineKeyboardMarkup(keyboard)


def change_violation_action(group_id: int) -> Group:
    group = GroupRepo.get_or_none(group_id)

    if group.violation_action == "ban":
        group.violation_action = "permission"
    elif group.violation_action == "permission":
        group.violation_action = "none"
    elif group.violation_action == "none":
        group.violation_action = "ban"

    GroupRepo.save(group)
    return group

def change_auto_events(group_id: int) -> Group:
    group = GroupRepo.get_or_none(group_id)
    group.auto_events = not group.auto_events

    GroupRepo.save(group)
    return group

def set_timezone(group_id: int, timezone: str, job_queue) -> Group:
    group = GroupRepo.get_or_none(group_id)

    # timezones dont match anymore so remove all events
    EventService.remove_all_group_events(job_queue, group_id)

    group.timezone = timezone
    GroupRepo.save(group)
    return group
