# Difficult Rocket Update Logs

## 2021/04/09 V 0.2.3/4

### Add 

- support many things(also forget)

### Change

- `tools.name_handler()` now use `str.format` to handler str
- `DR/sys_value` folder now move to `DR/configs/sys_value`

### DEBUG

- many `tools.name_handler()` use bug(cause crashes)
- `{date}` can be successful use in `tools.name_handler()` (if you define the format of date)
- log file's filename incorrect (should be `xxxx-xx-xx xx-xx-xx DR.log` but be `{date} DR.log`)

## 2021/03/27 V 0.2.2/1

### Add

- add local libs
    - `pyglet 1.5.15`
    - `json   0.9.5`

PS: now I'm not sure witch lib will be import first

the local lib or the pip libs

So I'll add some other code to make sure that DR will first try to import pip libs

not the local libs (todo)

### DEBUG

- some bugs(I forget them)
