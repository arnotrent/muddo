import json, random, string
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.core.models import ContactRequest, NewsletterSubscriber
from apps.products.models import Product
from apps.distributors.models import Distributor


def _send(subject, to, body):
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to, fail_silently=True)
        return True
    except Exception:
        return False

def _ref():
    return 'ENQ-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def index(request):
    stats = {k: Product.objects.filter(category=v).count()
             for k, v in [('pesticides','pesticide'),('herbicides','herbicide'),('fungicides','fungicide'),('other','other')]}
    stats['distributors'] = Distributor.objects.count()
    all_p = list(Product.objects.all())
    featured = random.sample(all_p, min(6, len(all_p)))
    why_cards = [
        ('shield-alt','#c43010','#fce8e2','100% Authentic','All products MAAIF-registered, sourced directly from certified manufacturers. Zero counterfeits, ever.'),
        ('users','#1a6abf','#e0eeff','Farmer First',"Our pricing and advice are designed around Uganda's farmers — retail and wholesale, no minimum."),
        ('flask','#e8651a','#fef2e8','Quality Assured','Every product meets MAAIF registration and international quality standards before we stock it.'),
        ('map-marked-alt','#d4902a','#fef5e0','Nationwide Reach','11 authorised outlets across Central, Eastern, Northern and Western Uganda.'),
        ('headset','#c43010','#fce8e2','Expert Support','Our trained team provides dosage guidance, application timing and crop-specific advice.'),
        ('handshake','#1a6abf','#e0eeff','Long-term Partners','We build relationships with farmers and distributors, not just transactions — season after season.'),
    ]
    categories = [
        ('bug','#c43010','#fce8e2','Pesticides','pesticides','pesticides','/static/images/product_acelemectin.png'),
        ('seedling','#2d6e35','#e8f5e9','Herbicides','herbicides','herbicides','/static/images/product_maizeplus.png'),
        ('microscope','#5e35b1','#ede0ff','Fungicides','fungicides','fungicides','/static/images/product_toplaxym.png'),
        ('boxes','#a06810','#fef5e0','Fertilizers & Equipment','other_products','other','/static/images/products_all.png'),
    ]
    return render(request, 'index.html', {'stats':stats, 'featured':featured, 'why_cards':why_cards, 'categories':categories})

def about(request):
    stats_list = [('2020','Year Founded'),(f'{Product.objects.count()}+','Product Lines'),
                  (f'{Distributor.objects.count()}+','Distributor Outlets'),('4','Regions Covered')]
    faqs = [
        ('Are your products MAAIF-registered?',
         'Yes. All products distributed by Muddo Agro Chemicals LTD are registered with Uganda\'s Ministry of Agriculture, Animal Industry and Fisheries (MAAIF). Certificates available on request.'),
        ('Do you sell wholesale?',
         'Absolutely. We supply retail and wholesale quantities. Contact us at +256 772 507582 for bulk pricing and distributor partnerships.'),
        ('How do I choose the right product?',
         'Call us or visit our Kampala office. Describe your crop and the pest, weed, or disease you are seeing — our team will recommend the right product, dosage and timing.'),
        ('Are your products environmentally safe?',
         'All registered products include environmental safety assessments. Always follow label instructions: observe buffer zones, pre-harvest intervals, and use proper PPE.'),
        ('Do you deliver upcountry?',
         'Products are available through our 11-outlet nationwide network. Use our Store Locator to find the nearest outlet. For large bulk orders direct delivery can be arranged.'),
        ('What is the minimum order?',
         'No minimum for retail. For wholesale pricing, minimums vary by product — contact our sales team for a quote.'),
        ('How do I report a product problem?',
         'Call +256 772 507582 or email kulanju_w@yahoo.com immediately. Keep the product, note the batch number, and describe the issue. We investigate all complaints promptly.'),
        ('What is your return policy?',
         'Sealed, unused products in original packaging may be returned within 7 days with proof of purchase. Contact us before returning any item.'),
    ]
    product_samples = [
        ('Muddosate','Herbicide','#2d6e35','#e8f5e9'),('MD Maize Plus','Herbicide','#2d6e35','#e8f5e9'),
        ('MAX 2.4-D','Herbicide','#2d6e35','#e8f5e9'),('MD Ametryn','Herbicide','#2d6e35','#e8f5e9'),
        ('Weed IT 75.7 XL','Herbicide','#2d6e35','#e8f5e9'),('MD Acelemectin','Pesticide','#c43010','#fce8e2'),
        ('MD FOS','Pesticide','#c43010','#fce8e2'),('Top Fenos','Pesticide','#c43010','#fce8e2'),
        ('MD Thion','Pesticide','#c43010','#fce8e2'),('MD Thoate','Pesticide','#c43010','#fce8e2'),
        ('Top-Laxly M','Fungicide','#5e35b1','#ede0ff'),('MD Top Laxlyn','Fungicide','#5e35b1','#ede0ff'),
        ('Toplaxly','Fungicide','#5e35b1','#ede0ff'),('Copper Oxychloride','Fungicide','#5e35b1','#ede0ff'),
        ('Urea 46%N','Fertilizer','#a06810','#fef5e0'),('NPK 17:17:17','Fertilizer','#a06810','#fef5e0'),
        ('Foliar Boost','Fertilizer','#a06810','#fef5e0'),('Knapsack Sprayer','Equipment','#1a6abf','#e0eeff'),
    ]
    return render(request, 'about.html', {'stats_list':stats_list, 'faqs':faqs, 'product_samples':product_samples})

def contact(request):
    if request.method == 'POST':
        ref = _ref()
        cr = ContactRequest.objects.create(
            ref_number=ref,
            name=request.POST.get('name','').strip(),
            email=request.POST.get('email','').strip(),
            phone=request.POST.get('phone','').strip(),
            subject=request.POST.get('subject','').strip(),
            message=request.POST.get('message','').strip(),
        )
        _send(f'Muddo Agro — Enquiry Received [{ref}]', [cr.email],
              f"Dear {cr.name},\n\nThank you for contacting Muddo Agro Chemicals LTD.\n"
              f"Your reference number is: {ref}\n\nWe'll respond within 1 business day.\n\n"
              f"Muddo Agro Team\n+256 772 507582")
        _send(f'New Enquiry [{ref}] — {cr.subject}', [settings.COMPANY_EMAIL],
              f"From: {cr.name} <{cr.email}>\nPhone: {cr.phone}\nSubject: {cr.subject}\n\n{cr.message}")
        messages.success(request, f'Message sent! Your reference number is <strong>{ref}</strong>. Use it to track your enquiry.')
        return redirect('contact')
    return render(request, 'contact.html')

def track(request):
    ref = request.GET.get('ref','').strip().upper()
    result, rows = None, []
    if ref:
        try:
            result = ContactRequest.objects.get(ref_number=ref)
            rows = [('Name',result.name),('Email',result.email),('Phone',result.phone or '—'),
                    ('Subject',result.subject),('Status',result.status.title()),
                    ('Date',result.created_at.strftime('%d %b %Y %H:%M')),('Message',result.message)]
        except ContactRequest.DoesNotExist:
            pass
    return render(request, 'track.html', {'ref':ref, 'result':result, 'enquiry_rows':rows})

def search(request):
    q = request.GET.get('q','').strip()
    results = {'products':[], 'distributors':[]}
    if q and len(q) >= 2:
        results['products'] = list((Product.objects.filter(name__icontains=q) |
                                     Product.objects.filter(active_ingredient__icontains=q) |
                                     Product.objects.filter(crops__icontains=q) |
                                     Product.objects.filter(description__icontains=q)).distinct()[:20])
        results['distributors'] = list((Distributor.objects.filter(name__icontains=q) |
                                         Distributor.objects.filter(district__icontains=q) |
                                         Distributor.objects.filter(region__icontains=q)).distinct()[:10])
    return render(request, 'search.html', {'q':q, 'results':results})

def api_search(request):
    q = request.GET.get('q','').strip()
    if len(q) < 2: return JsonResponse([], safe=False)
    products = (Product.objects.filter(name__icontains=q) | Product.objects.filter(active_ingredient__icontains=q))[:8]
    return JsonResponse([{'id':p.id,'name':p.name,'category':p.category,'image':p.display_image} for p in products], safe=False)

def compare(request):
    products_list = [{'id':p.id,'name':p.name,'category':p.category,'description':p.description or '',
                      'active_ingredient':p.active_ingredient or '','formulation':p.formulation or '',
                      'crops':p.crops or '','dosage':p.dosage or '','packing':p.packing or '',
                      'image_url':p.display_image,'stock_qty':p.stock_qty}
                     for p in Product.objects.all()]
    return render(request, 'compare.html', {'all_products':products_list, 'all_products_json':json.dumps(products_list)})

def subscribe(request):
    if request.method != 'POST': return JsonResponse({'ok':False}, status=405)
    try: data = json.loads(request.body)
    except Exception: data = {}
    email = (data.get('email') or '').strip().lower()
    name  = (data.get('name')  or '').strip()
    if not email or '@' not in email: return JsonResponse({'ok':False,'message':'Invalid email.'}, status=400)
    obj, created = NewsletterSubscriber.objects.get_or_create(email=email, defaults={'name':name,'active':True})
    if not created and obj.active: return JsonResponse({'ok':True,'message':"You're already subscribed!"})
    if not created: obj.active=True; obj.save()
    return JsonResponse({'ok':True,'message':"Subscribed! You'll receive our latest updates."})

def sitemap(request):
    base = request.build_absolute_uri('/').rstrip('/')
    urls = [('/',1.0,'weekly'),('/pesticides/',0.9,'weekly'),('/herbicides/',0.9,'weekly'),
            ('/fungicides/',0.9,'weekly'),('/other-products/',0.9,'weekly'),
            ('/distributors/',0.8,'monthly'),('/contact/',0.7,'monthly'),('/about/',0.6,'monthly')]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, freq in urls:
        xml.append(f'  <url><loc>{base}{path}</loc><priority>{pri}</priority><changefreq>{freq}</changefreq></url>')
    for p in Product.objects.values('id'):
        xml.append(f'  <url><loc>{base}/product/{p["id"]}/</loc><priority>0.8</priority><changefreq>monthly</changefreq></url>')
    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type='application/xml')

def robots(request):
    base = request.build_absolute_uri('/')
    return HttpResponse('\n'.join(['User-agent: *','Allow: /','Disallow: /admin-panel/','Disallow: /agent/',
                                    'Disallow: /login/','Disallow: /api/','Disallow: /django-admin/',
                                    f'Sitemap: {base}sitemap.xml']), content_type='text/plain')

def error_404(request, exception=None):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '404.html', status=500)
