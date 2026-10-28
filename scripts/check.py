"""AI 개념 지도 점검·안내.

usage:
  python scripts/check.py            # graph.json·articles 일관성 검사. 문제 있으면 종료 코드 1
  python scripts/check.py next [n]   # 다음에 정리할 planned 노드 n개(우선순위 → 얕은 깊이 → 추가 순)
  python scripts/check.py stats      # 큰 가지별 노드 수(전체/정리)
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent


def load():
    return json.loads((ROOT / "data" / "graph.json").read_text(encoding="utf-8"))


def depth(byid, n):
    d = 0
    while n.get("parent"):
        n, d = byid[n["parent"]], d + 1
    return d


def domain_of(byid, n):
    """노드가 속한 큰 가지(depth 1 조상)의 id. 루트는 'root'."""
    if not n.get("parent"):
        return "root"
    while byid[n["parent"]].get("parent"):
        n = byid[n["parent"]]
    return n["id"]


def check(g):
    errs = []
    byid = {}
    for n in g["nodes"]:
        if n["id"] in byid:
            errs.append(f"중복 id: {n['id']}")
        byid[n["id"]] = n
    roots = [n for n in g["nodes"] if not n.get("parent")]
    if len(roots) != 1:
        errs.append(f"루트가 {len(roots)}개")
    for n in g["nodes"]:
        i = n["id"]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i):
            errs.append(f"id 형식: {i}")
        if n.get("parent") and n["parent"] not in byid:
            errs.append(f"부모 없음: {i} → {n['parent']}")
        if n.get("parent") in byid and n.get("domain") != domain_of(byid, n):
            errs.append(f"domain 값: {i} = {n.get('domain')} (큰 가지 id {domain_of(byid, n)}여야 함)")
        if n.get("status") not in ("planned", "done"):
            errs.append(f"status 값: {i}")
        art = ROOT / "articles" / f"{i}.md"
        if n.get("status") == "done" and not art.exists():
            errs.append(f"글 없음: {i}")
        for r in n.get("related", []):
            if r not in byid:
                errs.append(f"related 없음: {i} → {r}")
    for art in (ROOT / "articles").glob("*.md"):
        if art.stem not in byid:
            errs.append(f"노드 없는 글: {art.name}")
            continue
        text = art.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(#([^)]+)\)", text):
            if link not in byid:
                errs.append(f"깨진 노드 링크: {art.name} → #{link}")
        if text.count("```") % 2:
            errs.append(f"코드 블록 안 닫힘: {art.name}")
    return errs


def main():
    g = load()
    byid = {n["id"]: n for n in g["nodes"]}
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "next":
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        order = {n["id"]: i for i, n in enumerate(g["nodes"])}
        todo = [n for n in g["nodes"] if n.get("status") == "planned"]
        todo.sort(key=lambda n: (n.get("priority", 5), depth(byid, n), order[n["id"]]))
        for n in todo[:k]:
            print(f"{n['id']}\t{n['label']}\t부모={n.get('parent')}\tp={n.get('priority', 5)}\t{n.get('summary', '')}")
        print(f"planned {len(todo)}개 남음")
    elif cmd == "stats":
        tops = [n for n in g["nodes"] if n.get("parent") and not byid[n["parent"]].get("parent")]
        for t in tops:
            ns = [n for n in g["nodes"] if n.get("domain") == t["id"]]
            print(f"{t['id']}\t{t['label']}\t{len(ns)}\tdone {sum(n.get('status') == 'done' for n in ns)}")
        print(f"큰 가지 {len(tops)}개")
    else:
        errs = check(g)
        print("\n".join(errs) if errs else f"OK · 노드 {len(g['nodes'])}개")
        sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
