# -*- coding: utf-8 -*-
from logging import getLogger
import urlparse

import requests

import ckan.logic as logic
import ckan.lib.base as base
from ckan.common import _, request, c
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.logic.schema as schema
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.lib.mailer as mailer
from pylons import config
import ckan.lib.captcha as captcha

DataError = dictization_functions.DataError
unflatten = dictization_functions.unflatten


log = getLogger(__name__)


class SuggestController(base.BaseController):

    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))


    def _send_suggestion(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')

            c.form = data_dict['name']
            captcha.check_recaptcha(request)

            #return base.render('suggest/form.html')
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))

        except captcha.CaptchaError:
            error_msg = _(u'Mauvais code captcha. Essayez de nouveau')
            h.flash_error(error_msg)
            return self.suggest_form(data_dict)


        errors = {}
        error_summary = {}

        if (data_dict["email"] == ''):

            errors['email'] = [u'Valeur manquante']
            error_summary['email'] =  u'Valeur manquante'

        if (data_dict["name"] == ''):

            errors['name'] = [u'Valeur manquante']
            error_summary['name'] =  u'Valeur manquante'


        if (data_dict["suggestion"] == ''):

            errors['suggestion'] = [u'Valeur manquante']
            error_summary['suggestion'] =  u'Valeur manquante'


        if len(errors) > 0:
            return self.suggest_form(data_dict, errors, error_summary)
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.

            if data_dict['organization'] == 'all':
                mail_to = config.get('email_to')
            else:
                mail_to = logic.get_action('organization_show')( {},
                                    {'id': data_dict['organization']})['email']

            recipient_name = 'Données Quebec'.decode('utf8')
            subject = 'Suggestion de jeu de données'.decode('utf8')

            body = 'Soumis par %s (%s)\n' % (data_dict["name"], data_dict["email"])

            if (data_dict["category"] != ''):
                body += 'Catégorie de données: %s'.decode('utf8') % data_dict["category"]

            body += 'Nature de la demande: %s'.decode('utf8') % data_dict["suggestion"]

            if (data_dict["usage"] != ''):
                body += 'Utilisation visée: %s'.decode('utf8') % data_dict["usage"]

            try:
                mailer.mail_recipient(recipient_name, mail_to,
                        subject, body)
            except mailer.MailerException:
                raise


            return base.render('suggest/suggest_success.html')


    def suggest_form(self, data=None, errors=None, error_summary=None):
        suggest_new_form = 'suggest/suggest_form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_suggestion(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        c.form = base.render(suggest_new_form, extra_vars=vars)

        return base.render('suggest/form.html')



class SuggestAppController(base.BaseController):

    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))


    def _send_suggestion(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')

            c.form = data_dict['name']
            captcha.check_recaptcha(request)

            #return base.render('suggest/form.html')
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))

        except captcha.CaptchaError:
            error_msg = _(u'Mauvais code captcha. Essayez de nouveau')
            h.flash_error(error_msg)
            return self.suggest_form(data_dict)


        errors = {}
        error_summary = {}

        if (data_dict["email"] == ''):

            errors['email'] = [u'Valeur manquante']
            error_summary['email'] =  u'Valeur manquante'

        if (data_dict["name"] == ''):

            errors['name'] = [u'Valeur manquante']
            error_summary['name'] =  u'Valeur manquante'


        if (data_dict["url"] == ''):

            errors['url'] = [u'Valeur manquante']
            error_summary['url'] =  u'Valeur manquante'


        if (data_dict["suggestion"] == ''):

            errors['suggestion'] = [u'Valeur manquante']
            error_summary['suggestion'] =  u'Valeur manquante'


        if len(errors) > 0:
            return self.suggest_form(data_dict, errors, error_summary)
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.

            if data_dict['organization'] == 'all':
                mail_to = config.get('email_to')
            else:
                mail_to = logic.get_action('organization_show')( {},
                                    {'id': data_dict['organization']})['email']

            recipient_name = 'Données Quebec'.decode('utf8')
            subject = 'Suggestion d\'utilisation de données'.decode('utf8')

            body = 'Soumis par %s (%s)\n' % (data_dict["name"], data_dict["email"])

            body += 'Adresse de l\'utilisation: %s'.decode('utf8') % data_dict["url"]
            body += 'Description de l\'utilisation: %s'.decode('utf8') % data_dict["suggestion"]



            try:
                mailer.mail_recipient(recipient_name, mail_to,
                        subject, body)
            except mailer.MailerException:
                raise


            return base.render('suggestapp/suggest_success.html')


    def suggest_form(self, data=None, errors=None, error_summary=None):
        suggest_new_form = 'suggestapp/suggest_form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_suggestion(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        c.form = base.render(suggest_new_form, extra_vars=vars)

        return base.render('suggestapp/form.html')



class ContactController(base.BaseController):

    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))


    def _send_contact(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')

            c.form = data_dict['name']
            captcha.check_recaptcha(request)
            #return base.render('suggest/form.html')
        except logic.NotAuthorized:
            base.abort(401, _('Vous n\'êtes pas autorisé à accéder à cette page'))
        except captcha.CaptchaError:
            error_msg = _(u'Mauvais code captcha. Veuillez réessayer.')
            h.flash_error(error_msg)
            return self.contact_form(data_dict)

        errors = {}
        error_summary = {}

        if (data_dict["email"] == ''):

            errors['email'] = [u'Valeur manquante']
            error_summary['email'] =  u'Valeur manquante'

        if (data_dict["name"] == ''):

            errors['name'] = [u'Valeur manquante']
            error_summary['name'] =  u'Valeur manquante'


        if (data_dict["content"] == ''):

            errors['content'] = [u'Valeur manquante']
            error_summary['content'] =  u'Valeur manquante'


        if len(errors) > 0:
            return self.suggest_form(data_dict, errors, error_summary)
        else:

            if data_dict['organization'] == 'all':
                mail_to = config.get('email_to')
            else:
                mail_to = logic.get_action('organization_show')( {},
                                    {'id': data_dict['organization']})['email']
                                    
            recipient_name = 'Données Québec'.decode('utf8')
            subject = 'Question/commentaire d\'un visiteur'.decode('utf8')

            body = 'Soumis par %s (%s)\n'.decode('utf8') % (data_dict["name"], data_dict["email"])

            body += 'Demande: %s'.decode('utf8') % data_dict["content"]

            try:
                mailer.mail_recipient(recipient_name, mail_to,
                        subject, body)
            except mailer.MailerException:
                raise


            return base.render('contact/success.html')


    def contact_form(self, data=None, errors=None, error_summary=None):
        suggest_new_form = 'contact/form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_contact(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        c.form = base.render(suggest_new_form, extra_vars=vars)

        return base.render('contact/contact_base.html')
