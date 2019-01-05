import requests


# Translate between the API and what is used locally
def translate_platform_name(operating_system, preinstalled_software):
    os = {'Linux': 'linux',
          'RHEL': 'rhel',
          'SUSE': 'sles',
          'Windows': 'mswin'}
    software = {'NA': '',
                'SQL Std': 'SQL',
                'SQL Web': 'SQLWeb',
                'SQL Ent': 'SQLEnterprise'}

    return os[operating_system] + software[preinstalled_software]


