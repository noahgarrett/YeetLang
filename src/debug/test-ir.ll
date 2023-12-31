; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca [19 x i8]
  store [19 x i8] c"I have %i apples..\00", [19 x i8]* %".2"
  %".4" = getelementptr [19 x i8], [19 x i8]* %".2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 69)
  ret i32 1
}
