INSERT INTO public.shops (shop_id, shop_name, shop_function, shop_real_name, shop_nb_min_pages, shop_nb_max_pages)
VALUES
(1, 'jahwaggysrecords', 'scrap_jahwaggysrecords', 'Jah Waggys Records', 4, 400),
(2, 'onlyrootsreggae', 'scrap_onlyrootsreggae', 'OnlyRoots Reggae', 4, 100),
(3, 'controltower', 'scrap_controltower', 'Control Tower Records', 50, 3000),
-- (4, 'reggaefever', 'scrap_reggaefever', 'Reggae Fever,' 4, 600), -- not used now
(5, 'pataterecords', 'scrap_pataterecords', 'Patate Records', 4, 400),
(6, 'lionvibes', 'scrap_lionvibes', 'LionVibes', 4, 100);
-- (7, 'toolboxrecords', 'scrap_toolboxrecords', 'Toolbox Records', 4, 55), -- not used now
-- (8, 'reggaemuseum', 'scrap_reggaemuseum', 'Reggae Museum', 4, 150); -- not used now

INSERT INTO public.shops_links (shop_id, shop_link)
VALUES
(1, 'https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection?page='),
(1, 'https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection?page='),
(1, 'https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection?page='),
(1, 'https://jahwaggysrecords.com/fr/18-test-press-selection?page='),
-- onlyrootsreggae links
(2, 'https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=X&order=product.date_add.desc'),
(2, 'https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=X&order=product.date_add.desc'),
(2, 'https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=X&order=product.date_add.desc'),
-- controltower links
(3, 'https://controltower.fr/fr/'),
-- reggaefever links
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Dub&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Dancehall&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Dub+Poetry&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Reggae&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Steppers&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?format=7&style=Ska%2BRocksteady&sort=relDate_riddim&page='),
-- -- ('https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?genKind=keyword&generic=&format=10&style=&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?genKind=keyword&generic=&format=12&style=&sort=relDate_riddim&page='),
-- (4, 'https://www.reggaefever.ch/articleList?genKind=keyword&generic=&format=LP&style=&sort=relDate_riddim&page='),
-- pataterecords links
(5, 'https://www.patate-records.com/shop/1/X/type/1/'),
(5, 'https://www.patate-records.com/shop/1/X/type/2/'),
(5, 'https://www.patate-records.com/shop/1/X/type/3/'),
-- lionvibes links
(6, 'https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=7%22&page=X&sort_by=created-descending'),
(6, 'https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=10%22&page=X&sort_by=created-descending'),
(6, 'https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=12%22&page=X&sort_by=created-descending'),
(6, 'https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=LP&page=X&sort_by=created-descending');
-- -- toolboxrecords links
-- (7, 'https://www.toolboxrecords.com/fr/catalog/3/dub-ragga/#page='),
-- -- reggaemuseum links
-- (8, 'https://www.reggae-museum.com/shop/24-dancehall-new-roots#/page-X'),
-- (8, 'https://www.reggae-museum.com/shop/26-rub-a-dub-early-digital#/page-X'),
-- (8, 'https://www.reggae-museum.com/shop/27-ska-rocksteady-roots#/page-X'),
-- (8, 'https://www.reggae-museum.com/shop/28-12-inch-records#/page-X');
