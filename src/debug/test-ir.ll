; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = add i32 1, 2
  %".3" = mul i32 3, 4
  %".4" = sub i32 4, 2
  %".5" = sdiv i32 %".3", %".4"
  %".6" = sdiv i32 %".5", 2
  %".7" = sub i32 %".2", %".6"
  %".8" = alloca i32
  store i32 %".7", i32* %".8"
  %".10" = load i32, i32* %".8"
  ret i32 %".10"
}
