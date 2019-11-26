from flask import Flask, current_app, request
from flask_babelex import get_locale
from flask_sqlalchemy import SQLAlchemy

from flask_transalchemy.model import TranslationMixin


class TransAlchemy(object):
    """Flask-TransAlchemy extension class.

    :param app: Flask application instance
    :param db: Flask-SQLAlchemy instance

    """
    def __init__(self, app: Flask, db: SQLAlchemy, label_route: str = None):
        self.app = app
        self.db = db
        self.model = None
        self.route = label_route
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize extension and create `Translation` model class.

        :param app: Flask application instance
        """
        app.extensions["babel_alchemy"] = self

        class Translation(self.db.Model, TranslationMixin):
            pass

        self.model = Translation

        if self.route:
            @self.app.route(
                '/{}/<label>'.format(self.route),
                endpoint='label_translations'
            )
            def translate(label):
                return self.get_label(label, **request.args)

    def set_label(self, label: str, value: str, language: str = None):
        """Save label translation in database.

        :param label: Label name ('attribute' field in table)
        :param value: Translated label text.
        :param language: Language of translation
        """
        if language is None:
            language = str(get_locale())

        translation = self.model(
            attribute=label,
            language=language,
            value=value
        )
        self.db.session.add(translation)
        self.db.session.commit()


    def get_label(self, label: str, language: str = None):
        """Get translated label from database.

        Labels are stored in the table without table name and record_id.

        :param label: Label name ('attribute' field in table)
        :param language: Language of translation
        :return: Translated label text.
        """
        if language is None:
            language = str(get_locale())

        qry = self.model.query.filter_by(
            table=None,
            record_id=None,
            attribute=label,
            language=language
        )
        translation = qry.first()

        if translation is None:
            return label

        return translation.value


def set_label(label: str, value: str, language: str = None):
    """Shortcut for `BabelAlchemy.set_label()`.

    :param label: Label name ('attribute' field in table)
    :param value: Translated label text.
    :param language: Language of translation
    """
    babel_alchemy = current_app.extensions.get("babel_alchemy")
    return babel_alchemy.set_label(label, value, language)


def get_label(label: str, language: str = None):
    """Shortcut for `BabelAlchemy.get_label()`.

    Labels are stored in the table without table name and record_id.

    :param label: Label name ('attribute' field in table)
    :param language: Language of translation
    :return: Translated label text.
    """
    babel_alchemy = current_app.extensions.get("babel_alchemy")
    return babel_alchemy.get_label(label, language)
