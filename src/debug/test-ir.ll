; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 25, i32* %".2"
  store i32 5, i32* %".2"
  %".5" = load i32, i32* %".2"
  ret i32 %".5"
}
