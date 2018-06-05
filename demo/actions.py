# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from demo.api import MailChimpAPI
from demo import config
from demo.gdrive_service import GDriveService

logger = logging.getLogger(__name__)


class ActionSubscribeNewsletter(Action):

    def name(self):
        return "action_subscribe_newsletter"

    def run(self, dispatcher, tracker, domain):
        email = tracker.get_slot('email')
        if email:
            # for now we'll do this randomly
            # client = MailChimpAPI(config.mailchimp_api_key)
            # subscribed = client.subscribe_user(config.mailchimp_list, email)
            import random

            if random.random() < 0.5:
                subscribed = True
            else:
                subscribed = False

            return [SlotSet('subscribed', subscribed)]


class ActionStoreSalesInfo(Action):

    def name(self):
        return "action_store_sales_info"

    def run(self, dispatcher, tracker, domain):
        import datetime
        budget = tracker.get_slot('budget')
        company = tracker.get_slot('company')
        email = tracker.get_slot('email')
        jobfunction = tracker.get_slot('jobfunction')
        name = tracker.get_slot('name')
        use_case = tracker.get_slot('use_case')
        date = datetime.datetime.now().strftime("%d/%m/%Y")

        sales_info = [company, use_case, budget, date, name, jobfunction,
                      email]

        gdrive = GDriveService()
        try:
            gdrive.store_data(sales_info)
            return [SlotSet('data_stored', True)]
        except Exception as e:
            logger.error("Failed to write data to gdocs. Error: {}"
                         "".format(e.message), exc_info=True)
            return [SlotSet('data_stored', False)]


class ActionStoreBudget(Action):

    def name(self):
        return "action_store_budget"

    def run(self, dispatcher, tracker, domain):

        budget = next(tracker.get_latest_entity_values('number'), None)
        if not budget:
            budget = next(tracker.get_latest_entity_values('amount-of-money'),
                          None)
        if not budget:
            budget = tracker.latest_message.text

        return [SlotSet('budget', budget)]


class ActionStoreUsecase(Action):

    def name(self):
        return "action_store_usecase"

    def run(self, dispatcher, tracker, domain):

        use_case = tracker.latest_message.text

        return [SlotSet('use_case', use_case)]
