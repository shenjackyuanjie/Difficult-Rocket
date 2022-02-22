#=
some_eval:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-02-22
=#

function boom!(状态::Vector{Int64}, 动作::Vector{Int64})::Bool
    if 动作[1] == 动作[2]
        if 状态[动作[1]] >= 2
            状态[动作[1]] -= 2  # 对应种类粒子减少两个
            状态[2] += 1  # 乙种+1
            return true
        else
            return false
        end
    elseif 状态[动作[1]] >= 1 * 状态[动作[2]] >= 1
        状态[动作[1]] -= 1
        状态[动作[2]] -= 1  # 对应种类粒子减少两个
        状态[(6 - 动作[1] - 动作[2])] += 1  # 第三种粒子+1
        return true
    else
        return false
    end
end

function bumper(层数::Int64, 状态::Vector{Int64}, 动作::Union{Vector{Int64}, Missing} = missing)
#     println("stack: $层数 动作: $动作 状态: $状态")
    if !ismissing(动作)
        if !boom!(状态, 动作)
            return false
        end
    end
    if (状态[1] + 状态[2] + 状态[3]) == 1
        global gets
        gets = [gets[i]+状态[i] for i=1:3]
        return true
    else
        if 层数 <= 3
            for x = 1:3
                Threads.@threads for y = x:3
                    bumper(层数 + 1, copy(状态), [x, y])
                end
            end
        else
            for x = 1:3
                for y = x:3
                    bumper(层数+1, copy(状态), [x, y])
                end
            end
        end
    end
end

gets = [0, 0, 0]

function countspeed()
    last = [0, 0, 0]
    global gets
    for timein = 1:20
        println("ruaa")
        @time sleep(1)
        new = [gets[i]-last[i] for i = 1:3]
        println("总计 $gets    新的 $new")
        last = gets
    end
end

function runbump(times, 状态)
    for x = 1:times
        global gets
        gets = [0, 0, 0]
#         @async countspeed()
        @time bumper(1, 状态, missing)
        sleep(0.2)
        print("$x ")
        println(gets)
    end
end

println(Threads.nthreads())

runbump(20, [6, 4, 5])

