; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define float @"test"(float %".1")
{
test_entry:
  %".3" = alloca float
  store float %".1", float* %".3"
  %".5" = load float, float* %".3"
  %".6" = fadd float %".5", 0x4016000000000000
  ret float %".6"
}

define i32 @"main"()
{
main_entry:
  %".2" = alloca float
  store float 0x4016000000000000, float* %".2"
  %".4" = load float, float* %".2"
  %".5" = call float @"test"(float %".4")
  %".6" = alloca [3 x i8]
  store [3 x i8] c"%i\00", [3 x i8]* %".6"
  %".8" = getelementptr [3 x i8], [3 x i8]* %".6", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", float %".5")
  ret i32 0
}
