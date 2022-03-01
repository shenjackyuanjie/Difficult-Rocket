#=
DR:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-02-19
=#


using PyCall

HiMessage = """
Difficult Rocket is writen by shenjackyuanjie
mail: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888""" :: String


function py__init__()
    println(HiMessage)
    py"""
    import sys
    sys.path.append(".")
    sys.path.append("libs/")
    """
    game = pyimport("Difficult_Rocket.main")
    Game = game.Game()
    Game.start()
end



@timev py__init__()
