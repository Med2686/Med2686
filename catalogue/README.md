# Catalogue de skills (inactifs)

Skills tiers rangés par catégorie. **Ils ne sont pas chargés par Claude Code** : seuls ceux de
`.claude/skills/` le sont. Ce rangement évite que des centaines de skills de développement
parasitent le déclenchement du mentor et de `ba-fonctionnel`.

```bash
scripts/activer-skill.sh <nom>      # copie le skill dans .claude/skills/ (actif à la session suivante)
scripts/desactiver-skill.sh <nom>   # le retire de .claude/skills/
scripts/update-catalogue.py         # met à jour le catalogue depuis les dépôts sources
```

Pour changer un skill de catégorie : modifiez `categories.tsv`, puis relancez `update-catalogue.py`.
Fichier généré : ne pas modifier à la main.

## Sources

| Source | Dépôt | Commit | Licence |
| --- | --- | --- | --- |
| awesome-claude-skills | [https://github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/tree/be2a406907dbc61b73e6827ded415c96139d13a2) | `be2a406907db` | Apache-2.0 |
| ECC | [https://github.com/affaan-m/ECC](https://github.com/affaan-m/ECC/tree/ef648e01899ba3e8dc6371642deaaf64b4477775) | `ef648e01899b` | MIT |

## Sommaire

- [01-ba-specs-recette-produit](#01-ba-specs-recette-produit) (14)
- [02-redaction-communication](#02-redaction-communication) (13)
- [03-documents-bureautique](#03-documents-bureautique) (12)
- [04-recherche-veille-analyse](#04-recherche-veille-analyse) (17)
- [05-business-vente-marketing-finance](#05-business-vente-marketing-finance) (19)
- [06-secteurs-metier](#06-secteurs-metier) (18)
- [07-dev-langages-frameworks](#07-dev-langages-frameworks) (52)
- [08-dev-tests-qualite](#08-dev-tests-qualite) (36)
- [09-dev-architecture-api-donnees](#09-dev-architecture-api-donnees) (20)
- [10-devops-infra-reseau](#10-devops-infra-reseau) (20)
- [11-securite](#11-securite) (12)
- [12-agents-ia-claude-code](#12-agents-ia-claude-code) (59)
- [13-design-ui-medias](#13-design-ui-medias) (28)
- [14-integrations-apps](#14-integrations-apps) (3)

## 01-ba-specs-recette-produit

| Skill | Source | Description |
| --- | --- | --- |
| `architecture-decision-records` | ECC | Capture architectural decisions as numbered ADR markdown files in docs/adr/ with context, alternatives considered, consequences, and an index README. Use whe… |
| `blueprint` | ECC | Turn a one-line objective into a step-by-step construction plan for multi-session, multi-agent engineering projects: one-PR-sized steps with self-contained c… |
| `click-path-audit` | ECC | Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cancel each other out, pr… |
| `codebase-onboarding` | ECC | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use… |
| `contract-first` | ECC | Coordinate frontend/backend or service-to-service work through one authoritative machine-checkable contract (OpenAPI, AsyncAPI, Protocol Buffers, or JSON Sch… |
| `council` | ECC | Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use when multiple valid paths exist and you need structured disagreement… |
| `dev-team` | ECC | Simulate a collaborative dev team session where multiple role-based personas (PM, Architect, Developer, QA) respond to the same problem together in one sessi… |
| `jira-integration` | ECC | Use this skill when retrieving Jira tickets, analyzing requirements, updating ticket status, adding comments, or transitioning issues. Provides Jira API patt… |
| `living-docs-governance` | ECC | Keep a long-lived project's documentation from rotting by assigning existing project docs clear constitution, map, status, and history roles, then wiring the… |
| `plan-canvas` | ECC | Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes without leaving the page.… |
| `product-capability` | ECC | Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invariants, interfaces, and… |
| `product-lens` | ECC | Validate the why before building through four product diagnostics — a YC-style product diagnostic that produces PRODUCT-BRIEF.md with a go/no-go recommendati… |
| `project-flow-ops` | ECC | Operate execution flow across GitHub and Linear by triaging issues and pull requests, linking active work, and keeping GitHub public-facing while Linear rema… |
| `recursive-decision-ledger` | ECC | Run repeated rollouts ("Prime Gauss" style recursive prompting) while keeping an append-only decision ledger of trials, marks, coherence checks, and promotio… |

## 02-redaction-communication

| Skill | Source | Description |
| --- | --- | --- |
| `article-writing` | ECC | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand… |
| `brand-voice` | ECC | Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and… |
| `changelog-generator` | awesome-claude-skills | Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clea… |
| `content-research-writer` | awesome-claude-skills | Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on… |
| `counterparty-channel-discipline` | ECC | Per-channel strict prompts, mention gating, silent observation, and a communication autonomy policy for agents that sit in shared channels with external coun… |
| `email-ops` | ECC | Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up workflow for ECC. Use when the user wants to organize email, draft o… |
| `growth-log` | ECC | Write growth log entries that extract reusable patterns from completed work — root cause, transferable rule, and a recognizable signal — instead of diary-sty… |
| `i18n-sync` | ECC | Translate and synchronize application JSON locale files using source-key usage, project terminology, and focused validation. Use when adding keys or language… |
| `internal-comms` | awesome-claude-skills | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenev… |
| `messages-ops` | ECC | Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a thread before replyin… |
| `operator-approval-loop` | ECC | Operator approval contract with internal filing notices for agent-drafted outbound messages, hashed drafts, epoch-keyed decisions, durable delivery claims an… |
| `tailored-resume-generator` | awesome-claude-skills | Analyzes job descriptions and generates tailored resumes that highlight relevant experience, skills, and achievements to maximize interview chances |
| `visa-doc-translate` | ECC | Translate visa document images (bank deposit, employment, income, and retirement certificates; HEIC, PNG, or JPG) into English via OCR and produce a bilingua… |

## 03-documents-bureautique

| Skill | Source | Description |
| --- | --- | --- |
| `docx` | awesome-claude-skills | Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude… |
| `esign-field-placement` | ECC | Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, using a fixed signature… |
| `file-organizer` | awesome-claude-skills | Intelligently organizes your files and folders across your computer by understanding context, finding duplicates, suggesting better structures, and automatin… |
| `frontend-slides` | ECC | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a… |
| `google-workspace-ops` | ECC | Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, trackers, decks, and shared documents. Use when the user needs to fi… |
| `invoice-organizer` | awesome-claude-skills | Automatically organizes invoices and receipts for tax preparation by reading messy files, extracting key information, renaming them consistently, and sorting… |
| `master-agreement-generator` | ECC | Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A workflow limited to… |
| `nutrient-document-processing` | ECC | Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. Works with PDFs, DOCX, XLSX, PPTX, HTML, and images. Use when co… |
| `pdf` | awesome-claude-skills | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs… |
| `pptx` | awesome-claude-skills | Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying o… |
| `regex-vs-llm-structured-text` | ECC | Decision framework for parsing structured text (quizzes, forms, invoices, receipts, tables) with a hybrid regex-first pipeline — regex extraction handles 95%… |
| `xlsx` | awesome-claude-skills | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work… |

## 04-recherche-veille-analyse

| Skill | Source | Description |
| --- | --- | --- |
| `benchmark-methodology` | ECC | Score a scoped competitor set into comparable profile cards: nine weighted dimensions (positioning, voice, visual craft, offer packaging, evidence, enterpris… |
| `competitive-ads-extractor` | awesome-claude-skills | Extracts and analyzes competitors' ads from ad libraries (Facebook, LinkedIn, etc.) to understand what messaging, problems, and creative approaches are worki… |
| `competitive-platform-analysis` | ECC | Use when scoping a competitive landscape — identifying, categorising, and score-filtering a competitor set before any benchmarking begins. Decides who counts… |
| `competitive-report-structure` | ECC | Assemble scored competitor profile cards (from benchmark-methodology) into a decision-grade competitive report with landscape map, competitor tiers, benchmar… |
| `deep-research` | ECC | Produce cited research reports from multiple web sources using firecrawl and exa MCP tools — plan sub-questions, search and deep-read sources, then synthesiz… |
| `documentation-lookup` | ECC | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when th… |
| `exa-search` | ECC | Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered… |
| `knowledge-ops` | ECC | Knowledge base management, ingestion, sync, and retrieval across multiple storage layers (local files, MCP memory, vector stores, Git repos). Use when the us… |
| `market-research` | ECC | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use… |
| `prediction-market-oracle-research` | ECC | Research prediction markets as data sources or oracle signals for products, agents, dashboards, and corporate decision intelligence. Use for source-grounded… |
| `research-ops` | ECC | Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation built from current… |
| `scientific-db-pubmed-database` | ECC | Direct PubMed and NCBI E-utilities search workflows for biomedical literature, MeSH queries, PMID lookup, citation retrieval, and API-backed literature monit… |
| `scientific-db-uspto-database` | ECC | USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible IP research logs. U… |
| `scientific-pkg-gget` | ECC | gget CLI and Python workflow for quick genomic database queries, sequence lookup, BLAST-style searches, enrichment checks, and reproducible bioinformatics ev… |
| `scientific-thinking-literature-review` | ECC | Systematic literature-review workflow for academic, biomedical, technical, and scientific topics, including search planning, source screening, synthesis, cit… |
| `scientific-thinking-scholar-evaluation` | ECC | Structured scholarly-work evaluation for papers, proposals, literature reviews, methods sections, evidence quality, citation support, and research-writing fe… |
| `search-first` | ECC | Research-before-coding workflow: search npm/PyPI, MCP servers, skills, and GitHub for existing tools before writing custom code, then adopt, extend, or build… |

## 05-business-vente-marketing-finance

| Skill | Source | Description |
| --- | --- | --- |
| `brand-discovery` | ECC | Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice, narrative, founder t… |
| `connections-optimizer` | ECC | Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recommendations, and channel-specific warm outreach drafted in the user's… |
| `content-engine` | ECC | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social… |
| `crosspost` | ECC | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identica… |
| `customer-billing-ops` | ECC | Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-portal recovery, and plan analysis using connected billing tools lik… |
| `domain-name-brainstormer` | awesome-claude-skills | Generates creative domain name ideas for your project and checks availability across multiple TLDs (.com, .io, .dev, .ai, etc.). Saves hours of brainstorming… |
| `ecc-tools-cost-audit` | ECC | Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway PR creation, quota bypass, premium-model leakage, duplicate jobs, or… |
| `finance-billing-ops` | ECC | Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapshot, pricing compariso… |
| `investor-materials` | ECC | Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use when the user needs inv… |
| `investor-outreach` | ECC | Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants outreach to angels, VCs… |
| `lead-intelligence` | ECC | AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking, warm path discovery… |
| `lead-research-assistant` | awesome-claude-skills | Identifies high-quality leads for your product or service by analyzing your business, searching for target companies, and providing actionable contact strate… |
| `marketing-campaign` | ECC | End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy, email sequences, s… |
| `raffle-winner-picker` | awesome-claude-skills | Picks random winners from lists, spreadsheets, or Google Sheets for giveaways, raffles, and contests. Ensures fair, unbiased selection with transparency. |
| `seo` | ECC | Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content strategy. Use when the… |
| `social-graph-ranker` | ECC | Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap analysis across X and LinkedIn. Use when the user wants the reusable… |
| `social-publisher` | ECC | Agent-driven scheduling and publishing of social media posts across 13 platforms via SocialClaw. Use when the user wants to publish to X, LinkedIn, Instagram… |
| `twitter-algorithm-optimizer` | awesome-claude-skills | Analyze and optimize tweets for maximum reach using Twitter's open-source algorithm insights. Rewrite and edit user tweets to improve engagement and visibili… |
| `x-api` | ECC | X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits, and platform-native… |

## 06-secteurs-metier

| Skill | Source | Description |
| --- | --- | --- |
| `carrier-relationship-management` | ECC | Manage truckload, LTL, and intermodal carrier portfolios: sourcing and FMCSA vetting, freight rate and fuel-surcharge negotiation, RFPs and routing guides, c… |
| `customs-trade-compliance` | ECC | Codified customs and trade compliance expertise — HS/HTS tariff classification with GRI rules, commercial invoices and entry documentation, Incoterms 2020, F… |
| `energy-procurement` | ECC | Procure electricity and natural gas for commercial and industrial facilities: tariff and rate-schedule optimization, demand-charge mitigation, supplier RFPs,… |
| `healthcare-cdss-patterns` | ECC | Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA), alert severity cla… |
| `healthcare-emr-patterns` | ECC | EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workflows, prescription generation, clinical decision support integratio… |
| `healthcare-eval-harness` | ECC | Patient safety evaluation harness for healthcare application deployments. Automated test suites for CDSS accuracy, PHI exposure, clinical workflow integrity,… |
| `healthcare-phi-compliance` | ECC | Protected Health Information (PHI) and PII compliance patterns for healthcare applications: data classification, row-level access control, tamper-proof audit… |
| `hipaa-compliance` | ECC | HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is explicitly framed around HIPAA, PHI handling, covered entities, BAAs,… |
| `inventory-demand-planning` | ECC | Codified demand planning expertise for multi-location retailers: demand forecasting method selection, ABC/XYZ segmentation, safety stock and reorder-point op… |
| `ito-baskets` | ECC | Read-only Itô basket and prediction-market data skill. Index the live basket catalog, compare a basket against user-supplied research or a watchlist, build a… |
| `ito-compute` | ECC | Query live GPU inventory, submit an authenticated Itô fixed-rate RFQ, inspect RFQ or procurement status, revoke device credentials, and run explicitly gated… |
| `ito-inference` | ECC | Inspect the availability of model serving on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confir… |
| `ito-training` | ECC | Inspect the availability of ML training on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confirme… |
| `logistics-exception-management` | ECC | Codified freight-exception handling expertise for shipment delays, damages, losses, shortages, and carrier disputes, with escalation protocols, carrier-speci… |
| `prediction-market-risk-review` | ECC | Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk. Use before any workf… |
| `production-scheduling` | ECC | Codified expertise for production scheduling, job sequencing, line balancing, changeover optimization, and bottleneck resolution in discrete and batch manufa… |
| `quality-nonconformance` | ECC | Quality control and non-conformance management for regulated manufacturing (FDA 21 CFR 820, IATF 16949, AS9100): NCR lifecycle and disposition, 5-Why/Ishikaw… |
| `returns-reverse-logistics` | ECC | Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims manageme… |

## 07-dev-langages-frameworks

| Skill | Source | Description |
| --- | --- | --- |
| `android-clean-architecture` | ECC | Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patter… |
| `angular-developer` | ECC | Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practices on reactivity (sig… |
| `bun-runtime` | ECC | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support. |
| `code-tour` | ECC | Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, architecture walkthrou… |
| `codehealth-mcp` | ECC | Real-time structural Code Health via CodeScene MCP — review before edits, verify score deltas after changes, gate commits and PRs. Use when reviewing code qu… |
| `coding-standards` | ECC | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framewo… |
| `compose-multiplatform-patterns` | ECC | Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI. Use when… |
| `content-hash-cache-pattern` | ECC | Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation. Use when repeated… |
| `cpp-coding-standards` | ECC | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and i… |
| `dart-flutter-patterns` | ECC | Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, state management (BLoC… |
| `django-celery` | ECC | Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Use when adding backgr… |
| `django-patterns` | ECC | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps. Use when building… |
| `dotnet-patterns` | ECC | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET applications. Use w… |
| `error-handling` | ECC | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, and user-facing error… |
| `evm-token-decimals` | ECC | Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift, and safe normaliza… |
| `fastapi-patterns` | ECC | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorization, transactional se… |
| `foundation-models-on-device` | ECC | Apple FoundationModels framework for on-device LLM — text generation, guided generation with @Generable, tool calling, and snapshot streaming in iOS 26+. Use… |
| `frontend-patterns` | ECC | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or reviewing React or… |
| `generating-python-installer` | ECC | Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist slimming, DLL footprint analysis, and Inno Setup packaging to ship the… |
| `git-workflow` | ECC | Git workflow patterns including branching strategies, commit conventions, keeping history clean and readable, tidying local commits before merging, merge vs… |
| `github-ops` | ECC | GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security monitoring using th… |
| `golang-patterns` | ECC | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications. Use when writing or reviewing Go cod… |
| `inherit-legacy-style` | ECC | Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conflicts with the operator one at a time, and writing… |
| `java-coding-standards` | ECC | Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, reactive patterns, and… |
| `jpa-patterns` | ECC | JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in Spring Boot. Use wh… |
| `kotlin-coroutines-flows` | ECC | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing. Use when writing co… |
| `kotlin-exposed-patterns` | ECC | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use… |
| `kotlin-ktor-patterns` | ECC | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing. Use when buildi… |
| `kotlin-patterns` | ECC | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety,… |
| `laravel-patterns` | ECC | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps. Use when bu… |
| `laravel-plugin-discovery` | ECC | Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibi… |
| `nestjs-patterns` | ECC | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade TypeScript backends. Use… |
| `nextjs-turbopack` | ECC | Next.js 16+ and Turbopack guidance — incremental Rust bundling, file-system caching, faster dev startup and HMR, Turbopack vs webpack tradeoffs, and the midd… |
| `nodejs-keccak256` | ECC | Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks selectors, signatures,… |
| `nuxt4-patterns` | ECC | Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR-safe data fetching with useFetch and useAsyncData. Use when buildin… |
| `perl-patterns` | ECC | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or reviewing modern Perl 5.36… |
| `plankton-code-quality` | ECC | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Use when setting up wri… |
| `python-patterns` | ECC | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. Use when writing or re… |
| `quarkus-patterns` | ECC | Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI services, data access with Panache, and async processing. Use for Jav… |
| `rails-patterns` | ECC | Ruby on Rails framework patterns for Rails 7.1+ and 8.x apps. Covers the directory contract, skinny controllers with service objects, form objects, query obj… |
| `react-native-patterns` | ECC | React Native and Expo app patterns — Expo Router navigation, state separation (server/client/route/form), TanStack Query data fetching with Zod, performant l… |
| `react-patterns` | ECC | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetching, state manageme… |
| `react-performance` | ECC | React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-labs/agent-skills). Org… |
| `rust-patterns` | ECC | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications. Use when writing or r… |
| `springboot-patterns` | ECC | Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java Spring Boot backend w… |
| `swift-actor-persistence` | ECC | Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage, eliminating data races by design. Use when persisting data in… |
| `swift-concurrency-6-2` | ECC | Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances for main actor types.… |
| `swiftui-patterns` | ECC | SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/macOS UI best practi… |
| `tinystruct-patterns` | ECC | Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on tinystruct — including… |
| `ui-to-vue` | ECC | Use when the user has UI screenshots or design exports that need batch conversion into Vue 3 components, especially with Vant, Element Plus, or Ant Design Vue. |
| `vite-patterns` | ECC | Vite build tool patterns including config, plugins, HMR, env variables, proxy setup, SSR, library mode, dependency pre-bundling, and build optimization. Acti… |
| `vue-patterns` | ECC | Vue.js 3 Composition API patterns, component architecture, reactivity best practices, Pinia state management, Vue Router navigation, and Nuxt SSR patterns. A… |

## 08-dev-tests-qualite

| Skill | Source | Description |
| --- | --- | --- |
| `ai-regression-testing` | ECC | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and pattern… |
| `benchmark` | ECC | Measure performance baselines and detect regressions across browser Core Web Vitals (LCP, INP, CLS, page weight), API endpoint latency percentiles, and build… |
| `benchmark-optimization-loop` | ECC | Convert 'make it faster' requests into a bounded measured optimization loop — baseline first, generate one-hypothesis variants, benchmark each against a corr… |
| `browser-qa` | ECC | Run automated post-deploy UI verification with a browser automation MCP (claude-in-chrome, Playwright, or Puppeteer): console-error and Core Web Vitals smoke… |
| `canary-watch` | ECC | Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regre… |
| `cpp-testing` | ECC | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers. |
| `csharp-testing` | ECC | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when writing or reviewing xU… |
| `django-tdd` | ECC | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Use when writing Djang… |
| `django-verification` | ECC | Run the full Django verification loop — environment check, mypy/ruff/black linting, migration safety, pytest with coverage targets, pip-audit and bandit secu… |
| `e2e-testing` | ECC | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. Use when writing Playwr… |
| `flutter-dart-code-review` | ECC | Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, MobX, Signals)… |
| `fsharp-testing` | ECC | F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices. Use when writing F#… |
| `golang-testing` | ECC | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices. Use… |
| `kotlin-testing` | ECC | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin prac… |
| `laravel-tdd` | ECC | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. Use when writing Laravel t… |
| `laravel-verification` | ECC | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness. Use when verifyi… |
| `orch-add-feature` | ECC | Orchestrate building a brand-new feature end to end — research, plan, TDD implementation, review, and gated commit — by delegating each phase to the matching… |
| `orch-build-mvp` | ECC | Orchestrate bootstrapping a working MVP from a design or spec document — ingest the SDD/PRD, plan thin vertical slices, scaffold the first end-to-end slice,… |
| `orch-change-feature` | ECC | Orchestrate altering an existing, working feature to new desired behavior — update its tests to the new spec, change the implementation to match, review, and… |
| `orch-fix-defect` | ECC | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase to the matching ECC a… |
| `orch-pipeline` | ECC | Shared orchestration engine behind the orch-* skill family — the gated Research-Plan-TDD-Review-Commit pipeline, size classifier, agent and command map, and… |
| `orch-refine-code` | ECC | Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without changing behavior, keep tests green, review, and gated commit. Use… |
| `perl-testing` | ECC | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. Use when writing Perl tests with T… |
| `production-audit` | ECC | Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge checks, and "what breaks in prod?" questions without sending repo… |
| `python-testing` | ECC | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. Use when writing pytest tests — fixtu… |
| `quarkus-tdd` | ECC | Test-driven development for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel testing, and JaCoCo. Use when adding features, fixing bugs, or refact… |
| `quarkus-verification` | ECC | Verification loop for Quarkus projects: build, static analysis (Checkstyle, PMD, SpotBugs), tests with JaCoCo coverage, OWASP dependency and container securi… |
| `react-testing` | ECC | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the decision boundary betwee… |
| `rust-testing` | ECC | Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology. Use whe… |
| `springboot-tdd` | ECC | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bugs, or refactoring. |
| `springboot-verification` | ECC | Run the full Spring Boot verification loop — Maven or Gradle build, SpotBugs, PMD, and Checkstyle static analysis, unit and Testcontainers integration tests… |
| `swift-protocol-di-testing` | ECC | Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Swift Testing. Use whe… |
| `tdd-workflow` | ECC | Test-driven development workflow: write a failing test first, watch it fail, implement the smallest change to green, then refactor with 80%+ coverage across… |
| `verification-loop` | ECC | Run a six-phase verification of a Claude Code session's work — build, type check, lint, tests with coverage, security grep, and diff review — then produce a… |
| `webapp-testing` | awesome-claude-skills | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing… |
| `windows-desktop-e2e` | ECC | E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto and Windows UI Automation. Use when writing E2E tests for a Window… |

## 09-dev-architecture-api-donnees

| Skill | Source | Description |
| --- | --- | --- |
| `api-connector-builder` | ECC | Build a new API connector or provider by matching the target repo's existing integration pattern exactly. Use when adding one more integration without invent… |
| `api-design` | ECC | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.… |
| `backend-patterns` | ECC | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. Use when build… |
| `clickhouse-io` | ECC | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. Use when writing… |
| `data-scraper-agent` | ECC | Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Runs on a schedule, enri… |
| `data-throughput-accelerator` | ECC | Diagnose and accelerate large data movement — ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, and table synchronization — by isolatin… |
| `database-migrations` | ECC | Safe, reversible database migration patterns: forward-only production changes, expand-contract zero-downtime renames, concurrent indexes, batched backfills,… |
| `hexagonal-architecture` | ECC | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orchestration across TypeS… |
| `latency-critical-systems` | ECC | Optimize and verify latency-sensitive systems — realtime dashboards, market data feeds, streaming agents, execution gateways, queues, and caches — by trackin… |
| `mailtrap-email-integration` | ECC | Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, and API authenticatio… |
| `mcp-builder` | awesome-claude-skills | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use whe… |
| `mcp-server-patterns` | ECC | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for lates… |
| `ml-adoption-playbook` | ECC | End-to-end methodology for AI agents and software engineers to add machine learning algorithms to existing non-ML codebases. Covers problem framing, data rea… |
| `mle-workflow` | ECC | Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and rollback. Use when… |
| `mysql-patterns` | ECC | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. Use when designing MySQL or MariaD… |
| `postgres-patterns` | ECC | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when designing PostgreSQL s… |
| `prisma-patterns` | ECC | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count… |
| `pytorch-patterns` | ECC | PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architectures, and data loading.… |
| `recsys-pipeline-architect` | ECC | Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework popularized by… |
| `redis-patterns` | ECC | Redis data structure patterns, caching strategies, distributed locks, rate limiting, pub/sub, and connection management for production applications. Use when… |

## 10-devops-infra-reseau

| Skill | Source | Description |
| --- | --- | --- |
| `cisco-ios-patterns` | ECC | Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe change-window verificati… |
| `dashboard-builder` | ECC | Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. Use when turning metrics into a working dashboard… |
| `deployment-patterns` | ECC | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists for web appli… |
| `docker-patterns` | ECC | Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orches… |
| `flox-environments` | ECC | Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use when setting up projec… |
| `homelab-network-readiness` | ECC | Readiness checklist for homelab VLAN segmentation, local DNS filtering (Pi-hole, AdGuard Home), and WireGuard-style remote access. Use when planning or revie… |
| `homelab-network-setup` | ECC | Practical home and homelab network planning for gateways, switches, access points, IP ranges, DHCP reservations, DNS, cabling, and common beginner mistakes.… |
| `homelab-pihole-dns` | ECC | Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS resolution on a home ne… |
| `homelab-vlan-segmentation` | ECC | Segmenting home networks into VLANs for IoT, guest, trusted, and server traffic using UniFi, pfSense/OPNsense, and MikroTik — including switch trunk config,… |
| `homelab-wireguard-vpn` | ECC | WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home network from mobile and l… |
| `kubernetes-patterns` | ECC | Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for production-grade deploymen… |
| `netmiko-ssh-automation` | ECC | Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network automation error han… |
| `network-bgp-diagnostics` | ECC | Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence collection. Use when a… |
| `network-config-validation` | ECC | Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale references, management-p… |
| `network-interface-health` | ECC | Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, and Linux hosts. Use… |
| `opensource-pipeline` | ECC | Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager). Triggers: '/openso… |
| `repo-scan` | ECC | Bootstrap pointer that installs the external repo-scan skill from a pinned, reviewable commit. Use when repo-scan must be installed before running its cross-… |
| `terminal-opener` | ECC | Open an executable and its argument array in a visible terminal window through a reusable, shell-free launch plan with dry-run, JSON, capability detection, d… |
| `terminal-ops` | ECC | Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow fix pushed with exa… |
| `uncloud` | ECC | Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices, publishing ports, s… |

## 11-securite

| Skill | Source | Description |
| --- | --- | --- |
| `defi-amm-security` | ECC | Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation attacks, oracle manipu… |
| `django-security` | ECC | Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure deployment configuration… |
| `gateguard` | ECC | PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit) attempt until the agent presents concrete facts (importers, data sch… |
| `laravel-security` | ECC | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployment configurations. U… |
| `llm-trading-agent-security` | ECC | Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send simulation, circuit bre… |
| `perl-security` | ECC | Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/SQLi/CSRF), and perlc… |
| `quarkus-security` | ECC | Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators,… |
| `safety-guard` | ECC | Guard against destructive operations with three modes: Careful intercepts dangerous commands (rm -rf, git push --force, DROP TABLE) for confirmation, Freeze… |
| `security-bounty-hunter` | ECC | Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely reachable vulnerabilities that qualify for real reports instead of n… |
| `security-review` | ECC | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Pro… |
| `security-scan` | ECC | Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Checks CLAUD… |
| `springboot-security` | ECC | Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring Boot services. Use… |

## 12-agents-ia-claude-code

| Skill | Source | Description |
| --- | --- | --- |
| `agent-architecture-audit` | ECC | Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for wrapper regression, memory pollution, tool discipline failures, hid… |
| `agent-eval` | ECC | Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency metrics. Use when choo… |
| `agent-harness-construction` | ECC | Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates. Use when defining or revising an agent'… |
| `agent-introspection-debugging` | ECC | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. Use when an agent run fails… |
| `agent-payment-x402` | ECC | Add x402 payment execution to AI agents with per-task budgets, spending controls, and non-custodial wallets. Supports Base through agentwallet-sdk and X Laye… |
| `agent-self-evaluation` | ECC | Use after completing any non-trivial task. The agent self-rates its output on 5 axes — accuracy, completeness, clarity, actionability, conciseness — with con… |
| `agent-sort` | ECC | Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, rules, hooks, and extras into DAILY vs LIBRARY buckets using paral… |
| `agentic-engineering` | ECC | Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. Use when planning or executing engineering work that… |
| `agentic-os` | ECC | Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, specialist agents, slash commands, file-based memory, scheduled au… |
| `ai-first-engineering` | ECC | Engineering operating model for teams where AI agents generate a large share of implementation output. Use when setting team process, review gates, or owners… |
| `automation-audit-ops` | ECC | Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user wants to know which jobs, hooks, connectors, MCP servers, or wrappe… |
| `autonomous-agent-harness` | ECC | Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone… |
| `autonomous-loops` | ECC | Patterns and architectures for autonomous Claude Code loops — from simple sequential pipelines to RFC-driven multi-agent DAG systems. Retained for compatibil… |
| `ck` | ECC | Persistent per-project memory for Claude Code (Context Keeper) driven by deterministic Node.js /ck commands: init, save, resume, info, list, forget, and v1-t… |
| `claude-devfleet` | ECC | Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progress, and read structur… |
| `config-gc` | ECC | Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, caches) for redundant,… |
| `configure-ecc` | ECC | Run the conversational ECC setup wizard inside the current harness: inventory the install, collect scope (user/project/local) and hook mode (off/minimal/stan… |
| `context-budget` | ECC | Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized… |
| `continuous-agent-loop` | ECC | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. Use when running an agent loop that must self-check, gate on… |
| `continuous-learning` | ECC | [DEPRECATED - use continuous-learning-v2] Legacy v1 stop-hook skill extractor. v2 is a strict superset with instinct-based, project-scoped, hook-reliable lea… |
| `continuous-learning-v2` | ECC | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agen… |
| `cost-aware-llm-pipeline` | ECC | Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic, and prompt caching. Use when LLM spend needs t… |
| `cost-tracking` | ECC | Track and report Claude Code token usage, spending, and budgets from the local ECC cost-tracker metrics log. Use when the user asks about costs, spending, us… |
| `council-multi-model` | ECC | Add one optional external Codex critique after the existing council has produced a decision draft. Use when an ambiguous, high-consequence decision would ben… |
| `delivery-gate` | ECC | Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (surface text heuristics), stale learning logs (files… |
| `developer-growth-analysis` | awesome-claude-skills | Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant learning resources f… |
| `dmux-workflows` | ECC | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex, OpenCode, and other… |
| `dynamic-workflow-mode` | ECC | Design task-local harnesses, eval gates, and reusable skill extraction for Claude dynamic workflow mode and other adaptive agent harnesses. Use when building… |
| `ecc-guide` | ECC | Answer questions about ECC by reading the live repo surface — agents, skills, commands, hooks, rules, install profiles, and docs — instead of memory. Use whe… |
| `ecc-recipes` | ECC | Map a described workflow to the right ECC command group with run-order and stop condition, or browse all command-group recipe families read live from the com… |
| `enterprise-agent-ops` | ECC | Operational controls for long-lived or cloud-hosted agent systems — runtime lifecycle (start, pause, stop, restart), observability (logs, metrics, traces), l… |
| `eval-harness` | ECC | Eval-driven development (EDD) framework for AI coding sessions — define capability and regression evals before coding, grade with code-based, model-based, ru… |
| `gan-style-harness` | ECC | GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harness design paper. Use… |
| `hermes-imports` | ECC | Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifacts. Use when preparing a Hermes workflow for public ECC reuse witho… |
| `hookify-rules` | ECC | Create and configure hookify rules — markdown files with YAML frontmatter that match bash, file, prompt, or stop events by regex or conditions and show warn/… |
| `iterative-retrieval` | ECC | Pattern for progressively refining context retrieval to solve the subagent context problem. Use when a subagent lacks the context it needs and retrieval must… |
| `langsmith-fetch` | awesome-claude-skills | Debug LangChain and LangGraph agents by fetching execution traces from LangSmith Studio. Use when debugging agent behavior, investigating errors, analyzing t… |
| `loop-design-check` | ECC | Design a goal-oriented agent loop or review one for failure modes: spinning, Goodhart-gaming the verifier, or running a wrong answer to completion. Covers ma… |
| `nanoclaw-repl` | ECC | Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for model switching, skill… |
| `nasiko-control-plane` | ECC | Manage the experimental Nasiko CLI lifecycle through ECC — read-only status checks, consent-gated install of the pinned qualified version with dry-run previe… |
| `openclaw-persona-forge` | ECC | 为 OpenClaw AI Agent 锻造完整的龙虾灵魂方案。根据用户偏好或随机抽卡， 输出身份定位、灵魂描述(SOUL.md)、角色化底线规则、名字和头像生图提示词。 如当前环境提供已审核的生图 skill，可自动生成统一风格头像图片。 当用户需要创建、设计或定制 OpenClaw 龙虾灵魂时使用。 不适用于… |
| `parallel-execution-optimizer` | ECC | Speed up a task by turning it into a dependency graph of parallel lanes with a lane matrix, batched reads and checks, write surfaces isolated by file, worktr… |
| `plan-orchestrate` | ECC | Read a plan document, decompose it into steps, design a per-step agent chain from the ECC catalogue, and emit ready-to-paste /orchestrate custom prompts. Gen… |
| `prompt-optimizer` | ECC | Analyze draft prompts, detect intent and missing context, match ECC commands, skills, and agents, and output a ready-to-paste optimized prompt with diagnosis… |
| `ralphinho-rfc-pipeline` | ECC | Split an RFC into a multi-agent execution DAG — decompose into work units with dependencies and acceptance tests, run research, plan, implement, test, and re… |
| `rules-distill` | ECC | Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files. Use when the same principle keeps rec… |
| `santa-method` | ECC | Multi-agent adversarial verification: two independent reviewers with the same rubric must both pass before output ships, with a fix-and-re-review convergence… |
| `skill-comply` | ECC | Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, runs agents, classifie… |
| `skill-creator` | awesome-claude-skills | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capa… |
| `skill-scout` | ECC | Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. Use when the user wants to create, build, fork, or find a skil… |
| `skill-share` | awesome-claude-skills | A skill that creates new Claude skills and automatically shares them on Slack using Rube for seamless team collaboration and skill discovery. |
| `skill-stocktake` | ECC | Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequential subagent batch e… |
| `strategic-compact` | ECC | Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. Use when a session is… |
| `team-agent-orchestration` | ECC | Run team-based orchestration for agent squads: work items with owners and scope, agent Kanban state, branch isolation, control pane visibility, and merge gat… |
| `team-builder` | ECC | Interactive picker that discovers available agent personas via the claude agents command and agents/ markdown globs, groups them into domains, has the user s… |
| `token-budget-advisor` | ECC | Offer a choice of response depth (25%/50%/75%/100%) with token estimates before answering, then answer at that level. Use when the user asks to control respo… |
| `unified-memory` | ECC | Share durable, inspectable context and handoffs between Claude, Codex, Hermes, Cursor, OpenCode, and other agents through the local ECC Memory Vault. Use whe… |
| `unified-notifications-ops` | ECC | Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use when the real proble… |
| `workspace-surface-audit` | ECC | Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value ECC-native skills, hooks, agents,… |

## 13-design-ui-medias

| Skill | Source | Description |
| --- | --- | --- |
| `accessibility` | ECC | Design, implement, and audit accessible UI to WCAG 2.2 Level AA across Web, iOS, and Android — semantic ARIA roles and labels, accessibility traits and hints… |
| `artifacts-builder` | awesome-claude-skills | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use… |
| `blender-motion-state-inspection` | ECC | Use this skill when inspecting Blender characters, rigs, poses, animation retargeting, ground contact, facing direction, or model-vs-motion alignment where s… |
| `brand-guidelines` | awesome-claude-skills | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand co… |
| `canvas-design` | awesome-claude-skills | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art… |
| `design-system` | ECC | Generate a design system from an existing codebase or audit one for visual consistency: extract tokens (colors, typography, spacing, shadows) into design-tok… |
| `fal-ai-media` | ECC | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-… |
| `frontend-a11y` | ECC | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and screen reader suppor… |
| `frontend-design-direction` | ECC | Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications, components, landing… |
| `image-enhancer` | awesome-claude-skills | Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity. Perfect for preparing images for presentations, docu… |
| `ios-icon-gen` | ECC | Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source icons from 200+ colle… |
| `liquid-glass-design` | ECC | iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing for SwiftUI, UIKit, and WidgetKit. Use when buildi… |
| `make-interfaces-feel-better` | ECC | Apply concrete design-engineering details that make interfaces feel polished. Use when reviewing or improving UI spacing, typography, borders, shadows, motio… |
| `manim-video` | ECC | Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if need… |
| `motion-advanced` | ECC | Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG path drawing, custom hooks, imperative sequences (useAnimate), loa… |
| `motion-foundations` | ECC | Motion tokens, spring presets, performance rules, device adaptation, accessibility enforcement, and SSR safety for React / Next.js using motion/react. Founda… |
| `motion-patterns` | ECC | Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, page transitions, exit animations, scroll, and layout — built on mot… |
| `remotion-video-creation` | ECC | Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transitions, and more. Use… |
| `slack-gif-creator` | awesome-claude-skills | Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints and composable animation primitives. This skill applies when use… |
| `taste` | ECC | Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop family — a named-genre aesthetic vocabulary, mood +… |
| `taste-application` | ECC | Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the reference's cut rhythm, generate on fal, grade with… |
| `taste-distillation` | ECC | Measure a set of reference videos into a reusable style pack - colour grade as a 3D LUT, cut rhythm as a shot-length distribution, hero stills, screen-blend… |
| `tasteforge-video` | ECC | Use for file-driven multimodal image, video, and 3D-asset discovery; taste interviews; distill or apply workflows; style-pack validation; editable EDL/FCPXML… |
| `theme-factory` | awesome-claude-skills | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors… |
| `ui-demo` | ECC | Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web applicati… |
| `video-downloader` | awesome-claude-skills | Download YouTube videos with customizable quality and format options. Use this skill when the user asks to download, save, or grab YouTube videos. Supports v… |
| `video-editing` | ECC | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion… |
| `videodb` | ECC | Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs, or RTSP feeds, build spoken and scene indexes… |

## 14-integrations-apps

| Skill | Source | Description |
| --- | --- | --- |
| `composio-skills` | awesome-claude-skills | Lot de 832 skills « <app>-automation » ; nécessitent un compte et une clé API Composio. |
| `connect` | awesome-claude-skills | Connect Claude to any app. Send emails, create issues, post messages, update databases - take real actions across Gmail, Slack, GitHub, Notion, and 1000+ ser… |
| `connect-apps` | awesome-claude-skills | Connect Claude to external apps like Gmail, Slack, GitHub. Use this skill when the user wants to send emails, create issues, post messages, or take actions i… |
