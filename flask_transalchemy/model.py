from flask import current_app
from flask_babelex import get_locale
from flask_sqlalchemy import Model
import sqlalchemy as sa
from werkzeug.local import LocalProxy


translate = LocalProxy(lambda: current_app.extensions["translate"])


class TranslationMixin(Model):
    """Declarative Mixin class for translation model."""
    table = sa.Column(sa.String(64), primary_key=True)
    record_id = sa.Column(sa.Integer, primary_key=True)
    attribute = sa.Column(sa.String(64), primary_key=True, nullable=False)
    language = sa.Column(sa.String(2), primary_key=True, nullable=False)
    value = sa.Column(sa.Text)


class TranslatableMixin(object):
    """Declarative Mixin class for translatable models."""
    translatable_columns = []

    def get_translation(self, attribute: str, language: str):
        """Get translation of field in requested language.

        :param attribute: Field name
        :param language: Translation language identifier string (e.g. 'en')

        :return: Translated field value. If no translation found, the value
            stored in the model is returned.

        """
        if attribute in self.translatable_columns:
            record = translate.model.query.filter_by(
                table=self.__tablename__,
                record_id=self.id,
                attribute=attribute,
                language=language
            ).first()

            translation = getattr(record, "value", None)

            if translation is not None:
                return translation

        raise AttributeError("No translations found.")

    def set_translation(self, attribute: str, language: str, value: str):
        """Save translation of field.

        :param attribute: Field name
        :param language: Translation language identifier string (e.g. 'en')
        :param value: Translated value

        """
        if attribute in self.translatable_columns:
            record = translate.model.query.filter_by(
                table=self.__tablename__,
                record_id=self.id,
                attribute=attribute,
                language=language
            ).first()

            if record is None:
                record = translate.model(
                    table=self.__tablename__,
                    record_id=self.id,
                    attribute=attribute,
                    language=language,
                    value=value
                )
                translate.db.session.add(record)

            else:
                record.value = value
        else:
            raise AttributeError("Can't set translation for attribute.")

    def __setattr__(self, key, value):
        """Save translated value automatically."""
        if key in self.translatable_columns:
            try:
                language = str(get_locale())
                self.set_translation(key, language, value)
            except AttributeError:
                return super().__setattr__(key, value)

    def __getattribute__(self, item):
        """Get translated value automatically."""
        try:
            language = str(get_locale())
            return self.get_translation(item, language)
        except AttributeError:
            return super().__getattribute__(item)
