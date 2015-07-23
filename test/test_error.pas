program test_1;
type
    arr = array [0..50] of integer;
var i,a,b,k,x,y,sum,testfunc : integer;
    aa:arr;
function fib(x:integer):integer;
begin
  if ((x = 0) or (x = 1)) then
    fib:=1
  else
    fib:=fib(x - 2) + fib(x - 1);
end;

function gao(x:integer):integer;
begin
  gao:=7;
end;

begin
 i=10;
 a=fib(10);
 b:=123456
 writeln(b);

 aa[3]:=10; 
 a:=aa[3];
 aa[10]:=10;
 b:=fib(aa[10]);
 writeln(b);
 writeln(gao(8));
end.