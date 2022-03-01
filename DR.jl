#=
DR:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-02-19
=#


include("Difficult_Rocket/main.jl")

HiMessage = """
Difficult Rocket is writen by shenjackyuanjie
mail: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888""" :: String

@timev GLFW__init__()
