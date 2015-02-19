
from ckan.plugins import toolkit, IConfigurer, SingletonPlugin, implements, IRoutes, IConfigurer

class CustomTheme(SingletonPlugin):
    implements(IConfigurer)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "static")


class ContactPagesPlugin(SingletonPlugin):
    
    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)

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