create procedure dorepeat(pl INT)
begin
  set @x = 0;
  repeat set @x = @x + 1; until @x > pl end repeat;
end
;


