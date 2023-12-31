; ModuleID = "main"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"print"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca [8 x i8]
  store [8 x i8] c"pples %\00", [8 x i8]* %".2"
  %".4" = getelementptr [8 x i8], [8 x i8]* %".2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"print"(i8* %".4", i32 12)
}
