import io
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from apps.products.models import Product

CAT_TABS = [('Pesticides','pesticides','bug'),('Herbicides','herbicides','seedling'),
            ('Fungicides','fungicides','microscope'),('Fertilizers & Equipment','other_products','boxes')]

CAT_META = {
    'pesticide': {'template':'products/pesticides.html','page_title':'Pesticides','page_tag':'Insect & Pest Control',
                  'page_desc':'Professional-grade insecticides for control of all major crop pests across Uganda.','hero_icon':'bug','hero_color':'#7a1010','hero_color_dark':'#300505'},
    'herbicide': {'template':'products/herbicides.html','page_title':'Herbicides','page_tag':'Weed Control',
                  'page_desc':'Selective and non-selective herbicides for effective weed management in all crops.','hero_icon':'seedling','hero_color':'#1a5a20','hero_color_dark':'#0a2010'},
    'fungicide': {'template':'products/fungicides.html','page_title':'Fungicides','page_tag':'Disease Control',
                  'page_desc':'Systemic and contact fungicides for prevention and control of fungal diseases.','hero_icon':'microscope','hero_color':'#2d1a6b','hero_color_dark':'#100a2a'},
    'other':     {'template':'products/other_products.html','page_title':'Fertilizers & Equipment','page_tag':'Agri Inputs',
                  'page_desc':'Fertilizers, foliar feeds and spraying equipment to maximise your crop yields.','hero_icon':'boxes','hero_color':'#7a4a10','hero_color_dark':'#3a1e05'},
}

def _product_list(request, category):
    meta = CAT_META[category]
    products = Product.objects.filter(category=category).select_related('inventory')
    return render(request, meta['template'], {'products':products, 'cat_tabs':CAT_TABS, **meta})

def pesticides(request):    return _product_list(request, 'pesticide')
def herbicides(request):    return _product_list(request, 'herbicide')
def fungicides(request):    return _product_list(request, 'fungicide')
def other_products(request):return _product_list(request, 'other')

def product_detail(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    related = Product.objects.filter(category=p.category).exclude(pk=p.pk).order_by('?')[:3]
    specs = [('Active Ingredient',p.active_ingredient),('Formulation',p.formulation),
             ('Target Crops',p.crops),('Application Rate',p.dosage),
             ('Pack Sizes',p.packing),('Category',p.get_category_display()),
             ('Stock',('In Stock' if p.stock_qty>10 else ('Low Stock' if p.stock_qty>0 else 'Out of Stock')))]
    return render(request, 'products/product_detail.html', {'product':p,'related':related,'specs':specs})

def product_spec_sheet(request, product_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_RIGHT
    from datetime import datetime

    p = get_object_or_404(Product, pk=product_id)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)

    DARK  = colors.HexColor('#0d2b14'); MID  = colors.HexColor('#2d6e35')
    GOLD  = colors.HexColor('#c8a84b'); LGRN = colors.HexColor('#e8f5e9')
    LGRY  = colors.HexColor('#f5f5f5'); BLK  = colors.HexColor('#111')
    MUTED = colors.HexColor('#565656'); WHT  = colors.white

    CAT_C = {'pesticide':colors.HexColor('#c43010'),'herbicide':MID,'fungicide':colors.HexColor('#5e35b1'),'other':colors.HexColor('#f57c00')}
    cat_c = CAT_C.get(p.category, MID)

    h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20, textColor=WHT)
    h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, textColor=DARK)
    bd = ParagraphStyle('bd', fontName='Helvetica', fontSize=10, textColor=BLK, leading=15)
    sm = ParagraphStyle('sm', fontName='Helvetica', fontSize=8.5, textColor=MUTED)
    lbl= ParagraphStyle('lb', fontName='Helvetica-Bold', fontSize=9.5, textColor=MUTED)

    story = []
    hdr = Table([[Paragraph(f'<b>{p.name}</b>', h1),
                  Paragraph(f'<b>{p.get_category_display()}</b><br/><font size="9">TECHNICAL DATA SHEET</font>',
                            ParagraphStyle('r',fontName='Helvetica-Bold',fontSize=13,textColor=cat_c,alignment=TA_RIGHT))]],
                colWidths=[120*mm, 54*mm])
    hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK),('PADDING',(0,0),(-1,-1),14),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(hdr)

    band = Table([[Paragraph('MUDDO AGRO CHEMICALS LTD · Kampala, Uganda · +256 772 507582 · muddoagro811@gmail.com', sm)]],colWidths=[174*mm])
    band.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LGRN),('PADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),1.5,MID)]))
    story += [band, Spacer(1,8*mm)]

    if p.description:
        story += [Paragraph('<b>PRODUCT DESCRIPTION</b>',h2),Spacer(1,3*mm),Paragraph(p.description,bd),Spacer(1,7*mm)]

    specs = [('Active Ingredient',p.active_ingredient or '—'),('Formulation',p.formulation or '—'),
             ('Target Crops',p.crops or '—'),('Application Rate',p.dosage or '—'),('Pack Sizes',p.packing or '—'),
             ('Category',p.get_category_display())]
    rows = [[Paragraph(k,lbl),Paragraph(v,ParagraphStyle('bv',fontName='Helvetica-Bold',fontSize=10,textColor=BLK))] for k,v in specs]
    t = Table(rows, colWidths=[55*mm,119*mm])
    t.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[WHT,LGRY]),('TOPPADDING',(0,0),(-1,-1),9),
                           ('BOTTOMPADDING',(0,0),(-1,-1),9),('LEFTPADDING',(0,0),(-1,-1),10),
                           ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#e0e0e0')),
                           ('LINEBELOW',(0,-1),(-1,-1),1.5,MID)]))
    story += [Paragraph('<b>TECHNICAL SPECIFICATIONS</b>',h2),Spacer(1,3*mm),t,Spacer(1,8*mm)]

    safety = [['01','Read the complete product label before use.'],
              ['02','Wear appropriate PPE: gloves, goggles, face mask and protective clothing.'],
              ['03','Mix in clean water using a calibrated sprayer. Never exceed recommended rate.'],
              ['04','Observe the pre-harvest interval (PHI) stated on the label.'],
              ['05','Store in sealed original container in a cool, dry place away from children.'],
              ['06','Triple-rinse and puncture empty containers. Never burn or reuse.']]
    st = Table(safety, colWidths=[12*mm,162*mm])
    st.setStyle(TableStyle([('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('TEXTCOLOR',(0,0),(0,-1),MID),
                            ('FONTSIZE',(0,0),(-1,-1),9.5),('TOPPADDING',(0,0),(-1,-1),7),
                            ('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),8),
                            ('LINEBELOW',(0,0),(-1,-1),0.3,colors.HexColor('#e0e0e0'))]))
    story += [Paragraph('<b>SAFE USE DIRECTIONS</b>',h2),Spacer(1,3*mm),st,Spacer(1,8*mm)]

    ft = Table([[Paragraph('Informational only. Always refer to the registered product label.',sm),
                 Paragraph(f'Generated: {datetime.now().strftime("%d %b %Y")}',
                           ParagraphStyle('fd',fontName='Helvetica',fontSize=8.5,textColor=MUTED,alignment=TA_RIGHT))]],
               colWidths=[120*mm,54*mm])
    ft.setStyle(TableStyle([('LINEABOVE',(0,0),(-1,0),0.5,colors.HexColor('#e0e0e0')),('TOPPADDING',(0,0),(-1,0),8)]))
    story.append(ft)

    doc.build(story); buf.seek(0)
    return FileResponse(buf, as_attachment=True,
                        filename=f'MACL_{p.name.replace(" ","_")}_DataSheet.pdf',
                        content_type='application/pdf')
