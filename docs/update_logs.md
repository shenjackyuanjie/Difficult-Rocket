# Difficult Rocket Update Logs

- Thanks `Github copilot` for translate (lazy yes!)
- 感谢 `Github copilot` 的翻译(甚至这句话也是copilot翻译的)

# SR tool PC Update Logs

- 从~~0.6.1~~1.0版本开始，这个更新日志将主要用于记录SRtool的更新
  - 并且使用中文记录更新
- ~~github copilot 真好用~~

## Readme First!
##### most badge can be clicked and jump
[![Generic badge](https://img.shields.io/badge/SemVer-2.0.0-blue.svg)](https://Semver.org/)
![Generic badge](https://img.shields.io/badge/Version-1.0-yellow.svg)

- [![Readme-github](https://img.shields.io/badge/Readme-Github-blue.svg?style=flat-square&logo=Github)](https://github.com/shenjackyuanjie/Difficult-Rocket)
- [![Readme-gitee](https://img.shields.io/badge/Readme-Gitee-blue.svg?style=flat-square&logo=Gitee)](https://gitee.com/shenjackyuanjie/Difficult-Rocket)
- [![Readme-gitee](https://img.shields.io/badge/Readme-中文(点我!)-blue.svg?style=flat-square)](README-cn.md)
- Using [SemVer 2.0.0](https://semver.org/) to manage version

## 202112 V 1.1

### Change

- 以后DR的更新日志不会再在这里同步（咕咕咕）
- 没啥
- 同步了DR的更新（虽说其实没有）

## 20211110 V 1.0 (V 0.6.1)

- 热烈祝贺1.0的发布！
- lazy了，1.1再把一些版本参数改成1.1吧

### Change

- 把`api/translate`移动到根目录下
  - move `api/translate` to root directory
- 现在命令会慢慢消失，而不是立即消失
  - Now the command will disappear slowly, not immediately

### Command

- 现在可以使用`set long xxx(int)` 指令来在拖入图片后设置坐标轴点的长度
  - Now you can use `set long xxx(int)` command to set the length of the axis point
- `set scale xxx(int)` 用于设置坐标缩放
  - `set scale xxx(int)` to set the scale of the coordinate
- 删除了`fps`相关指令(因为没有fps记录器了)
  - Delete `fps` related command (because there is no fps recorder now)

- 命令内容输出使用`CommandText`而不是`str`
  - 也就是说可以使用`CommandText.match`来匹配命令内容
  - command output use `CommandText` instead of `str`
    - means you can use `CommandText.match` to match command content
- 命令解析现在使用新的`CommandText.match`
  - command parse now use new `CommandText.match`

### Add

- `gui/widgets.py` InputBox
  - making

## 20211025 V 0.6.0

#### Command Line Update!

### Change

- now `Difficult Rocket` will only fit python3.8+
  - because `:=`
  - 现在 `Difficult Rocket` 只适用于 python3.8+
    - 因为 `:=` 的使用
- now main crash report handler have new way to handler crash
  - 现在主程序崩溃时的报告处理方式有了新的方式
- now fonts' folder's name is `HarmonyOS_Sans`
  - 现在字体文件夹的名字改为 `HarmonyOS_Sans`

### Add

- `Difficult_Rocket.graphics.widgets.Parts`
  - have many costume value
  - 有很多自定义数值
- `libs/fonts` now have `HarmonyOS_Sans` font
  - 现在 `libs/fonts` 有 `HarmonyOS_Sans` 字体
- handler of `on_key_press` and `on_key_release` and `on_text`
  - 添加了 `on_key_press` 和 `on_key_release` 和 `on_text` 的处理方式
- `game.config` config file
- `lang/en-us.json5` now up to date with `lang/zh-CN.json5`
- `translate/Lang.翻译` same as `Lang.lang`
- `command/CommandLine` to render command line
- `@new_thread` now can option if log this thread to `crash` or not
- `start.cmd` witch could debug easier

### Translate

- Add
  - `window`
    - `message.text`
    - `command.text`
    - `text.motion`
    - `text.motion_select`
    - `setup.use_time_ns`
    - `fonts.found`
    - `game.input_stop`
    - `game.command_stop`
    - `game.window_stop`
    - `game.stop_get`
    - `game.stop`
    - `game.end`
  - `client`
    - `setup.use_time_ns`

### Command

- now you can press `t` to call out a message window
  - or press `/` to open command line
  - not done
  - ~~useless until now~~
- new command
  - `/min_fps`
    - get min fps in 5 second
  - `/max_fps`
    - get max fps in 5 second
  - `/stop`
    - stop the game
  - `/default`
    - switch window size to default size

## 20210928 V 0.5.2

### Change

- now bin folder use the name `Difficult_Rocket`
- now test files no longer have `_test_` prefix
- now will always use local `pyglet` 
  - may change later
- fitting `pypy3.10` (well······ not success (because OpenGL, blame it))
- now `crash-report` have more information
- now when pressed, the sprite will rotate randomly
- now `pyglet.app.run()` use multiprocess
- now will allways use `libs/` lib when using `pyglet` or `json5`
- now `tools.config()` is `tools.load_file()`
- now `lang` file have `server``client` and `window`

### Add

- ~~mods support will be done in 1.0.0~~
  - just maybe
- now you can use `DEBUGGING` to test or check game run stats
  - when `True` it will always make a crash report
- now `Difficult_Rocket.api.translate.Lang` can be used to auto translate text in `configs/lang/xxx.json5`
  - you can use `translate.tr[xxx]` to use translated info
  - and use `.format` to format info's `{}`
  - if translate is not found, `Lang` will try to find translate in default language translate
  - (witch was `zh-CN`)
- `crash` now have more information about multiprocess
- add some unused read_input in `client`
- now when `logs/` is not found logger will info `logger.mkdir`

### DEBUG

- now version on the window will be `0.5.2`

### Delete

- now `client.Client` and `server.Server` only use `net_mode` option
- `api.new_thread` have no more extra line of testing
- `configs/view.json5` now removed

### Translate

- add `mouse.release` and `language` to en-us
- add `language` to `zh-CN`
- add `tr.lang(xx, xx)` that can solve error on getting item from lang file
  - `tr[xxx]` can also use but won't solve error when item not found
  - so best use `tr.lang(xx, xx)`

## 20210902 V 0.5.1

### Change

- crash report's format
- crash report now use multithreading!
- some info in `client`
- `tools/format_bool` now use more clever way to format

### Add

- `on_resize(self, width, height):` in `client`
- auto crash report in `bin/crash/create_crash_report`
- `bin/api/Exp.py` some Exception
- `bin/api/translate` to create a `translate` class that can reload language

## 20210823 V 0.5.0

### Change

- many `sys.path.append()` and
- `try: import xxx except: from bin import xxx` has been removed
- and now IDE won't blame you when you open the file anymore!(LOL)
- `Server` now use Dev to delivery message between thread(will be done in 0.6.0)
- test files now use `_test_*.py` for names

### Add

- `crash.py` to handle and create crash report (not done)
- `DragSprite` (maybe will add in future pyglet update PR has been published)

### Delete

- `name_hanlder` in `configs.py`

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
    - will be rewritten in 0.5.0
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
