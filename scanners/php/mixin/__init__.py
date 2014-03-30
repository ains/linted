import lxml.builder as builder


class XmlConfigureMixin(object):
    def build_xml_config(self, root):
        config = self.settings.get_scanner_config()
        rule_settings = self.settings.get_scanner_rules()

        E = builder.ElementMaker()

        for rule_set in config['selected_rule_sets']:
            rule_location = "rulesets/{}".format(rule_set)
            rule_node = E.rule(ref=rule_location)

            custom_rules = []

            for (rule_name, rule_configuration) in rule_settings[rule_set].items():
                if not self.settings.get_rule_enabled(rule_set, rule_name):
                    rule_node.append(E.exclude(name=rule_name))
                else:
                    ref = "{}/{}".format(rule_location, rule_name)
                    custom_rule = E.rule(ref=ref)
                    custom_properties = E.properties(E.priority('1'))

                    for property_name, value in rule_configuration['properties'].items():
                        custom_properties.append(E.property(name=property_name, value=value))
                        custom_rule.append(custom_properties)
                        custom_rules.append(custom_rule)

            root.append(rule_node)
            root.extend(custom_rules)

        return root