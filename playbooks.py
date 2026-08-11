"""Document classification, built-in playbooks, and defensible rule matching."""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from typing import Any


CONTRACT_CATEGORIES = [
    "Residential lease",
    "Employment agreement",
    "Service agreement",
    "NDA",
    "Vendor agreement",
    "Commercial lease",
    "General contract review",
]


def _rule(rule_id, title, categories, keywords, preferred, fallback, trigger, owner="Legal", required=True):
    return {
        "id": rule_id,
        "title": title,
        "finding_categories": categories,
        "keywords": keywords,
        "required": required,
        "preferred_position": preferred,
        "fallback_position": fallback,
        "escalation_trigger": trigger,
        "owner": owner,
    }


BUILTIN_PLAYBOOKS = [
    {
        "id": "builtin-residential-lease",
        "name": "Residential lease review",
        "description": "Tenant and landlord terms in a residential tenancy, including access, repairs, deposit, rent, renewal, and exit.",
        "contract_types": ["Residential lease"],
        "is_default": False,
        "rules": [
            _rule("lease-entry", "Landlord access and entry", ["property_access"], ["enter", "entry", "access", "inspection"], "Entry only for stated reasons with reasonable notice, except genuine emergencies.", "Define notice, permitted purposes, and emergency access.", "Unrestricted or unexplained access to the home."),
            _rule("lease-repairs", "Repairs and habitability", ["repairs_maintenance"], ["repair", "maintenance", "habitability", "condition"], "Responsibility, response times, and reporting routes are clear.", "List landlord and tenant duties and an escalation route.", "The tenant carries structural or safety duties without qualification."),
            _rule("lease-deposit", "Deposit and deductions", ["deposit_payment"], ["deposit", "deduction", "refund"], "Deposit amount, permitted deductions, evidence, and return timing are stated.", "Require itemised deductions and a defined return process.", "Broad forfeiture or no return timeline."),
            _rule("lease-exit", "Termination, renewal, and possession", ["termination_renewal"], ["termination", "notice", "renewal", "vacate", "possession"], "Notice, renewal, cure, and move-out rules are mutual and clear.", "A practical exit route with defined notice and cure.", "Automatic renewal, one-sided termination, or disproportionate holdover consequences."),
        ],
    },
    {
        "id": "builtin-employment-agreement",
        "name": "Employment agreement review",
        "description": "Employment terms covering role, pay, benefits, termination, confidentiality, restrictive covenants, and work product.",
        "contract_types": ["Employment agreement"],
        "is_default": False,
        "rules": [
            _rule("employment-compensation", "Compensation and benefits", ["compensation_benefits"], ["salary", "compensation", "bonus", "benefit"], "Pay, review timing, benefits, and discretionary elements are explicit.", "Separate guaranteed and discretionary compensation.", "Unclear pay, recoverable wages, or wholly discretionary earned compensation.", "People / Finance"),
            _rule("employment-termination", "Termination and notice", ["termination_renewal"], ["termination", "notice", "dismissal", "probation"], "Grounds, notice, final pay, and post-termination duties are clear.", "Defined notice and treatment of accrued compensation.", "Immediate termination rights with unclear cause or forfeiture.", "People / Legal"),
            _rule("employment-restrictions", "Post-employment restrictions", ["restrictive_covenant"], ["non-compete", "non-solicit", "restraint", "restricted"], "Restrictions are limited by activity, time, and geography.", "Narrow restrictions to legitimate interests and relevant clients or staff.", "Broad restrictions that materially limit future work."),
            _rule("employment-ip", "Work product and intellectual property", ["intellectual_property"], ["invention", "work product", "intellectual property", "copyright"], "Employment-created work is defined and prior or personal IP is excluded.", "Schedule pre-existing IP and limit assignment to relevant work.", "Assignment reaches unrelated, prior, or independently created work."),
        ],
    },
    {
        "id": "builtin-service-agreement",
        "name": "Service agreement review",
        "description": "Services scope, acceptance, fees, change control, service levels, liability, data, and termination.",
        "contract_types": ["Service agreement"],
        "is_default": False,
        "rules": [
            _rule("services-scope", "Scope and acceptance", ["scope_performance"], ["services", "deliverable", "acceptance", "scope"], "Deliverables, dependencies, acceptance, and change control are testable.", "Document scope and a written change process.", "Open-ended work or deemed acceptance without a meaningful review period.", "Business owner"),
            _rule("services-payment", "Fees and payment", ["deposit_payment", "compensation_benefits"], ["fee", "invoice", "payment", "price"], "Fees, milestones, taxes, disputes, and late consequences are clear.", "Defined invoice dates and a dispute process.", "Unilateral price changes, acceleration, or disproportionate late charges.", "Finance"),
            _rule("services-liability", "Liability and indemnity", ["liability_indemnity"], ["liability", "indemnity", "indemnification", "damages"], "Exposure is mutual, proportionate, and capped with narrow carve-outs.", "Cap ordinary claims and define the indemnity procedure.", "Unlimited or asymmetric exposure.", "Legal / Finance"),
            _rule("services-exit", "Termination and transition", ["termination_renewal"], ["termination", "renewal", "transition", "exit"], "Exit rights, cure, fees, data return, and transition support are clear.", "A practical exit right with notice and defined handoff.", "Lock-in, automatic renewal without notice, or punitive exit fees."),
        ],
    },
    {
        "id": "builtin-nda",
        "name": "NDA review",
        "description": "Confidentiality scope, permitted use, exclusions, compelled disclosure, duration, return, and remedies.",
        "contract_types": ["NDA"],
        "is_default": False,
        "rules": [
            _rule("nda-scope", "Confidential information and use", ["confidentiality_data"], ["confidential information", "permitted purpose", "use", "disclose"], "Protected information and permitted use are specific and operational.", "Limit use to the stated evaluation or relationship.", "Everything is confidential indefinitely or use is broader than the purpose."),
            _rule("nda-exclusions", "Standard exclusions", ["confidentiality_exclusions"], ["publicly available", "already known", "independently developed", "rightfully received"], "Public, prior-known, independent-development, and lawful third-party exclusions are present.", "Add conventional exclusions with an evidence standard.", "No meaningful exclusion from confidentiality duties."),
            _rule("nda-duration", "Duration and return", ["termination_renewal"], ["term", "survive", "return", "destroy"], "The confidentiality period and return or deletion process fit the information.", "Separate ordinary confidential information from genuine trade secrets.", "Indefinite duties for all information or impossible deletion obligations."),
            _rule("nda-remedies", "Remedies and residual risk", ["liability_indemnity"], ["injunction", "equitable relief", "indemnity", "damages"], "Remedies are proportionate and do not predetermine entitlement.", "Preserve ordinary legal processes and notice where practical.", "Automatic relief, broad indemnity, or one-sided fee recovery."),
        ],
    },
    {
        "id": "builtin-vendor-agreement",
        "name": "Vendor agreement review",
        "description": "Supply, ordering, service levels, price, security, audit, liability, continuity, and exit terms.",
        "contract_types": ["Vendor agreement"],
        "is_default": False,
        "rules": [
            _rule("vendor-supply", "Supply and service commitments", ["scope_performance"], ["supply", "service level", "delivery", "acceptance"], "Quantities, delivery, acceptance, service levels, and remedies are measurable.", "Define performance measures and a remedy process.", "Uncommitted performance or sole-remedy language that defeats the bargain.", "Procurement"),
            _rule("vendor-data", "Confidentiality, security, and data", ["confidentiality_data"], ["confidential", "personal data", "security", "breach"], "Use is purpose-limited with safeguards, incident notice, and return or deletion.", "Written security duties and no unrelated data use.", "Broad reuse, missing security duties, or no incident notice.", "Security / Legal"),
            _rule("vendor-liability", "Liability and indemnity", ["liability_indemnity"], ["liability", "indemnity", "damages", "claim"], "Caps and indemnities track controllable risks and include a claims process.", "Cap ordinary claims and narrow each indemnity.", "Unlimited, duplicative, or asymmetric exposure.", "Legal / Finance"),
            _rule("vendor-exit", "Continuity and exit", ["termination_renewal"], ["termination", "renewal", "transition", "business continuity"], "Termination, renewal, data return, continuity, and transition are workable.", "Defined notice, transition support, and return of customer assets.", "Lock-in, silent renewal, or no continuity plan.", "Procurement / Legal"),
        ],
    },
    {
        "id": "builtin-commercial-lease",
        "name": "Commercial lease review",
        "description": "Premises, permitted use, rent review, service charge, repairs, assignment, insurance, access, renewal, and exit.",
        "contract_types": ["Commercial lease"],
        "is_default": False,
        "rules": [
            _rule("commercial-rent", "Rent, review, and service charge", ["deposit_payment"], ["rent", "service charge", "review", "operating expense"], "Rent changes and pass-through costs use defined methods, evidence, and challenge rights.", "Cap or objectively define variable charges.", "Unilateral increases or unbounded pass-through costs.", "Finance / Property"),
            _rule("commercial-repair", "Repair, condition, and reinstatement", ["repairs_maintenance"], ["repair", "condition", "reinstatement", "dilapidation"], "Condition is documented and repair or reinstatement duties are proportionate.", "Attach a condition schedule and limit reinstatement.", "Full repair obligations regardless of initial condition."),
            _rule("commercial-use", "Use, access, and transfer", ["property_access", "assignment_transfer"], ["permitted use", "access", "assignment", "sublet"], "Use, landlord access, assignment, and subletting rules support the business.", "Reasonable consent standards and notice for non-emergency access.", "Unrestricted access or absolute transfer restrictions."),
            _rule("commercial-exit", "Break, renewal, and termination", ["termination_renewal"], ["break", "renewal", "termination", "notice"], "Break conditions, notice, renewal, and default cure are precise and achievable.", "Reduce break conditions to objective, controllable requirements.", "Technical conditions can defeat an otherwise valid break."),
        ],
    },
    {
        "id": "builtin-general-contract-review",
        "name": "General contract review",
        "description": "A cautious fallback for agreements that do not confidently fit a specific contract category.",
        "contract_types": ["General contract review"],
        "is_default": True,
        "rules": [
            _rule("scope", "Scope and responsibilities", ["scope_performance"], ["scope", "obligation", "deliverable", "responsibility"], "Each party's responsibilities and acceptance conditions are specific.", "Clarify deliverables, dependencies, and change control.", "Open-ended or one-sided performance duties.", "Business owner"),
            _rule("payment", "Payment and value exchange", ["deposit_payment", "compensation_benefits"], ["payment", "fee", "price", "compensation"], "Amounts, timing, disputes, and adjustments are clear.", "Define payment dates and a fair dispute process.", "Unilateral changes, acceleration, or disproportionate penalties.", "Finance"),
            _rule("liability", "Liability and indemnity", ["liability_indemnity"], ["liability", "indemnity", "damages", "claim"], "Risk allocation is mutual, proportionate, and procedurally clear.", "Cap ordinary claims and narrow exceptional exposure.", "Unlimited or asymmetric exposure."),
            _rule("termination", "Termination and renewal", ["termination_renewal"], ["termination", "renewal", "notice", "cure"], "Exit, cure, renewal, and surviving duties are clear.", "A practical exit right with notice and cure.", "Silent renewal or one-sided termination."),
        ],
    },
]

# Backwards-compatible import for existing integrations and tests.
DEFAULT_PLAYBOOK = deepcopy(next(item for item in BUILTIN_PLAYBOOKS if item["id"] == "builtin-general-contract-review"))


CLASSIFICATION_SIGNALS = {
    "Residential lease": [r"residential (?:lease|tenancy)", r"dwelling", r"tenant", r"security deposit", r"landlord"],
    "Employment agreement": [r"employment agreement", r"employee", r"salary", r"probation", r"employer"],
    "Service agreement": [r"services agreement", r"statement of work", r"deliverables", r"service provider", r"client"],
    "NDA": [r"non-disclosure agreement", r"nondisclosure agreement", r"confidential information", r"disclosing party", r"receiving party"],
    "Vendor agreement": [r"vendor agreement", r"supplier", r"purchase order", r"service levels?", r"procurement"],
    "Commercial lease": [r"commercial lease", r"leased premises", r"permitted use", r"service charge", r"business premises"],
}


def classify_contract(text: str) -> dict[str, Any]:
    """Classify before analysis; return a confirmation gate when evidence is weak."""
    sample = re.sub(r"\s+", " ", (text or "").lower())[:80_000]
    scores = {
        category: sum(1 for pattern in patterns if re.search(pattern, sample))
        for category, patterns in CLASSIFICATION_SIGNALS.items()
    }
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    category, score = ranked[0] if ranked else ("General contract review", 0)
    runner_up = ranked[1][1] if len(ranked) > 1 else 0
    confident = score >= 2 and score > runner_up
    if not confident:
        category = "General contract review"
    confidence = "High" if score >= 4 and score >= runner_up + 2 else "Medium" if confident else "Low"
    matched = [pattern for pattern in CLASSIFICATION_SIGNALS.get(category, []) if re.search(pattern, sample)]
    return {
        "contract_category": category,
        "confidence": confidence,
        "requires_confirmation": not confident,
        "reason": "Matched document-language signals: " + ", ".join(matched[:4]) if matched else "No contract type had enough distinct document-language signals.",
        "confirmed_by_user": False,
    }


def ensure_builtin_playbooks(store: Any, owner_id: str) -> dict[str, Any]:
    existing = {item["id"]: item for item in store.list_playbooks(owner_id)}
    for playbook in BUILTIN_PLAYBOOKS:
        if playbook["id"] not in existing:
            store.save_playbook(owner_id, deepcopy(playbook))
    playbooks = store.list_playbooks(owner_id)
    return next(item for item in playbooks if item["id"] == "builtin-general-contract-review")


def ensure_default_playbook(store: Any, owner_id: str) -> dict[str, Any]:
    return ensure_builtin_playbooks(store, owner_id)


def playbook_for_category(playbooks: list[dict[str, Any]], category: str) -> dict[str, Any] | None:
    normalized = str(category or "").strip().lower()
    for playbook in playbooks:
        if any(str(value).strip().lower() == normalized for value in playbook.get("contract_types", [])):
            return playbook
    return next((item for item in playbooks if item.get("id") == "builtin-general-contract-review"), None)


def finding_key(finding: dict[str, Any], index: int = 0) -> str:
    raw = "|".join(str(finding.get(key) or "") for key in ("title", "issue", "citation", "quote", "clause"))
    return hashlib.sha256(f"{index}|{raw}".encode("utf-8")).hexdigest()[:24]


def _evidence_text(finding: dict[str, Any]) -> str:
    # Only user-document evidence and finding identity are matchable. Generated
    # explanations and recommendations are deliberately excluded.
    return " ".join(str(finding.get(key) or "") for key in ("title", "issue", "clause", "quote", "citation")).lower()


def _keyword_score(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if re.search(rf"\b{re.escape(keyword.lower())}\b", text))


def evaluate_report(report: dict[str, Any], playbook: dict[str, Any] | None) -> dict[str, Any]:
    if not playbook:
        return {"playbook_name": "No playbook", "deviations": [], "summary": {}}
    report_category = report.get("contract_category") or report.get("classification", {}).get("contract_category")
    allowed_types = playbook.get("contract_types", [])
    if report_category and allowed_types and report_category not in allowed_types:
        return {
            "playbook_id": playbook.get("id"),
            "playbook_name": playbook.get("name"),
            "category_mismatch": True,
            "deviations": [],
            "summary": {},
        }
    findings: list[tuple[str, dict[str, Any]]] = []
    findings.extend(("risk", item) for item in report.get("risk_assessment", []))
    findings.extend(("possible_gap", item) for item in report.get("missing_protections", []))
    deviations = []
    used_findings: set[int] = set()
    for rule in playbook.get("rules", []):
        keywords = [str(item).lower() for item in rule.get("keywords", []) if item]
        semantic_categories = set(rule.get("finding_categories", []))
        candidates = []
        for finding_type, finding in findings:
            finding_category = str(finding.get("applicable_category") or "").strip()
            if semantic_categories and finding_category and finding_category not in semantic_categories:
                continue
            score = _keyword_score(_evidence_text(finding), keywords)
            if semantic_categories and finding_category in semantic_categories:
                score += 3
            if score > 0 and id(finding) not in used_findings:
                candidates.append((score, finding_type, finding))
        candidates.sort(key=lambda item: item[0], reverse=True)
        score, finding_type, finding = candidates[0] if candidates else (0, "", {})
        if score == 0:
            status = "Not detected" if rule.get("required") else "Not applicable"
            attention = "Needs verification" if rule.get("required") else "Low"
        else:
            used_findings.add(id(finding))
            severity = str(finding.get("risk_level", "")).lower()
            if finding_type == "possible_gap" or severity == "high":
                status, attention = "Escalate", "High"
            elif severity in {"medium", "needs verification"}:
                status, attention = "Review", "Medium" if severity == "medium" else "Needs verification"
            else:
                status, attention = "Within guardrail", "Low"
        deviations.append({
            "rule_id": rule.get("id"),
            "title": rule.get("title"),
            "status": status,
            "attention": attention,
            "preferred_position": rule.get("preferred_position"),
            "fallback_position": rule.get("fallback_position"),
            "escalation_trigger": rule.get("escalation_trigger"),
            "owner": rule.get("owner"),
            "matched_finding": finding.get("title") or finding.get("issue") or "",
            "citation": finding.get("citation") or "",
            "quote": finding.get("quote") or "",
            "semantic_category": finding.get("applicable_category") or "",
        })
    summary = {
        "escalate": sum(item["status"] == "Escalate" for item in deviations),
        "review": sum(item["status"] in {"Review", "Not detected"} for item in deviations),
        "within_guardrail": sum(item["status"] == "Within guardrail" for item in deviations),
    }
    return {
        "playbook_id": playbook.get("id"),
        "playbook_name": playbook.get("name"),
        "contract_category": report_category,
        "category_mismatch": False,
        "deviations": deviations,
        "summary": summary,
    }
