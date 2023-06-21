/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */


use std::collections::HashMap;

type TranslateMapper = HashMap<String, HashMap<String, HashMap<String, String>>>;

pub struct Translater {
    pub data: TranslateMapper,
    pub language: String,
}
