; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca [10 x i8]
  store [10 x i8] c"apples %i\00", [10 x i8]* %".2"
  %".4" = getelementptr [10 x i8], [10 x i8]* %".2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 2)
  ret i32 1
}
