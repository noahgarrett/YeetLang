; ModuleID = "main"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"print"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = add i32 45, 5
  %".3" = alloca i32
  store i32 %".2", i32* %".3"
}
