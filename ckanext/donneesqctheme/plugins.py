import ckan.logic as logic

from ckan.plugins import (toolkit, IConfigurer, SingletonPlugin, implements,
    IRoutes, IConfigurer, ITemplateHelpers)

class CustomTheme(SingletonPlugin):
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "static")


class ContactPagesPlugin(SingletonPlugin):

    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
    implements(ITemplateHelpers, inherit=True)

    def update_config(self, config):
        config['ckan.resource_proxy_enabled'] = True

    def before_map(self, m):
        m.connect('suggest' ,'/suggest',
                    controller='ckanext.donneesqctheme.controller:SuggestController',
                    action='suggest_form')

        m.connect('contact', '/contact',
                    controller='ckanext.donneesqctheme.controller:ContactController',
                    action='contact_form')



        return m

    def get_helpers(self):
        return {
            'get_organizations': _get_organizations()
        }

def _get_organizations():
    orgs = [
        {'text': 'All Organizations', 'value': 'all'}
    ]
    org_list = logic.get_action('organization_list')({}, {})
    for o in org_list:
        org = logic.get_action('organization_show')({}, {'id': o})
        orgs.append({'text': org['display_name'], 'value': o})

    return orgs
