from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.products.models import Product
from apps.inventory.models import Inventory
from apps.distributors.models import Distributor
from apps.agents.models import Agent

IMG = {
    'muddosate':   '/static/images/product_muddosate.png',
    'maizeplus':   '/static/images/product_maizeplus.png',
    'max24d':      '/static/images/product_max24d_selective.png',
    'acelemectin': '/static/images/product_acelemectin.png',
    'mdfos':       '/static/images/product_mdfos.png',
    'toplaxym':    '/static/images/product_toplaxym.png',
    'toplaxlyn':   '/static/images/product_toplaxlyn.png',
    'store':       '/static/images/product_store.png',
    'all':         '/static/images/products_all.png',
}

PRODUCTS = [
    # ── HERBICIDES ─────────────────────────────────────────────────────────
    dict(name='MUDDOSATE 480SL', category='herbicide', img='muddosate', stock=120, reorder=20,
         active_ingredient='Glyphosate 480 g/l', formulation='Soluble Liquid (SL)',
         crops='All crops (pre-plant/directed), Plantations, Couch grass, Kikuyu grass, Non-crop areas',
         dosage='3–6 L/ha in 200–400 L water. Annual grasses: 3–4 L/ha. Couch/perennial: 5–6 L/ha.',
         packing='100ml, 500ml, 1L, 5L, 20L',
         description='MUDDOSATE is MACL\'s flagship non-selective systemic herbicide for total control of annual and perennial weeds. Absorbed through leaves and translocated throughout the plant including roots. Available wholesale and retail across Uganda.'),
    dict(name='MD MAIZE PLUS 40OD', category='herbicide', img='maizeplus', stock=95, reorder=15,
         active_ingredient='Nicosulfuron 40 g/l', formulation='Oil Dispersion (OD)',
         crops='Maize (selective — safe on the crop at label rates)',
         dosage='0.5–0.75 L/ha at 2–6 leaf stage of weeds. Maximum 1 L/ha.',
         packing='100ml, 250ml, 500ml, 1L, 5L',
         description='MD MAIZE PLUS is a selective post-emergence herbicide for control of grass and broad-leaved weeds in maize. It is highly effective — once used you will not regret it. Available in all package sizes for wholesale and small quantities.'),
    dict(name='MAX 2.4-D 720SL', category='herbicide', img='max24d', stock=140, reorder=25,
         active_ingredient='2,4-D Dimethylamine salt 720 g/l', formulation='Soluble Liquid (SL)',
         crops='Maize, Wheat, Sorghum, Sugarcane, Rice, Pastures, Plantation crops',
         dosage='1.0–2.0 L/ha in 200–400 L water. Apply at 4–6 leaf stage of weeds.',
         packing='100ml, 250ml, 500ml, 1L, 5L, 20L',
         description='MAX 2.4-D is a selective systemic herbicide for control of broad-leaved weeds in cereal crops. Available in all packages at MACL. Proven performance on maize, sorghum and wheat farms across all four regions of Uganda.'),
    dict(name='MD AMETRYN 500SC', category='herbicide', img='all', stock=60, reorder=10,
         active_ingredient='Ametryn 500 g/l', formulation='Suspension Concentrate (SC)',
         crops='Sugarcane, Pineapple, Maize, Banana plantations',
         dosage='4–6 L/ha in 400–600 L water. Apply to moist soil pre- or early post-emergence.',
         packing='500ml, 1L, 5L',
         description='MD AMETRYN is an MACL-distributed selective pre- and early post-emergence herbicide as listed on the official company letterhead. Trusted by sugarcane and pineapple growers across Uganda.'),
    dict(name='WEED IT 75.7 XL', category='herbicide', img='all', stock=75, reorder=15,
         active_ingredient='Glyphosate 75.7% w/w', formulation='Water Soluble Granule (SG)',
         crops='Non-selective — pre-plant or directed spray in all crops, roadsides, plantations',
         dosage='1.5–2.5 kg/ha in 200–300 L water.',
         packing='200g, 500g, 1kg',
         description='WEED IT 75.7 XL is an MACL-distributed product listed on the official company letterhead. Concentrated water-soluble granule formulation of glyphosate for cost-effective, complete vegetation control.'),
    # ── PESTICIDES ─────────────────────────────────────────────────────────
    dict(name='MD ACELEMECTIN 48EC', category='pesticide', img='acelemectin', stock=88, reorder=15,
         active_ingredient='Abamectin 18 g/l + Acetamiprid 30 g/l', formulation='Emulsifiable Concentrate (EC)',
         crops='Cotton, Vegetables, Watermelon, Passion Fruit, Tomatoes, Coffee, Beans',
         dosage='500 ml–1 L/ha in 200 L water. Begin at first sign of infestation.',
         packing='100ml, 250ml, 500ml, 1L',
         description='MD ACELEMECTIN 48EC is a broad-spectrum insecticide used to control all sucking and biting insect pests. Available at MACL wholesale and retail. Outstanding performance on mites, aphids, whitefly, bollworm on watermelon, passion fruit and tomatoes.'),
    dict(name='MD FOS 48EC', category='pesticide', img='mdfos', stock=105, reorder=20,
         active_ingredient='Chlorpyrifos 480 g/l', formulation='Emulsifiable Concentrate (EC)',
         crops='Maize, Vegetables, Fruits, Beans, Coffee, Cotton, Tobacco, Groundnuts',
         dosage='1–2 L/ha foliar; 3–4 L/ha soil drench in 200–400 L water.',
         packing='100ml, 250ml, 500ml, 1L, 5L',
         description='M-D FOS 48EC is a broad-spectrum organophosphate insecticide with contact and stomach action. Effective against stem borers, army worms, aphids and soil-dwelling larvae. Available at MACL wholesale and small quantities.'),
    dict(name='TOP FENOS 50EC', category='pesticide', img='all', stock=55, reorder=10,
         active_ingredient='Fenvalerate 50 g/l', formulation='Emulsifiable Concentrate (EC)',
         crops='Cotton, Maize, Vegetables, Sorghum, Sunflower, Tobacco',
         dosage='500 ml–1 L/ha in 200–300 L water. Repeat after 10–14 days if needed.',
         packing='100ml, 500ml, 1L',
         description='TOP FENOS 50EC is an MACL-distributed pyrethroid insecticide as listed on the official company letterhead. Fast knockdown action with long residual effect on major crop pests across Uganda.'),
    dict(name='MD THION 350EC', category='pesticide', img='all', stock=70, reorder=12,
         active_ingredient='Dimethoate 350 g/l', formulation='Emulsifiable Concentrate (EC)',
         crops='Vegetables, Coffee, Tea, Citrus, Tobacco, Beans, Groundnuts',
         dosage='500 ml–1 L/ha in 200–400 L water.',
         packing='100ml, 250ml, 500ml, 1L',
         description='MD THION is an MACL-listed organophosphate insecticide providing reliable systemic and contact control of thrips, mites, aphids and caterpillars in key Ugandan crops.'),
    dict(name='MD THOATE 40EC', category='pesticide', img='all', stock=62, reorder=10,
         active_ingredient='Dimethoate 400 g/l', formulation='Emulsifiable Concentrate (EC)',
         crops='Coffee, Vegetables, Cotton, Cereals, Tobacco, Tea',
         dosage='500 ml/ha in 200–400 L water. Apply at first sign of pest pressure.',
         packing='100ml, 500ml, 1L, 5L',
         description='MD THOATE 40EC is distributed by Muddo Agro Chemicals LTD as listed on the official company letterhead. Systemic insecticide and acaricide with contact and stomach action for a wide range of pests.'),
    # ── FUNGICIDES ─────────────────────────────────────────────────────────
    dict(name='TOP-LAXLY M 72WP', category='fungicide', img='toplaxym', stock=115, reorder=20,
         active_ingredient='Metalaxyl-M 4% + Mancozeb 64%', formulation='Wettable Powder (WP)',
         crops='Onions, Tomatoes, French Beans, Watermelon, Potatoes, Peppers, Carrots',
         dosage='2.0–2.5 kg/ha in 400–600 L water. Apply every 7–14 days.',
         packing='100g, 250g, 500g, 1kg',
         description='TOP-LAXLY M is a systemic fungicide for control of downy mildew, black spots and blight. Available in 3 package sizes. Very effective on VEGETABLES once applied. A top MACL product backed by excellent farmer results across Uganda.'),
    dict(name='MD TOP LAXLYN 72WP', category='fungicide', img='toplaxlyn', stock=90, reorder=15,
         active_ingredient='Metalaxyl 8% + Mancozeb 64%', formulation='Wettable Powder (WP)',
         crops='Vegetables, Potatoes, Grapes, Groundnuts, Tobacco',
         dosage='2.5 kg/ha in 500 L water. Apply 10–14 days before expected disease pressure.',
         packing='250g, 500g, 1kg',
         description='MD TOP LAXLYN 72WP is a systemic and contact fungicide for control of downy mildew, Alternaria blight and mixed fungal diseases. MACL-distributed with proven performance across Uganda\'s vegetable farms.'),
    dict(name='TOPLAXLY 72WP', category='fungicide', img='all', stock=80, reorder=15,
         active_ingredient='Cymoxanil 8% + Mancozeb 64%', formulation='Wettable Powder (WP)',
         crops='Potatoes, Tomatoes, Cucurbits, Tobacco',
         dosage='2.0–2.5 kg/ha. Preventative: every 7–10 days.',
         packing='100g, 250g, 500g, 1kg',
         description='TOPLAXLY (as listed on the MACL company letterhead) is a protective and curative fungicide against late blight, downy mildew and related diseases. Available across the MACL nationwide distributor network.'),
    dict(name='COPPER OXYCHLORIDE 850WP', category='fungicide', img='all', stock=78, reorder=12,
         active_ingredient='Copper Oxychloride 850 g/kg', formulation='Wettable Powder (WP)',
         crops='Coffee, Banana, Vegetables, Citrus, Stone Fruits, Potatoes',
         dosage='2–3 kg/ha in 400–600 L water. Apply at 10–14 day intervals.',
         packing='100g, 500g, 1kg, 5kg',
         description='A trusted multi-site protective fungicide and bactericide for a wide range of fungal and bacterial diseases. Long-established MACL product used by coffee and vegetable farmers across all regions of Uganda.'),
    # ── FERTILIZERS & EQUIPMENT ────────────────────────────────────────────
    dict(name='UREA 46%N', category='other', img='all', stock=200, reorder=40,
         active_ingredient='Nitrogen (N) 46%', formulation='Prilled Granular',
         crops='Maize, Rice, Vegetables, Coffee, Sugarcane, Wheat, all field crops',
         dosage='50–200 kg/ha. Top-dress in split applications. Do not apply to wet foliage.',
         packing='1 kg, 5 kg, 25 kg, 50 kg bags',
         description='High-analysis nitrogen fertilizer for rapid vegetative growth. Urea is the most concentrated solid nitrogen source, widely used by Uganda\'s farmers for maize, vegetables and cash crops. Available at MACL wholesale and retail.'),
    dict(name='NPK 17:17:17', category='other', img='all', stock=180, reorder=30,
         active_ingredient='N 17% + P₂O₅ 17% + K₂O 17%', formulation='Compound Granular',
         crops='All crops — maize, vegetables, coffee, tea, sugarcane, horticulture',
         dosage='200–400 kg/ha basal application at or before planting.',
         packing='1 kg, 5 kg, 25 kg, 50 kg bags',
         description='Balanced compound fertilizer supplying equal nitrogen, phosphorus and potassium. Ideal for basal application at planting. Promotes strong root development and overall plant vigour. Available at MACL for retail and wholesale.'),
    dict(name='FOLIAR BOOST 20-20-20+TE', category='other', img='all', stock=95, reorder=15,
         active_ingredient='N 20% + P₂O₅ 20% + K₂O 20% + Zn, Fe, Mn, B, Cu', formulation='Water Soluble Powder',
         crops='Vegetables, Flowers, Fruits, Coffee, Tea, Greenhouse crops',
         dosage='3–5 g/L foliar spray; 2–5 kg/ha through drip irrigation.',
         packing='250g, 500g, 1 kg, 5 kg',
         description='Premium water-soluble foliar fertilizer with balanced NPK plus essential trace elements. Rapidly absorbed through leaves for immediate correction of deficiencies. Excellent for high-value horticultural crops.'),
    dict(name='KNAPSACK SPRAYER 16L', category='other', img='store', stock=35, reorder=5,
         active_ingredient='N/A — Equipment', formulation='Manual Knapsack Sprayer',
         crops='All field, vegetable and plantation spray applications',
         dosage='16-litre tank. Operating pressure: 2–4 bar. Adjustable flat fan nozzle.',
         packing='Per unit',
         description='Heavy-duty manual knapsack sprayer with 16-litre polyethylene tank. Features anti-drip nozzle, adjustable brass nozzle, pressure relief valve and padded shoulder straps. Essential equipment sold at MACL Kampala.'),
]

DISTRIBUTORS = [
    ('Muddo Agro HQ — Kampala','Central','Kampala','Container Village Nakivubo, Equity Bank Basement V013, P.O Box 25240','0772-507582 / 0702-507582','kulanju_w@yahoo.com',0.3136,32.5811),
    ('Nakasero Agro Supplies','Central','Kampala','Nakasero Market, Stall 47','+256 701 234567','',0.3180,32.5750),
    ('Wakiso District Outlet','Central','Wakiso','Namulanda Trading Centre, Entebbe Road','+256 754 223344','',0.0667,32.4833),
    ('Masaka Agro Store','Central','Masaka','Birch Avenue, Masaka Town, Plot 12','+256 789 990011','',-0.3396,31.7369),
    ('Jinja Agro Distributor','Eastern','Jinja','Main Street, Jinja Town, Plot 45','+256 782 334455','',0.4244,33.2041),
    ('Mbale Farm Supplies','Eastern','Mbale','Republic Street, Mbale, Shop 12','+256 703 445566','',1.0796,34.1753),
    ('Iganga Agricultural Centre','Eastern','Iganga','Market Street, Iganga Town','+256 756 112233','',0.6085,33.4683),
    ('Gulu Northern Branch','Northern','Gulu','Chwa II Road, Gulu Town','+256 772 556677','',2.7748,32.2990),
    ('Lira Agro Centre','Northern','Lira','Obote Avenue, Lira Town','+256 755 889900','',2.2499,32.8998),
    ('Mbarara Western Hub','Western','Mbarara','High Street, Mbarara, Plot 8','+256 786 667788','',-0.6072,30.6545),
    ('Fort Portal Outlet','Western','Kabarole','Bwamba Road, Fort Portal Town','+256 701 778899','',0.6620,30.2750),
]

AGENTS = [
    ('Alice Namukasa','alice','alice@muddo.ug','+256 701 111001','Central','Kampala'),
    ('Robert Opio','robert','robert@muddo.ug','+256 702 222002','Eastern','Jinja'),
    ('Grace Atim','grace','grace@muddo.ug','+256 703 333003','Northern','Gulu'),
    ('Patrick Tendo','patrick','patrick@muddo.ug','+256 704 444004','Western','Mbarara'),
]


class Command(BaseCommand):
    help = 'Seed real MACL products, distributors and demo agents'

    def add_arguments(self, p):
        p.add_argument('--force', action='store_true', help='Re-seed even if data exists')

    def handle(self, *args, **options):
        force = options['force']

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@muddo.ug', 'muddo@admin2024')
            self.stdout.write(self.style.SUCCESS('✓ Admin user created  (admin / muddo@admin2024)'))
        else:
            self.stdout.write('  Admin exists — skipping.')

        if not Product.objects.exists() or force:
            if force: Product.objects.all().delete()
            added = 0
            for r in PRODUCTS:
                p, created = Product.objects.get_or_create(name=r['name'], defaults={
                    'category': r['category'], 'description': r['description'],
                    'active_ingredient': r['active_ingredient'], 'formulation': r['formulation'],
                    'crops': r['crops'], 'dosage': r['dosage'], 'packing': r['packing'],
                    'image_url': IMG.get(r['img'], IMG['all']),
                })
                if created:
                    Inventory.objects.create(product=p, stock_qty=r['stock'], reorder_level=r['reorder'], unit='units')
                    added += 1
            self.stdout.write(self.style.SUCCESS(f'✓ {added}/{len(PRODUCTS)} products seeded'))
        else:
            self.stdout.write(f'  Products exist ({Product.objects.count()}) — skipping (use --force).')

        if not Distributor.objects.exists() or force:
            if force: Distributor.objects.all().delete()
            for r in DISTRIBUTORS:
                Distributor.objects.get_or_create(name=r[0], defaults={
                    'region':r[1],'district':r[2],'address':r[3],'phone':r[4],'email':r[5],'lat':r[6],'lng':r[7]})
            self.stdout.write(self.style.SUCCESS(f'✓ {len(DISTRIBUTORS)} distributors seeded'))

        if not Agent.objects.exists() or force:
            n = 0
            for name, username, email, phone, region, district in AGENTS:
                if not User.objects.filter(username=username).exists():
                    f, *l = name.split(' ', 1)
                    u = User.objects.create_user(username, email, 'agent@2024',
                                                  first_name=f, last_name=' '.join(l) if l else '')
                    Agent.objects.create(user=u, phone=phone, region=region, district=district)
                    n += 1
            self.stdout.write(self.style.SUCCESS(f'✓ {n} demo agents seeded  (password: agent@2024)'))

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Done!\n'
            '   Run:   python manage.py runserver\n'
            '   Admin: http://127.0.0.1:8000/login/  →  admin / muddo@admin2024\n'
        ))
