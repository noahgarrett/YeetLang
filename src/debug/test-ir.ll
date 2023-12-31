; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"testing"()
{
testing_entry:
  ret i32 5
}

define i32 @"main"()
{
main_entry:
  %".2" = call i32 @"testing"()
  ret i32 %".2"
}
