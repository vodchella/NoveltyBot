#!/usr/bin/env python3
# -*- coding: utf-8 -*-

SET_USER_ID = """
declare
  idSelf number;
begin
  select max(u.user_id)
  into   idSelf
  from   users u
  where  u.distinguished_name = :user_name;
  pkg_audit.SetUserID(idSelf);
  pkg_session_parameters.SetParameter('Format_Call_Stack', '%s');
end;
"""

UPDATE_REPORT_BODY = """
update xv_templates x set x.template_body = :clob_data where x.xv_template_id = :id
"""

GET_REPORT_NAME = """
select x.template_name from xv_templates x where x.xv_template_id = :id
"""
