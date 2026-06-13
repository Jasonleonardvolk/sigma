INSURANCE PAGE - DEPLOYMENT README
============================================================
invariant.pro/insurance/
Created 2026-06-04

FILES
------------------------------------------------------------

index.html              The insurance proof page (download
                        from Claude chat, save here, rename
                        to index.html)

insurance-fail.svr.json Real Ed25519-signed FAIL receipt
                        (embedded in the HTML, also
                        standalone for verification testing)

insurance-pass.svr.json Real Ed25519-signed PASS receipt
                        (embedded in the HTML, also
                        standalone for verification testing)

DEPLOYMENT
------------------------------------------------------------

The page is a single self-contained HTML file. No build
step. No framework dependency. No backend.

To deploy to invariant.pro/insurance/:

  1. Download insurance_page.html from the Claude chat.
  2. Rename it to index.html.
  3. Place it in the insurance/ directory of the Cloudflare
     Pages deployment source (satya.git, branch main).
  4. Push to GitHub. Cloudflare Pages will deploy it.

The page loads one external dependency:
  tweetnacl.js from cdnjs.cloudflare.com (Ed25519 verification)

All receipt data is embedded in the HTML. No API calls.
No server-side processing.

WHAT THE PAGE DOES
------------------------------------------------------------

1. Hero: "AI insurance needs evidence before the loss."
2. Five-stage walkthrough:
     AI Action -> Evidence State -> Verification ->
     Obstruction -> SVR Receipt
3. PASS/FAIL scenario toggle with receipt display:
     Summary tab / Checked Items tab / JSON tab
4. Real Ed25519 signature verification in-browser:
     Uses tweetnacl.js. No server call. Math runs locally.
5. Underwriting Delta:
     Without SIGMA vs With SIGMA side-by-side.
6. Insurance Consequences:
     Underwriting, Claims, Product Design, Revenue,
     Procurement, Risk Selection.
7. CTAs:
     "Review the receipt artifact" -> /receipts/
     "Request the underwriting packet" -> email

RECEIPTS
------------------------------------------------------------

Both receipts are signed with a demo Ed25519 keypair.

Public key (hex):
  c9c2481b95fa053ba8dfc1c63f43e153662fb4d1ea8e43d82826001466a19cef

Keypair seed: SHA-256 of "invariant-insurance-demo-keypair-v1"

The signatures are real and the in-browser verification
performs actual Ed25519 cryptographic verification, not a
simulated check. Visitors can confirm the signature validates
by clicking "Verify receipt signature."

FAIL scenario: AI agent claims CC9.2 vendor-risk readiness
  but evidence only covers access-review scope. 2 of 4
  checks fail. Verdict: UNSAFE_TO_SUBMIT.

PASS scenario: AI agent gives narrower access-review
  recommendation within documented scope. 3 of 3 checks
  pass. Verdict: SAFE_TO_SUBMIT.

OUTREACH INTEGRATION
------------------------------------------------------------

The page replaces the PDF one-pager as the primary
outreach artifact. The updated outreach message template:

  Subject: AI liability underwriting needs pre-loss evidence

  Hi [Name],

  I built a short interactive walkthrough for AI insurance
  teams.

  It shows an AI compliance agent making an unsupported
  customer-facing recommendation, SIGMA detecting the
  evidence mismatch, and an SVR receipt being generated
  and verified in-browser.

  The reason I think this matters for AI liability
  underwriting: the receipt creates pre-loss evidence of
  what the AI checked, what failed, and whether the result
  can be independently verified.

  Walkthrough:
  https://invariant.pro/insurance/

  Would an artifact like this be useful in AI liability
  underwriting, or is this outside how your team thinks
  about model/output risk?

  Jason Volk
  Invariant Research

PDFs remain supporting material for follow-up conversations.
The page does the work. The email only points to the proof.
