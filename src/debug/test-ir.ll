; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"in_mandelbrot"(float %".1", float %".2", float %".3")
{
in_mandelbrot_entry:
  %".5" = alloca float
  store float %".1", float* %".5"
  %".7" = alloca float
  store float %".2", float* %".7"
  %".9" = alloca float
  store float %".3", float* %".9"
  %".11" = alloca float
  store float              0x0, float* %".11"
  %".13" = alloca float
  store float              0x0, float* %".13"
  %".15" = alloca float
  store float              0x0, float* %".15"
  %".17" = load float, float* %".9"
  %".18" = fcmp ogt float %".17",              0x0
  br i1 %".18", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
while_loop_entry_0:
  %".20" = load float, float* %".11"
  %".21" = load float, float* %".11"
  %".22" = fmul float %".20", %".21"
  %".23" = load float, float* %".13"
  %".24" = load float, float* %".13"
  %".25" = fmul float %".23", %".24"
  %".26" = fsub float %".22", %".25"
  %".27" = load float, float* %".5"
  %".28" = fadd float %".26", %".27"
  store float %".28", float* %".15"
  %".30" = load float, float* %".11"
  %".31" = fmul float 0x4000000000000000, %".30"
  %".32" = load float, float* %".13"
  %".33" = fmul float %".31", %".32"
  %".34" = load float, float* %".7"
  %".35" = fadd float %".33", %".34"
  store float %".35", float* %".13"
  %".37" = load float, float* %".15"
  store float %".37", float* %".11"
  %".39" = load float, float* %".9"
  %".40" = fsub float %".39", 0x3ff0000000000000
  store float %".40", float* %".9"
  %".42" = load float, float* %".11"
  %".43" = load float, float* %".11"
  %".44" = fmul float %".42", %".43"
  %".45" = load float, float* %".13"
  %".46" = load float, float* %".13"
  %".47" = fmul float %".45", %".46"
  %".48" = fadd float %".44", %".47"
  %".49" = fcmp ogt float %".48", 0x4010000000000000
  br i1 %".49", label %"while_loop_entry_0.if", label %"while_loop_entry_0.endif"
while_loop_otherwise_0:
  ret i32 1
while_loop_entry_0.if:
  ret i32 0
while_loop_entry_0.endif:
  %".52" = load float, float* %".9"
  %".53" = fcmp ogt float %".52",              0x0
  br i1 %".53", label %"while_loop_entry_0", label %"while_loop_otherwise_0"
}

define i32 @"mandel"()
{
mandel_entry:
  %".2" = fmul float 0x4000000000000000, 0xbff0000000000000
  %".3" = alloca float
  store float %".2", float* %".3"
  %".5" = alloca float
  store float 0x3ff0000000000000, float* %".5"
  %".7" = fmul float 0x3ff8000000000000, 0xbff0000000000000
  %".8" = alloca float
  store float %".7", float* %".8"
  %".10" = alloca float
  store float 0x3ff8000000000000, float* %".10"
  %".12" = alloca float
  store float 0x4054000000000000, float* %".12"
  %".14" = alloca float
  store float 0x4044000000000000, float* %".14"
  %".16" = alloca float
  store float 0x408f400000000000, float* %".16"
  %".18" = load float, float* %".5"
  %".19" = load float, float* %".3"
  %".20" = fsub float %".18", %".19"
  %".21" = load float, float* %".12"
  %".22" = fdiv float %".20", %".21"
  %".23" = alloca float
  store float %".22", float* %".23"
  %".25" = load float, float* %".10"
  %".26" = load float, float* %".8"
  %".27" = fsub float %".25", %".26"
  %".28" = load float, float* %".14"
  %".29" = fdiv float %".27", %".28"
  %".30" = alloca float
  store float %".29", float* %".30"
  %".32" = load float, float* %".10"
  %".33" = alloca float
  store float %".32", float* %".33"
  %".35" = alloca float
  store float              0x0, float* %".35"
  %".37" = load float, float* %".33"
  %".38" = load float, float* %".8"
  %".39" = fcmp oge float %".37", %".38"
  br i1 %".39", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
while_loop_entry_1:
  %".41" = load float, float* %".3"
  store float %".41", float* %".35"
  %".43" = load float, float* %".35"
  %".44" = load float, float* %".5"
  %".45" = fcmp olt float %".43", %".44"
  br i1 %".45", label %"while_loop_entry_2", label %"while_loop_otherwise_2"
while_loop_otherwise_1:
  ret i32 0
while_loop_entry_2:
  %".47" = load float, float* %".35"
  %".48" = load float, float* %".33"
  %".49" = load float, float* %".16"
  %".50" = call i32 @"in_mandelbrot"(float %".47", float %".48", float %".49")
  %".51" = icmp eq i32 %".50", 1
  br i1 %".51", label %"while_loop_entry_2.if", label %"while_loop_entry_2.else"
while_loop_otherwise_2:
  %".71" = alloca [2 x i8]
  store [2 x i8] c"\0a\00", [2 x i8]* %".71"
  %".73" = getelementptr [2 x i8], [2 x i8]* %".71", i32 0, i32 0
  %".74" = call i32 (i8*, ...) @"printf"(i8* %".73")
  %".75" = load float, float* %".33"
  %".76" = load float, float* %".30"
  %".77" = fsub float %".75", %".76"
  store float %".77", float* %".33"
  %".79" = load float, float* %".33"
  %".80" = load float, float* %".8"
  %".81" = fcmp oge float %".79", %".80"
  br i1 %".81", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
while_loop_entry_2.if:
  %".53" = alloca [2 x i8]
  store [2 x i8] c"*\00", [2 x i8]* %".53"
  %".55" = getelementptr [2 x i8], [2 x i8]* %".53", i32 0, i32 0
  %".56" = call i32 (i8*, ...) @"printf"(i8* %".55")
  br label %"while_loop_entry_2.endif"
while_loop_entry_2.else:
  %".58" = alloca [2 x i8]
  store [2 x i8] c".\00", [2 x i8]* %".58"
  %".60" = getelementptr [2 x i8], [2 x i8]* %".58", i32 0, i32 0
  %".61" = call i32 (i8*, ...) @"printf"(i8* %".60")
  br label %"while_loop_entry_2.endif"
while_loop_entry_2.endif:
  %".63" = load float, float* %".35"
  %".64" = load float, float* %".23"
  %".65" = fadd float %".63", %".64"
  store float %".65", float* %".35"
  %".67" = load float, float* %".35"
  %".68" = load float, float* %".5"
  %".69" = fcmp olt float %".67", %".68"
  br i1 %".69", label %"while_loop_entry_2", label %"while_loop_otherwise_2"
}

define i32 @"main"()
{
main_entry:
  %".2" = call i32 @"mandel"()
  ret i32 %".2"
}
