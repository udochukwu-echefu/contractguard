import { useEffect } from "react"
import {
  ArrowRight,
  Check,
  ChevronRight,
  CircleAlert,
  FileCheck2,
  FileSearch,
  GitCompareArrows,
  LockKeyhole,
  Quote,
  ScanSearch,
  ShieldCheck,
} from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"

const APP_URL = "https://contractguard-h5bvgcytmdwx2m3lfqwbkg.streamlit.app/"

function Brand() {
  return (
    <a className="brand" href="#top" aria-label="ContractGuard home">
      <span className="brand-mark" aria-hidden="true">
        <span>C</span>
        <span>G</span>
      </span>
      <span className="brand-name">ContractGuard</span>
    </a>
  )
}

function ProductFrame({ compact = false }) {
  return (
    <div className={`product-frame ${compact ? "product-frame-compact" : ""}`} role="img" aria-label="Example ContractGuard lease review showing an evidence-linked high-attention finding">
      <div className="product-window-bar">
        <div className="product-window-brand">
          <span className="product-window-mark">CG</span>
          <span>Lease review</span>
        </div>
        <Badge variant="dark">Evidence linked</Badge>
      </div>
      <div className="product-report-heading">
        <div>
          <span className="product-overline">Review report</span>
          <h3>Residential Lease Agreement</h3>
          <p>Tenant perspective · Lagos State · 12 pages</p>
        </div>
        <span className="attention-pill"><CircleAlert /> High attention</span>
      </div>
      <div className="product-summary" aria-label="Review summary">
        <span><strong>3</strong> high</span>
        <span><strong>1</strong> medium</span>
        <span><strong>2</strong> possible gaps</span>
        <span><strong>8</strong> obligations</span>
      </div>
      <div className="product-tabs" aria-hidden="true">
        <span>Overview</span>
        <span className="active">Risks</span>
        <span>Negotiate</span>
        <span>Obligations</span>
      </div>
      <div className="product-finding">
        <div className="finding-number">01</div>
        <div className="finding-copy">
          <div className="finding-title-row">
            <h4>Unrestricted entry rights</h4>
            <Badge>High attention</Badge>
          </div>
          <p>The landlord may enter at any time without prior notice, which may conflict with quiet enjoyment and privacy expectations.</p>
          <div className="evidence-row">
            <Quote aria-hidden="true" />
            <div>
              <span>Section 7 · Page 6</span>
              <blockquote>“The Landlord or their agents may enter the Premises at any time of day or night...”</blockquote>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function App() {
  useEffect(() => {
    const elements = document.querySelectorAll("[data-reveal]")
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.setAttribute("data-visible", "true")
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.12 },
    )
    elements.forEach((element) => observer.observe(element))

    let progressFrame
    const updateScrollProgress = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight
      const progress = scrollable > 0 ? window.scrollY / scrollable : 0
      document.documentElement.style.setProperty("--scroll-progress", Math.min(Math.max(progress, 0), 1))
      progressFrame = undefined
    }
    const handleScroll = () => {
      if (!progressFrame) progressFrame = window.requestAnimationFrame(updateScrollProgress)
    }
    updateScrollProgress()
    window.addEventListener("scroll", handleScroll, { passive: true })
    window.addEventListener("resize", handleScroll)

    return () => {
      observer.disconnect()
      window.removeEventListener("scroll", handleScroll)
      window.removeEventListener("resize", handleScroll)
      if (progressFrame) window.cancelAnimationFrame(progressFrame)
      document.documentElement.style.removeProperty("--scroll-progress")
    }
  }, [])

  return (
    <div className="site-shell" id="top">
      <div className="scroll-progress" aria-hidden="true" />
      <a className="skip-link" href="#main-content">Skip to content</a>
      <header className="site-header">
        <div className="nav-shell">
          <Brand />
          <nav className="nav-links" aria-label="Primary navigation">
            <a href="#workflow">Workflow</a>
            <a href="#risk-detection">Risk detection</a>
            <a href="#trust">Trust</a>
          </nav>
          <Button asChild size="sm">
            <a href={APP_URL}>Open workspace <ArrowRight /></a>
          </Button>
        </div>
      </header>

      <main id="main-content">
        <section className="hero section-shell" aria-labelledby="hero-title">
          <div className="hero-copy" data-reveal>
            <Badge className="hero-badge"><ScanSearch /> Contract risk intelligence</Badge>
            <h1 id="hero-title" aria-label="Find the clause that changes the deal.">
              <span className="hero-line" aria-hidden="true">Find the clause</span>
              <span className="hero-line" aria-hidden="true">that changes</span>
              <span className="hero-line" aria-hidden="true">the deal.</span>
            </h1>
            <p>
              ContractGuard turns dense agreements into evidence-linked risk reports, negotiation priorities, obligations, deadlines, and grounded answers.
            </p>
            <div className="hero-action-row">
              <Button asChild size="lg">
                <a href={APP_URL}>Review a contract <ArrowRight /></a>
              </Button>
              <span>PDF, DOCX, and TXT · First-pass review</span>
            </div>
          </div>
          <div className="hero-product" data-reveal>
            <div className="hero-product-note">
              <span>Every finding points back to the document.</span>
              <ChevronRight aria-hidden="true" />
            </div>
            <ProductFrame />
          </div>
        </section>

        <section className="audience" aria-labelledby="audience-title">
          <div className="section-shell audience-grid">
            <div className="audience-intro" data-reveal>
              <span className="section-index">Built across the deal team</span>
              <h2 id="audience-title">A clearer contract for everyone who has to act on it.</h2>
              <p>From first draft to final signature, ContractGuard turns one agreement into decisions each role can use.</p>
            </div>
            <div className="audience-ledger" aria-label="Who ContractGuard is designed for">
              {[
                ["01", "Founders", "See material exposure before committing"],
                ["02", "Operations", "Find terms that affect delivery and access"],
                ["03", "Finance", "Surface payments, renewals, and liability"],
                ["04", "Procurement", "Compare supplier risk and obligations"],
                ["05", "Independent professionals", "Review the deal in plain language"],
              ].map(([number, role, outcome]) => (
                <div className="audience-row" key={role} data-reveal>
                  <span className="audience-number">{number}</span>
                  <h3>{role}</h3>
                  <p>{outcome}</p>
                  <ChevronRight aria-hidden="true" />
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="workflow section-shell" id="workflow" aria-labelledby="workflow-title">
          <div className="workflow-intro" data-reveal>
            <span className="section-index">01 / Workflow</span>
            <h2 id="workflow-title">From agreement to action, without the legal fog.</h2>
            <p>One narrow workflow keeps attention on the terms that matter and the evidence behind them.</p>
          </div>
          <div className="workflow-steps">
            {[
              ["01", "Set the review context", "Choose your side, jurisdiction, goal, and risk posture before analysis begins."],
              ["02", "Extract and inspect", "ContractGuard parses the document, runs OCR when needed, and preserves source locations."],
              ["03", "Prioritize what changes", "Review risks, missing protections, negotiation asks, obligations, payments, and deadlines."],
              ["04", "Take the evidence with you", "Ask grounded follow-ups or export a report for negotiation and professional review."],
            ].map(([number, title, copy]) => (
              <article className="workflow-step" key={number} data-reveal>
                <span>{number}</span>
                <div>
                  <h3>{title}</h3>
                  <p>{copy}</p>
                </div>
                <ArrowRight aria-hidden="true" />
              </article>
            ))}
          </div>
        </section>

        <section className="risk-showcase" id="risk-detection" aria-labelledby="risk-title">
          <div className="section-shell risk-showcase-grid">
            <div className="risk-copy" data-reveal>
              <span className="section-index section-index-dark">02 / Risk detection</span>
              <h2 id="risk-title">The conclusion is only useful when you can inspect the evidence.</h2>
              <p>
                Risk labels stay attached to the source clause, location, explanation, confidence, and a specific next step. No hidden chain of reasoning. No generic chatbot answer.
              </p>
              <ul className="risk-proof-list">
                <li><Check /> Verbatim clause excerpts</li>
                <li><Check /> Page, section, and line references</li>
                <li><Check /> Confidence and uncertainty disclosed</li>
                <li><Check /> Suggested language to discuss</li>
              </ul>
            </div>
            <div className="document-inspector" data-reveal>
              <div className="document-page">
                <div className="document-page-head">
                  <span>Residential Lease Agreement</span>
                  <span>Page 6 / 12</span>
                </div>
                <p className="document-line wide" />
                <p className="document-line" />
                <div className="document-highlight">
                  <span>7. Access to premises</span>
                  <p>The Landlord or their agents may enter the Premises at any time of day or night to inspect the property or perform repairs, without requiring prior notice.</p>
                </div>
                <p className="document-line wide" />
                <p className="document-line short" />
              </div>
              <aside className="inspector-panel" aria-label="ContractGuard finding details">
                <div className="inspector-heading">
                  <Badge>High attention</Badge>
                  <span>High confidence</span>
                </div>
                <h3>Entry without notice</h3>
                <p>This term gives the landlord unusually broad access and may undermine privacy and quiet enjoyment.</p>
                <Separator className="inspector-separator" />
                <span className="inspector-label">Negotiation ask</span>
                <p>Require reasonable written notice except in a genuine emergency.</p>
                <div className="source-chip"><FileSearch /> Source 2 · Section 7</div>
              </aside>
            </div>
          </div>
        </section>

        <section className="capabilities section-shell" aria-labelledby="capabilities-title">
          <div className="capabilities-heading" data-reveal>
            <span className="section-index">03 / Review surface</span>
            <h2 id="capabilities-title">A report designed for the next decision.</h2>
          </div>
          <div className="capability-ledger">
            {[
              [FileCheck2, "Prioritize the risk", "Separate high, medium, and low attention findings, then see why each one matters from your side of the agreement.", "Risk report"],
              [GitCompareArrows, "Prepare the negotiation", "Turn findings into ranked asks, fallback positions, and example replacement language to review with counsel.", "Negotiation plan"],
              [ScanSearch, "Track obligations and dates", "Extract who must do what, when notice is required, what gets paid, and which deadlines can trigger consequences.", "Responsibility matrix"],
            ].map(([Icon, title, copy, label]) => (
              <article className="capability-row" key={title} data-reveal>
                <span className="capability-label">{label}</span>
                <div className="capability-title"><Icon aria-hidden="true" /><h3>{title}</h3></div>
                <p>{copy}</p>
                <ChevronRight aria-hidden="true" />
              </article>
            ))}
          </div>
        </section>

        <section className="trust section-shell" id="trust" aria-labelledby="trust-title">
          <div className="trust-heading" data-reveal>
            <ShieldCheck aria-hidden="true" />
            <div>
              <span className="section-index">04 / Trust</span>
              <h2 id="trust-title">Trust is part of the product, not a footer claim.</h2>
            </div>
          </div>
          <div className="trust-ledger">
            <div className="trust-lead" data-reveal>
              <p>Contract review is consequential. ContractGuard states what it processes, shows its evidence, and keeps uncertainty visible.</p>
              <Badge variant="neutral"><LockKeyhole /> Transparent by design</Badge>
            </div>
            {[
              ["Source-linked", "Material findings include a location and a short document excerpt."],
              ["Context-aware", "Analysis starts with your party, jurisdiction, goal, and risk posture."],
              ["Temporary processing", "Upload files are deleted after parsing; session history is not durable storage."],
              ["Honest limits", "ContractGuard is for education and first-pass triage, not legal advice."],
            ].map(([title, copy]) => (
              <div className="trust-row" key={title} data-reveal>
                <h3>{title}</h3>
                <p>{copy}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="closing-cta" aria-labelledby="cta-title">
          <div className="section-shell closing-cta-inner" data-reveal>
            <div>
              <span>Before the signature</span>
              <h2 id="cta-title">Know what you are agreeing to.</h2>
            </div>
            <div className="closing-action">
              <p>Upload a contract. Inspect the risks. Leave with evidence and better questions.</p>
              <Button asChild variant="inverse" size="lg">
                <a href={APP_URL}>Open ContractGuard <ArrowRight /></a>
              </Button>
            </div>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="section-shell footer-inner">
          <Brand />
          <p>Evidence-linked first-pass contract review.</p>
          <div className="footer-links">
            <a href={APP_URL}>Live app</a>
            <a href="https://github.com/udochukwu-echefu/contractguard">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
