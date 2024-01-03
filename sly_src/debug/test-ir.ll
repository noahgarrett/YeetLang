; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
main_entry_block:
  %".2" = alloca i32
  store i32 69, i32* %".2"
  %".4" = alloca float
  store float 0x40515ae140000000, float* %".4"
  %".6" = alloca [5 x i8]
  store [5 x i8] c"yeet\00", [5 x i8]* %".6"
  %".8" = alloca i32
  store i32 0, i32* %".8"
  br label %"for_loop_entry_0"
for_loop_entry_0:
  %".11" = load i32, i32* %".8"
  %".12" = icmp eq i32 %".11", 4
  br i1 %".12", label %"for_loop_entry_0.if", label %"for_loop_entry_0.endif"
for_loop_otherwise_0:
  %".26" = load i32, i32* %".2"
  %".27" = icmp slt i32 %".26", 420
  br i1 %".27", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
for_loop_entry_0.if:
  br label %"for_loop_otherwise_0"
for_loop_entry_0.endif:
  %".15" = load i32, i32* %".8"
  %".16" = alloca [9 x i8]
  store [9 x i8] c"i = %i\0a\00\00", [9 x i8]* %".16"
  %".18" = getelementptr [9 x i8], [9 x i8]* %".16", i32 0, i32 0
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", i32 %".15")
  %".20" = load i32, i32* %".8"
  %".21" = add i32 %".20", 1
  store i32 %".21", i32* %".8"
  %".23" = load i32, i32* %".8"
  %".24" = icmp slt i32 %".23", 10
  br i1 %".24", label %"for_loop_entry_0", label %"for_loop_otherwise_0"
while_loop_entry_1:
  %".29" = load i32, i32* %".2"
  %".30" = add i32 %".29", 10
  store i32 %".30", i32* %".2"
  %".32" = load i32, i32* %".2"
  %".33" = icmp eq i32 %".32", 79
  br i1 %".33", label %"while_loop_entry_1.if", label %"while_loop_entry_1.endif"
while_loop_otherwise_1:
  %".44" = call i32 @"inside_scope"()
  %".45" = alloca [18 x i8]
  store [18 x i8] c"inside_scope = %i\00", [18 x i8]* %".45"
  %".47" = getelementptr [18 x i8], [18 x i8]* %".45", i32 0, i32 0
  %".48" = call i32 (i8*, ...) @"printf"(i8* %".47", i32 %".44")
  ret i32 1
while_loop_entry_1.if:
  br label %"while_loop_entry_1"
while_loop_entry_1.endif:
  %".36" = load i32, i32* %".2"
  %".37" = alloca [9 x i8]
  store [9 x i8] c"x = %i\0a\00\00", [9 x i8]* %".37"
  %".39" = getelementptr [9 x i8], [9 x i8]* %".37", i32 0, i32 0
  %".40" = call i32 (i8*, ...) @"printf"(i8* %".39", i32 %".36")
  %".41" = load i32, i32* %".2"
  %".42" = icmp slt i32 %".41", 420
  br i1 %".42", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
}

define i32 @"inside_scope"()
{
inside_scope_entry_block:
  %".2" = alloca i32
  store i32 49, i32* %".2"
  %".4" = load i32, i32* %".2"
  ret i32 %".4"
}
