#=
html:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-04-26
=#

using PyCall

include("../../utils/translate.jl")

struct default_style
    font_name::String
    font_size::UInt8
    bold::Bool
    italic::Bool
end

default_style = default_style(fonts.HOS)