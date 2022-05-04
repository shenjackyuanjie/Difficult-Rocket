
struct part
    x::Float64
    y::Float64
    father::Vector{pointer, Nothing}
    children::Vector{(pointer, Nothing)}
end

command_tree = Dict(

)

function command_parser(command_tree, command::String) :: Nothing

end