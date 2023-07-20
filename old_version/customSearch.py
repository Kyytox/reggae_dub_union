from scripts_scrap.scrap_shops import scrap_jahwaggysrecords
from scripts_scrap.scrap_shops import scrap_onlyrootsreggae
from scripts_scrap.scrap_shops import scrap_controltower
from scripts_scrap.scrap_shops import scrap_reggaefever
from scripts_scrap.scrap_shops import scrap_deeprootsreggae
from scripts_scrap.scrap_shops import scrap_pataterecords
from scripts_scrap.scrap_shops import scrap_toolboxrecords
from scripts_scrap.scrap_shops import scrap_lionvibes
from scripts_scrap.scrap_shops import scrap_reggaemuseum

import httpx 
import asyncio
from time import time

async def customSearch(req):
    print("customSearch")
    print("req", req)
    url_jahwaggys = f"https://jahwaggysrecords.com/fr/recherche?controller=search&s={req}"
    url_controltower = f"https://controltower.fr/fr/recherche?controller=search&orderby=position&orderway=desc&search_query={req}&submit_search="
    url_onlyrootsreggae = f"https://www.onlyroots-reggae.com/fr/recherche?controller=search&s={req}" 
    url_reggaefever = f"https://www.reggaefever.ch/articleList?genKind=keyword&generic={req}&format=&style="
    url_deeprootsreggae = f"http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/?ObjectID=10199658&ViewAction=FacetedSearchProducts&SearchString={req}"
    url_pataterecords = f"https://www.patate-records.com/focus/{req}/"
    url_toolboxrecords = f"https://www.toolboxrecords.com/fr/search/{req}"
    url_lionvibes = f"https://www.lionvibes.com/search.php?mode=quicksearch&search_string={req}"
    url_reggaemuseum = f"https://www.reggae-museum.com/shop/search?controller=search&orderby=position&orderway=desc&search_query={req}&submit_search="

    # # # Search
    _start = time()
    response = []
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [scrap_jahwaggysrecords(client, url_jahwaggys),
                scrap_onlyrootsreggae(client, url_onlyrootsreggae),
                # scrap_controltower(client, url_controltower),
                # scrap_reggaefever(client, url_reggaefever),
                scrap_deeprootsreggae(client, url_deeprootsreggae),
                scrap_pataterecords(client, url_pataterecords),
                scrap_toolboxrecords(client, url_toolboxrecords),
                scrap_lionvibes(client, url_lionvibes),
                scrap_reggaemuseum(client, url_reggaemuseum),
                ]
        for response_future in asyncio.as_completed(tasks):
            response.extend(await response_future)
        
    print(f"with gathering finished in: {time() - _start:.2f} seconds")
    
    
    print("response", len(response))
    # test = scrap_controltower("test")
    return response



def search(req):
    return asyncio.run(customSearch(req))