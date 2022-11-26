function run {
    python3.8.exe -O DR.py
}
function viz_run {
    viztracer.exe --output_file ./logs/viz_result.json --open --tracer_entries 10000000 DR.py
}
if ($args -eq "run") {
    run
} elseif ($args -eq "viz") {
    viz_run
} else {
    run
}
pause