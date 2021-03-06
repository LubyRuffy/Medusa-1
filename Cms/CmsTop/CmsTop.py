#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from Cms.CmsTop import CmsTopRemoteCodeExecution
from Cms.CmsTop import CmsTopSQLInjectionVulnerability
from Cms.CmsTop import CmsTopPathDisclosureVulnerability
from ClassCongregation import Prompt
def Main(ThreadPool,Url,Values,ProxyIp):
    ThreadPool.Append(CmsTopRemoteCodeExecution.medusa, Url, Values, ProxyIp)
    ThreadPool.Append(CmsTopSQLInjectionVulnerability.medusa, Url, Values, ProxyIp)
    ThreadPool.Append(CmsTopPathDisclosureVulnerability.medusa, Url, Values, ProxyIp)
    Prompt("CmsTop")