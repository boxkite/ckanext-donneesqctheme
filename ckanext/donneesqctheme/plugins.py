import ckan.logic as logic
import ckan.model as model
import ckan.lib.dictization.model_dictize as md
import logging

from ckan.plugins import (toolkit, IConfigurer, SingletonPlugin, implements,
    IRoutes, IConfigurer, ITemplateHelpers, IGroupForm, IPackageController,
    IOrganizationController, IConfigurable)

from ckan.lib.plugins import DefaultOrganizationForm
from ckan.logic.schema import group_form_schema
from ckan.logic.converters import convert_to_extras, convert_from_extras
from ckan.lib.navl.validators import ignore_missing

from ckanext.hierarchy.plugin import HierarchyForm

import time
import requests
import os
import calendar
import codecs

log = logging.getLogger('ckanext.donneesqctheme')

class CustomTheme(SingletonPlugin):
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "static")


class ContactPagesPlugin(SingletonPlugin):

    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
    implements(ITemplateHelpers, inherit=True)
    implements(IConfigurable, inherit=True)

    def update_config(self, config):
        config['ckan.resource_proxy_enabled'] = True

    def configure(self, config):

        try:
            self.carousel_url = config['donneesqc.carousel_url']
            self.last_articles_url = config['donneesqc.last_articles_url']
            self.tmp = config['donneesqc.tmp_dir']
            self.delay = config['donneesqc.cache_delay']

        except KeyError:
            #Should we throw an error message?
            self.carousel_url = None
            self.last_articles_url = None
            self.tmp = None
            self.delay = None

    def before_map(self, m):
        m.connect('suggest' ,'/suggest',
                    controller='ckanext.donneesqctheme.controller:SuggestController',
                    action='suggest_form')

        m.connect('contact', '/contact',
                    controller='ckanext.donneesqctheme.controller:ContactController',
                    action='contact_form')

        return m

    def _get_content(self,  url, name):
        path = self.tmp + name
        cache_delay = self.delay

        now = calendar.timegm(time.gmtime())
        try:
            html = ''
            if os.path.isfile(path) == False or (now - os.path.getmtime(path)) > cache_delay:
                r = requests.get(url, timeout=1)
                f = codecs.open(path ,'w', encoding='utf8')
                f.write(r.text)
                html += r.text
            else:
                f = codecs.open(path ,'r', encoding='utf8')
                html += f.read()
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None  

        return html      

    def _get_carousel_content(self):
        if self.carousel_url != None:
            return self._get_content(self.carousel_url, 'carousel')
        else:
            return None
 

    def _get_last_articles_content(self):
        if self.last_articles_url != None:
            return self._get_content(self.last_articles_url, 'articles')
        else:
            return None

        

    def get_helpers(self):
        return {
            'get_organizations': _get_organizations,
            'get_carousel_content': self._get_carousel_content,
            'get_last_articles_content': self._get_last_articles_content,
            'get_group_list' : _get_group_list

        }

class OrgPlugin(HierarchyForm):
    implements(IGroupForm, inherit=True)
    implements(IOrganizationController, inherit=True)

    def is_fallback(self):
        return False

    def group_types(self):
        return ['organization']

    def form_to_db_schema(self):
        schema = group_form_schema()

        schema.update({
            'email': [ignore_missing, convert_to_extras]
        })

        return schema

    def db_to_form_schema(self):
        schema = group_form_schema()

        schema.update({
            'email': [convert_from_extras, ignore_missing]
        })

        return schema

    def before_view(self, org_dict):
        org_dict['group_activity_stream'] = logic.get_action(
            'organization_activity_list')(
                {},
                {'id': org_dict['id'], 'offset': 0})

        return org_dict

class PackagePlugin(SingletonPlugin):
    implements(IPackageController, inherit=True)
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_resource('fanstatic', 'donneesqc')

    def before_view(self, pkg_dict):
        #fetch related items
        related_list = logic.get_action('related_list')({}, pkg_dict)
        pkg_dict['related_list'] = related_list

        res_ids = [res['id'] for res in pkg_dict['resources']]
        context = {'model': model, 'session': model.Session}
        view = model.Session.query(model.ResourceView).filter(
            model.ResourceView.resource_id.in_(res_ids)).filter(
            model.ResourceView.featured == True
        ).first()

        if view:
            pkg_dict['view'] = md.resource_view_dictize(view, context)
            pkg_dict['view_res'] = [res for res in pkg_dict['resources']
                    if res['id'] == pkg_dict['view']['resource_id']][0]
        return pkg_dict


def _get_organizations():
    orgs = [
        {'text': 'All Organizations', 'value': 'all'}
    ]
    org_list = logic.get_action('organization_list')({}, {})
    for o in org_list:
        org = logic.get_action('organization_show')({}, {'id': o})
        orgs.append({'text': org['display_name'], 'value': o})

    return orgs

def _get_group_list():

    groups = logic.get_action('group_list')(
        data_dict={'all_fields': True})

    return groups


