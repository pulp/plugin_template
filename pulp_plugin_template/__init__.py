import pkg_resources

__version__ = pkg_resources.get_distribution("default_app_config").version

default_app_config = 'pulp_plugin_template.app.PulpPluginTemplatePluginAppConfig'
