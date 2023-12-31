; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 5, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp eq i32 %".4", 5
  br i1 %".5", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  %".7" = alloca [4 x i8]
  store [4 x i8] c"yes\00", [4 x i8]* %".7"
  %".9" = getelementptr [4 x i8], [4 x i8]* %".7", i32 0, i32 0
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9")
  br label %"main_entry.endif"
main_entry.else:
  %".12" = alloca [3 x i8]
  store [3 x i8] c"no\00", [3 x i8]* %".12"
  %".14" = getelementptr [3 x i8], [3 x i8]* %".12", i32 0, i32 0
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14")
  br label %"main_entry.endif"
main_entry.endif:
  ret i32 0
}
