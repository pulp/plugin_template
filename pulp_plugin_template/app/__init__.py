from pulpcore.plugin import PulpPluginAppConfig


class PulpPluginTemplatePluginAppConfig(PulpPluginAppConfig):
    """ Entry point for the plugin_template plugin."""
    name = 'pulp_plugin_template.app'
    label = 'pulp_plugin_template'
