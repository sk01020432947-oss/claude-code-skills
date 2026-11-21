# 마케팅·광고·SNS (65개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/marketing.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-marketing && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-marketing && cd /tmp/ccs-marketing && git sparse-checkout set skills/affiliate-marketing skills/app-ads skills/article-content skills/brand-monitoring skills/brand-protection skills/brand-visual-generator skills/branding skills/cold-start-strategy skills/community-forum skills/competitor-research skills/content-marketing skills/content-strategy skills/conversion-optimization skills/creator-program skills/cro skills/ctv-ads skills/customer-research skills/directory-listing-ads skills/discount-marketing-strategy skills/display-ads skills/distribution-channels skills/education-program skills/email-marketing skills/employee-generated-content skills/google-ads skills/growth-funnel skills/gtm-strategy skills/indie-hacker-strategy skills/influencer-marketing skills/integrated-marketing skills/lead-magnets skills/linkedin-ads skills/linkedin-posts skills/localization-strategy skills/marketing-council skills/marketing-ideas skills/marketing-psychology skills/medium-posts skills/meta-ads skills/native-ads skills/offers skills/open-source-strategy skills/paid-ads-strategy skills/pinterest-posts skills/pmf-strategy skills/podcast-marketing skills/pricing-strategy skills/product-hunt-launch skills/product-launch skills/product-marketing skills/public-relations skills/rebranding-strategy skills/reddit-ads skills/reddit-posts skills/referral-program skills/retention-strategy skills/source-to-channels skills/tiktok-ads skills/tiktok-captions skills/translation skills/twitter-x-posts skills/video-marketing skills/visual-content skills/weekly-content-board skills/youtube-ads && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [affiliate-marketing](../skills/affiliate-marketing) | When the user wants to plan, implement, or optimize affiliate marketing strategy. Also use when the user mentions "affiliate marketing," "af | affiliate marketing,·affiliate program strategy,·CPS model, |
| [app-ads](../skills/app-ads) | When the user wants to run app install ads, user acquisition (UA), or promote mobile apps. Also use when the user mentions "app ads," "app i | app ads,·app install ads,·UA, |
| [article-content](../skills/article-content) | When the user wants to write, generate, or create article body content—blog post body, long-form content, how-to guide, listicle. Also use w | write article,·article content,·blog post content, |
| [brand-monitoring](../skills/brand-monitoring) | When the user wants to monitor brand mentions, detect trademark infringement, or set up brand monitoring. Also use when the user mentions "b | brand monitoring,·brand watch,·trademark watch, |
| [brand-protection](../skills/brand-protection) | When the user faces brand impersonation, fake websites, phishing sites, or trademark infringement. Also use when the user mentions "fake sit | fake site,·impersonation,·phishing site, |
| [brand-visual-generator](../skills/brand-visual-generator) | When the user wants to define, audit, or apply visual identity (typography, colors, spacing, design tokens, frontend aesthetics). Also use w | brand style guide,·visual identity,·design system, |
| [branding](../skills/branding) | When the user wants to define, audit, or apply brand strategy—purpose, values, positioning, storytelling, voice, narrative (not only visuals | brand strategy,·brand story,·brand storytelling, |
| [cold-start-strategy](../skills/cold-start-strategy) | When the user wants to plan cold start, get first users, or launch a new product with zero traction. Also use when the user mentions "cold s | cold start,·cold start problem,·first users, |
| [community-forum](../skills/community-forum) | When the user wants to promote via forums, communities, or invite users to join a community. Also use when the user mentions "forum promotio | forum promotion,·Indie Hacker,·Hacker News, |
| [competitor-research](../skills/competitor-research) | When the user wants to analyze competitors for SEO, content, backlinks, or positioning. Also use when the user mentions "competitor analysis | competitor analysis,·competitor research,·competitor keywords, |
| [content-marketing](../skills/content-marketing) | When the user wants to plan content marketing across channels, define content types and formats, or create a content repurposing strategy. A | content marketing strategy,·content types,·content formats, |
| [content-strategy](../skills/content-strategy) | When the user wants to plan content, or asks which topic or piece to prioritize, what to write about, or why posts bring no customers: topic |  |
| [conversion-optimization](../skills/conversion-optimization) | When the user wants to improve conversion rates, run A/B tests, optimize funnels, or reduce friction. Also use when the user mentions "CRO," | CRO,·conversion rate optimization,·A/B test, |
| [creator-program](../skills/creator-program) | When the user wants to plan, implement, or optimize creator program strategy. Also use when the user mentions "creator program," "creator pa | creator program,·creator partnership,·content co-creation, |
| [cro](../skills/cro) | When the user wants more conversions from a page or form, or asks why a page isn't converting, what to change first, or whether to add or re |  |
| [ctv-ads](../skills/ctv-ads) | When the user wants to run CTV, OTT, or streaming TV ads. Also use when the user mentions "CTV ads," "connected TV," "OTT advertising," "str | CTV ads,·connected TV,·OTT advertising, |
| [customer-research](../skills/customer-research) | When the user wants to run or synthesize customer research, or asks what customer quotes, reviews, or feedback really mean, what is safe to  |  |
| [directory-listing-ads](../skills/directory-listing-ads) | When the user wants to run paid ads within directories or marketplaces. Also use when the user mentions "Taaft ads," "Shopify App Store ads, | Taaft ads,·Shopify App Store ads,·G2 sponsored, |
| [discount-marketing-strategy](../skills/discount-marketing-strategy) | When the user wants to plan, implement, or optimize discount and promotional pricing strategy. Also use when the user mentions "discount str | discount strategy,·promo code,·coupon, |
| [display-ads](../skills/display-ads) | When the user wants to run display, banner, or ad network campaigns. Also use when the user mentions "display ads," "banner ads," "ad networ | display ads,·banner ads,·ad network, |
| [distribution-channels](../skills/distribution-channels) | When the user wants to plan product distribution via marketplaces, app stores, or third-party platforms. Also use when the user mentions "di | distribution channels,·marketplace listing,·app store listing, |
| [education-program](../skills/education-program) | When the user wants to plan, implement, or optimize student and education discount programs. Also use when the user mentions "student discou | student discount,·education discount,·student plan, |
| [email-marketing](../skills/email-marketing) | When the user wants to plan email marketing, EDM, newsletter strategy, or email deliverability. Also use when the user mentions "email marke | email marketing,·EDM,·newsletter, |
| [employee-generated-content](../skills/employee-generated-content) | When the user wants to plan, implement, or optimize employee-generated content (EGC) or employee advocacy. Also use when the user mentions " | EGC,·employee advocacy,·employee content, |
| [google-ads](../skills/google-ads) | When the user wants to set up, optimize, or manage Google Ads campaigns. Also use when the user mentions "Google Ads," "Google Search Ads,"  | Google Ads,·Google Search Ads,·PPC, |
| [growth-funnel](../skills/growth-funnel) | When the user wants to plan growth using the AARRR framework, diagnose growth bottlenecks, or map actions across the customer lifecycle. Als | growth funnel,·AARRR,·pirate metrics, |
| [gtm-strategy](../skills/gtm-strategy) | When the user wants to plan go-to-market strategy, GTM framework, or market entry. Also use when the user mentions "GTM," "go-to-market," "m | GTM,·go-to-market,·market entry, |
| [indie-hacker-strategy](../skills/indie-hacker-strategy) | When the user wants indie hacker or bootstrapping founder strategy—growth, channels, Build in Public, or solo founder tactics. Also use when | indie hacker,·indie developer,·bootstrapping, |
| [influencer-marketing](../skills/influencer-marketing) | When the user wants to plan, implement, or optimize influencer marketing strategy. Also use when the user mentions "influencer marketing," " | influencer marketing,·KOL,·creator partnership, |
| [integrated-marketing](../skills/integrated-marketing) | When the user wants to plan integrated marketing, coordinate channels, or clarify program vs channel vs campaign. Also use when the user men | IMC,·integrated marketing,·channel mix, |
| [lead-magnets](../skills/lead-magnets) | When the user wants to plan or improve a lead magnet, or asks what to give away for emails or how much to ask in return (gating, form fields |  |
| [linkedin-ads](../skills/linkedin-ads) | When the user wants to set up, optimize, or manage LinkedIn Ads. Also use when the user mentions "LinkedIn Ads," "LinkedIn Campaign Manager, | LinkedIn Ads,·LinkedIn Campaign Manager,·Sponsored Content, |
| [linkedin-posts](../skills/linkedin-posts) | When the user wants to create LinkedIn post copy or optimize for LinkedIn. Also use when the user mentions "LinkedIn post," "LinkedIn articl | LinkedIn post,·LinkedIn article,·professional post, |
| [localization-strategy](../skills/localization-strategy) | Plan, audit, implement, migrate, or validate localization for multilingual products and websites, including locale scope, market readiness,  |  |
| [marketing-council](../skills/marketing-council) | When the user wants several expert takes on a marketing decision, or asks what a famous marketer would say about it: a simulated board (Seth |  |
| [marketing-ideas](../skills/marketing-ideas) | When the user wants marketing ideas or growth tactics for a software product, or asks what to try to get attention or the next customers wit |  |
| [marketing-psychology](../skills/marketing-psychology) | When the user wants to apply psychology to marketing, or asks why buyers behave or value things as they do, or whether a persuasion tactic i |  |
| [medium-posts](../skills/medium-posts) | When the user wants to write, publish, republish, or optimize posts on Medium.com (canonical tags, distribution, Medium SEO). Also use when  | Medium,·Medium article,·Medium story, |
| [meta-ads](../skills/meta-ads) | When the user wants to set up, optimize, or manage Meta (Facebook/Instagram) Ads. Also use when the user mentions "Meta Ads," "Facebook Ads, | Meta Ads,·Facebook Ads,·Instagram Ads, |
| [native-ads](../skills/native-ads) | When the user wants to run native ads on Taboola, Outbrain, or similar platforms. Also use when the user mentions "native ads," "Taboola," " | native ads,·Taboola,·Outbrain, |
| [offers](../skills/offers) | When the user wants to design or improve the offer itself, or asks why it isn't selling or how to add urgency honestly: value stacking, bonu |  |
| [open-source-strategy](../skills/open-source-strategy) | When the user wants open source strategy, OSS commercialization, or open source growth. Also use when the user mentions "open source strateg | open source strategy,·OSS strategy,·open source commercialization, |
| [paid-ads-strategy](../skills/paid-ads-strategy) | When the user wants to plan paid ads strategy, allocate ad budget, or choose paid channels. Also use when the user mentions "paid ads," "pai | paid ads,·paid media,·PPC, |
| [pinterest-posts](../skills/pinterest-posts) | When the user wants to create Pinterest Pins, optimize Pin descriptions, or grow Pinterest presence. Also use when the user mentions "Pinter | Pinterest,·Pin,·Pinterest SEO, |
| [pmf-strategy](../skills/pmf-strategy) | When the user wants to validate product-market fit, measure PMF, or plan before scaling. Also use when the user mentions "PMF," "product-mar | PMF,·product-market fit,·product market fit, |
| [podcast-marketing](../skills/podcast-marketing) | When the user wants to plan, create, or market a podcast. Also use when the user mentions "podcast," "podcast strategy," "podcast SEO," "sho | podcast,·podcast strategy,·podcast SEO, |
| [pricing-strategy](../skills/pricing-strategy) | When the user wants to plan, design, or optimize pricing strategy and structure. Also use when the user mentions "pricing strategy," "pricin | pricing strategy,·pricing model,·pricing tiers, |
| [product-hunt-launch](../skills/product-hunt-launch) | When the user wants to launch on Product Hunt, prepare a PH submission, or plan launch day (hunter, first comment, timing, upvotes). Also us | Product Hunt,·launch on Product Hunt,·PH launch, |
| [product-launch](../skills/product-launch) | When the user wants to plan a product launch, execute launch channels, or create a launch checklist. Also use when the user mentions "produc | product launch,·launch strategy,·product announcement, |
| [product-marketing](../skills/product-marketing) | When the user wants to create or update the product marketing context doc (.agents/product-marketing.md), or asks what belongs in it or whet |  |
| [public-relations](../skills/public-relations) | When the user wants to plan PR, write a press release, or manage media relations. Also use when the user mentions "public relations," "PR,"  | public relations,·PR,·press release, |
| [rebranding-strategy](../skills/rebranding-strategy) | When the user wants to plan or execute a rebrand—domain change, 301 redirects, migration, or announcement. Also use when the user mentions " | rebranding,·rebrand,·domain change, |
| [reddit-ads](../skills/reddit-ads) | When the user wants to set up, optimize, or manage Reddit Ads. Also use when the user mentions "Reddit Ads," "Promoted Posts," "subreddit ta | Reddit Ads,·Promoted Posts,·subreddit targeting, |
| [reddit-posts](../skills/reddit-posts) | When the user wants to create Reddit post copy, comments, or optimize for Reddit. Also use when the user mentions "Reddit post," "subreddit, | Reddit post,·subreddit,·r/, |
| [referral-program](../skills/referral-program) | When the user wants to plan, implement, or optimize referral program strategy. Also use when the user mentions "referral program," "referral | referral program,·referral marketing,·user referral, |
| [retention-strategy](../skills/retention-strategy) | When the user wants to reduce churn, improve customer retention, or plan lifecycle marketing. Also use when the user mentions "retention," " | retention,·churn,·customer lifecycle, |
| [source-to-channels](../skills/source-to-channels) | 하나의 원천(YouTube URL·웹 글 URL·내 원고/설교 전사본)을 받아 브리프 1장을 만들고, 채널별 산출물(블로그·뉴스레터·스레드·링크드인·카드뉴스·썸네일·쇼츠 대본·소그룹 질문)을 기존 스킬로 병렬 생성한 뒤 검수하는 오케스트레이터. "원소 | 원소스 멀티채널·이 영상/글/설교로 콘텐츠 만들어줘·한 번에 여러 채널 |
| [tiktok-ads](../skills/tiktok-ads) | When the user wants to set up, optimize, or manage TikTok Ads. Also use when the user mentions "TikTok Ads," "TikTok for Business," "TikTok  | TikTok Ads,·TikTok for Business,·TikTok Pixel, |
| [tiktok-captions](../skills/tiktok-captions) | When the user wants to create TikTok video captions, scripts, or optimize for TikTok. Also use when the user mentions "TikTok post," "TikTok | TikTok post,·TikTok caption,·TikTok video, |
| [translation](../skills/translation) | Translate, transcreate, review, or maintain multilingual product and marketing content, including source locking, glossary decisions, langua |  |
| [twitter-x-posts](../skills/twitter-x-posts) | When the user wants to create X (Twitter) post copy, threads, or optimize for X platform. Also use when the user mentions "X post," "X threa | X post,·X thread,·Twitter post, |
| [video-marketing](../skills/video-marketing) | When the user wants to plan video marketing, create video scripts, or optimize for short-form or long-form video. Also use when the user men | video marketing,·video script,·short-form video, |
| [visual-content](../skills/visual-content) | When the user wants to plan, create, or repurpose visual content (images, infographics, social post images) across channels. Also use when t | content images,·social media images,·infographic, |
| [weekly-content-board](../skills/weekly-content-board) | 매주 "이번 주에 뭘 만들지"를 정하는 콘텐츠 의사결정 회의를 Workflow 도구(다이나믹 워크플로우)로 자동화해 승인 가능한 HTML 보고서를 뽑아낸다. "위클리보드", "AI 마케팅 본부", "콘텐츠 기획 회의 자동화", "이번 주 콘텐츠 뭐 만 | 이번 주에 뭘 만들지·위클리보드·AI 마케팅 본부 |
| [youtube-ads](../skills/youtube-ads) | When the user wants to run YouTube ads, set up TrueView or Bumper campaigns, or optimize video ad creative. Also use when the user mentions  | YouTube ads,·TrueView,·Bumper ads, |
