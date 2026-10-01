#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
myBookSkill 技能分发管理工具 (Skill Distribution Tool)

用法:
    python3 distribute.py --list
    python3 distribute.py --skill test-case-generation --target global
    python3 distribute.py --skill test-case-generation --target /Users/jevons/myCode/f360-deepcheck
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = BASE_DIR / "skills"
GLOBAL_SKILLS_DIR = Path.home() / ".gemini" / "config" / "skills"

def list_skills():
    print(f"\n📦 myBookSkill 仓库可用技能列表 (位于: {SKILLS_DIR}):")
    if not SKILLS_DIR.exists():
        print("  [空] 暂未创建任何技能。")
        return []
    
    skills = []
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)
            print(f"  • {item.name}")
    print()
    return skills

def distribute(skill_name: str, target: str):
    source_skill_path = SKILLS_DIR / skill_name
    if not source_skill_path.exists() or not (source_skill_path / "SKILL.md").exists():
        print(f"❌ 错误: 技能 '{skill_name}' 不存在于 {SKILLS_DIR}")
        sys.exit(1)
        
    if target.lower() == "global":
        dest_dir = GLOBAL_SKILLS_DIR / skill_name
    else:
        target_path = Path(target).resolve()
        # 若传入的是项目根目录，分发到该项目的 .agents/skills/
        if (target_path / ".agents").exists() or target_path.is_dir():
            dest_dir = target_path / ".agents" / "skills" / skill_name
        else:
            dest_dir = target_path / skill_name
            
    dest_dir.parent.mkdir(parents=True, exist_ok=True)
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
        
    shutil.copytree(source_skill_path, dest_dir)
    print(f"✅ 成功分发技能 '{skill_name}' 到目标位置:")
    print(f"   ↳ {dest_dir}")

def main():
    parser = argparse.ArgumentParser(description="myBookSkill 技能统一分发工具")
    parser.add_argument("--list", action="store_true", help="列出所有可用技能")
    parser.add_argument("--skill", type=str, help="要分发的技能名称")
    parser.add_argument("--target", type=str, help="分发目标: 'global' 或具体项目目录路径")
    
    args = parser.parse_args()
    if args.list or len(sys.argv) == 1:
        list_skills()
        return
        
    if not args.skill or not args.target:
        print("❌ 参数不足: 分发技能必须同时指定 --skill 和 --target")
        sys.exit(1)
        
    distribute(args.skill, args.target)

if __name__ == "__main__":
    main()
