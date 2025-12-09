# -*- coding: utf-8 -*-
"""
- 仅校验 pred.json 的格式；
"""

import json
import os
import sys
import zipfile
import shutil
import glob
import logging
from typing import Dict, List, Tuple, Set


# ------------------------ 只校验 pred.json ------------------------
def _validate_pred_format(pred_json) -> Tuple[bool, str]:
    """
    仅对 pred.json 做格式校验：
      - 顶层必须 list
      - 每条包含 record_id(str)、problems(list)
      - problems[*] 必含非空字符串：field、issue_type、rule_id、description
    """
    if not isinstance(pred_json, list):
        return False, "pred.json 顶层必须为数组(list)。"

    for i, rec in enumerate(pred_json):
        if not isinstance(rec, dict):
            return False, f"pred.json 第{i}条应为对象。"
        rid = rec.get("record_id")
        probs = rec.get("problems")
        if not isinstance(rid, str) or not rid.strip():
            return False, f"第{i}条 record_id 缺失或不是非空字符串。"
        if not isinstance(probs, list):
            return False, f"第{i}条 problems 缺失或不是数组。"
        for j, p in enumerate(probs):
            if not isinstance(p, dict):
                return False, f"第{i}条 problems[{j}] 应为对象。"
            for key in ("field", "issue_type", "rule_id", "description"):
                val = p.get(key)
                if not isinstance(val, str) or not val.strip():
                    print(i, rec, p)
                    return False, f"第{i}条 problems[{j}].{key} 缺失或不是非空字符串。"
    return True, ""


# ------------------------ 主入口 ------------------------
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    # 固定指定要校验的文件（test3.json）
    pred_path = "manbobobo.json"

    # 校验文件是否存在
    if not os.path.exists(pred_path):
        print(f"错误：文件 {pred_path} 不存在！")
        print("程序执行结束（因文件不存在）")  # 异常场景也提示结束
        return

    try:
        # 读取并校验文件
        with open(pred_path, "r", encoding="utf-8") as f:
            pred_cases = json.load(f)

        ok, msg = _validate_pred_format(pred_cases)
        if not ok:
            print(f"格式校验失败：{msg}")
        else:
            print('文件格式校验通过：file format is ok.')

        # 核心新增：程序正常完成时的提示
        print("\n✅ 程序已正常完成所有校验流程！")

    except json.JSONDecodeError:
        # 兼容JSON格式错误的场景
        print(f"错误：{pred_path} 不是合法的JSON文件（解析失败）")
        print("\n✅ 程序已正常完成流程（因JSON解析失败终止）")
    except Exception as e:
        # 捕获其他未知异常，仍提示程序完成
        print(f"未知错误：{str(e)}")
        print("\n✅ 程序已正常完成流程（因未知错误终止）")


# 修正入口执行条件
if __name__ == "__main__":
    main()