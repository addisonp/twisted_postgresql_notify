# twisted_postgresql_notify
twisted implementation on postgresql notification

requirements
  twisted
  psycopg2
  python 2.7.x
  
  postgresql
    have a trigger that executes a notification (see source code below)
    
begin
execute 'notify ' || new.name || ',''' || new.id || '|' || new.param || '''';
return NULL;
end
