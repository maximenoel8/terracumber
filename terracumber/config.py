"""Manage HCL files as configuration files"""
import hcl2

def read_config(path):
    """Return a dictionary with all the variables from a HCL file"""
    config = {}
    with open(path, 'r') as cfg:
        hcl_data = hcl2.load(cfg)
        if 'variable' not in hcl_data.keys():
            return config
        for var_block in hcl_data['variable']:
            for var_name, var_attributes in var_block.items():
                # Some python-hcl2 versions include surrounding quotes in the key name
                var_name = var_name.strip('"')
                # python-hcl2 <4.0 wraps each variable's attributes in a list
                if isinstance(var_attributes, list):
                    if not var_attributes:
                        continue
                    var_attributes = var_attributes[0]
                try:
                    value = var_attributes['default']
                    # python-hcl2 <4.0 also wraps scalar values in lists
                    if isinstance(value, list):
                        value = value[0] if value else None
                    if value is None:
                        config[var_name] = 'null'
                    else:
                        config[var_name] = value
                except (KeyError, TypeError):
                    # KeyError: no 'default' defined (e.g. SCC_USER)
                    # TypeError: unexpected format from an older python-hcl2
                    pass
    return config
