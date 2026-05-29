from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import FileResponse
import io

from apps.agents.models import Agent
from apps.products.models import Product
from apps.requests_app.models import SupplyRequest
from apps.messaging.models import Message


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_staff else 'agent_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        role     = request.POST.get('role','agent')
        user = authenticate(request, username=username, password=password)
        if user:
            if role == 'admin' and user.is_staff:
                login(request, user); return redirect('admin_dashboard')
            elif role == 'agent' and not user.is_staff:
                try:
                    a = user.agent_profile
                    if a.status != 'active':
                        messages.error(request,'Your account is deactivated.'); return render(request,'auth/login.html')
                    a.last_seen = timezone.now(); a.save(update_fields=['last_seen'])
                except Agent.DoesNotExist: pass
                login(request, user); return redirect('agent_dashboard')
            else:
                messages.error(request,'Wrong role selected for this account.')
        else:
            messages.error(request,'Invalid username or password.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request); return redirect('login')

@login_required
def agent_dashboard(request):
    if request.user.is_staff: return redirect('admin_dashboard')
    try: agent = request.user.agent_profile
    except Agent.DoesNotExist:
        messages.error(request,'Agent profile not found.'); return redirect('login')
    agent.last_seen = timezone.now(); agent.save(update_fields=['last_seen'])
    my_requests = SupplyRequest.objects.filter(agent=agent).order_by('-created_at')[:10]
    unread      = Message.objects.filter(receiver_id=agent.id, receiver_role='agent', read=False).count()
    last_msg    = Message.objects.filter(sender_role='admin', receiver_id=agent.id, receiver_role='agent').order_by('-id').first()
    return render(request, 'agent/dashboard.html', {
        'agent':agent,'my_requests':my_requests,'unread':unread,
        'last_msg':last_msg,'total_products':Product.objects.count()})

@login_required
def agent_chat(request):
    if request.user.is_staff: return redirect('admin_chat')
    agent  = get_object_or_404(Agent, user=request.user)
    admin_u = User.objects.filter(is_staff=True).first()
    return render(request, 'agent/chat.html', {'agent':agent,'admin_id':admin_u.id if admin_u else 1})

@staff_member_required
def admin_agents(request):
    agents = Agent.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin/agents.html', {'agents':agents})

@staff_member_required
def admin_add_agent(request):
    if request.method != 'POST': return redirect('admin_agents')
    username = request.POST.get('username','').strip()
    name     = request.POST.get('name','').strip()
    email    = request.POST.get('email','').strip()
    phone    = request.POST.get('phone','').strip()
    region   = request.POST.get('region','').strip()
    district = request.POST.get('district','').strip()
    password = request.POST.get('password','')
    if User.objects.filter(username=username).exists():
        messages.error(request,'Username already taken.'); return redirect('admin_agents')
    first,*rest = name.split(' ',1)
    u = User.objects.create_user(username=username,email=email,password=password,
                                  first_name=first,last_name=' '.join(rest) if rest else '')
    Agent.objects.create(user=u,phone=phone,region=region,district=district)
    messages.success(request,f'Agent {name} added!')
    return redirect('admin_agents')

@staff_member_required
def admin_delete_agent(request, aid):
    if request.method == 'POST':
        a = get_object_or_404(Agent, pk=aid); a.user.delete()
        messages.success(request,'Agent removed.')
    return redirect('admin_agents')

@staff_member_required
def admin_toggle_agent(request, aid):
    if request.method == 'POST':
        a = get_object_or_404(Agent, pk=aid)
        a.status = 'inactive' if a.status == 'active' else 'active'
        a.save(update_fields=['status'])
        messages.success(request,f'Agent set to {a.status}.')
    return redirect('admin_agents')

@staff_member_required
def agent_report_pdf(request, aid):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_RIGHT
    from datetime import datetime

    agent = get_object_or_404(Agent, pk=aid)
    reqs  = SupplyRequest.objects.filter(agent=agent).order_by('-created_at')
    buf   = io.BytesIO()
    doc   = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)

    DARK=colors.HexColor('#0d2b14'); MID=colors.HexColor('#2d6e35'); GOLD=colors.HexColor('#c8a84b')
    LGRY=colors.HexColor('#f5f5f5'); LGRN=colors.HexColor('#e8f5e9'); WHT=colors.white; MUTED=colors.HexColor('#565656')

    h1 = ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=20,textColor=WHT)
    h2 = ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=12,textColor=DARK)
    bd = ParagraphStyle('bd',fontName='Helvetica-Bold',fontSize=10,textColor=colors.HexColor('#111'))
    sm = ParagraphStyle('sm',fontName='Helvetica',fontSize=8.5,textColor=MUTED)
    lb = ParagraphStyle('lb',fontName='Helvetica-Bold',fontSize=9.5,textColor=MUTED)

    story = []
    hdr = Table([[Paragraph('<b>AGENT REPORT</b>',h1),
                  Paragraph(f'<b>{agent.name}</b><br/><font size="10">{agent.region or "—"} Region</font>',
                            ParagraphStyle('r',fontName='Helvetica-Bold',fontSize=14,textColor=GOLD,alignment=TA_RIGHT))]],colWidths=[100*mm,74*mm])
    hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK),('PADDING',(0,0),(-1,-1),14),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(hdr)
    band = Table([[Paragraph(f'MUDDO AGRO CHEMICALS LTD · Report: {datetime.now().strftime("%d %B %Y")}',sm)]],colWidths=[174*mm])
    band.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRN),('PADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),1.5,MID)]))
    story += [band,Spacer(1,8*mm)]

    profile = [('Full Name',agent.name),('Username',agent.username),('Email',agent.email or '—'),
               ('Phone',agent.phone or '—'),('Region',agent.region or '—'),('District',agent.district or '—'),
               ('Status',agent.status.title()),
               ('Joined',agent.created_at.strftime('%Y-%m-%d') if agent.created_at else '—'),
               ('Last Active',agent.last_seen.strftime('%Y-%m-%d %H:%M') if agent.last_seen else 'Never')]
    pr = [[Paragraph(k,lb),Paragraph(v,bd)] for k,v in profile]
    pt = Table(pr,colWidths=[55*mm,119*mm])
    pt.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[WHT,LGRY]),('TOPPADDING',(0,0),(-1,-1),8),
                            ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),10),
                            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#e0e0e0')),('LINEBELOW',(0,-1),(-1,-1),1.5,MID)]))
    story += [Paragraph('<b>AGENT PROFILE</b>',h2),Spacer(1,3*mm),pt,Spacer(1,8*mm)]

    if reqs.exists():
        sr_rows = [['#','Product','Qty','Status','Date']]
        for i,r in enumerate(reqs):
            sr_rows.append([str(i+1),r.product_name,r.quantity,r.status.title(),r.created_at.strftime('%Y-%m-%d')])
        srt = Table(sr_rows,colWidths=[10*mm,75*mm,35*mm,30*mm,24*mm])
        srt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),WHT),
                                  ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
                                  ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHT,LGRY]),
                                  ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                                  ('LEFTPADDING',(0,0),(-1,-1),8),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#e0e0e0'))]))
        story += [Paragraph('<b>SUPPLY REQUEST HISTORY</b>',h2),Spacer(1,3*mm),srt]

    doc.build(story); buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'MACL_Agent_{agent.name.replace(" ","_")}.pdf', content_type='application/pdf')
