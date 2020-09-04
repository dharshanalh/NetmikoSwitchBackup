from __future__ import unicode_literals
from netmiko.hp.hp_procurve import HPProcurveSSH, HPProcurveTelnet
from netmiko.hp.hp_comware import HPComwareSSH, HPComwareTelnet
# Following lines should be added here
# 	from netmiko.hp.hp_comwarejinhua import HPComwareJinhuaSSH, HPComwareJinhuaTelnet
# 	from netmiko.hp.hp_comware512900 import HPComware512900SSH, HPComware512900Telnet
# 	from netmiko.hp.hp_comwarefoes import HPComwareFoesSSH, HPComwareFoesTelnet

from netmiko.hp.hp_comwarejinhua import HPComwareJinhuaSSH, HPComwareJinhuaTelnet
from netmiko.hp.hp_comware512900 import HPComware512900SSH, HPComware512900Telnet
from netmiko.hp.hp_comwarefoes import HPComwareFoesSSH, HPComwareFoesTelnet

# following line should be added with following fields
# 'HPComwareJinhuaSSH', 'HPComwareJinhuaTelnet', 'HPComware512900SSH', 'HPComware512900Telnet', 'HPComwareFoesSSH', 'HPComwareFoesTelnet'
__all__ = ['HPProcurveSSH', 'HPProcurveTelnet', 'HPComwareSSH', 'HPComwareTelnet', 'HPComwareJinhuaSSH', 'HPComwareJinhuaTelnet', 'HPComware512900SSH', 'HPComware512900Telnet', 'HPComwareFoesSSH', 'HPComwareFoesTelnet']
