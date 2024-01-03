; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry_block:
  %".2" = alloca i32
  store i32 0, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp slt i32 %".4", 10
  br i1 %".5", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
while_loop_entry_0:
  %".7" = load i32, i32* %".2"
  %".8" = icmp eq i32 %".7", 7
  br i1 %".8", label %"while_loop_entry_0.if", label %"while_loop_entry_0.endif"
while_loop_otherwise_0:
  %".36" = load i32, i32* %".2"
  %".37" = alloca [7 x i8]
  store [7 x i8] c"a = %i\00", [7 x i8]* %".37"
  %".39" = getelementptr [7 x i8], [7 x i8]* %".37", i32 0, i32 0
  %".40" = call i32 (i8*, ...) @"printf"(i8* %".39", i32 %".36")
  ret i32 0
while_loop_entry_0.if:
  %".10" = alloca [26 x i8]
  store [26 x i8] c"HIT THE BREAK STATEMENT\0a\00\00", [26 x i8]* %".10"
  %".12" = getelementptr [26 x i8], [26 x i8]* %".10", i32 0, i32 0
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  br label %"while_loop_otherwise_0"
while_loop_entry_0.endif:
  %".15" = load i32, i32* %".2"
  %".16" = icmp eq i32 %".15", 4
  br i1 %".16", label %"while_loop_entry_0.endif.if", label %"while_loop_entry_0.endif.endif"
while_loop_entry_0.endif.if:
  %".18" = alloca [19 x i8]
  store [19 x i8] c"HIT THE CONTINUE\0a\00\00", [19 x i8]* %".18"
  %".20" = getelementptr [19 x i8], [19 x i8]* %".18", i32 0, i32 0
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20")
  %".22" = load i32, i32* %".2"
  %".23" = add i32 %".22", 2
  store i32 %".23", i32* %".2"
  br label %"while_loop_entry_0"
while_loop_entry_0.endif.endif:
  %".26" = alloca [11 x i8]
  store [11 x i8] c"Adding 1\0a\00\00", [11 x i8]* %".26"
  %".28" = getelementptr [11 x i8], [11 x i8]* %".26", i32 0, i32 0
  %".29" = call i32 (i8*, ...) @"printf"(i8* %".28")
  %".30" = load i32, i32* %".2"
  %".31" = add i32 %".30", 1
  store i32 %".31", i32* %".2"
  %".33" = load i32, i32* %".2"
  %".34" = icmp slt i32 %".33", 10
  br i1 %".34", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
}
