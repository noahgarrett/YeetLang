; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 25, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp slt i32 %".4", 50
  br i1 %".5", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
while_loop_entry_0:
  %".7" = load i32, i32* %".2"
  %".8" = add i32 %".7", 1
  store i32 %".8", i32* %".2"
  %".10" = load i32, i32* %".2"
  %".11" = alloca [11 x i8]
  store [11 x i8] c"yeet: %i\0a\00\00", [11 x i8]* %".11"
  %".13" = getelementptr [11 x i8], [11 x i8]* %".11", i32 0, i32 0
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", i32 %".10")
  %".15" = load i32, i32* %".2"
  %".16" = icmp slt i32 %".15", 50
  br i1 %".16", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
while_loop_otherwise_0:
  %".18" = load i32, i32* %".2"
  ret i32 %".18"
}
