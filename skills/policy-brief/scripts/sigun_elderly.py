"""시군 노인복지시설 분석용 통계 일괄 조회 (korean-stats 원격 MCP).

사용: python3 sigun_elderly.py 시군명 공단코드 전남코드 인구코드
예:   python3 sigun_elderly.py 여수시 15350AC400M102 A03 46130
코드는 get_table_info(filter=시군명)로 찾는다 (SKILL.md "시군 코드 예" 참고).
"""
import json, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://mcp.gomdori.app/stats"


def call(tool, args):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    raw = urllib.request.urlopen(req, timeout=120).read().decode()
    if raw.startswith("event:"):
        raw = [l[6:] for l in raw.splitlines() if l.startswith("data: ")][-1]
    text = "".join(c.get("text", "") for c in json.loads(raw).get("result", {}).get("content", []))
    try:
        return [(r["period"], r["value"]) for r in json.loads(text).get("data", [])]
    except Exception:
        return text[:200]


def jobs(name, C, A, P):
    j = {"고령비율": {"orgId": "101", "tableId": "DT_1YL20631", "periodType": "Y", "regionName": name, "recentCount": 6},
         "인구": {"orgId": "101", "tableId": "DT_1B040A3", "periodType": "Y", "recentCount": 2, "objL1": P, "itemId": "T20"}}
    for it, nm in [("002", "기관"), ("003", "정원")]:
        for l2 in ["001", "003", "00302", "00305", "10", "1001", "1002", "1003", "1004", "1005", "1006",
                   "11", "1101", "1102", "1103", "1104", "1105", "1106"]:
            j[f"{nm} {l2}"] = {"orgId": "350", "tableId": "DT_35006_N021", "periodType": "Y", "recentCount": 2,
                              "objL1": C, "objL2": l2, "itemId": it}
    for l2 in ["00101", "00102", "00103", "00104", "00107", "00109"]:
        for l3 in ["350060A01", "350060A02", "350060A03"]:
            j[f"인력 {l2} {l3}"] = {"orgId": "350", "tableId": "DT_35006_N022", "periodType": "Y", "recentCount": 2,
                                   "objL1": C, "objL2": l2, "objL3": l3, "itemId": "001"}
    for l2 in ["001", "002", "003", "004", "005", "006", "007"]:
        j[f"수급 등급 {l2}"] = {"orgId": "350", "tableId": "DT_35006_N030", "periodType": "Y", "recentCount": 2,
                               "objL1": C, "objL2": l2, "objL3": "001", "objL4": "0", "itemId": "T001"}
    j["급여비용"] = {"orgId": "350", "tableId": "DT_35006_N030", "periodType": "Y", "recentCount": 1,
                   "objL1": C, "objL2": "001", "objL3": "001", "objL4": "0", "itemId": "T004"}
    for l3 in ["002", "003", "004", "005", "006", "007", "008", "011", "013"]:
        j[f"수급 급여 {l3}"] = {"orgId": "350", "tableId": "DT_35006_N030", "periodType": "Y", "recentCount": 1,
                               "objL1": C, "objL2": "001", "objL3": l3, "objL4": "0", "itemId": "T001"}
    for t, bs in [("DT_215008_007", ["B01", "B02", "B03"]), ("DT_215008_008", ["B01", "B02", "B03"]),
                  ("DT_215008_009", ["B01", "B02", "B03", "B04", "B05", "B06", "B08", "B07"])]:
        for b in bs:
            for it in ["T001", "T002", "T003", "T004"]:
                j[f"{t[-3:]} {b} {it}"] = dict(orgId="215", tableId=t, periodType="F", recentCount=3,
                                               objL1=A, objL2=b, itemId=it)
    F = dict(orgId="215", periodType="F", recentCount=3, objL1=A, itemId="T001")
    j["노인1인가구"] = dict(F, tableId="DT_215008_006", objL2="B02", objL3="C01", objL4="D06")
    j["노인가구계"] = dict(F, tableId="DT_215008_006", objL2="B02", objL3="C01", objL4="D01")
    j["기초수급 노인"] = dict(F, tableId="DT_215008_011", objL2="B02", objL3="C01")
    j["기초수급 전체"] = dict(F, tableId="DT_215008_011", objL2="B01", objL3="C01")
    j["기초연금"] = dict(F, tableId="DT_215008_014", objL2="C01")
    return j


if __name__ == "__main__":
    name, C, A, P = sys.argv[1:5]
    J = jobs(name, C, A, P)
    with ThreadPoolExecutor(6) as ex:
        for k, v in zip(J, ex.map(lambda k: call("get_statistics_data", J[k]), J)):
            print(k, v)
