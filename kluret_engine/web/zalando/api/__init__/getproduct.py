import requests
from bs4 import BeautifulSoup
import json
import os

# Base URL without page number
base_url = "https://www.zalando.se/man/drdenim-online-shop.gina-tricot-1.happy-socks-online-shop.hummel-1.jack-and-jones.jdy.jlindeberg.kaffe-online-shop.lego.mamalicious.na-kd-online-shop.noisy-may-online-shop.object-online-shop.only-online-shop.pieces-online-shop.selected.skagen-online-shop.tigerofsweden.vero-moda.vila-1.yas-online-shop.zarko.zizzi-online-shop.2nd-day.7-days-active.8848-altitude.aimn.aknvas.andiata.anerkjendt.angulus.arket.arkk-copenhagen.ask-scandinavia.asra.august-berg.avavav.b-copenhagen.b-young.ball.becksoendergaard.bertoni.birgitte-herskind.bisgaard.bite-studios.bjoern-borg.blanche.blendshe-1.bolinder-stockholm.boob-design.brogger.bruun-and-stengade.bruuns-bazaar.btfcph.bubbleroom.busnel.by-garment-makers.by-malene-birger.by-malina.bytimo.calou-stockholm.carin-wester.casall.casual-friday.cellbes-of-sweden.cheapo.chelsea.chiquelle.cj-of-sweden.clean-cut-copenhagen.color-kids.copenhagen.copenhagen-muse.copenhagen-shoes.craft.cras.cream.custommade.dagmar.daily-sports.danefa-kobenhavn.daniel-wellington.danish-endurance.dansk-copenhagen.davida-cashmere.day-birger.day-et.deadwood.decadent-copenhagen.dedicated.design-letters.designers-remix.didrikson.dranella.ecco.efva-attling.envii.esme-studios.estelle-and-thild.eton.face-stockholm.filippa-k.fiveunits.fjaellraeven.foreo.fransa.freequent.gabba.gant.garment-project.gestuz.golden-beards.gosh-copenhagen.gustav.h2o.haglofs.halo.han-kjobenhavn.helly-hansen.henrik-vibskov.hofmann-copenhagen.holzweiler.hope.hosbjerg.houdini.hunkydory.hust-claire.hvisk.icaniwill.icepeak.ichi.ichi-petite.ida-sjoestedt.iiqual.ilse-jacobsen.indiska.inwear.isbjoern-of-sweden.ivy-copenhagen.ivylee-copenhagen.jane-konig.jascha-stockholm.jbs-of-denmark.joha.julie-sandlau.jumperfabriken.junarose.just-junkies.karen-by-simonsen.karitraa.klaettermusen.kronstadt.laest.larsson-and-jennings.les-deux.levete-room.lexington.libertine-libertine.lilboo.limited-by-name-it.linda-hallberg.lindbergh.lindex.line-of-oslo.lisberg-jewellery.little-liffner.loewengrip.lollys-laundry.love-copenhagen.luhta.lumene.m-by-m.maanesten.mads-norgaard.mainio.makia.maria-black.marimekko.marmar-copenhagen.martin-asbjorn.matinique.meraki.mikk-line.mini-rodini.minimum.modstroem.molo.monki.moods-of-norway.mos-mosh.moves.mr-bear-family.muesli-by-green-cotton.munthe.name-it.nellycom.neo-noir.nialaya.nikolaj-storm.nn07.noa-noa.nordahl-jewellery.nordgreen.nordicdots.norr.norrona.norse-projects.notes-du-nord.nudie.nue-denmark.nuemph.nunoo.odd-molly.only-sons.oscar-jacobson.papu.part-two.pavement.peak-performance.pieces-maternity.pilgrim.rains.re-new-copenhagen.reima.resterods.resume.rodebjer.rohnisch.royal-republiq.rukka.saint-tropez.salming.samsoe-and-samsoe.san-babila-milano.sand-copenhagen.sandgaard.sandqvist.scandinavian-biolabs.selahatin.sence-copenhagen.shoedesign-copenhagen.sif-jakobs-jewellery.simply-copenhagen.sirup-copenhagen.skandinavisk.smafolk.sneaky-steve.snoe-of-sweden.soaked-in-luxury.soener-by-sweden.sofie-schnoor.soft-gallery.solid.something-new.soulland.soyaconcept.stamm.stella-nova.stenstroems.stiksen.still-nordic.stockh-lm.stockh-lm-studio.stylein.summery-copenhagen.swedemount.swedish-stockings.true-organic-of-sweden.vagabond.vibe-harslof.viking.weekday.wheat.why7.won-hundred.wood-wood/?p="

# Number of pages to scrape
total_pages = 262

# List to store all product URLs
all_product_links = []

# Loop through each page number
for page in range(1, total_pages + 1):
    # Construct the URL for the current page
    url = base_url + str(page)
    print(f"Scraping page {page} - URL: {url}")

    # Send a GET request to fetch the page content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the product links on the page
        for article in soup.find_all('article', {'role': 'link'}):
            link = article.find('a', href=True)
            if link:
                all_product_links.append(link['href'])
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

    # Save the collected links to a JSON file after each page
    file_path = os.path.join(os.getcwd(), 'product_links.json')
    with open(file_path, 'w') as json_file:
        json.dump(all_product_links, json_file, indent=4)

    print(f"Links for page {page} saved to {file_path}")

print("All product links have been saved to product_links.json")
