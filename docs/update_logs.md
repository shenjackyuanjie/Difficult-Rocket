# Difficult Rocket Update Logs

## Readme

- [README](https://github.com/shenjackyuanjie/Difficult-Rocket)
- [中文README](README-cn.md)
- Using [SemVer 2.0.0](https://semver.org/) to manage version

## 202108 V 0.5.0

making

## 20210811 V 0.4.6

### DEBUG

- game window doesn't use input `(*args, **kwargs)` to setup

### Change

- language type `zh-cn` -> `zh-CN`
- game window config now use `configs/main.config` to config
- `on_mouse_click` function's debug message now use `self.lang` to debug message (witch is multi-language)
- server client and main now use `logging.getLogger()`

### Add

- `[window_default]` in `configs/main.config`
- server and client now will output `PID` and `PPID` info as `INFO`
- `client` now change to `ClientWindow`

### Delete

- all game window render has been deleted
- - will be rewritten in 0.5.0
- delete some useless code
- delete some useless file

## 20210723 V 0.4.5

### DEBUG

- `new_thread.py` link of stackoverflow have an extra 'find' in the middle REMOVED

### Add

- `new_thread.py` now can use @new_thread to get a threaded fun

### Change

- `README.md` and `README-cn.md` change URL to file path
- `README.md` and `README-cn.md` some label style change
- Pre-installed `pyglet` upgrade from `1.5.16` -> `1.5.18`
- Pre-installed `json5` upgrade from `0.9.5` -> `0.9.6`


## 20210708 V 0.4.4

### PS

- Nice day everyone!
- I have finish my final exam on grade 8.
- Will soon reach grade 9, so update will be late very much.

### Change

- function `tools.config()` way of raise error change `tools.report_file_error()`
- function `tools.cb()` change name to `tools.format_bool()`
- config.py clear some useless import class
- changing configfile to main.config *doing

### Test change

- `test_config_file.py`
- `test_for_speed.py`
- `test_logging_conf.py`
- `test_speed_of_sprite.py`

## 2021/06/26 V 0.4.3

### DEBUG

- some name_format bug

### Change

- doing: change render pip line ('m really doing)
- default FPS from 120 -> 60

### Add

- add performance_test folder
- add some performances test

## 2021/05/24 V 0.4.2

### DEBUG

- using python version 3.8.9 still report `best3.8+`(lang name)(actually is debugging)

### Change

- change back how configs.py/name_format work(replace str) fix some issue
- doing remake for config sys (lazy yes!)
- clear bin/pyglet (already exits in bin/lib)

### Need Do

- debug name_format

## 2021/04/17 V 0.4.1

PS:

- `Va.b.c`

- a : Big Version (Big rewrite times) (now at DEMO making)
- b : Middle Rewrite Times (Yes I've rewritten for 4 times)
- c : normal updates

### DEBUG

- solve pre-installed lib can't use
- solve pre-installed lib's bug
- some other bugs

### Change

- plan to change config file format to .config (plan to)
- reformat all files (including libs)

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
    - `json5  0.9.5`

PS: now I'm not sure witch lib will be import first

the local lib or the pip libs

So I'll add some other code to make sure that DR will first try to import pip libs

not the local libs (todo)

### DEBUG

- some bugs(I forget them)
