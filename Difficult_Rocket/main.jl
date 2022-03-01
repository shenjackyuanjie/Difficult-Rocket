#=
main:
- Julia version: 1.7.2
- Author: shenjack
- Date: 2022-02-19
=#

using GLFW

export GLFW__init__

function GLFW__init__()
    # Create a window and its OpenGL context
    window = GLFW.CreateWindow(1024, 768, "DR-GLFW test")

    # Make the window's context current
    GLFW.MakeContextCurrent(window)
    GLFW.WindowHint(GLFW.CONTEXT_VERSION_MAJOR, 3)
    GLFW.WindowHint(GLFW.CONTEXT_VERSION_MINOR, 3)
    println(GLFW.VulkanSupported())

    glClear() = ccall(@eval(GLFW.GetProcAddress("glClear")), Cvoid, (Cuint,), 0x00004000)

    GC.gc() # Force garbage collection so that improper reference management is more apparent via crashes

    # Loop until the user closes the window
    while !GLFW.WindowShouldClose(window)

        # Render here

        # Swap front and back buffers
        GLFW.SwapBuffers(window)

        # Poll for and process events
        GLFW.PollEvents()
    end

    GLFW.DestroyWindow(window)
end
