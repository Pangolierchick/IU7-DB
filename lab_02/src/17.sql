insert into accs(id, name, timecreated, profileurl, profilestate)
values(1234, "test_2", 
      (select avg(accs.timecreated)
      from accs), "test.com", 1);
