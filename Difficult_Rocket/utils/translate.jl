#=
translate:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-04-26
=#

module fonts

export HOS, HOS_C, HOS_S, HOS_T
const HOS = "HarmonyOS Sans" :: String
const HOS_S = "HarmonyOS Sans SC" :: String
const HOS_T = "HarmonyOS Sans TC" :: String
const HOS_C = "HarmonyOS Sans Condensed" :: String

export 鸿蒙字体, 鸿蒙简体, 鸿蒙繁体, 鸿蒙窄体
鸿蒙字体 = HOS
鸿蒙简体 = HOS_S
鸿蒙繁体 = HOS_T
鸿蒙窄体 = HOS_C

export CC, CM, CCPL, CMPL
CC = "Cascadia Code" :: String
CM = "Cascadia Mono" :: String
CCPL = "Cascadia Code PL" :: String
CMPL = "Cascadia Mono PL" :: String

微软等宽 = CC
微软等宽无线 = CM
微软等宽带电线 = CCPL
微软等宽带电线无线 = CMPL


end