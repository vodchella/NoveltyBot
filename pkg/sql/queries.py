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

GET_NONEXISTANT_POLICIES = """
with n as (%s)
select listagg(n.num, ', ')
       within group (order by n.num) as num_list,
       count(*) as cnt
from   n
where  not exists (select 1
                   from   policies p
                   where  p.policy_number = n.num)
"""

UPDATE_RESCINDING_REASON_TO_NULL = """
update policies p
set    p.resciding_reason_id = null,
       p.resciding_date = null
where  p.policy_number in (%s)
"""

SELECT_TEXT_FROM_DUAL = """
select \'%s\' as num from dual
"""
