# SEO·검색 노출 (48개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/seo.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-seo && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-seo && cd /tmp/ccs-seo && git sparse-checkout set skills/ai-traffic-tracking skills/analytics-tracking skills/backlink-analysis skills/canonical-tag skills/content-optimization skills/core-web-vitals skills/directory-submission skills/domain-architecture skills/domain-selection skills/eeat-signals skills/entity-seo skills/favicon-generator skills/featured-snippet skills/generative-engine-optimization skills/google-search-console skills/grokipedia-recommendations skills/heading-structure skills/image-optimization skills/indexing skills/indexnow skills/internal-links skills/keyword-research skills/link-building skills/local-seo skills/meta-description skills/mobile-friendly skills/multi-domain-brand-seo skills/open-graph skills/page-metadata skills/parasite-seo skills/programmatic-seo skills/rendering-strategies skills/robots-txt skills/schema-markup skills/seo-audit skills/seo-monitoring skills/seo-strategy skills/serp-features skills/site-crawlability skills/title-tag skills/traffic-analysis skills/twitter-cards skills/url-slug-generator skills/url-structure skills/video-optimization skills/website-structure skills/xml-sitemap skills/youtube-seo && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [ai-traffic-tracking](../skills/ai-traffic-tracking) | Compatibility pointer for AI assistant referrals and generative search visibility; maintained in Open Analytics. |  |
| [analytics-tracking](../skills/analytics-tracking) | Compatibility pointer for GA4 event, key-event and User-ID tracking; maintained in Open Analytics. |  |
| [backlink-analysis](../skills/backlink-analysis) | When the user wants to analyze backlinks, audit link profile, or identify link issues. Also use when the user mentions "backlink analysis,"  | backlink analysis,·backlink audit,·referring domains, |
| [canonical-tag](../skills/canonical-tag) | Audit and fix duplicate-page canonicalization across protocol, host, slash, default-document, extension, case, and tracking-parameter URL va |  |
| [content-optimization](../skills/content-optimization) | When the user wants to optimize content for SEO—word count, H2 keywords, keyword density, multimedia, tables, lists. Also use when the user  | content length,·word count,·keyword stuffing, |
| [core-web-vitals](../skills/core-web-vitals) | When the user wants to optimize Core Web Vitals, fix LCP, INP, or CLS issues. Also use when the user mentions "Core Web Vitals," "CWV," "LCP | Core Web Vitals,·CWV,·LCP, |
| [directory-submission](../skills/directory-submission) | When the user wants to submit a product or app to directories, curated lists, launch platforms, or app stores—and needs ready-to-paste copy  | directory submission,·get listed,·app store listing, |
| [domain-architecture](../skills/domain-architecture) | When the user wants to decide domain structure for multiple products or brands—subfolder vs subdomain vs independent domain. Also use when t | subfolder vs subdomain,·subdirectory vs subdomain,·multiple products domain, |
| [domain-selection](../skills/domain-selection) | When the user wants to choose an SEO-friendly domain for a new site—brand vs keyword domain, TLD selection, or domain best practices. Also u | domain choice,·pick domain,·SEO-friendly domain, |
| [eeat-signals](../skills/eeat-signals) | When the user wants to improve E-E-A-T, add trust signals, or optimize for expertise and authority. Also use when the user mentions "E-E-A-T | E-E-A-T,·E-E-A-T signals,·experience expertise authority trust, |
| [entity-seo](../skills/entity-seo) | When the user wants to optimize for entity recognition, Knowledge Graph, or entity-based SEO. Also use when the user mentions "entity SEO,"  | entity SEO,·entity optimization,·Knowledge Graph, |
| [favicon-generator](../skills/favicon-generator) | When the user wants to implement, optimize, or audit favicon and app icons. Also use when the user mentions "favicon," "app icon," "browser  | favicon,·app icon,·browser icon, |
| [featured-snippet](../skills/featured-snippet) | When the user wants to optimize for Featured Snippets, Position Zero, or snippet extraction. Also use when the user mentions "featured snipp | featured snippet,·position zero,·snippet optimization, |
| [generative-engine-optimization](../skills/generative-engine-optimization) | When the user wants to optimize for AI search visibility (ChatGPT, Claude, Perplexity, AI Overviews). Also use when the user mentions "GEO," | GEO,·AEO,·generative engine optimization, |
| [google-search-console](../skills/google-search-console) | Compatibility pointer for Search Console performance and indexing analysis; maintained in Open Analytics. |  |
| [grokipedia-recommendations](../skills/grokipedia-recommendations) | When the user wants to add recommendations, links, or content to Grokipedia. Also use when the user mentions "Grokipedia," "GEO wiki," "AI e | Grokipedia,·GEO wiki,·AI encyclopedia, |
| [heading-structure](../skills/heading-structure) | When the user wants to write or optimize H1-H6, fix heading hierarchy, improve content structure, rewrite an H1, or align headings with page |  |
| [image-optimization](../skills/image-optimization) | When the user wants to optimize images for search engines and performance. Also use when the user mentions "image SEO," "alt text," "image c | image SEO,·alt text,·image captions, |
| [indexing](../skills/indexing) | When the user wants to fix indexing issues from Search Console, use noindex, or implement Google Indexing API. Also use when the user mentio | fix indexing,·not indexed,·Crawled - currently not indexed, |
| [indexnow](../skills/indexnow) | When the user wants to implement IndexNow, notify search engines of new/updated URLs, or speed up Bing indexing. Also use when the user ment | IndexNow,·Bing indexing,·URL notification, |
| [internal-links](../skills/internal-links) | When the user wants to optimize internal linking, fix orphan pages, or improve link structure. Also use when the user mentions "internal lin | internal links,·internal linking,·anchor text, |
| [keyword-research](../skills/keyword-research) | When the user wants to research keywords, find target keywords, or analyze search intent. Also use when the user mentions "keyword research, | keyword research,·keyword tool,·target keywords, |
| [link-building](../skills/link-building) | When the user wants to build backlinks, acquire links, or improve off-page SEO. Also use when the user mentions "link building," "backlinks, | link building,·backlinks,·off-page SEO, |
| [local-seo](../skills/local-seo) | When the user wants to optimize for local search, set up Google Business Profile, or build local citations. Also use when the user mentions  | local SEO,·Google Business Profile,·Google Maps, |
| [meta-description](../skills/meta-description) | When the user wants to write, audit, or optimize a meta description, SEO description, SERP snippet candidate, duplicate description, descrip |  |
| [mobile-friendly](../skills/mobile-friendly) | When the user wants to optimize for mobile-first indexing or fix mobile usability. Also use when the user mentions "mobile-friendly," "mobil | mobile-friendly,·mobile-first indexing,·mobile SEO, |
| [multi-domain-brand-seo](../skills/multi-domain-brand-seo) | When the user wants to optimize brand search for a company with multiple domains (e.g. parent company.com vs product.ai). Ensure the parent/ | brand search,·multi-domain SEO,·company domain first, |
| [open-graph](../skills/open-graph) | When the user wants to add, audit, implement, or optimize Open Graph metadata for social sharing, including og:title, og:description, og:ima |  |
| [page-metadata](../skills/page-metadata) | When the user wants a full-page metadata audit or implementation across discovery, search intent, title, description, canonical, robots, hre | metadata audit,·sitewide meta optimization,·metadata implementation, |
| [parasite-seo](../skills/parasite-seo) | When the user wants to choose or execute third-party platform SEO (high-authority sites for rankings or backlinks). Also use when the user m | parasite SEO,·parasitic SEO,·barnacle SEO, |
| [programmatic-seo](../skills/programmatic-seo) | When the user wants to create SEO pages at scale using templates and data—including AI-assisted, grounded copy for per-URL differentiation ( | programmatic SEO,·programmatic SEO pages,·template pages, |
| [rendering-strategies](../skills/rendering-strategies) | When the user wants to choose or optimize rendering strategy for SEO. Also use when the user mentions "SSR," "SSG," "CSR," "ISR," "static re | SSR,·SSG,·CSR, |
| [robots-txt](../skills/robots-txt) | When the user wants to configure, audit, or optimize robots.txt. Also use when the user mentions "robots.txt," "crawler rules," "block crawl | robots.txt,·crawler rules,·block crawlers, |
| [schema-markup](../skills/schema-markup) | When the user wants to add or optimize structured data (Schema.org, JSON-LD). Also use when the user mentions "schema," "structured data," " | schema,·structured data,·JSON-LD, |
| [seo-audit](../skills/seo-audit) | When the user wants to run an SEO audit, technical SEO audit, or site health check. Also use when the user mentions "SEO audit," "technical  | SEO audit,·technical audit,·site audit, |
| [seo-monitoring](../skills/seo-monitoring) | Compatibility pointer for recurring SEO monitoring; maintained in Open Analytics. |  |
| [seo-strategy](../skills/seo-strategy) | When the user wants to plan SEO strategy, prioritize SEO work, or understand the SEO workflow. Also use when the user mentions "SEO strategy | SEO strategy,·SEO plan,·SEO roadmap, |
| [serp-features](../skills/serp-features) | When the user wants to understand or optimize for SERP feature types (PAA, sitelinks, rich results, AI Overviews). Also use when the user me | SERP,·SERP features,·search result features, |
| [site-crawlability](../skills/site-crawlability) | When the user wants to improve crawlability, fix orphan pages, or optimize site structure for search engines. Also use when the user mention | crawlability,·crawl budget,·orphan pages, |
| [title-tag](../skills/title-tag) | When the user wants to write, audit, or optimize an HTML title tag, SEO title, page title, SERP title, browser-tab title, duplicate title, o |  |
| [traffic-analysis](../skills/traffic-analysis) | Compatibility pointer for source, UTM and direct-traffic analysis; maintained in Open Analytics. |  |
| [twitter-cards](../skills/twitter-cards) | When the user wants to add, audit, implement, or optimize Twitter Card metadata for X link previews, including twitter:card, twitter:title,  |  |
| [url-slug-generator](../skills/url-slug-generator) | When the user wants to create, optimize, or validate URL slugs for content pages. Also use when the user mentions "URL slug," "URL path," "b | URL slug,·URL path,·blog URL, |
| [url-structure](../skills/url-structure) | When the user wants to optimize URL structure, fix URL issues, or plan URL hierarchy. Also use when the user mentions "URL structure," "URL  | URL structure,·URL optimization,·slug, |
| [video-optimization](../skills/video-optimization) | When the user wants to optimize videos for Google Search, video sitemap, VideoObject schema, or video SEO on websites. Also use when the use | video SEO,·video sitemap,·VideoObject, |
| [website-structure](../skills/website-structure) | When the user wants to plan website structure, decide which pages to build, or prioritize pages for a new or existing site. Also use when th | website structure,·site structure,·which pages do I need, |
| [xml-sitemap](../skills/xml-sitemap) | When the user wants to create, audit, or optimize sitemap.xml. Also use when the user mentions "sitemap," "sitemap.xml," "sitemap index," "l | sitemap,·sitemap.xml,·sitemap index, |
| [youtube-seo](../skills/youtube-seo) | When the user wants to optimize YouTube videos for search, create video descriptions, or improve channel visibility. Also use when the user  | YouTube SEO,·YouTube description,·YouTube tags, |
