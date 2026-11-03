# SCHEMA.md 템플릿

위키가 매 세션 **가장 먼저 읽는 규칙서**. 에이전트의 기억이 아니라, 기억을
관리하는 방법을 적는다. 처음부터 완성하지 말 것 — 도메인 + 태그만 있는 1차본으로
시작해, 원하는 검색 결과를 자연어로 요구할 때마다 규칙이 자라게 한다.

```markdown
# SCHEMA

## Domain
<한 문단. 이 위키가 다루는 범위와, 다루지 않는 범위.>

## Layers
- L1 `10. Raw Sources/` — 원본. 불변. 절대 편집 금지.
- L2 `20. Wiki/` — 합성 페이지(concept / entity / comparison). 에이전트가 관리.
- L3 `SCHEMA.md` — 이 문서. 구조와 분류 체계의 단일 진실 원천.

## Tag taxonomy
10~20개만. 예상 질문 목록에서 역으로 도출한다. 여기 없는 태그는 사용 금지.

| canonical | aliases | 설명 |
|---|---|---|
| `cold-outreach` | 콜드메일, cold-email | 첫 접촉 방법 |
| ... | | |

## Page thresholds
- 2개 이상 소스에 등장하거나, 한 소스의 핵심일 때만 페이지를 만든다.
- 스쳐가는 언급은 페이지로 만들지 않는다. 페이지는 200줄을 넘기지 않는다.
- 모든 페이지는 outbound `[[wikilink]]`를 최소 2개 가진다.

## Frontmatter
```yaml
title:
type: concept | entity | comparison | query | transcript
created: / updated:
tags: [taxonomy에 선언된 것만]
sources: [10. Raw Sources/youtube/<id>.md]
confidence: high | medium | low
contested: false
```

## 출처 규약 (이 위키의 존재 이유)
합성 페이지의 모든 주장 아래에 다음 한 줄을 붙인다.

> 출처: <영상 제목> — https://www.youtube.com/watch?v=<ID>&t=<시작초>s
> (00:12:53–00:14:41) "<원문 인용 1~2문장>"

- 시작·끝 시간을 **둘 다** 남긴다. 시작만 남기면 검증이 불가능하다.
- 인용은 원문 그대로. 요약을 인용처럼 쓰지 않는다.
- 여러 영상을 조합한 답변은 조합한 만큼 출처 줄을 쓴다.

## Query protocol
1. `index.md`를 먼저 읽는다.
2. 관련 concept 페이지를 읽는다. 없으면 raw를 grep한다.
3. 답변에 출처 규약을 그대로 적용한다.
4. 답변이 실질적이면 `30. Queries/`에 파일로 남기고 `log.md`에 기록한다.

## Time sensitivity
<시황·법령·가격처럼 시간이 지나면 사실이 뒤집히는 도메인이면 여기에
유효기간과 재검증 주기를 명시한다. 아니면 "해당 없음".>
```

## 진화 방법

새 규칙을 손으로 쓰지 말고, **원하는 결과를 한 문장으로 요구**한 뒤 스키마가
어떻게 바뀌는지 확인한다.

> "검색 결과에 답이 나온 영상의 시작·끝 시간을 원본 링크와 함께 보여줘.
>  가장 단순한 방법으로, 영상 한 개만 시험해줘."

이 한 문장이 layer / claim block / query protocol 규칙을 만들어낸다. 결과가
틀리면 페이지를 고치지 말고 SCHEMA.md를 고친다.
