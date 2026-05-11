from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable

# ─── Brand Colors ───────────────────────────────────────────
NAVY      = colors.HexColor("#0A1628")
BLUE      = colors.HexColor("#1A3A6B")
ACCENT    = colors.HexColor("#2563EB")
GOLD      = colors.HexColor("#F59E0B")
LIGHT_BG  = colors.HexColor("#EFF6FF")
TEAL      = colors.HexColor("#0EA5E9")
GREEN     = colors.HexColor("#10B981")
RED       = colors.HexColor("#EF4444")
GRAY      = colors.HexColor("#6B7280")
WHITE     = colors.white
SOFT_GRAY = colors.HexColor("#F3F4F6")
REEL_CLR  = colors.HexColor("#7C3AED")
CAROUSEL_CLR = colors.HexColor("#0EA5E9")
STATIC_CLR   = colors.HexColor("#10B981")

W, H = A4

# ─── Page numbering ─────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY)
        self.drawRightString(W - 1.5*cm, 1*cm,
                             f"Page {self._pageNumber} of {page_count}  |  CredFix Services — 15-Day Content Plan")

# ─── Styles ─────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# Core styles
cover_title   = S("CoverTitle",    fontSize=34, textColor=WHITE, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=42, spaceAfter=8)
cover_sub     = S("CoverSub",      fontSize=14, textColor=GOLD,  alignment=TA_CENTER, fontName="Helvetica", leading=20, spaceAfter=4)
cover_tagline = S("CoverTag",      fontSize=11, textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER, fontName="Helvetica", leading=16)

section_head  = S("SectionHead",   fontSize=20, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=26)
day_title     = S("DayTitle",      fontSize=15, textColor=WHITE, fontName="Helvetica-Bold", leading=20)
post_type     = S("PostType",      fontSize=10, textColor=WHITE, fontName="Helvetica-Bold", leading=14)
post_title    = S("PostTitle",     fontSize=13, textColor=NAVY,  fontName="Helvetica-Bold", leading=18, spaceBefore=4)
body          = S("Body",          fontSize=9.5, textColor=colors.HexColor("#1F2937"), fontName="Helvetica", leading=14, spaceAfter=5)
body_b        = S("BodyB",         fontSize=9.5, textColor=NAVY,  fontName="Helvetica-Bold", leading=14, spaceAfter=3)
label         = S("Label",         fontSize=8.5, textColor=ACCENT, fontName="Helvetica-Bold", leading=12, spaceAfter=2, spaceBefore=6)
hindi_label   = S("HindiLabel",    fontSize=8.5, textColor=colors.HexColor("#7C3AED"), fontName="Helvetica-Bold", leading=12, spaceAfter=2, spaceBefore=6)
kannada_label = S("KannadaLabel",  fontSize=8.5, textColor=GREEN, fontName="Helvetica-Bold", leading=12, spaceAfter=2, spaceBefore=6)
script_text   = S("ScriptText",    fontSize=9,   textColor=colors.HexColor("#374151"), fontName="Helvetica", leading=13, spaceAfter=3)
cta_text      = S("CTAText",       fontSize=9.5, textColor=ACCENT, fontName="Helvetica-Bold", leading=13, spaceAfter=4)
caption_text  = S("CaptionText",   fontSize=9,   textColor=colors.HexColor("#374151"), fontName="Helvetica", leading=13, spaceAfter=4)
hashtag_text  = S("HashtagText",   fontSize=8.5, textColor=TEAL,  fontName="Helvetica", leading=12, spaceAfter=4)
slide_label   = S("SlideLabel",    fontSize=8,   textColor=CAROUSEL_CLR, fontName="Helvetica-Bold", leading=11, spaceAfter=1)
slide_body    = S("SlideBody",     fontSize=8.5, textColor=colors.HexColor("#374151"), fontName="Helvetica", leading=12, spaceAfter=3)
note_text     = S("NoteText",      fontSize=8,   textColor=GRAY,  fontName="Helvetica-Oblique", leading=11, spaceAfter=3)
hook_style    = S("HookStyle",     fontSize=9.5, textColor=RED,   fontName="Helvetica-Bold", leading=13, spaceAfter=3)
content_style = S("ContentStyle",  fontSize=9.5, textColor=NAVY,  fontName="Helvetica", leading=13, spaceAfter=3)
cta_style     = S("CTAStyle",      fontSize=9.5, textColor=GREEN, fontName="Helvetica-Bold", leading=13, spaceAfter=3)
toc_item      = S("TOCItem",       fontSize=10,  textColor=NAVY,  fontName="Helvetica", leading=16, leftIndent=10)

# ─── Helpers ────────────────────────────────────────────────
def colored_box(text, bg, text_color=WHITE, fontsize=10):
    data = [[Paragraph(f'<font color="#{text_color.hexval()[2:] if hasattr(text_color,"hexval") else "FFFFFF"}">{text}</font>',
                        S("cb", fontSize=fontsize, textColor=text_color, fontName="Helvetica-Bold",
                          alignment=TA_CENTER, leading=fontsize+4))]]
    t = Table(data, colWidths=[W - 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), bg),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING", (0,0),(-1,-1), 12),
        ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [6,6,6,6]),
    ]))
    return t

def badge(text, color):
    data = [[Paragraph(text, S("bdg", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold",
                                alignment=TA_CENTER, leading=10))]]
    t = Table(data, colWidths=[3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), color),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
    ]))
    return t

def day_header_table(day_num, theme):
    data = [[
        Paragraph(f"DAY {day_num}", S("dhn", fontSize=22, textColor=GOLD, fontName="Helvetica-Bold",
                                       alignment=TA_LEFT, leading=26)),
        Paragraph(theme, S("dht", fontSize=12, textColor=colors.HexColor("#CBD5E1"),
                            fontName="Helvetica", alignment=TA_RIGHT, leading=16))
    ]]
    t = Table(data, colWidths=[4*cm, W-8*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), NAVY),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING", (0,0),(-1,-1), 14),
        ("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

def post_header(post_num, post_type_str, post_title_str, color):
    icon = {"🎬 REEL": "🎬", "📱 CAROUSEL": "📱", "🖼 STATIC": "🖼"}.get(post_type_str, "📌")
    data = [[
        Paragraph(f"POST {post_num}  |  {post_type_str}", S("pht", fontSize=9, textColor=WHITE,
                   fontName="Helvetica-Bold", alignment=TA_LEFT, leading=12)),
        Paragraph("", S("empty", fontSize=1))
    ],[
        Paragraph(post_title_str, S("ptl", fontSize=12, textColor=WHITE, fontName="Helvetica-Bold",
                                     alignment=TA_LEFT, leading=16)),
        Paragraph("", S("empty", fontSize=1))
    ]]
    t = Table(data, colWidths=[W-5.5*cm, 1*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), color),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING", (0,0),(-1,-1), 12),
        ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("SPAN",        (0,0),(1,0)),
        ("SPAN",        (0,1),(1,1)),
    ]))
    return t

def section_block(label_text, content_paras, bg=SOFT_GRAY, label_color=ACCENT):
    items = [Paragraph(f'<font color="#{format(label_color.rgb()[0]*255,"02x") if False else "2563EB"}">{label_text}</font>',
                       S("slb", fontSize=8.5, textColor=label_color, fontName="Helvetica-Bold", leading=12, spaceAfter=4))]
    items += content_paras
    data = [[items]]
    t = Table([[items]], colWidths=[W-5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), bg),
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING", (0,0),(-1,-1), 12),
        ("RIGHTPADDING",(0,0),(-1,-1),12),
        ("BOX",         (0,0),(-1,-1), 0.5, label_color),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB"), spaceAfter=6, spaceBefore=6)

def sp(h=6):
    return Spacer(1, h)

# ─── Content Data ───────────────────────────────────────────

DAYS = [

# ════════════════════════════════════════════════════════════
# DAY 1
# ════════════════════════════════════════════════════════════
{
"day": 1,
"theme": "Debt Navigator — Know Your Debt, Own Your Plan",
"posts": [
{
"num": 1, "type": "🎬 REEL", "color": REEL_CLR,
"title": "Loan Rejected… Again! 😤 | Debt Navigator",
"service": "Debt Navigator",
"duration": "20–25 sec",
"scene": "📍 SCENE: Inside a bank branch. Formal cabin. @BOY sits across the manager's desk. Manager slides back a paper file.",
"script_en": [
("🎣 HOOK (0–6s)", RED, [
"@MANAGER slides the papers back across the desk.",
'@MANAGER: "Your loan application has been rejected."',
'@BOY leans forward, frustrated: "Again?! This is the THIRD time. Same bank. Same answer."',
'@BOY holds his head. Looks into camera: "Loan. Rejected."',
]),
("📖 CONTENT (6–18s)", NAVY, [
'@BOY drops hands, looks up: "At least tell me WHY?"',
'@MANAGER: "Low credit score… too many EMIs already running."',
'@BOY: "Great. Problems I already know. What\'s the SOLUTION?"',
"[Pause. @BOY stands, looks directly into camera]",
'@BOY: "But wait — what if ONE app showed you exactly why your loan keeps getting rejected... and exactly how to fix it?"',
]),
("📣 CTA (18–25s)", GREEN, [
'@BOY [calm, direct]: "That\'s CredFix. Debt Navigator."',
'"Download now. Stop guessing. Start rebuilding your score."',
"[LOGO + App Store / Play Store screen appears]",
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@MANAGER papers wapas karta hai.",
'@MANAGER: "Aapka loan reject ho gaya."',
'@BOY (frustrated): "Phir se?! Teen baar ho gaya. Ek hi bank. Ek hi jawab."',
'@BOY sir pakad leta hai, camera ki taraf dekhta hai: "Loan... Reject."',
]),
("📖 CONTENT — Hindi", NAVY, [
'@BOY: "Kam se kam bataiye kyun?"',
'@MANAGER: "Credit score low hai... bahut saare EMI chal rahe hain."',
'@BOY: "Shukriya. Ye sab toh pata tha. Solution kya hai?"',
"[Ruk jaata hai. Camera ki taraf seedha dekhta hai]",
'@BOY: "Lekin... ek app hai jo exactly batata hai aapka loan kyun reject ho raha hai — aur kaise theek karein?"',
]),
("📣 CTA — Hindi", GREEN, [
'@BOY [shant, seedha]: "Woh hai CredFix. Debt Navigator."',
'"Abhi download karein. Andaze lagana band karein. Score rebuild karna shuru karein."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@MANAGER papers wapas koduttane.",
'@MANAGER: "Nimma loan reject aagide."',
'@BOY (frustrated): "Matthe?! Mooru sari aayitu. Ondu bank. Ondu answer."',
'@BOY tala hidikolluttane, camera kaḍe noDuttane: "Loan... Reject."',
]),
("📖 CONTENT — Kannada", NAVY, [
'@BOY: "Kadeya paksha yaake antha helri?"',
'@MANAGER: "Credit score kama ide... thumba EMI haakvagide."',
'@BOY: "Dhanyavaada. Idu nange gotta ittu. Parantu parantu solution?"',
"[Ninthukolluttane. Camera kaḍe noDuttane]",
'@BOY: "Aadare... ondu app ide — nimma loan yaake reject aaguttide antha exact aagi heli — mattu haege sari maduvudu antha?"',
]),
("📣 CTA — Kannada", GREEN, [
'@BOY [shaantha, nera]: "Aduve CredFix. Debt Navigator."',
'"Ega download madi. Andaajisuva beda. Score rebuild shuru madi."',
]),
],
"visual_note": "Warm bank interior lighting. Slow zoom on boy's face. End screen: CredFix logo + Download button graphic.",
"hashtags": "#CredFix #LoanRejected #DebtNavigator #CreditScore #FinancialFreedom #DebtHelp #India #PersonalFinance",
},
{
"num": 2, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "5 Signs You Urgently Need a Debt Repayment Plan",
"service": "Debt Navigator",
"slides": [
("SLIDE 1 — COVER", "🚨 Are You Trapped in Debt?\nHere Are 5 Warning Signs You Can\'t Ignore\n\n[CredFix Debt Navigator]"),
("SLIDE 2", "⚠️ Sign #1: You\'re Only Paying Minimums\nPaying only the minimum every month?\nYou\'re barely touching the principal.\nInterest is eating you alive."),
("SLIDE 3", "⚠️ Sign #2: Loan Gets Rejected Every Time\nMultiple rejections = your credit profile is broken.\nYou need a plan, not just an application."),
("SLIDE 4", "⚠️ Sign #3: You Don\'t Know How Much You Owe\nIf you can\'t add up your total debt right now,\nyou\'re not in control. CredFix maps it all."),
("SLIDE 5", "⚠️ Sign #4: EMIs Are > 40% of Your Income\nYour debt-to-income ratio is dangerously high.\nThis is a red flag for every lender."),
("SLIDE 6 — CTA", "✅ The Fix: CredFix Debt Navigator\nPersonalized repayment plan\nPrioritizes high-interest & secured loans\nStep-by-step roadmap to freedom\n\n📲 Download CredFix Now"),
],
"caption": "Debt is sneaky. It doesn\'t shout — it whispers. But these 5 signs are screaming at you. If you recognize even 2 of them, it\'s time to act. CredFix Debt Navigator builds your personalized repayment roadmap. 🔗 Download now — link in bio.",
"hashtags": "#DebtFree #DebtNavigator #CredFix #PersonalFinance #MoneyTips #LoanIndia #CreditHealth #FinancialPlanning",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 2
# ════════════════════════════════════════════════════════════
{
"day": 2,
"theme": "Debt Navigator — Break the EMI Trap",
"posts": [
{
"num": 3, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "Credit Score Myth vs Fact 💡",
"service": "Debt Navigator / Credit Health",
"visual": "Split-screen: Left side RED background (MYTH), Right side GREEN background (FACT). Bold typography. CredFix branding at bottom.",
"pairs": [
("MYTH", "Checking my credit score will lower it."),
("FACT", "Checking your OWN score is a soft inquiry — it NEVER affects your score."),
("MYTH", "Closing old credit cards improves your score."),
("FACT", "Closing old cards can HURT your score by reducing available credit."),
("MYTH", "You need to carry a balance to build credit."),
("FACT", "Paying in FULL every month is the best way to build credit."),
],
"caption": "The lies about credit scores are costing you money. 💸 Here\'s the truth — straight, no filter. CredFix helps you understand exactly where you stand and what to do next. Save this post. Share it. Someone you know needs this. 📲 Download CredFix — link in bio.",
"hashtags": "#CreditScore #CreditMyths #FinanceTips #CredFix #DebtFree #MoneyFacts #IndiaFinance #CreditHealth",
},
{
"num": 4, "type": "🎬 REEL", "color": REEL_CLR,
"title": "Trapped in EMIs with No Way Out 😰 | Debt Navigator",
"service": "Debt Navigator",
"duration": "20–25 sec",
"scene": "📍 SCENE: @GIRL sitting at a kitchen table, surrounded by phone bills, bank statements, EMI receipts. Overwhelmed look.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@GIRL stares at papers. Phone buzzes — another EMI reminder.",
'@GIRL [exhales]: "Personal loan EMI. Credit card EMI. Car loan. And still no salary left."',
'Looks at camera: "Is this... is this even a life?"',
]),
("📖 CONTENT (5–18s)", NAVY, [
"@GIRL picks up one paper after another.",
'@GIRL: "I have 4 EMIs. I don\'t even remember which one is due when."',
'"Every month I pay. Every month I\'m back to zero."',
"[Pause]",
'"What if someone could just... show me which loan to kill first?"',
'"Which one is eating the most interest. Which one is dragging me down."',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix Debt Navigator does exactly that."',
'"It maps ALL your debts. Prioritizes the high-interest ones first."',
'"So you pay smarter — not just more."',
'"Download CredFix. Take back control."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@GIRL papers dekh rahi hai. Phone buzzes — EMI reminder.",
'@GIRL: "Personal loan EMI. Credit card EMI. Car loan. Aur phir bhi salary khatam."',
'Camera ki taraf: "Kya ye... kya ye zindagi hai?"',
]),
("📖 CONTENT — Hindi", NAVY, [
"@GIRL ek ek paper uthati hai.",
'@GIRL: "Mere 4 EMI hain. Mujhe yaad bhi nahi konsa kab dena hai."',
'"Har mahine bharta hoon. Har mahine zero pe wapas aata hoon."',
"[Ruk jaati hai]",
'"Koi ek aisa ho jo bata de — pehle kaunsa loan khatam karna chahiye?"',
'"Kaunsa sabse zyada interest le raha hai. Kaunsa mujhe neeche kheench raha hai."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Debt Navigator bilkul yahi karta hai."',
'"Saare debts ka naksha banata hai. Sabse pehle high-interest wala."',
'"Taaki aap smart tarike se bharo — sirf zyada nahi."',
'"CredFix download karein. Control wapas lijiye."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@GIRL papers noDuttale. Phone buzzes — EMI reminder.",
'@GIRL: "Personal loan EMI. Credit card EMI. Car loan. Adaru salary illave."',
'Camera kaḍe: "Ivalu... ivalu jiivana?"',
]),
("📖 CONTENT — Kannada", NAVY, [
"@GIRL ondu ondu paper ettikolluttale.",
'@GIRL: "Nalige 4 EMI ide. Yaavudu yaavaaga kodabeku antha nenapu illa."',
'"Prathi tingalu koDuttene. Prathi tingalu zero ge barta iddene."',
"[Ninthukolluttane]",
'"Yaaro ondu helabeku — mutham yaavudu loan mugisabeku?"',
'"Yaavudu interest thumba tegeetide. Yaavudu nannanu kelage edhistide."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Debt Navigator nera ituve maduttade."',
'"Ella debts na map maduttade. Motta mutham high-interest anannu."',
'"Haage neevu smart aagi kodtiri — just jaasta alla."',
'"CredFix download madi. Control wapas tegiri."',
]),
],
"visual_note": "Warm kitchen light. Papers everywhere. Close-up of phone EMI alerts. End card: CredFix branding.",
"hashtags": "#EMITrap #DebtNavigator #CredFix #PersonalLoan #FinancialStress #MoneyProblems #DebtHelp #IndiaFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 3
# ════════════════════════════════════════════════════════════
{
"day": 3,
"theme": "Debt Navigator — How It Works",
"posts": [
{
"num": 5, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "How CredFix Debt Navigator Actually Works — Step by Step",
"service": "Debt Navigator",
"slides": [
("SLIDE 1 — COVER", "🗺 Your Personalized Debt\nRepayment Roadmap Starts Here\n\nCredFix Debt Navigator — Step by Step"),
("SLIDE 2", "🔍 Step 1: Full Debt Audit\nWe map every loan, EMI, credit card balance.\nPersonal loans. Car loans. Credit cards.\nAll in one clear picture."),
("SLIDE 3", "📊 Step 2: Priority Scoring\nWe rank your debts by:\n• Interest rate (highest first)\n• Loan type (secured vs unsecured)\n• Risk of legal action\nSo you know exactly what to tackle first."),
("SLIDE 4", "💡 Step 3: Personalized Plan\nYour custom repayment schedule.\nMonth-by-month. Rupee-by-rupee.\nBuilt for YOUR income. Not a generic template."),
("SLIDE 5", "📈 Step 4: Track Progress\nWatch your credit score rise.\nSee interest savings in real time.\nCelebrate every milestone."),
("SLIDE 6 — CTA", "🚀 Ready to Start?\nCredFix Debt Navigator\n✅ Personal repayment plan\n✅ High-interest loan priority\n✅ Secured loan protection\n✅ Real-time tracking\n\n📲 Download CredFix — Link in Bio"),
],
"caption": "Getting out of debt doesn\'t happen by accident. It happens with a plan. 🗺 CredFix Debt Navigator gives you a step-by-step roadmap — built specifically for your debts, your income, your life. Save this. You\'ll thank yourself later. 📲 Download — link in bio.",
"hashtags": "#DebtNavigator #CredFix #DebtRepayment #FinancialPlan #GetOutOfDebt #MoneyManagement #CreditHealth #IndiaFinance",
},
{
"num": 6, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "High-Interest Loan? Pay THIS One First 💰",
"service": "Debt Navigator",
"visual": "Bold infographic. Dark navy background. Large interest rate comparisons displayed visually. CredFix branding.",
"pairs": [
("Credit Card Debt", "24–42% Interest Rate — PAY THIS FIRST"),
("Personal Loan", "12–24% Interest Rate — Pay Second"),
("Car Loan", "9–12% Interest Rate — Pay Third"),
("Home Loan", "7–9% Interest Rate — Pay Last"),
],
"caption": "Not all debt is equal. The ORDER you pay matters more than the amount. 💡 A credit card charging 36% interest is literally 5x more expensive than your home loan. CredFix Debt Navigator automatically prioritizes your debts so you stop wasting money on interest. 💸 Save this post. Share it with anyone drowning in EMIs. 📲 Download CredFix — link in bio.",
"hashtags": "#DebtPayoff #HighInterest #CreditCard #EMI #CredFix #DebtNavigator #MoneyTips #PersonalFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 4
# ════════════════════════════════════════════════════════════
{
"day": 4,
"theme": "Debt Shield — You Have Legal Rights",
"posts": [
{
"num": 7, "type": "🎬 REEL", "color": REEL_CLR,
"title": "Debt Collectors Threatening You? This Is ILLEGAL 🛡️ | Debt Shield",
"service": "Debt Shield",
"duration": "20–25 sec",
"scene": "📍 SCENE: @MAN sitting at home. Phone rings repeatedly. Aggressive voice on phone. He looks scared, cornered.",
"script_en": [
("🎣 HOOK (0–6s)", RED, [
"Phone rings. @MAN picks up.",
'CALLER [aggressive]: "Pay NOW or we\'re sending people to your house."',
'@MAN [shaken]: "What? You can\'t do that..."',
'@MAN looks at camera: "They call me 8 times a day. My family. My colleagues."',
]),
("📖 CONTENT (6–18s)", NAVY, [
'@MAN: "I know I owe money. But does that mean I have no rights?"',
"[Stands up. Resolute.]",
'"In India, debt collectors CANNOT call before 8AM or after 7PM."',
'"They CANNOT threaten you, abuse you, or call your family."',
'"They CANNOT visit your home without notice."',
'"If they do ANY of this — it is ILLEGAL."',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix Debt Shield protects you."',
'"We respond to legal notices. We represent you. We stop the harassment."',
'"You owe money — not your dignity."',
'"Download CredFix. Get protected."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"Phone bajta hai. @MAN phone uthata hai.",
'CALLER [aggressive]: "Abhi pay karo warna ghar pe aadmi bhejte hain."',
'@MAN [dara hua]: "Kya? Aap aisa nahi kar sakte..."',
'@MAN camera ki taraf: "Din mein 8 baar call karte hain. Ghar mein. Office mein."',
]),
("📖 CONTENT — Hindi", NAVY, [
'@MAN: "Haan, mujhe paisa dena hai. Par kya mujhe koi haq nahi?"',
"[Khada ho jaata hai. Himmat ke saath.]",
'"India mein, recovery agents raat 8 baje se pehle ya sham 7 ke baad NAHI call kar sakte."',
'"Dhhamki, gaali, family ko call karna — ye sab ILLEGAL hai."',
'"Bina notice ke ghar nahi aa sakte."',
'"Agar ye karte hain — ye crime hai."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Debt Shield aapki raksha karta hai."',
'"Legal notice ka jawab dete hain. Aapki taraf se ladne ke liye hain."',
'"Aap paisa waapas karo — lekin apni izzat mat kho."',
'"CredFix download karein. Suraksha lijiye."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"Phone aDuttade. @MAN phone ettukolluttane.",
'CALLER [aggressive]: "Ega pay madi illda manege janra kalisthivi."',
'@MAN [bhaya aagi]: "Enu? Nimge hage madakke agalla..."',
'@MAN camera kaḍe: "Dinakke 8 sari phone maaDuttare. Manege. Office ge."',
]),
("📖 CONTENT — Kannada", NAVY, [
'@MAN: "Haan, nanu haṇa kodabeku. Aadare nange yaavude hakku illa?"',
"[Eddu ninthukolluttane. Dhairya dinda.]",
'"India nalli, recovery agents beLigge 8 gaṇṭeyinda munde ya sanje 7 gaṇṭe nantara call maaDabaradu."',
'"BhayapaDisu, badidu, familyge call maaDuva — ellavu ILLEGAL."',
'"Notice illa manege baruvudu agalla."',
'"Haage madidare — adu crime."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Debt Shield nimma rakshane maduttade."',
'"Legal notice ge uttara koduttivi. Nimminda aaD aaDuttivi."',
'"Haṇa wapas kodi — aadare nimma gaurava biDabedi."',
'"CredFix download madi. Suraksha paDeyri."',
]),
],
"visual_note": "Dark moody home setting. Phone ringing audio effect. Close-up on man's fearful face turning resolute. Bold text overlays with legal rights.",
"hashtags": "#DebtShield #DebtCollectors #KnowYourRights #CredFix #HarassmentProtection #LegalRights #DebtHelp #India",
},
{
"num": 8, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "Your 6 Legal Rights as a Borrower in India",
"service": "Debt Shield",
"slides": [
("SLIDE 1 — COVER", "⚖️ You Have Rights.\nDebt Collectors Can\'t Take Those Away.\n\n6 Legal Rights Every Borrower Must Know\n[CredFix Debt Shield]"),
("SLIDE 2", "🔴 Right #1: Right to Dignity\nRecovery agents CANNOT use abusive language,\nthreaten you, or humiliate you.\nRBI guidelines strictly prohibit this."),
("SLIDE 3", "🔴 Right #2: Calling Hours Only\nCollectors can ONLY call between\n8:00 AM – 7:00 PM.\nCalls outside this window = RBI violation."),
("SLIDE 4", "🔴 Right #3: No Unauthorized Visits\nNo one can show up at your home or office\nwithout prior appointment and proper ID.\nIf they do — document it immediately."),
("SLIDE 5", "🔴 Right #4: Right to Legal Representation\nYou have the right to have a lawyer\nor authorized representative handle all communications.\nCredFix can be that representative."),
("SLIDE 6", "🔴 Right #5: Debt Validation Right\nYou can demand a written statement of\nthe exact amount owed — including principal,\ninterest, and penalties."),
("SLIDE 7 — CTA", "🛡️ CredFix Debt Shield\nLegal notice responses\nHarassment protection\nDebt representation\n\nYou owe money — not your dignity.\n📲 Download CredFix Now"),
],
"caption": "Did you know debt collectors CANNOT legally call you after 7PM? Most people don\'t. And that ignorance costs them their peace, their mental health, their dignity. CredFix Debt Shield puts the law on YOUR side. 📲 Download — link in bio.",
"hashtags": "#BorrowerRights #DebtShield #CredFix #LegalRights #RBI #DebtHelp #HarassmentProtection #IndiaFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 5
# ════════════════════════════════════════════════════════════
{
"day": 5,
"theme": "Debt Shield — Legal Notice Protection",
"posts": [
{
"num": 9, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "Received a Legal Notice from a Bank? Do THIS — Not That ⚠️",
"service": "Debt Shield",
"visual": "Two columns: DO (green checkmarks) vs DON\'T (red crosses). Clean, high-contrast design. CredFix branded.",
"pairs": [
("DO — Read it carefully & note the deadline", "DON'T — Ignore or hide it"),
("DO — Consult CredFix or a lawyer immediately", "DON'T — Sign anything without legal advice"),
("DO — Keep all copies safely", "DON'T — Panic and agree to unfair terms"),
("DO — Respond within the notice period", "DON'T — Assume it will go away on its own"),
],
"caption": "A legal notice is NOT the end. It\'s the BEGINNING of a negotiation. 💼 Most people panic and make it worse. The right response at the right time can save you lakhs. CredFix Debt Shield experts handle legal notice responses so you don\'t have to face it alone. 📲 Get protected — link in bio.",
"hashtags": "#LegalNotice #DebtShield #CredFix #BankNotice #DebtHelp #LegalRights #PersonalFinance #India",
},
{
"num": 10, "type": "🎬 REEL", "color": REEL_CLR,
"title": "I Got a Legal Notice from the Bank 😱 | Debt Shield",
"service": "Debt Shield",
"duration": "18–22 sec",
"scene": "📍 SCENE: @WOMAN opens a courier at her door. Sees 'LEGAL NOTICE' printed in red on the envelope. Face drops.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@WOMAN tears open envelope. Reads. Eyes widen.",
'@WOMAN [alarmed]: "Legal notice. From the bank."',
'Looks at camera: "I don\'t even know what this MEANS."',
]),
("📖 CONTENT (5–18s)", NAVY, [
'"Is this… am I getting sued?"',
'"What do I do? Do I sign? Do I ignore it? Do I call them back?"',
"[Phone rings — it's the bank]",
'"No. No no no. I\'m not signing ANYTHING without knowing what I\'m agreeing to."',
'[Pause, resolute]: "I need someone who actually knows this stuff."',
]),
("📣 CTA (18–22s)", GREEN, [
'"CredFix Debt Shield."',
'"We read it. We respond. We represent you."',
'"Don\'t face legal notices alone."',
'"Download CredFix — right now."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@WOMAN lifafa kholti hai. Padhti hai. Aankhen phail jaati hain.",
'@WOMAN [alarmed]: "Legal notice. Bank se."',
'Camera ki taraf: "Mujhe samajh hi nahi aa raha ye kya hai."',
]),
("📖 CONTENT — Hindi", NAVY, [
'"Kya ye... kya mujh par case ho raha hai?"',
'"Main kya karoon? Sign karoon? Ignore karoon? Unhe wapas call karoon?"',
"[Phone bajta hai — bank hai]",
'"Nahi. Kuch bhi sign nahi karungi bina samjhe."',
'[Ruk jaati hai]: "Mujhe koi chahiye jo ye samjhe."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Debt Shield."',
'"Hum padhte hain. Hum jawab dete hain. Hum aapki taraf se khade hain."',
'"Legal notice akele mat samhalo."',
'"CredFix abhi download karein."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@WOMAN cover bittukolluttale. Oduttale. Kannu doḍḍadu aaguttade.",
'@WOMAN [alarmed]: "Legal notice. Bank inda."',
'Camera kaḍe: "Idu yaava arthave artha aaguttilla nange."',
]),
("📖 CONTENT — Kannada", NAVY, [
'"Ivalu... nanage case aaguttidale?"',
'"Naanu enu maaDali? Sign maaDali? Bidli? Avarige wapas call maaDali?"',
"[Phone aDuttade — bank adu]",
'"Alla. Yenu arthaagathe antha sign maaDalla."',
'[Ninthukolluttane]: "Idu tiliyuva yaaraadroo beku."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Debt Shield."',
'"Naavu oduttivi. Uttara koduttivi. Nimminda aaD aaDuttivi."',
'"Legal notice yakkela edurisikoLLbedi."',
'"CredFix ega download madi."',
]),
],
"visual_note": "Cinematic natural home lighting. Close-up on red 'LEGAL NOTICE' stamp. Slow motion envelope opening. Bold text overlays.",
"hashtags": "#LegalNotice #DebtShield #CredFix #BankNotice #DebtHelp #Harassment #India #PersonalFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 6
# ════════════════════════════════════════════════════════════
{
"day": 6,
"theme": "Debt Shield — Protection Overview",
"posts": [
{
"num": 11, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "How CredFix Debt Shield Protects You — 4 Ways",
"service": "Debt Shield",
"slides": [
("SLIDE 1 — COVER", "🛡️ Stop Facing Debt Alone.\nCredFix Debt Shield Has Your Back.\n\n4 Powerful Ways We Protect You"),
("SLIDE 2", "⚖️ Protection #1: Legal Notice Response\nReceived a notice from your bank or lender?\nWe read, analyze, and respond on your behalf.\nDeadlines won\'t catch you off guard."),
("SLIDE 3", "🤝 Protection #2: Legal Representation\nOur experts stand between you and lenders.\nAll negotiations, all communications —\nhandled professionally."),
("SLIDE 4", "📵 Protection #3: Harassment Shield\nIllegal calls? Threats? Office visits?\nWe file complaints with RBI and banking ombudsman.\nThe harassment stops — legally."),
("SLIDE 5", "💬 Protection #4: Debt Settlement Negotiation\nWe negotiate directly with lenders\nto reduce your outstanding amounts,\nwaive penalties, and set fair terms."),
("SLIDE 6 — CTA", "🔒 You Don\'t Have to Face This Alone\nCredFix Debt Shield:\n✅ Legal notice response\n✅ Expert representation\n✅ Harassment protection\n✅ Settlement negotiation\n\n📲 Download CredFix — Link in Bio"),
],
"caption": "Debt is a financial problem. But the harassment that comes with it is a human rights problem. 🛡️ CredFix Debt Shield makes sure you\'re protected on BOTH fronts. You owe money — not your peace of mind. 📲 Download — link in bio.",
"hashtags": "#DebtShield #CredFix #LegalProtection #HarassmentProtection #DebtSettlement #BorrowerRights #IndiaFinance",
},
{
"num": 12, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "Recovery Agent Called After 7PM? HERE'S What to Do 📵",
"service": "Debt Shield",
"visual": "Step-by-step action guide. Dark background with numbered steps in gold. CredFix branded.",
"pairs": [
("Step 1", "Stay calm. Do NOT argue on the phone."),
("Step 2", "Note the time, date, caller\'s name & number."),
("Step 3", "Record the conversation if possible (legal in India)."),
("Step 4", "File a complaint with your bank\'s grievance cell."),
("Step 5", "Contact CredFix Debt Shield for expert help."),
],
"caption": "After 7PM calls are a violation of RBI guidelines. You have the right to complain — and CredFix can do it for you. 📲 Get protected — link in bio.",
"hashtags": "#RecoveryAgent #RBI #DebtShield #CredFix #HarassmentProtection #BorrowerRights #KnowYourRights #India",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 7
# ════════════════════════════════════════════════════════════
{
"day": 7,
"theme": "Debt Coaching — One-on-One Financial Planning",
"posts": [
{
"num": 13, "type": "🎬 REEL", "color": REEL_CLR,
"title": "One Coaching Call Changed Everything 📞 | Debt Coaching",
"service": "Debt Coaching",
"duration": "20–25 sec",
"scene": "📍 SCENE: @MAN sitting at a small desk, stressed, looking at a notebook full of numbers. Phone rings — CredFix Coach calling.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@MAN staring at notebook. Scratching out numbers. Frustrated.",
'@MAN: "I make decent money. So WHY am I always broke by the 15th?"',
'Looks at camera: "I\'ve been asking this for 3 years. No one has an answer."',
]),
("📖 CONTENT (5–18s)", NAVY, [
"Phone rings. CredFix Debt Coach is calling.",
"@MAN picks up. 30-minute conversation begins.",
'@MAN [later, relieved]: "He didn\'t judge me. He just... showed me."',
'"I was spending 52% of my income on EMIs. No wonder."',
'"He gave me a plan. Month by month. Step by step."',
'"First time in 3 years I actually felt like I could breathe."',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix Debt Coaching. One-on-one with a real expert."',
'"They don\'t just tell you what\'s wrong."',
'"They show you exactly how to fix it."',
'"Book your first session. Download CredFix."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@MAN notebook dekh raha hai. Numbers kaaat raha hai. Frustrated.",
'@MAN: "Main theek kamaata hoon. Toh phir 15 tarikh tak paisa kyun khatam ho jaata hai?"',
'Camera ki taraf: "Teen saal se pooch raha hoon. Koi jawab nahi deta."',
]),
("📖 CONTENT — Hindi", NAVY, [
"Phone bajta hai. CredFix Debt Coach ka call.",
"@MAN phone uthata hai. 30 minute ki baatcheet.",
'@MAN [baad mein, sukoon se]: "Unhone judge nahi kiya. Bas... dikhaya."',
'"Meri 52% income EMI mein ja rahi thi. Koi ajeeb baat nahi."',
'"Unhone plan diya. Mahine mahine. Kadam kadam."',
'"Teen salon mein pehli baar laga ki... saans le sakta hoon."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Debt Coaching. Ek sachche expert ke saath."',
'"Sirf galti nahi batate — theek karne ka raasta bhi batate hain."',
'"Pehla session book karein. CredFix download karein."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@MAN notebook noDuttane. Numbers haakuttane. Frustrated.",
'@MAN: "Naanu sariyaagi kasadu maduttene. Haage aadaru 15ne tarihige haṇa yaake muguttade?"',
'Camera kaḍe: "Mooru varshadinda keeLuttiddene. Yaaru uttara koduttilla."',
]),
("📖 CONTENT — Kannada", NAVY, [
"Phone aDuttade. CredFix Debt Coach call maaDuttare.",
"@MAN phone ettukolluttane. 30 nimiShadda maatukata.",
'@MAN [nantara, niralagi]: "Avaru judge maaDalilla. Bari... tOrisidaru."',
'"Nanna 52% income EMI ge hoguttittu. Aadu aashcharya alla."',
'"Avaru plan kottu. TingaLu tingaLu. Hejje hejje."',
'"Mooru varshadalli motta mutham nanu... ushiru bidu bahudu antha anisitu."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Debt Coaching. Nijavaada expert jote."',
'"Yenu tappaagide antha heLalla — haege sari maaDuvudu antha tOristare."',
'"Motta session book madi. CredFix download madi."',
]),
],
"visual_note": "Warm home-office light. Notebook close-ups. Phone call audio effect. Emotional before-after split: stressed → relieved face.",
"hashtags": "#DebtCoaching #CredFix #FinancialCoach #DebtFree #MoneyManagement #PersonalFinance #IndiaFinance #LifeChange",
},
{
"num": 14, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "6 Steps to Financial Freedom with CredFix Debt Coaching",
"service": "Debt Coaching",
"slides": [
("SLIDE 1 — COVER", "🧭 The 6-Step Road to\nFinancial Freedom\n\nCredFix Debt Coaching — Your Personal Guide"),
("SLIDE 2", "Step 1️⃣: Full Financial Audit\nWhere does your money ACTUALLY go?\nIncome. Expenses. EMIs. Savings.\nWe map your complete financial picture."),
("SLIDE 3", "Step 2️⃣: Debt Prioritization\nNot all debt is equal.\nWe rank what to pay off first\nbased on interest, type & urgency."),
("SLIDE 4", "Step 3️⃣: Budget Redesign\nBuild a budget that works for YOUR life.\nNot a textbook template.\nA real, liveable plan."),
("SLIDE 5", "Step 4️⃣: One-on-One Coaching Sessions\nRegular check-ins with your personal coach.\nAsk anything. No judgment.\nReal accountability."),
("SLIDE 6", "Step 5️⃣ & 6️⃣: Track + Rebuild\nMonitor your progress weekly.\nWatch your credit score climb.\nCelebrate every win."),
("SLIDE 7 — CTA", "💪 Your Coach Is Waiting\nCredFix Debt Coaching:\n✅ Personalized 1-on-1 sessions\n✅ Real financial expert\n✅ No judgment, just solutions\n✅ Step-by-step freedom plan\n\n📲 Book Now — Link in Bio"),
],
"caption": "Financial freedom isn\'t a dream. It\'s a 6-step process. 🧭 And with a CredFix Debt Coach walking beside you — it\'s a process you don\'t have to face alone. Save this. Share it with someone who\'s been struggling too long. 📲 Download — link in bio.",
"hashtags": "#DebtCoaching #FinancialFreedom #CredFix #MoneyCoach #DebtFree #PersonalFinance #6Steps #IndiaFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 8
# ════════════════════════════════════════════════════════════
{
"day": 8,
"theme": "Debt Coaching — Why You Need a Coach",
"posts": [
{
"num": 15, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "DIY Debt Management vs CredFix Debt Coaching — The Real Difference",
"service": "Debt Coaching",
"visual": "Side-by-side comparison table. Dark background. DIY column in gray, CredFix column in gold. Bold, punchy text.",
"pairs": [
("DIY: Guess which loan to pay first", "CredFix: Expert-ranked priority plan"),
("DIY: Generic online calculators", "CredFix: Built for YOUR income & debts"),
("DIY: No one to talk to at 2AM", "CredFix: Coach available when you need"),
("DIY: Motivated for 2 weeks, then quit", "CredFix: Accountability keeps you on track"),
("DIY: Still stressed in year 3", "CredFix: Real progress, real milestones"),
],
"caption": "There\'s nothing wrong with trying to figure it out yourself. But why try alone when you can have an expert? 🧠 CredFix Debt Coaching gives you a real person, a real plan, and real results. The only question is — how long are you willing to wait? 📲 Download — link in bio.",
"hashtags": "#DebtCoaching #CredFix #DIYvsExpert #MoneyCoach #DebtFree #PersonalFinance #IndiaFinance",
},
{
"num": 16, "type": "🎬 REEL", "color": REEL_CLR,
"title": "From Drowning in Debt to Finally Breathing 😮‍💨 | Debt Coaching",
"service": "Debt Coaching",
"duration": "20–25 sec",
"scene": "📍 SCENE: Dual timeline. @GIRL — before: slumped on sofa, bill papers everywhere. After: same sofa, smiling, phone in hand showing CredFix dashboard.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"[BEFORE] @GIRL surrounded by bills, EMI reminders, bank statements.",
'@GIRL: "I have ₹3.2 lakhs in debt and I don\'t even know where to start."',
'Looks at camera: "Every plan I make falls apart by Day 10."',
]),
("📖 CONTENT (5–18s)", NAVY, [
"[FLASHBACK] Phone screen shows CredFix Debt Coaching session.",
'@GIRL [narrating]: "My coach asked me one question: \'What does your ideal month look like?\'"',
'"Nobody had ever asked me that."',
'"We worked backwards from there. Debts ranked. Budget set. First target: Credit card."',
'"Month 2, I paid off my highest-interest card."',
'"Month 4, my credit score went up 40 points."',
]),
("📣 CTA (18–25s)", GREEN, [
"[AFTER] @GIRL smiling. App shows debt reduction progress.",
'"CredFix Debt Coaching. This is what a plan looks like."',
'"Download CredFix. Your coach is waiting."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"[PEHLE] @GIRL bills se ghiri hui, papers bikre hue.",
'@GIRL: "Mere upar ₹3.2 lakh ka karz hai aur mujhe nahi pata shuruat kahan se karoon."',
'Camera ki taraf: "Jo bhi plan banati hoon, woh 10 din mein toot jaata hai."',
]),
("📖 CONTENT — Hindi", NAVY, [
"[FLASHBACK] Phone screen CredFix coaching session dikha raha hai.",
'@GIRL [batati hai]: "Coach ne ek sawaal poocha: \'Aapka ideal mahina kaisa lagta hai?\'"',
'"Kisine kabhi aisa nahi poocha tha."',
'"Hum wahaan se peeche aaye. Debts rank kiye. Budget seta hua. Pehla target: credit card."',
'"2nd mahine mein, highest-interest card bhara."',
'"4th mahine mein, credit score 40 points upar gaya."',
]),
("📣 CTA — Hindi", GREEN, [
"[BAAD MEIN] @GIRL muskura rahi hai. App mein debt reduction dikh raha hai.",
'"CredFix Debt Coaching. Yahi hai plan."',
'"CredFix download karein. Aapka coach wait kar raha hai."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"[MUNDE] @GIRL bills naDuve kutti, papers ellede.",
'@GIRL: "Nanna meele ₹3.2 lakh saala ide, yaallinda shuru maaDali antha gothilla."',
'Camera kaḍe: "Yaavude plan maaDidaroo, 10 dina nalli mugihutte."',
]),
("📖 CONTENT — Kannada", NAVY, [
"[FLASHBACK] Phone screen CredFix coaching session tOrisuttade.",
'@GIRL [heluttale]: "Coach ondu prashne keeLidaru: \'Nimma ideal tingaLu haege iruttade?\'"',
'"Yaaro kabbu hage keeLiralla."',
'"Naavu alli inda hinde bandvi. Debts rank maaDi. Budget seTTu. Motta target: credit card."',
'"2ne tingaLalli, highest-interest card pay maaDide."',
'"4ne tingaLalli, credit score 40 points meele hOyitu."',
]),
("📣 CTA — Kannada", GREEN, [
"[NANTARA] @GIRL nagattidale. App nalli debt reduction tOrisuttade.",
'"CredFix Debt Coaching. Idu plan haege iruttade."',
'"CredFix download madi. Nimma coach kaayttiddare."',
]),
],
"visual_note": "Split-screen before/after. Warm cinematic tones. App screen recording overlay. Uplifting background music transition.",
"hashtags": "#DebtCoaching #CredFix #DebtFree #FinancialJourney #MoneyCoach #CreditScore #PersonalFinance #IndiaFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 9
# ════════════════════════════════════════════════════════════
{
"day": 9,
"theme": "Debt Coaching — What It Looks Like",
"posts": [
{
"num": 17, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "What Happens in a CredFix Debt Coaching Session?",
"service": "Debt Coaching",
"slides": [
("SLIDE 1 — COVER", "📞 What Actually Happens\nIn a Debt Coaching Session?\n\nNo Jargon. No Judgment. Just Solutions."),
("SLIDE 2", "🗣️ Session 1: Discovery\n\'Tell me everything\' moment.\nYour coach listens — income, debts, spending, stress.\nZero judgment. Complete confidentiality."),
("SLIDE 3", "📋 Session 2: Your Custom Plan\nNot a template. Not a PDF you forget.\nA living, breathing plan built for your numbers.\nWith clear monthly targets."),
("SLIDE 4", "📞 Ongoing: Weekly Check-Ins\nShort 15-20 min calls.\n\'How\'s the plan going? What\'s blocking you?\'\nReal-time adjustments when life happens."),
("SLIDE 5", "📊 Tracking: Your Dashboard\nSee your debt going down.\nCredit score going up.\nEvery month, you\'re winning."),
("SLIDE 6 — CTA", "💼 Book Your First Session\nCredFix Debt Coaching:\n✅ Real expert, not a bot\n✅ Completely confidential\n✅ Personalized to your situation\n✅ Results you can measure\n\n📲 Download CredFix Now"),
],
"caption": "A debt coaching session isn\'t about shame or judgment. It\'s about finally having someone smart in your corner. 🏆 CredFix Debt Coaching — because you deserve more than generic advice. 📲 Download — link in bio.",
"hashtags": "#DebtCoaching #CredFix #FinancialCoach #MoneyHelp #PersonalFinance #DebtFree #IndiaFinance",
},
{
"num": 18, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "The #1 Reason People Stay Stuck in Debt Forever",
"service": "Debt Coaching",
"visual": "Large bold statement poster. Dark navy background. Gold headline. CredFix branding.",
"pairs": [
("The Reason", "They never have a plan. They just hope it gets better."),
("The Truth", "Debt doesn\'t fix itself. Hope is not a strategy."),
("The Solution", "CredFix Debt Coaching gives you the PLAN you\'ve been missing."),
("The Outcome", "Real progress. Real milestones. Real freedom."),
],
"caption": "Hope is powerful. But hope alone never paid off a loan. 📋 A plan does. CredFix Debt Coaching creates your personalized financial resolution plan — and then walks with you until you\'re free. 📲 Download — link in bio.",
"hashtags": "#DebtFree #CredFix #DebtCoaching #FinancialPlanning #MoneyMindset #PersonalFinance #India",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 10
# ════════════════════════════════════════════════════════════
{
"day": 10,
"theme": "Legal Consultation — Know Your Rights",
"posts": [
{
"num": 19, "type": "🎬 REEL", "color": REEL_CLR,
"title": "A Lawyer in My Corner Changed the Game ⚖️ | Legal Consultation",
"service": "Legal Consultation",
"duration": "20–25 sec",
"scene": "📍 SCENE: @MAN at a lawyer's office. Overwhelmed. Lawyer calmly reviews papers and explains.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@MAN sits across from a lawyer, hands folded, looking lost.",
'@MAN: "I owe ₹8 lakhs. The bank is threatening to take my car."',
'"I signed so many papers. I don\'t even know what my rights are."',
'Looks at camera: "I felt completely alone."',
]),
("📖 CONTENT (5–18s)", NAVY, [
'LAWYER [calm]: "Let me see the loan agreement."',
'[Reviews] "This clause here — it\'s actually not enforceable."',
'@MAN: "Wait... WHAT?"',
'"You have more rights than you think. The bank can\'t do this without going through proper legal process."',
'"And we can negotiate the outstanding amount."',
'@MAN [exhales]: "Why didn\'t anyone tell me this before?"',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix Legal Consultation."',
'"Expert lawyers. Accessible to everyone."',
'"Know your rights. Understand your liabilities."',
'"Download CredFix. Don\'t face debt law alone."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@MAN lawyer ke saamne baith hai, haath bande, kho hua sa.",
'@MAN: "Mujhe ₹8 lakh dena hai. Bank meri gaadi le jaane ki dhamki de raha hai."',
'"Maine bahut kaagaz sign kiye hain. Mujhe pata bhi nahi mere kya haq hain."',
'Camera ki taraf: "Main bilkul akela feel kar raha tha."',
]),
("📖 CONTENT — Hindi", NAVY, [
'LAWYER [shant]: "Loan agreement dikhao."',
'[Dekhta hai] "Ye clause... ye actually enforceable nahi hai."',
'@MAN: "Ruko... KYA?"',
'"Aapke paas bahut zyada haq hain. Bank bina proper legal process ke ye nahi kar sakta."',
'"Aur hum outstanding amount negotiate kar sakte hain."',
'@MAN [saans lete hue]: "Kisine pehle kyun nahi bataya?"',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Legal Consultation."',
'"Expert lawyers. Sabke liye accessible."',
'"Apne haq samjhein. Liabilities samjhein."',
'"CredFix download karein. Debt law akele mat samhalo."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@MAN lawyer munde kuti aagide, kaigaLu muLidu, haarida haage.",
'@MAN: "Nanu ₹8 lakh kodabeku. Bank nanna gaaDi tegkobeku antha bhaya haaLuttide."',
'"Thumba documents sign maaDiddene. Nanna hakku yaavudu antha gothillave."',
'Camera kaḍe: "Naanu tumba eka aagi ideene anta anisitu."',
]),
("📖 CONTENT — Kannada", NAVY, [
'LAWYER [shaanthaagi]: "Loan agreement tOri."',
'[NoDuttare] "Ee clause — idu nijavaagiyoo enforce maaDabaradu."',
'@MAN: "Nillu... ENU?"',
'"Nimage thumba hakku ide. Sari kaanuni prakriye illdu bank idu maaDabaradu."',
'"Mattu naavu outstanding amount negotiate maaDabahudu."',
'@MAN [ushiru bidu]: "Yaaro munde yaake helillave?"',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Legal Consultation."',
'"Expert lawyers. Ella riguu accessible."',
'"Nimma hakku tiliyiri. Liabilities arthamaaDikoli."',
'"CredFix download madi. Debt kaanunu yakkela edurisikoLLbedi."',
]),
],
"visual_note": "Formal office setting. Warm desk lamp light. Papers and legal documents visible. Lawyer and client interaction — trust-building visual.",
"hashtags": "#LegalConsultation #CredFix #DebtLaw #BorrowerRights #LegalHelp #ExpertLawyer #IndiaFinance #DebtHelp",
},
{
"num": 20, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "5 Times You NEED a Debt Lawyer — Not Just Google",
"service": "Legal Consultation",
"slides": [
("SLIDE 1 — COVER", "⚖️ 5 Times Google\nIsn\'t Enough — You Need\na Real Debt Lawyer\n\n[CredFix Legal Consultation]"),
("SLIDE 2", "🔴 Situation #1: Bank Is Seizing Your Property\nOnce the legal process starts,\nevery hour matters.\nA lawyer can stop or slow the process."),
("SLIDE 3", "🔴 Situation #2: Court Summons Received\nThis is NOT optional.\nFailing to respond can result in\nex-parte judgements against you."),
("SLIDE 4", "🔴 Situation #3: Guarantor on Someone Else\'s Loan\nYou may be liable for amounts\nyou didn\'t even spend.\nKnow exactly what you\'re exposed to."),
("SLIDE 5", "🔴 Situation #4: Dispute Loan Amounts or Terms\nBanks make errors too.\nA lawyer reviews your agreement\nand disputes unfair terms."),
("SLIDE 6 — CTA", "🔴 Situation #5: Multiple Lenders Chasing You\nMultiple creditors = multiple legal threats.\nOne CredFix lawyer manages all of it.\n\n⚖️ CredFix Legal Consultation\n📲 Download Now — Link in Bio"),
],
"caption": "There\'s a difference between reading about debt law and actually knowing how it applies to YOUR situation. ⚖️ CredFix Legal Consultation connects you with real debt law experts — fast. 📲 Download — link in bio.",
"hashtags": "#LegalConsultation #CredFix #DebtLawyer #BorrowerRights #LegalHelp #IndiaFinance #DebtHelp #ExpertLawyer",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 11
# ════════════════════════════════════════════════════════════
{
"day": 11,
"theme": "Legal Services — Debt Rights & Representation",
"posts": [
{
"num": 21, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "5 Debt Rights Most Indians Don't Know They Have ⚖️",
"service": "Legal Consultation / Debt Shield",
"visual": "Bold numbered list poster. Dark navy background with gold numbers. Each right in white text. CredFix branded.",
"pairs": [
("Right 1", "You CANNOT be arrested for not repaying a consumer loan."),
("Right 2", "You have the right to know the EXACT amount you owe at any time."),
("Right 3", "Banks must give 60-day notice before repossessing secured assets."),
("Right 4", "You can NEGOTIATE loan terms even after defaulting."),
("Right 5", "Recovery agents must show authorization letters before speaking to you."),
],
"caption": "You\'re not powerless. You just don\'t know your power yet. 💪 These rights exist. CredFix Legal Consultation helps you use them. Save this. Share it. Your knowledge is your shield. 📲 Download CredFix — link in bio.",
"hashtags": "#DebtRights #CredFix #BorrowerRights #LegalRights #DebtHelp #IndiaFinance #KnowYourRights #PersonalFinance",
},
{
"num": 22, "type": "🎬 REEL", "color": REEL_CLR,
"title": "The Court Summons That Almost Destroyed Me 📄 | Legal Representation",
"service": "Legal Representation",
"duration": "20–25 sec",
"scene": "📍 SCENE: @BOY receives a court summons at his door. Pale. Shaking hands. Sits down heavily.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@BOY opens the door. Courier handed over.",
"He reads it. Face goes pale.",
'@BOY [shaking]: "Court summons. The bank is taking me to court."',
'Looks at camera: "I\'ve never been inside a court in my life."',
]),
("📖 CONTENT (5–18s)", NAVY, [
'"My hands were shaking. My wife didn\'t know what to say."',
'"A friend told me to call CredFix."',
'"I did. Within 2 hours, a debt lawyer was reviewing my case."',
'"He explained everything. What the bank could and couldn\'t do."',
'"He represented me. I didn\'t have to face it alone."',
'[Pause]: "The case was settled out of court. No judgment against me."',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix Legal Representation."',
'"Expert lawyers for debt disputes and court cases."',
'"You don\'t have to walk into that court alone."',
'"Download CredFix. We\'ve got you."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@BOY darwaza kholta hai. Courier milta hai.",
"Padhta hai. Chehra safed ho jaata hai.",
'@BOY [kaanpte hue]: "Court summons. Bank mujhe court le ja raha hai."',
'Camera ki taraf: "Meri zindagi mein kabhi court ke andar nahi gaya."',
]),
("📖 CONTENT — Hindi", NAVY, [
'"Haath kaanp rahe the. Biwi ke paas koi lafz nahi the."',
'"Dost ne CredFix ko call karne ko kaha."',
'"Maine kiya. 2 ghante mein ek debt lawyer mera case dekh raha tha."',
'"Unhone sab samjhaya. Bank kya kar sakta hai, kya nahi."',
'"Unhone meri taraf se ladai ki. Mujhe akele nahi jaana pada."',
'[Ruka]: "Mamla court se bahar settle hua. Mere khilaf koi judgment nahi."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix Legal Representation."',
'"Debt disputes aur court cases ke liye expert lawyers."',
'"Aapko akele us court mein nahi jaana."',
'"CredFix download karein. Hum aapke saath hain."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@BOY bagilu tereeyuttane. Courier baruttade.",
"Oduttane. Mugha beLettu haagaaguttade.",
'@BOY [naaDuttane]: "Court summons. Bank nannanu court ge kaLisutte."',
'Camera kaḍe: "Naanu yaavattu court oLage hOgillave."',
]),
("📖 CONTENT — Kannada", NAVY, [
'"Kaigaḷu naaDuttiddaavu. Hende enu heLuvudu antha gothiralla."',
'"Snehita CredFix ge call maaDu antha heLidanu."',
'"Naanu maaDide. 2 gaṇṭe nalli, ondu debt lawyer nanna case noDuttidda."',
'"Avaru ella vivisitidaru. Bank enu maaDabahudu, enu maaDabaradu."',
'"Avaru namma padiyaagi aaDidaru. Naanu yakkela hOgabahudittu."',
'[Ninthukolluttane]: "Case court hordage settle aayitu. Nanna virudda yaavude judgment illa."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix Legal Representation."',
'"Debt disputes mattu court cases ge expert lawyers."',
'"Neevu ekelaage aa court oḷage hOgabeku alla."',
'"CredFix download madi. Naavu nimmajote iddivi."',
]),
],
"visual_note": "Dramatic door opening. Summons close-up. Trembling hands. Cut to confident lawyer walking in. Tone shift: panic → resolution.",
"hashtags": "#LegalRepresentation #CourtSummons #CredFix #DebtLawyer #BorrowerRights #LegalHelp #IndiaFinance #DebtHelp",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 12
# ════════════════════════════════════════════════════════════
{
"day": 12,
"theme": "Credit Health Rebuilding — The Road Back",
"posts": [
{
"num": 23, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "Your Credit Score Rebuild Roadmap — From 500 to 750+",
"service": "Credit Health Rebuilding",
"slides": [
("SLIDE 1 — COVER", "📈 Credit Score: 500 → 750+\nThe Roadmap Nobody Talks About\n\n[CredFix Credit Health Rebuilding]"),
("SLIDE 2", "📍 Where You Might Be Now\nScore below 600?\nMultiple missed payments?\nLoans rejected repeatedly?\nThis is NOT the end. This is the starting line."),
("SLIDE 3", "Month 1–2: Stabilize\nStop any new defaults.\nPay at least minimum on all active loans.\nDispute any wrong entries on your credit report."),
("SLIDE 4", "Month 3–4: Activate\nGet a secured credit card or credit-builder loan.\nUse 10–30% of limit only.\nPay FULL balance monthly."),
("SLIDE 5", "Month 5–8: Build Momentum\nConsistent on-time payments = score climbs.\nEvery 3 months, check your score.\nTarget: Cross 650."),
("SLIDE 6", "Month 9–12: Reach New Heights\nYour history is building.\nLenders see a changed profile.\nTarget: 700+. Loans approved. New chapter."),
("SLIDE 7 — CTA", "🚀 CredFix Credit Health Rebuilding\n✅ Personalized rebuild plan\n✅ Expert guidance every step\n✅ Real progress tracking\n✅ From broken to bankable\n\n📲 Start Rebuilding — Download CredFix"),
],
"caption": "A 550 credit score isn\'t a life sentence. It\'s a starting point. 📈 The road back to 750+ is real — and CredFix Credit Health Rebuilding walks it with you, step by step, month by month. Save this roadmap. Share it with someone who needs hope today. 📲 Download — link in bio.",
"hashtags": "#CreditScore #CreditRebuild #CredFix #CreditHealth #CreditRepair #FinancialFreedom #IndiaFinance #DebtFree",
},
{
"num": 24, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "Your Credit Score Range — What It Actually Means 📊",
"service": "Credit Health Rebuilding",
"visual": "Color-coded credit score range infographic. Traffic light style — red to green spectrum. CredFix branded.",
"pairs": [
("300–549 — POOR (Red)", "Most loans rejected. High-risk borrower profile."),
("550–649 — FAIR (Orange)", "Some loans possible, high interest rates."),
("650–699 — GOOD (Yellow)", "Better options, but still room to grow."),
("700–749 — VERY GOOD (Light Green)", "Competitive rates. Most lenders approve."),
("750–900 — EXCELLENT (Green)", "Best rates. Premium products. Full access."),
],
"caption": "Where are you on this scale right now? 📊 Wherever you are — CredFix Credit Health Rebuilding helps you move UP. Every 50 points can mean the difference between rejection and approval. 📲 Download CredFix — link in bio.",
"hashtags": "#CreditScore #CreditRange #CredFix #CreditHealth #CIBIL #CreditRepair #IndiaFinance #LoanApproval",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 13
# ════════════════════════════════════════════════════════════
{
"day": 13,
"theme": "Credit Health — Rebuilding Your Future",
"posts": [
{
"num": 25, "type": "🎬 REEL", "color": REEL_CLR,
"title": "My Credit Score Was 490. Now It's 720. Here's What Happened. 📈 | Credit Health",
"service": "Credit Health Rebuilding",
"duration": "20–25 sec",
"scene": "📍 SCENE: @WOMAN looks at her phone — CIBIL score showing 490. Time-lapse style journey. End: same phone showing 720.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"@WOMAN staring at phone screen. CIBIL score: 490.",
'@WOMAN: "490. My credit score is 490."',
'"Every lender I call... the answer is the same: Rejected."',
'Looks at camera: "I thought this was forever."',
]),
("📖 CONTENT (5–18s)", NAVY, [
'"CredFix showed me my full credit report for the first time."',
'"Two wrong entries I didn\'t even put there — disputed and removed."',
'"A secured credit card. Small balance. Pay in full. Every month."',
'"Month 3 — 560. Month 6 — 630. Month 10 — 680. Month 14 — 720."',
'"14 months. From hopeless to bankable."',
]),
("📣 CTA (18–25s)", GREEN, [
"@WOMAN holds phone up — 720 on screen. Big smile.",
'"CredFix Credit Health Rebuilding. This is real."',
'"Download CredFix. Your score doesn\'t define your future — your plan does."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"@WOMAN phone screen dekh rahi hai. CIBIL score: 490.",
'@WOMAN: "490. Mera credit score 490 hai."',
'"Jis lender ko bhi call karti hoon... ek hi jawab: Reject."',
'Camera ki taraf: "Mujhe laga ye hamesha ke liye hai."',
]),
("📖 CONTENT — Hindi", NAVY, [
'"CredFix ne pehli baar meri full credit report dikhaayi."',
'"Do galat entries jo maine ki hi nahi thi — dispute karke hata di gayi."',
'"Ek secured credit card. Chhota balance. Har mahine full pay."',
'"3rd mahine — 560. 6th — 630. 10th — 680. 14th — 720."',
'"14 mahine mein. Umeed se bankable tak."',
]),
("📣 CTA — Hindi", GREEN, [
"@WOMAN phone utha rahi hai — screen pe 720. Badi muskaan.",
'"CredFix Credit Health Rebuilding. Ye sach hai."',
'"CredFix download karein. Aapka score aapka bhavishya nahi — aapka plan decide karta hai."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"@WOMAN phone screen noDuttale. CIBIL score: 490.",
'@WOMAN: "490. Nanna credit score 490."',
'"Yaavude lender ge call maaDidaroo... ondu hane answer: Reject."',
'Camera kaḍe: "Idu yaavattu heegeye anta anisitu."',
]),
("📖 CONTENT — Kannada", NAVY, [
'"CredFix motta mutham nanna full credit report tOrisitu."',
'"Eradu tappu entries — naanu maaDillade — dispute maaDi tegedu.'  ,
'"Ondu secured credit card. Chikka balance. Prathi tingaLu full pay."',
'"3ne tingaLu — 560. 6ne — 630. 10ne — 680. 14ne — 720."',
'"14 tingaLu. Niraashah inda bankable vare."',
]),
("📣 CTA — Kannada", GREEN, [
"@WOMAN phone etti tOristale — screen nalli 720. Dodda nagattu.",
'"CredFix Credit Health Rebuilding. Idu nijavaadadu."',
'"CredFix download madi. Nimma score nimma bhavishya alla — nimma plan maduttade."',
]),
],
"visual_note": "Phone screen close-up with score. Time-lapse visual effect for score rising. Emotional music. End on bright, hopeful tone.",
"hashtags": "#CreditRebuild #CreditScore #CredFix #CreditHealth #CIBIL #490to720 #CreditRepair #IndiaFinance",
},
{
"num": 26, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "5 Things CredFix Does to Rebuild Your Credit Health",
"service": "Credit Health Rebuilding",
"slides": [
("SLIDE 1 — COVER", "🏥 Credit Health Rebuilding:\nWhat CredFix Actually Does\nFor Your Score\n\n5 Proven Steps"),
("SLIDE 2", "🔍 Step 1: Full Credit Report Analysis\nWe pull your CIBIL report.\nFind every error, dispute, and wrong entry.\nErrors alone can fix 30–80 points immediately."),
("SLIDE 3", "✅ Step 2: Dispute Resolution\nWrong entries removed on your behalf.\nWorking directly with credit bureaus.\nLegal, effective, proven."),
("SLIDE 4", "💳 Step 3: Credit-Building Strategy\nSecured cards. Credit-builder loans.\nOptimal usage ratios.\nBuilding history the smart way."),
("SLIDE 5", "📅 Step 4: Payment Plan Optimization\nNever miss a due date again.\nReminders + accountability.\nEvery on-time payment = score points."),
("SLIDE 6 — CTA", "📈 Step 5: Track + Celebrate\nMonthly score tracking.\nMilestone celebrations.\nFrom broken credit to bankable profile.\n\n🚀 Download CredFix Now — Link in Bio"),
],
"caption": "Credit repair isn\'t magic. It\'s a method. 🔬 CredFix Credit Health Rebuilding applies that method — scientifically, consistently — until your score reflects who you really are. 📲 Download — link in bio.",
"hashtags": "#CreditRepair #CreditHealth #CredFix #CreditScore #CIBIL #CreditRebuild #IndiaFinance #DebtFree",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 14
# ════════════════════════════════════════════════════════════
{
"day": 14,
"theme": "CredFix Complete — All Services Overview",
"posts": [
{
"num": 27, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "CredFix Services — Everything You Need. One App. 📱",
"service": "All Services",
"visual": "Clean service grid layout. 9 service icons in a 3x3 grid. Brand navy background, gold icons. CredFix logo centered at top.",
"pairs": [
("🗺 Debt Navigator", "Personalized repayment plans for your loans"),
("🛡 Debt Shield", "Legal protection from harassment & notices"),
("🎓 Debt Coaching", "One-on-one expert financial guidance"),
("⚖️ Legal Consultation", "Expert lawyers for your debt questions"),
("📄 Legal Notice Response", "Professional replies to bank & court notices"),
("👩‍⚖️ Legal Representation", "We stand in court & negotiations for you"),
("📵 Harassment Protection", "Stop illegal collector calls & visits"),
("🤝 Debt Settlement", "Negotiate and reduce what you actually owe"),
("📈 Credit Health Rebuilding", "Rebuild your score from the ground up"),
],
"caption": "One debt problem. Nine powerful solutions. All in one app. 💪 CredFix is India\'s most complete debt resolution platform. Whatever stage you\'re at — we have the service for you. 📲 Download CredFix — link in bio.",
"hashtags": "#CredFix #AllServices #DebtHelp #DebtFree #PersonalFinance #LegalHelp #CreditHealth #IndiaFinance",
},
{
"num": 28, "type": "🎬 REEL", "color": REEL_CLR,
"title": "Life Before vs After CredFix — The Real Difference 🌅 | All Services",
"service": "All Services",
"duration": "20–25 sec",
"scene": "📍 SCENE: Split — BEFORE: Dark room, bills everywhere, phone buzzing with collector calls. AFTER: Bright room, clear desk, phone showing CredFix score dashboard.",
"script_en": [
("🎣 HOOK (0–5s)", RED, [
"[BEFORE — dark, stressful]",
"@PERSON surrounded by bills. Phone ringing. Collector's aggressive voice.",
'@PERSON [exhausted]: "I wake up every morning... and the first thing I feel is dread."',
]),
("📖 CONTENT (5–18s)", NAVY, [
"[TRANSITION — downloading CredFix]",
'"Debt Navigator showed me which loan to kill first."',
'"Debt Shield stopped the harassment calls. Legally."',
'"My coach helped me breathe again."',
'"A lawyer explained what the bank could and couldn\'t do."',
'"My credit score went from 540 to 690."',
"[AFTER — bright, clear]",
'@PERSON [smiling]: "I still have debt. But now... I have a plan."',
]),
("📣 CTA (18–25s)", GREEN, [
'"CredFix. Debt Navigator. Debt Shield. Coaching. Legal."',
'"Everything you need to go from overwhelmed to in control."',
'"Download CredFix now. Your new chapter starts today."',
]),
],
"hindi": [
("🎣 HOOK — Hindi", colors.HexColor("#7C3AED"), [
"[PEHLE — andhera, stress]",
"@PERSON bills se ghira hua. Phone bajta rehta hai. Aggressive recovery agent.",
'@PERSON [thaka hua]: "Har subah uthta hoon... aur pehla ehsaas hota hai darpoka."',
]),
("📖 CONTENT — Hindi", NAVY, [
"[TRANSITION — CredFix download]",
'"Debt Navigator ne bataya pehle kaunsa loan khatam karoon."',
'"Debt Shield ne harassment calls legally band kiya."',
'"Coach ne mujhe phir se saans lene diya."',
'"Lawyer ne samjhaya bank kya kar sakta hai, kya nahi."',
'"Mera credit score 540 se 690 ho gaya."',
"[BAAD MEIN — ujala, saaf]",
'@PERSON [muskurate hue]: "Karz abhi bhi hai. Par... ab mere paas plan hai."',
]),
("📣 CTA — Hindi", GREEN, [
'"CredFix. Debt Navigator. Debt Shield. Coaching. Legal."',
'"Jo bhi chahiye overwhelmed se in control jaane ke liye."',
'"CredFix abhi download karein. Aapka naya adhyaay aaj se shuru."',
]),
],
"kannada": [
("🎣 HOOK — Kannada", GREEN, [
"[MUNDE — kaḍime, stress]",
"@PERSON bills naDuve. Phone aDuttade. Aggressive recovery agent.",
'@PERSON [dayaLu]: "Prathi beLigge eddu... mottame mUDu andu bhaya."',
]),
("📖 CONTENT — Kannada", NAVY, [
"[TRANSITION — CredFix download]",
'"Debt Navigator yaavudu loan mottama mugisabeku antha tOrisitu."',
'"Debt Shield haraasment calls legally nilittu."',
'"Coach nannanu matthe ushiru biDalu maaDitu."',
'"Lawyer bank enu maaDabahudu, enu maaDabaradu antha vivisitu."',
'"Nanna credit score 540 inda 690 aayitu."',
"[NANTARA — beLakina, saraLa]",
'@PERSON [nagattu]: "Saala iddae. Aadare... ega nanna hatra plan ide."',
]),
("📣 CTA — Kannada", GREEN, [
'"CredFix. Debt Navigator. Debt Shield. Coaching. Legal."',
'"Overwhelmed inda in control ge hogalikke yenu beka adella ide."',
'"CredFix ega download madi. Nimma hosa adhyaaya ega shuruvaguttade."',
]),
],
"visual_note": "Stark before/after split. Before: dim blue-gray tones. After: warm golden light. Same actor, same space — total mood transformation.",
"hashtags": "#CredFix #BeforeAfter #DebtFree #LifeChange #AllServices #DebtHelp #PersonalFinance #IndiaFinance",
},
]
},

# ════════════════════════════════════════════════════════════
# DAY 15
# ════════════════════════════════════════════════════════════
{
"day": 15,
"theme": "Grand Finale — Your Journey Starts NOW",
"posts": [
{
"num": 29, "type": "📱 CAROUSEL", "color": CAROUSEL_CLR,
"title": "15 Days of Financial Wisdom — Your Complete CredFix Playbook",
"service": "All Services",
"slides": [
("SLIDE 1 — COVER", "📚 15 Days. 15 Lessons.\nYour Complete Guide to\nTaking Back Financial Control\n\n[CredFix — Your Debt Resolution Partner]"),
("SLIDE 2", "Days 1–3: Know Your Debt\n• Map every loan and EMI\n• Rank by interest rate — highest first\n• Build your repayment priority order\n→ CredFix Debt Navigator"),
("SLIDE 3", "Days 4–6: Know Your Rights\n• Debt collectors have strict legal limits\n• Legal notices have response deadlines\n• Harassment is illegal — and stoppable\n→ CredFix Debt Shield"),
("SLIDE 4", "Days 7–9: Get a Coach\n• Generic advice doesn\'t work for your life\n• A real plan needs a real person\n• Accountability is the missing piece\n→ CredFix Debt Coaching"),
("SLIDE 5", "Days 10–11: Get Legal\n• Some situations need a lawyer, not Google\n• Your rights are powerful — use them\n• Expert legal help is now accessible\n→ CredFix Legal Consultation"),
("SLIDE 6", "Days 12–13: Rebuild\n• Credit scores can be fixed — with method\n• Dispute errors, build history, pay on time\n• 750+ is possible from anywhere\n→ CredFix Credit Health Rebuilding"),
("SLIDE 7 — CTA", "🚀 Day 15: Act\nYou\'ve learned. You\'ve seen what\'s possible.\nNow it\'s time to start.\n\nCredFix:\n🗺 Debt Navigator\n🛡 Debt Shield\n🎓 Debt Coaching\n⚖️ Legal Consultation\n📈 Credit Health Rebuilding\n\n📲 Download CredFix — Your Journey Starts Today"),
],
"caption": "15 days. 9 services. One mission: your financial freedom. 🚀 CredFix is India\'s most complete debt resolution platform — and it starts with one download. Stop waiting for things to get better on their own. Take the first step. 📲 Download CredFix — link in bio.",
"hashtags": "#CredFix #15DayChallenge #DebtFree #FinancialFreedom #PersonalFinance #IndiaFinance #DebtHelp #CreditHealth",
},
{
"num": 30, "type": "🖼 STATIC", "color": STATIC_CLR,
"title": "Your Debt-Free Journey Starts With One Step 🚀",
"service": "All Services — Final CTA",
"visual": "Powerful hero poster. Sunrise/dawn visual metaphor. Large bold CTA. All service icons around the CredFix logo. Inspiring, aspirational design.",
"pairs": [
("You deserve to sleep without dreading tomorrow.", ""),
("You deserve to answer your phone without fear.", ""),
("You deserve to walk into a bank and say YES.", ""),
("You deserve a plan. A coach. A lawyer. A score that opens doors.", ""),
("You deserve CredFix.", ""),
],
"caption": "The debt you carry today is not the story you have to live forever. 🌅 CredFix is built for people who are ready to fight back — smart, legally, and with expert support. 30 posts. 15 days. One message: Your freedom is possible. 📲 Download CredFix now — link in bio. 💙 #CredFix",
"hashtags": "#CredFix #DebtFree #FinancialFreedom #NewBeginning #TakeControl #PersonalFinance #IndiaFinance #YourJourneyStartsNow",
},
]
},

]

# ─── Build PDF ──────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        "/mnt/user-data/outputs/CredFix_15Day_Content_Plan.pdf",
        pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.8*cm
    )

    story = []

    # ── COVER PAGE ──────────────────────────────────────────
    # Simulate a colored background using a wide table
    cover_data = [[
        Paragraph("C R E D F I X", S("ctag", fontSize=11, textColor=GOLD, fontName="Helvetica-Bold",
                                       alignment=TA_CENTER, leading=16, charSpace=8)),
    ],[
        Paragraph("SERVICES", S("ctag2", fontSize=9, textColor=colors.HexColor("#94A3B8"),
                                 alignment=TA_CENTER, fontName="Helvetica", charSpace=5, leading=14)),
    ],[
        Spacer(1, 20),
    ],[
        Paragraph("15-DAY SOCIAL MEDIA", S("cvt", fontSize=28, textColor=WHITE, fontName="Helvetica-Bold",
                                            alignment=TA_CENTER, leading=34)),
    ],[
        Paragraph("CONTENT PLAN", S("cvt2", fontSize=36, textColor=GOLD, fontName="Helvetica-Bold",
                                     alignment=TA_CENTER, leading=42)),
    ],[
        Spacer(1, 16),
    ],[
        Paragraph("30 Ready-to-Use Posts  |  Reels, Carousels & Static", S("cvsub", fontSize=12,
                   textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER, fontName="Helvetica", leading=18)),
    ],[
        Paragraph("Reel Scripts in Hindi & Kannada  |  Cinematic Storytelling Format", S("cvsub2", fontSize=11,
                   textColor=colors.HexColor("#94A3B8"), alignment=TA_CENTER, fontName="Helvetica", leading=16)),
    ],[
        Spacer(1, 30),
    ],[
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", S("divider", fontSize=10, textColor=GOLD,
                   alignment=TA_CENTER, leading=14)),
    ],[
        Spacer(1, 16),
    ],[
        Paragraph("SERVICES COVERED", S("scl", fontSize=9, textColor=GOLD, fontName="Helvetica-Bold",
                                         alignment=TA_CENTER, charSpace=4, leading=14)),
    ],[
        Paragraph("Debt Navigator  •  Debt Shield  •  Debt Coaching\nLegal Consultation  •  Legal Representation\nHarassment Protection  •  Debt Settlement\nCredit Health Rebuilding",
                  S("svc", fontSize=10, textColor=WHITE, fontName="Helvetica", alignment=TA_CENTER, leading=18)),
    ],[
        Spacer(1, 30),
    ],[
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", S("divider2", fontSize=10, textColor=colors.HexColor("#334155"),
                   alignment=TA_CENTER, leading=14)),
    ],[
        Spacer(1, 14),
    ],[
        Paragraph("10 Reels  |  10 Carousels  |  10 Static Posts",
                  S("cnt", fontSize=10, textColor=TEAL, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14)),
    ],[
        Paragraph("2 Posts Per Day  |  Indian Market Optimized",
                  S("cnt2", fontSize=10, textColor=colors.HexColor("#94A3B8"), fontName="Helvetica",
                    alignment=TA_CENTER, leading=14)),
    ],[
        Spacer(1, 40),
    ],[
        Paragraph("credfix.in", S("url", fontSize=9, textColor=colors.HexColor("#475569"),
                   fontName="Helvetica", alignment=TA_CENTER, leading=12)),
    ]]

    cover_table = Table(cover_data, colWidths=[W - 3*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), NAVY),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING", (0,0),(-1,-1), 20),
        ("RIGHTPADDING",(0,0),(-1,-1),20),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ───────────────────────────────────
    story.append(Paragraph("CONTENT CALENDAR OVERVIEW", S("toc_h", fontSize=16, textColor=NAVY,
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=22, spaceAfter=16)))

    toc_rows = [["Day", "Theme", "Post 1", "Post 2"]]
    themes_short = [
        (1, "Debt Navigator — Know Your Debt", "🎬 Loan Rejected (Reel)", "📱 5 Warning Signs (Carousel)"),
        (2, "Debt Navigator — Break EMI Trap", "🖼 Credit Myths (Static)", "🎬 EMI Trap Story (Reel)"),
        (3, "Debt Navigator — How It Works", "📱 Step-by-Step Guide (Carousel)", "🖼 Interest Priority (Static)"),
        (4, "Debt Shield — Legal Rights", "🎬 Collector Harassment (Reel)", "📱 6 Borrower Rights (Carousel)"),
        (5, "Debt Shield — Legal Notices", "🖼 Do/Don't Legal Notice (Static)", "🎬 Bank Notice Panic (Reel)"),
        (6, "Debt Shield — Protection", "📱 4 Ways We Protect (Carousel)", "🖼 After 7PM Calls (Static)"),
        (7, "Debt Coaching — One-on-One", "🎬 One Call Changed All (Reel)", "📱 6 Steps to Freedom (Carousel)"),
        (8, "Debt Coaching — Why Coach?", "🖼 DIY vs Coaching (Static)", "🎬 Drowning to Breathing (Reel)"),
        (9, "Debt Coaching — The Process", "📱 Coaching Session (Carousel)", "🖼 #1 Reason Stuck (Static)"),
        (10, "Legal Consultation — Rights", "🎬 Lawyer Changed Game (Reel)", "📱 5 Times Need Lawyer (Carousel)"),
        (11, "Legal — Representation", "🖼 5 Rights You Didn't Know (Static)", "🎬 Court Summons Story (Reel)"),
        (12, "Credit Health — Roadmap", "📱 Score Rebuild Roadmap (Carousel)", "🖼 Score Range Guide (Static)"),
        (13, "Credit Health — Journey", "🎬 490 to 720 Story (Reel)", "📱 5 Things CredFix Does (Carousel)"),
        (14, "All Services — Overview", "🖼 All 9 Services (Static)", "🎬 Before vs After (Reel)"),
        (15, "Grand Finale — Act Now", "📱 15-Day Playbook (Carousel)", "🖼 Final CTA Poster (Static)"),
    ]

    for row in themes_short:
        toc_rows.append([str(row[0]), row[1], row[2], row[3]])

    toc_table = Table(toc_rows, colWidths=[1*cm, 5.5*cm, 5.5*cm, 5.5*cm])
    toc_style = TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,0), 8),
        ("ALIGN",        (0,0),(-1,-1), "CENTER"),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("FONTSIZE",     (0,1),(-1,-1), 7.5),
        ("FONTNAME",     (0,1),(-1,-1), "Helvetica"),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("GRID",         (0,0),(-1,-1), 0.3, colors.HexColor("#D1D5DB")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [SOFT_GRAY, WHITE]),
        ("TEXTCOLOR",    (0,1),(0,-1), NAVY),
        ("FONTNAME",     (0,1),(0,-1), "Helvetica-Bold"),
    ])
    # Highlight weekend rows
    for i in range(1, len(toc_rows)):
        if toc_rows[i][0] in ["7", "14"]:
            toc_style.add("BACKGROUND", (0,i), (-1,i), colors.HexColor("#DBEAFE"))
    toc_table.setStyle(toc_style)
    story.append(toc_table)
    story.append(sp(12))

    # Legend
    legend_data = [[
        Paragraph("🎬 REEL — Cinematic Story (Hindi + Kannada Versions Included)", 
                  S("leg", fontSize=8, textColor=REEL_CLR, fontName="Helvetica-Bold", leading=11)),
        Paragraph("📱 CAROUSEL — Slide-by-Slide Content",
                  S("leg2", fontSize=8, textColor=CAROUSEL_CLR, fontName="Helvetica-Bold", leading=11)),
        Paragraph("🖼 STATIC — Single Image Post",
                  S("leg3", fontSize=8, textColor=STATIC_CLR, fontName="Helvetica-Bold", leading=11)),
    ]]
    legend_t = Table(legend_data, colWidths=[(W-3*cm)/3]*3)
    legend_t.setStyle(TableStyle([
        ("ALIGN", (0,0),(-1,-1), "CENTER"),
        ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("BOX", (0,0),(0,-1), 1, REEL_CLR),
        ("BOX", (1,0),(1,-1), 1, CAROUSEL_CLR),
        ("BOX", (2,0),(2,-1), 1, STATIC_CLR),
        ("BACKGROUND", (0,0),(0,-1), colors.HexColor("#F3E8FF")),
        ("BACKGROUND", (1,0),(1,-1), colors.HexColor("#E0F2FE")),
        ("BACKGROUND", (2,0),(2,-1), colors.HexColor("#D1FAE5")),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
    ]))
    story.append(legend_t)
    story.append(PageBreak())

    # ── CONTENT PAGES ───────────────────────────────────────
    for day_data in DAYS:
        day = day_data["day"]
        theme = day_data["theme"]

        # Day divider header
        dh = day_header_table(day, theme)
        story.append(dh)
        story.append(sp(10))

        for post in day_data["posts"]:
            ptype = post["type"]
            pcolor = post["color"]
            ptitle = post["title"]
            pnum = post["num"]
            pservice = post.get("service", "")

            # Post header
            story.append(post_header(pnum, ptype, ptitle, pcolor))
            story.append(sp(6))

            # Service badge
            svc_data = [[
                Paragraph(f"Service: {pservice}", S("sv", fontSize=8, textColor=GRAY, fontName="Helvetica-Oblique", leading=11)),
            ]]

            # ── REEL ──────────────────────────────────────
            if "REEL" in ptype:
                dur = post.get("duration","20–25 sec")
                scene = post.get("scene","")

                # Duration + scene
                info_data = [[
                    Paragraph(f"⏱ Duration: {dur}", S("dur", fontSize=8.5, textColor=WHITE, fontName="Helvetica-Bold", leading=12)),
                    Paragraph(f"Hook → Content → CTA  |  Cinematic Storytelling Format", S("fmt", fontSize=8.5, textColor=GOLD, fontName="Helvetica", leading=12)),
                ]]
                info_t = Table(info_data, colWidths=[4.5*cm, W-9*cm])
                info_t.setStyle(TableStyle([
                    ("BACKGROUND", (0,0),(-1,-1), BLUE),
                    ("ALIGN", (0,0),(-1,-1), "LEFT"),
                    ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
                    ("TOPPADDING", (0,0),(-1,-1), 5),
                    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
                    ("LEFTPADDING", (0,0),(-1,-1), 10),
                    ("RIGHTPADDING", (0,0),(-1,-1), 8),
                ]))
                story.append(info_t)
                story.append(sp(5))

                # Scene
                scene_data = [[Paragraph(scene, S("sc", fontSize=8.5, textColor=colors.HexColor("#374151"),
                               fontName="Helvetica-Oblique", leading=12))]]
                scene_t = Table(scene_data, colWidths=[W-3*cm])
                scene_t.setStyle(TableStyle([
                    ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#FFF7ED")),
                    ("TOPPADDING", (0,0),(-1,-1), 6), ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                    ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ("BOX", (0,0),(-1,-1), 0.5, GOLD),
                ]))
                story.append(scene_t)
                story.append(sp(8))

                # English script
                story.append(Paragraph("🇬🇧 ENGLISH SCRIPT", S("lang", fontSize=9, textColor=ACCENT,
                             fontName="Helvetica-Bold", leading=12, spaceAfter=4)))
                for section_title, section_color, lines in post["script_en"]:
                    sec_header = [[Paragraph(section_title, S("sh", fontSize=8.5, textColor=WHITE,
                                   fontName="Helvetica-Bold", leading=11))]]
                    sh_t = Table(sec_header, colWidths=[W-3*cm])
                    sh_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), section_color),
                        ("TOPPADDING", (0,0),(-1,-1), 4), ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ]))
                    story.append(sh_t)
                    for line in lines:
                        story.append(Paragraph(f"  {line}", S("sl", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                     fontName="Helvetica", leading=13, leftIndent=8)))
                    story.append(sp(3))

                story.append(sp(6))

                # Hindi script
                story.append(Paragraph("🇮🇳 HINDI VERSION (हिंदी)", S("lang_h", fontSize=9, textColor=colors.HexColor("#7C3AED"),
                             fontName="Helvetica-Bold", leading=12, spaceAfter=4)))
                for section_title, section_color, lines in post["hindi"]:
                    sec_header = [[Paragraph(section_title, S("shh", fontSize=8.5, textColor=WHITE,
                                   fontName="Helvetica-Bold", leading=11))]]
                    sh_t = Table(sec_header, colWidths=[W-3*cm])
                    sh_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#7C3AED")),
                        ("TOPPADDING", (0,0),(-1,-1), 4), ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ]))
                    story.append(sh_t)
                    for line in lines:
                        story.append(Paragraph(f"  {line}", S("sl2", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                     fontName="Helvetica", leading=13, leftIndent=8)))
                    story.append(sp(3))

                story.append(sp(6))

                # Kannada script
                story.append(Paragraph("🌟 KANNADA VERSION (ಕನ್ನಡ)", S("lang_k", fontSize=9, textColor=GREEN,
                             fontName="Helvetica-Bold", leading=12, spaceAfter=4)))
                for section_title, section_color, lines in post["kannada"]:
                    sec_header = [[Paragraph(section_title, S("shk", fontSize=8.5, textColor=WHITE,
                                   fontName="Helvetica-Bold", leading=11))]]
                    sh_t = Table(sec_header, colWidths=[W-3*cm])
                    sh_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), GREEN),
                        ("TOPPADDING", (0,0),(-1,-1), 4), ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ]))
                    story.append(sh_t)
                    for line in lines:
                        story.append(Paragraph(f"  {line}", S("sl3", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                     fontName="Helvetica", leading=13, leftIndent=8)))
                    story.append(sp(3))

                story.append(sp(5))

                # Visual note + hashtags
                vn = post.get("visual_note","")
                if vn:
                    vn_data = [[Paragraph(f"🎥 Visual Direction: {vn}",
                                S("vn", fontSize=8, textColor=colors.HexColor("#6B7280"), fontName="Helvetica-Oblique", leading=11))]]
                    vn_t = Table(vn_data, colWidths=[W-3*cm])
                    vn_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), SOFT_GRAY),
                        ("TOPPADDING", (0,0),(-1,-1), 5), ("BOTTOMPADDING", (0,0),(-1,-1), 5),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                    ]))
                    story.append(vn_t)
                    story.append(sp(4))

                ht = post.get("hashtags","")
                if ht:
                    story.append(Paragraph(ht, S("ht", fontSize=8, textColor=TEAL, fontName="Helvetica", leading=12)))

            # ── CAROUSEL ──────────────────────────────────
            elif "CAROUSEL" in ptype:
                slides = post.get("slides", [])
                story.append(Paragraph(f"📱 {len(slides)} Slides  |  Ready to Design in Canva / Adobe Express",
                             S("cn", fontSize=8.5, textColor=CAROUSEL_CLR, fontName="Helvetica-Bold", leading=12, spaceAfter=6)))

                for i, (slide_title, slide_content) in enumerate(slides):
                    s_rows = [[
                        Paragraph(slide_title, S("st", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", leading=11)),
                    ],[
                        Paragraph(slide_content, S("sc2", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                  fontName="Helvetica", leading=13)),
                    ]]
                    s_t = Table(s_rows, colWidths=[W-3*cm])
                    bg = CAROUSEL_CLR if i == 0 or "CTA" in slide_title else colors.HexColor("#E0F2FE")
                    tc = WHITE if i == 0 or "CTA" in slide_title else colors.HexColor("#1F2937")
                    s_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(0,0), CAROUSEL_CLR if i == 0 else BLUE if "CTA" in slide_title else colors.HexColor("#0369A1")),
                        ("BACKGROUND", (0,1),(0,1), colors.HexColor("#E0F2FE") if i > 0 else colors.HexColor("#0284C7")),
                        ("TEXTCOLOR", (0,0),(0,0), WHITE),
                        ("TEXTCOLOR", (0,1),(0,1), colors.HexColor("#1E3A5F") if i > 0 else WHITE),
                        ("TOPPADDING", (0,0),(-1,-1), 4), ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                        ("BOX", (0,0),(-1,-1), 0.5, CAROUSEL_CLR),
                    ]))
                    story.append(s_t)
                    story.append(sp(3))

                story.append(sp(5))
                cap = post.get("caption","")
                if cap:
                    cap_data = [[Paragraph(f"📝 Caption:\n{cap}", S("cap", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                fontName="Helvetica", leading=13))]]
                    cap_t = Table(cap_data, colWidths=[W-3*cm])
                    cap_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#F0FDF4")),
                        ("TOPPADDING", (0,0),(-1,-1), 8), ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                        ("BOX", (0,0),(-1,-1), 0.5, GREEN),
                    ]))
                    story.append(cap_t)
                    story.append(sp(4))

                ht = post.get("hashtags","")
                if ht:
                    story.append(Paragraph(ht, S("ht2", fontSize=8, textColor=TEAL, fontName="Helvetica", leading=12)))

            # ── STATIC ────────────────────────────────────
            elif "STATIC" in ptype:
                visual = post.get("visual","")
                if visual:
                    vis_data = [[Paragraph(f"🖼 Visual Concept: {visual}",
                                S("vis", fontSize=8.5, textColor=colors.HexColor("#374151"), fontName="Helvetica-Oblique", leading=12))]]
                    vis_t = Table(vis_data, colWidths=[W-3*cm])
                    vis_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#FFF7ED")),
                        ("TOPPADDING", (0,0),(-1,-1), 6), ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                        ("BOX", (0,0),(-1,-1), 0.5, GOLD),
                    ]))
                    story.append(vis_t)
                    story.append(sp(8))

                pairs = post.get("pairs", [])
                if pairs:
                    story.append(Paragraph("📌 Content Blocks:", S("cb_lbl", fontSize=9, textColor=STATIC_CLR,
                                 fontName="Helvetica-Bold", leading=12, spaceAfter=4)))
                    for label_txt, val_txt in pairs:
                        if val_txt:
                            row_data = [[
                                Paragraph(label_txt, S("lbl", fontSize=8.5, textColor=WHITE, fontName="Helvetica-Bold", leading=11)),
                                Paragraph(val_txt, S("val", fontSize=8.5, textColor=colors.HexColor("#1F2937"), fontName="Helvetica", leading=12)),
                            ]]
                            rt = Table(row_data, colWidths=[4.5*cm, W-9*cm])
                            rt.setStyle(TableStyle([
                                ("BACKGROUND", (0,0),(0,0), STATIC_CLR),
                                ("BACKGROUND", (1,0),(1,0), colors.HexColor("#D1FAE5")),
                                ("TOPPADDING", (0,0),(-1,-1), 4), ("BOTTOMPADDING", (0,0),(-1,-1), 4),
                                ("LEFTPADDING", (0,0),(-1,-1), 8), ("RIGHTPADDING", (0,0),(-1,-1), 8),
                                ("BOX", (0,0),(-1,-1), 0.3, colors.HexColor("#A7F3D0")),
                                ("VALIGN", (0,0),(-1,-1), "MIDDLE"),
                            ]))
                            story.append(rt)
                        else:
                            story.append(Paragraph(f"  ✦ {label_txt}", S("bullet", fontSize=9, textColor=NAVY,
                                         fontName="Helvetica", leading=14, leftIndent=8)))
                        story.append(sp(2))

                story.append(sp(6))
                cap = post.get("caption","")
                if cap:
                    cap_data = [[Paragraph(f"📝 Caption:\n{cap}", S("cap2", fontSize=8.5, textColor=colors.HexColor("#1F2937"),
                                fontName="Helvetica", leading=13))]]
                    cap_t = Table(cap_data, colWidths=[W-3*cm])
                    cap_t.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#F0FDF4")),
                        ("TOPPADDING", (0,0),(-1,-1), 8), ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                        ("LEFTPADDING", (0,0),(-1,-1), 10), ("RIGHTPADDING", (0,0),(-1,-1), 10),
                        ("BOX", (0,0),(-1,-1), 0.5, GREEN),
                    ]))
                    story.append(cap_t)
                    story.append(sp(4))

                ht = post.get("hashtags","")
                if ht:
                    story.append(Paragraph(ht, S("ht3", fontSize=8, textColor=TEAL, fontName="Helvetica", leading=12)))

            story.append(sp(14))
            story.append(hr())
            story.append(sp(8))

        story.append(PageBreak())

    # ── BACK COVER / TIPS PAGE ──────────────────────────────
    tips_data = [[
        Paragraph("PRODUCTION TIPS & BEST PRACTICES", S("tips_h", fontSize=14, textColor=WHITE,
                   fontName="Helvetica-Bold", alignment=TA_CENTER, leading=20)),
    ],[
        Spacer(1, 12),
    ],[
        Paragraph("📱 REEL PRODUCTION GUIDELINES", S("tph", fontSize=10, textColor=GOLD,
                   fontName="Helvetica-Bold", leading=14)),
    ],[
        Paragraph("• Shoot in 9:16 vertical format (1080×1920px) for Instagram/YouTube Shorts\n• Keep subtitles ON — 85% of reels are watched without sound\n• Use jump cuts every 2-3 seconds to maintain energy\n• Record in good natural light or ring light — avoid shadows\n• Add trending background music at 20-30% volume\n• Always include your logo watermark in the bottom corner\n• Hook must appear in the FIRST 2 seconds or viewers scroll away\n• Film 3 takes of every scene — use the most natural one",
                  S("tp", fontSize=9, textColor=WHITE, fontName="Helvetica", leading=14)),
    ],[
        Spacer(1, 10),
    ],[
        Paragraph("📱 CAROUSEL DESIGN GUIDELINES", S("tph2", fontSize=10, textColor=TEAL,
                   fontName="Helvetica-Bold", leading=14)),
    ],[
        Paragraph("• Design in 1:1 square (1080×1080px) or 4:5 portrait for max reach\n• Slide 1 MUST stop the scroll — bold headline, strong visual\n• Keep each slide to ONE idea — do not overwhelm\n• Use consistent brand colors: CredFix Navy #0A1628, Gold #F59E0B, Blue #2563EB\n• End every carousel with a clear CTA slide\n• Use Canva, Adobe Express, or Figma for design\n• Recommended: 5-7 slides per carousel",
                  S("tp2", fontSize=9, textColor=WHITE, fontName="Helvetica", leading=14)),
    ],[
        Spacer(1, 10),
    ],[
        Paragraph("🖼 STATIC POST GUIDELINES", S("tph3", fontSize=10, textColor=GREEN,
                   fontName="Helvetica-Bold", leading=14)),
    ],[
        Paragraph("• Size: 1080×1080px square or 1080×1350px portrait\n• Strong visual hierarchy: Big headline → Supporting text → CTA\n• Keep text minimal — let the design breathe\n• Always include CredFix branding and website\n• Post at peak hours: 7-9 AM, 12-2 PM, 7-10 PM IST\n• Save-worthy content performs best — give real value",
                  S("tp3", fontSize=9, textColor=WHITE, fontName="Helvetica", leading=14)),
    ],[
        Spacer(1, 14),
    ],[
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", S("div3", fontSize=8,
                   textColor=colors.HexColor("#334155"), alignment=TA_CENTER, leading=10)),
    ],[
        Spacer(1, 10),
    ],[
        Paragraph("POSTING SCHEDULE RECOMMENDATION", S("ps", fontSize=10, textColor=GOLD,
                   fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14)),
    ],[
        Paragraph("Post 1: 8:00 AM IST  |  Post 2: 7:00 PM IST\nWeekdays: Reels + Carousels  |  Weekends: Static + Engagement Posts\nBest days: Tuesday, Wednesday, Friday, Sunday",
                  S("ps2", fontSize=9, textColor=WHITE, fontName="Helvetica", alignment=TA_CENTER, leading=15)),
    ],[
        Spacer(1, 20),
    ],[
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", S("div4", fontSize=8,
                   textColor=colors.HexColor("#334155"), alignment=TA_CENTER, leading=10)),
    ],[
        Spacer(1, 12),
    ],[
        Paragraph("CredFix Services  |  Your Complete Debt Resolution Partner",
                  S("footer", fontSize=10, textColor=GOLD, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=16)),
    ],[
        Paragraph("Debt Navigator  •  Debt Shield  •  Debt Coaching  •  Legal Consultation  •  Credit Health Rebuilding",
                  S("footer2", fontSize=8, textColor=colors.HexColor("#94A3B8"), fontName="Helvetica",
                    alignment=TA_CENTER, leading=13)),
    ]]

    tips_table = Table(tips_data, colWidths=[W-3*cm])
    tips_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), NAVY),
        ("TOPPADDING", (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0),(-1,-1), 20),
        ("RIGHTPADDING", (0,0),(-1,-1), 20),
    ]))
    story.append(tips_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF built successfully!")

if __name__ == "__main__":
    build_pdf()
