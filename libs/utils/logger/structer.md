# Logger

```
[App -> Logger +-> Handler(Formatter)] -> Queue(string io) -> [File Output] ?
               |-> Handler(Formatter)  -> Console Output]
```

```
[App -> Logger] -> Queue(raw log) -> [Facade +-> Handler(Formatter) -> File Output   ] ?
                                     [       |-> Handler(Formatter) -> Console Output]
```

