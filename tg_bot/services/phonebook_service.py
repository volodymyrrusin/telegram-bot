import sqlalchemy.exc
import re

from tg_bot.models import PhoneBook
from tg_bot import db


class PhonebookServiceException(Exception):
    pass


class PhonebookServices:

    @staticmethod
    def add_new_record(user_id, name, phone_number):
        if not re.fullmatch(r'^(\+380|380|0)\d{9}$', phone_number):
            raise PhonebookServiceException('Phone number has an incorrect format')
        record = PhoneBook(
            user_id=user_id,
            name=name,
            phone_number=phone_number
        )
        try:
            db.session.add(record)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise PhonebookServiceException('Such name or phone number already exist')

    @staticmethod
    def delete_record(user_id, name):
        record = db.session.scalar(db.select(PhoneBook).filter_by(user_id=user_id, name=name))
        if not record:
            raise PhonebookServiceException('No such contact')
        db.session.delete(record)
        db.session.commit()

    @staticmethod
    def list_of_contacts(user_id):
        contacts_list = db.session.scalars(db.Select(PhoneBook).filter_by(user_id=user_id)).all()
        if not contacts_list:
            raise PhonebookServiceException('Contacts list is empty')
        return contacts_list

    @staticmethod
    def show_phone_number(user_id, name):
        phone_number = db.session.scalar(
            db.Select(PhoneBook.phone_number).filter_by(user_id=user_id, name=name))
        if not phone_number:
            raise PhonebookServiceException('No such contact')
        return phone_number
