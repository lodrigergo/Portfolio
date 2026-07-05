# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, 'fonts') + os.sep
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'assets'))
pdfmetrics.registerFont(TTFont('DV', F+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', F+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVS', F+'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DVSB', F+'DejaVuSerif-Bold.ttf'))

NAVY = HexColor('#0b1424'); DEEP = HexColor('#060a14')
CYAN = HexColor('#22d3ee'); CYAND = HexColor('#0e7490')
TEXT = HexColor('#1b2233'); MUTED = HexColor('#5d6b82')
LINE = HexColor('#d9e0ea'); LIGHT = HexColor('#eaf7fa')

W, H = A4; M = 16*mm; HEAD = 46*mm

s_sec   = ParagraphStyle('sec', fontName='DVB', fontSize=10.5, textColor=NAVY, spaceBefore=13, spaceAfter=2)
s_body  = ParagraphStyle('body', fontName='DV', fontSize=9, leading=13.5, textColor=TEXT)
s_mut   = ParagraphStyle('mut', parent=s_body, textColor=MUTED)
s_bul   = ParagraphStyle('bul', parent=s_mut, leftIndent=10, bulletIndent=0)
s_job   = ParagraphStyle('job', fontName='DVB', fontSize=9.6, textColor=TEXT)
s_date  = ParagraphStyle('date', fontName='DVB', fontSize=8, textColor=CYAND, alignment=TA_RIGHT)
s_tech_h= ParagraphStyle('techh', fontName='DVB', fontSize=9, textColor=CYAND, spaceAfter=2)

def sec(title):
    return [Spacer(1,2), Paragraph(title.upper(), s_sec),
            HRFlowable(width='100%', thickness=1.6, color=CYAN, spaceBefore=1, spaceAfter=7, lineCap='butt')]

def entry(title, date, bullets):
    t = Table([[Paragraph(title, s_job), Paragraph(date, s_date)]], colWidths=[(W-2*M)*0.72, (W-2*M)*0.28])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    out = [t]
    for b in bullets: out.append(Paragraph(b, s_bul, bulletText='•'))
    out.append(Spacer(1,7))
    return out

def kv_rows(rows):
    data = [[Paragraph('<b>%s</b>' % k, s_body), Paragraph(v, s_mut)] for k,v in rows]
    t = Table(data, colWidths=[(W-2*M)*0.30, (W-2*M)*0.70])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
    return [t]

def tech_grid(cols):
    cells = []
    for h, items in cols:
        inner = [Paragraph(h, s_tech_h)] + [Paragraph(i, s_bul, bulletText='•') for i in items]
        cells.append(inner)
    t = Table([cells], colWidths=[(W-2*M)/2.0]*2)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),10),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return [t]


def sec_entries(title, items):
    out = [KeepTogether(sec(title) + entry(*items[0]))]
    for e in items[1:]: out.append(KeepTogether(entry(*e)))
    return out

def build(fn, L):
    def header(c, d):
        c.saveState()
        c.setFillColor(NAVY); c.rect(0, H-HEAD, W, HEAD, stroke=0, fill=1)
        c.setFillColor(CYAN); c.rect(0, H-HEAD-1.2*mm, W, 1.2*mm, stroke=0, fill=1)
        c.setFillColor(HexColor('#ffffff')); c.setFont('DVSB', 23)
        c.drawString(M, H-17*mm, L['name1'] + ' ')
        w1 = c.stringWidth(L['name1']+' ', 'DVSB', 23)
        c.setFillColor(CYAN); c.drawString(M+w1, H-17*mm, L['name2'])
        c.setFillColor(HexColor('#9fc4cf')); c.setFont('DVB', 10.5)
        c.drawString(M, H-24*mm, L['role'])
        c.setFont('DV', 8.6); c.setFillColor(HexColor('#c7d5db'))
        c.drawString(M, H-32*mm, 'gergolodri6@gmail.com   ·   +36 20 290 1141   ·   Pécs')
        c.drawString(M, H-37*mm, 'github.com/lodrigergo   ·   lodrigergo.github.io/Portfolio   ·   linkedin.com/in/gergő-lódri')
        footer(c, d)
        c.restoreState()
    def footer(c, d):
        c.setFont('DV', 7.5); c.setFillColor(MUTED)
        c.drawCentredString(W/2, 9*mm, '© 2026 Lódri Gergő  ·  gergolodri6@gmail.com')
        c.drawRightString(W-M, 9*mm, str(d.page))
        c.setFillColor(CYAN); c.rect(0, 0, W, 1*mm, stroke=0, fill=1)
    def later(c, d):
        c.saveState()
        c.setFillColor(NAVY); c.rect(0, H-13*mm, W, 13*mm, stroke=0, fill=1)
        c.setFillColor(HexColor('#ffffff')); c.setFont('DVSB', 10)
        c.drawString(M, H-8.5*mm, L['name1']+' '+L['name2'])
        c.setFillColor(CYAN); c.setFont('DV', 8.2)
        c.drawRightString(W-M, H-8.5*mm, L['doctitle'])
        footer(c, d)
        c.restoreState()

    doc = BaseDocTemplate(fn, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=15*mm,
                          title=L['doctitle'], author='Lódri Gergő')
    f1 = Frame(M, 15*mm, W-2*M, H-HEAD-20*mm, id='f1')
    f2 = Frame(M, 15*mm, W-2*M, H-13*mm-19*mm, id='f2')
    doc.addPageTemplates([PageTemplate(id='first', frames=[f1], onPage=header),
                          PageTemplate(id='later', frames=[f2], onPage=later)])
    story = [Paragraph('', s_body)]
    story += sec(L['s_profile']) + [Paragraph(L['profile'], s_mut)]
    story += sec(L['s_personal']) + kv_rows(L['personal'])
    story += sec_entries(L['s_exp'], L['exp'])
    story += sec_entries(L['s_edu'], L['edu'])
    story += sec(L['s_tech']) + tech_grid(L['tech'])
    story += sec_entries(L['s_proj'], L['proj'])
    story += sec_entries(L['s_cert'], L['cert'])
    story += sec_entries(L['s_int'], L['int'])
    story += sec(L['s_str']) + [Paragraph(L['strengths'], s_body)]
    story += [KeepTogether(sec(L['s_hobby']) + [Paragraph(L['hobby'], s_mut), Spacer(1,6)])]
    for e in L['ach']: story += entry(*e)
    from reportlab.platypus import NextPageTemplate
    story.insert(1, NextPageTemplate('later'))
    doc.build(story)

HU = dict(
 name1='Lódri', name2='Gergő', role='Szoftverfejlesztő és -tesztelő', doctitle='Önéletrajz',
 s_profile='Profil',
 profile='Szoftverfejlesztő és -tesztelő vagyok, elsősorban backend-fejlesztésben vagyok járatos: Java (WildFly, JaxRS, REST) és PHP alapon, MySQL adatbázissal építettem alkalmazásokat. Erős elkötelezettségem van az agilis működés és a Scrum iránt (PSM I tanúsítvány). Nyitott vagyok új lehetőségekre és szeretem a felelősségteljes, átlátható munkát.',
 s_personal='Személyes adatok',
 personal=[('Születési idő és hely:','2005. 01. 06., Veszprém'),
           ('Nyelvismeret:','Angol középszintű nyelvvizsga (B2) és emelt szintű érettségi'),
           ('Jogosítvány:','B kategóriás')],
 s_exp='Tapasztalat',
 exp=[('Informatika Ágazati Képzőközpont — Oktatás','2025. augusztus – jelen',['Oktatás.']),
      ('HelixLab — Fejlesztés','2025. augusztus – jelen',['Különböző alkalmazások fejlesztése.']),
      ('HelixLab — Gyakorlati hely','2024. január – 2025. június',['Szakmai gyakorlat valós fejlesztési projekteken.'])],
 s_edu='Tanulmányok',
 edu=[('Apáczai Csere János Technikum és Kollégium, Dombóvár','2023 – 2025',['Szoftverfejlesztő és -tesztelő végzettség.']),
      ('Illyés Gyula Gimnázium, Dombóvár','2019 – 2023',['Érettségi — emelt szintű angol és emelt szintű testnevelés.'])],
 s_tech='Tanult nyelvek és technológiák',
 tech=[('Backend és adatbázis',['Java — WildFly szerver','PHP — Laravel keretrendszer','MySQL — MAMP környezetben']),
       ('Frontend és eszközök',['HTML, CSS, JavaScript + Bootstrap 5','Angular keretrendszer','GitHub · Jira · Postman','Scrum és agilis módszertan','Mesterséges intelligencia — automatizálás, agentic coding (Claude)'])],
 s_proj='Projektek',
 proj=[('IAAK Dashboard','PHP',['Az IAAK Dashboard egy olyan felület, amely nagyon hasonlít a KRÉTA-hoz — annak egy továbbgondolt verziója. A Dashboard képes kezelni a diákokkal kapcsolatos információkat (pl. jelenléti mátrix, szabadság, táppénz). Beépített fizetési rendszerrel rendelkezik, és különféle dokumentumok exportálása is lehetséges. PHP nyelven szereztem tapasztalatot ezen a projekten.']),
       ('Visuelse','Java · JaxRS',['Egy építőipari cégnek fejlesztett dashboard-alkalmazás, amelyben az Excel- és PDF-generálást és -exportot fejlesztettem Java nyelven (JaxRS).'])],
 s_cert='Oklevelek',
 cert=[('Professional Scrum Master I (PSM I)','',['Önerőből, angol nyelven szerzett tanúsítvány.']),
       ('Szoftverfejlesztő és -tesztelő','',['Államilag elismert technikusi szakképesítés.']),
       ('Web Design','',['Web design kurzus oklevél.'])],
 s_int='Érdeklődés',
 int=[('Scrum Master','',['Mély affinitás a Scrum Master pozíció iránt.']),
      ('Adatbázis (MySQL)','',['A fejlesztés mellett adatbázisokkal is foglalkoztam.']),
      ('Backend (Java, PHP)','',['Ezekben a backend nyelvekben van tapasztalatom.']),
      ('Mesterséges intelligencia','',['Van tapasztalatom agentic coding területén (Claude) és projekt alapú agentek megtervezésében is.'])],
 s_str='Erősségek',
 strengths='Fejlődni akarás   ·   Rugalmasság   ·   Nyitottság   ·   Alkalmazkodás',
 s_hobby='Hobbi és sportsikerek',
 hobby='Hobbim a labdarúgás — jelenleg egy dombóvári megye I-es csapatban játszom, de játszottam már NB III-ban is. A foci egyensúlyban tartja a fizikai és szellemi állapotomat, és megtanított a csapatban való együttműködésre.',
 ach=[('Tolna Vármegyei I. osztály — bajnokcsapat','2024 – 2025',[]),
      ('Országos Fiú Futsal Bajnokság — I. hely','2015 – 2016',[]),
      ('Youth Football Festival, Kaposvár — I. hely (nemzetközi)','2016',[]),
      ('KOMM MIT Tournament, Barcelona — II. hely (nemzetközi)','2011',[])],
)

EN = dict(
 name1='Gergő', name2='Lódri', role='Software Developer & Tester', doctitle='Curriculum Vitae',
 s_profile='Profile',
 profile='I am a software developer and tester, mainly experienced in backend development: I have built applications on Java (WildFly, JaxRS, REST) and PHP, with a MySQL database. I have a strong commitment to agile ways of working and Scrum (PSM I certification). I am open to new opportunities and I value responsible, transparent work.',
 s_personal='Personal details',
 personal=[('Date and place of birth:','6 January 2005, Veszprém'),
           ('Languages:','English B2 (advanced school-leaving exam); Hungarian — native'),
           ('Driving licence:','Category B')],
 s_exp='Experience',
 exp=[('Informatics Sectoral Training Center — Teaching','Aug 2025 – present',['Teaching.']),
      ('HelixLab — Development','Aug 2025 – present',['Building various applications.']),
      ('HelixLab — Internship','Jan 2024 – June 2025',['Professional internship on real development projects.'])],
 s_edu='Education',
 edu=[('Apáczai Csere János Technical School, Dombóvár','2023 – 2025',['Software developer & tester qualification.']),
      ('Illyés Gyula Grammar School, Dombóvár','2019 – 2023',['School-leaving exam — advanced English and advanced PE.'])],
 s_tech='Technologies',
 tech=[('Backend & database',['Java — with WildFly server','PHP — with Laravel framework','MySQL — in a MAMP environment']),
       ('Frontend & tools',['HTML, CSS, JavaScript + Bootstrap 5','Angular framework','GitHub · Jira · Postman','Scrum and agile methodology','Artificial intelligence — automation, agentic coding (Claude)'])],
 s_proj='Projects',
 proj=[('IAAK Dashboard','PHP',['The IAAK Dashboard is an interface very similar to KRÉTA (the Hungarian school administration system) — a more advanced take on it. The dashboard manages student-related information (e.g. attendance matrix, holidays, sick leave). It has a built-in payment system and can export various documents. I gained PHP experience on this project.']),
       ('Visuelse','Java · JaxRS',['A dashboard application developed for a construction company, in which I built the Excel and PDF generation and export features in Java (JaxRS).'])],
 s_cert='Certificates',
 cert=[('Professional Scrum Master I (PSM I)','',['Certification earned independently, in English.']),
       ('Software Developer & Tester','',['State-accredited technician qualification.']),
       ('Web Design','',['Web design course certificate.'])],
 s_int='Interests',
 int=[('Scrum Master','',['Strong affinity for the Scrum Master role.']),
      ('Databases (MySQL)','',['Beyond development, I have also worked with databases.']),
      ('Backend (Java, PHP)','',['I have hands-on experience with these backend languages.']),
      ('Artificial Intelligence','',['I have experience with agentic coding (Claude) and with designing project-based agents.'])],
 s_str='Strengths',
 strengths='Eagerness to grow   ·   Flexibility   ·   Openness   ·   Adaptability',
 s_hobby='Hobby & sports achievements',
 hobby='My hobby is football — I currently play in a county first-division team in Dombóvár, and I have also played in the NB III. Football keeps my body and mind in balance and taught me how to cooperate in a team.',
 ach=[('Tolna County Division I — champion team','2024 – 2025',[]),
      ('National Boys Futsal Championship — 1st place','2015 – 2016',[]),
      ('Youth Football Festival, Kaposvár — 1st place (international)','2016',[]),
      ('KOMM MIT Tournament, Barcelona — 2nd place (international)','2011',[])],
)

build(os.path.join(OUT, 'Lodri_Gergo_oneletrajz.pdf'), HU)
build(os.path.join(OUT, 'Lodri_Gergo_CV_EN.pdf'), EN)
print('Kész: assets/Lodri_Gergo_oneletrajz.pdf és assets/Lodri_Gergo_CV_EN.pdf')
