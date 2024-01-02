; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry_block:
  %".2" = alloca i32
  store i32 4, i32* %".2"
  store i32 7, i32* %".2"
  %".5" = load i32, i32* %".2"
  %".6" = alloca [10 x i8]
  store [10 x i8] c"apples %i\00", [10 x i8]* %".6"
  %".8" = getelementptr [10 x i8], [10 x i8]* %".6", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".5")
  %".10" = load i32, i32* %".2"
  ret i32 %".10"
}
